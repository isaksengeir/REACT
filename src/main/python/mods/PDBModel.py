"""
Nice feature to get atom numbers of a selection:
> iterate sele, print("%s" % ID)
# https://pymolwiki.org/index.php?title=Modeling_and_Editing_Structures#Adding_and_using_your_own_fragments%3E
# Pymol has some build-in fragments (amino acids and simple functional groups). You can add your own fragments, eg.
# sugars, in this way: Create the molecule you want to use as a fragment. Save it as a .pkl file in
# <pymol_path>/data/chempy/fragments.
# If you want a menu item for your fragment, you can probably put it in <pymol_path>/modules/pmg_tk/skins/normal/__init__.py, but I haven't tried this.
#######
step 1:
* Load pdb file or import from project table
* select central molecule/ligand/reactant
* choose size of cluster (default 5 Å + include byres to avoid stupid cutting)
* Report back how many atoms current cluster will consist of - dynamically adjust size until happy.
> count_atoms cluster

--> Create cluster

step 2:
* Evaluate model, delete stuff, go back to step 1 to adjust size, or process model
** choose n-terminal capping: ace, methyl or H
** choose c-terminal capping: nme, methyl or H
"process model"

step 2 --> step 3 processing
* select terminals that have been chopped:
> select nterms, test and (elem n and (neighbor name CA and not neighbor name C))
> select cterms, test and (elem C and (neighbor name O and not neighbor name N))

* Get residue numbers of terminals to be fixed:
> iterate nterms, print("%s" % resi)
> iterate cterms, print("%s" % resi)

* Iterate over terminal residues, get_dihedral, attach terminal capping and set dihedral to original again.
*N-terms:
> get_dihedral prot///resnr/C, prot///resnr/CA, prot///resnr/N, prot///resnr/H
> editor.attach_amino_acid("prot///resnr/N", 'ace')
>  set_dihedral prot///resnr/C, prot///resnr/CA, prot///resnr/N, prot///resnr/H, dihedral_angle
*C-terms:
> get_dihedral prot///resnr/N, prot///resnr/CA, prot///resnr/C, prot///resnr/O
> editor.attach_amino_acid("prot///resnr/N", 'nme')
>  set_dihedral prot///resnr/N, prot///resnr/CA, prot///resnr/C, prot///resnr/O, dihedral_angle
> editor.attach_amino_acid("pl1", 'nme')

Step 3:
* Validate cluster (done by user visually).
* Add, delete H-atoms, methyl-groups?
** Save cluster & quit.
#######
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, Qt
from UIs.PDB_clusterWindow import Ui_ClusterPDB
from mods.DialogsAndExceptions import DialogMessage
from mods.common_functions import find_ligands_pdbfile


class ModelPDB(QtWidgets.QMainWindow):
    """
    User window to interact with global settings (REACT attributes
    workdir, DFT_settings and Ui_stylemode)
    """
    def __init__(self, parent):
        super().__init__(parent)

        self.react = parent
        self.ui = Ui_ClusterPDB()

        self.ui.setupUi(self)

        # TODO optimize this:
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        self.move(int(((screen_size.width() - window_size.width()) / 2)) - 250, 100)
        ###

        self.setWindowTitle("REACT - PDB model generation")

        # Need pymol for this:
        if not self.react.pymol:
            self.react.start_pymol()

        self.pymol = self.react.pymol

        self.selected_atoms = {"central": list(), "included": list()}

        # Connect signals from pymol
        self.pymol.atomsSelectedSignal.connect(self.update_selected_atoms)
        self.ui.select_byres.clicked.connect(self.update_inclusion_size)
        self.ui.include_solvent.clicked.connect(self.update_inclusion_size)

        self.ui.lineEdit_atoms_in_model.setText("0")
        #self.ui.lineEdit_inclusion_radius.insert("1")

        self.ui.slider_inclusion_size.valueChanged.connect(self.update_inclusion_size)
        self.ui.slider_inclusion_size.setValue(1)
        self.ui.button_pdb_from_table.clicked.connect(self.import_pdb_project_table)
        self.ui.button_set_cluster_center.clicked.connect(self.set_central_atoms)
        self.ui.button_update_manual_selection.clicked.connect(lambda: self.pymol.get_selected_atoms("included"))
        self.ui.button_create_model.clicked.connect(self.create_model)

    def load_pdb(self):
        pass

    def import_pdb_project_table(self):
        """
        take selected PDB file from project table
        :return:
        """
        file_ = self.react.get_selected_filepath
        if not file_.split(".")[-1] == "pdb":
            warn = DialogMessage(self, "PDB file required")
            warn.show()
            self.react.append_text("%s is not recognised as a pdb file." % (file_.split("/")[-1]))
            return
        self.ui.lineEdit_pdb_file.setText(file_)
        self.group_pdb_pymol(pdb_source=file_.split("/")[-1].split(".")[0], pdb_target="source")
        self.guess_highlight_ligand(pdb_file=file_, pymol_name="source")

    def guess_highlight_ligand(self, pdb_file, pymol_name):
        """
        Guess from pdb file what is the interesting region of the protein and highlight it in pymol
        :param pdb_file: path to pdb file
        :return:
        """
        residues = find_ligands_pdbfile(pdb_file)
        self.pymol.set_protein_ligand_rep(residues, pymol_name=pymol_name, group="pdb_model")

    def group_pdb_pymol(self, pdb_source, pdb_target):
        """
        Make a group in pymol for setting up PDB model / cluster
        :param pdb_source: pdb name (pymol) to copy into pdb_model group
        :param pdb_target: pymol name of internal pdb to create
        :return:
        """
        self.pymol.pymol_cmd("create %s, %s" % (pdb_target, pdb_source))
        self.pymol.pymol_cmd("group pdb_model, %s" % pdb_target)
        self.pymol.highlight(name=pdb_target, group="pdb_model")

    def set_central_atoms(self):
        """
        :return:
        """
        # Reset central atoms
        self.selected_atoms["central"] = list()
        self.selected_atoms["included"] = list()
        self.pymol.get_selected_atoms()

    @pyqtSlot(list)
    def update_selected_atoms(self, atoms):
        """
        Signal from PymolProcess when atoms are selected. Updates global self.selected_atoms dictionary
        :param: atoms list of atom numbers (str)
        :return:
        """
        if len(atoms) == 0:
            print("No atoms selected")
            self.react.append_text("No atoms selected")
            return
        # Remove duplicates (maybe not necessary):
        atoms = list(dict.fromkeys(atoms))
        if len(self.selected_atoms["central"]) < 1:
            self.selected_atoms["central"] = atoms
            self.pymol.set_selection(atoms=atoms, sele_name="central", object_name="source", group="pdb_model")
            self.pymol.highlight_atoms(atoms=atoms, color="lightmagenta", name="source", group="pdb_model")
            self.update_inclusion_size()
        else:
            self.selected_atoms["included"] = atoms
            self.pymol.set_selection(atoms=atoms, sele_name="included", object_name="source", group="pdb_model")
        print(atoms)
        self.ui.lineEdit_atoms_in_model.setText(str(len(atoms)))

    def update_inclusion_size(self):
        """
        Sets radius of residues to include in lineEdit
        :return:
        """
        expand_radius = self.ui.slider_inclusion_size.value()
        self.ui.lineEdit_inclusion_radius.setText(str(expand_radius))

        if self.selected_atoms["central"]:
            self.pymol.expand_sele(selection="central", sele_name="included", group="pdb_model", radius=expand_radius,
                                   by_res=self.ui.select_byres.isChecked(),
                                   include_solv=self.ui.include_solvent.isChecked())
            # Collect expansion atom numbers
            # Delay this in case user does rappid changes...
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.delayed_get_atoms)
            # Timer in milliseconds:
            self.timer.start(500)

    def delayed_get_atoms(self):
        self.timer.stop()
        self.pymol.get_selected_atoms(sele="included")

    def create_model(self):
        self.pymol.copy_sele_to_object(sele="included", target_name="model_tmp", group="pdb_model")
        self.pymol.pymol_cmd("disable source")
        self.pymol.pymol_cmd("hide cartoon, model_tmp")
        self.ui.tabWidget.setCurrentIndex(1)

    def closeEvent(self, event):
        self.react.cluster_window = None

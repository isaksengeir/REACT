"""
Nice feature to get atom numbers of a selection:
> iterate sele, print("%s" % rank)

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
> select nterms, test and (elem C and (neighbor name O and not neighbor name N))

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
from UIs.PDB_clusterWindow import Ui_ClusterPDB


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

    def load_pdb(self):
        pass

    def import_pdb_project_table(self):
        pass

    def closeEvent(self, event):
        self.react.cluster_window = None

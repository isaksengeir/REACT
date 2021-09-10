from PyQt5 import QtWidgets
from UIs.SetupWindow import Ui_SetupWindow
from mods.GaussianFile import InputFile


class CalcSetupWindow(QtWidgets.QMainWindow, Ui_SetupWindow):
    def __init__(self, parent, filepath):
        super(CalcSetupWindow, self).__init__(parent)
        self.react = parent

        self.pymol = False
        if self.react.pymol:
            self.pymol = self.react.pymol

        self.ui = Ui_SetupWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REACT - Calculation setup")
        self.job = InputFile(parent, filepath)
        self.filepath = self.react.tabWidget.currentWidget().currentItem().text()
        self.filename = self.filepath.split("/")[-1]
        #TODO can we remove this dependency of doing 'state - 1' ?
        self.mol_obj = self.react.states[self.react.get_current_state - 1].get_molecule_object(self.filepath)


        self.read_selected_file()
        self.fill_main_tab()

        self.ui.Button_add_job.clicked.connect(lambda: self.add_item_to_list(self.ui.LineEdit_add_job, self.ui.List_add_job, self.job.job_options))
        self.ui.Button_del_job.clicked.connect(lambda:  self.del_item_from_list(self.ui.List_add_job, self.job.job_options))
        self.ui.button_add_link0.clicked.connect(lambda: self.add_item_to_list(self.ui.lineEdit_link0, self.ui.list_link0, self.job.link0_options))
        self.ui.button_del_link0.clicked.connect(lambda: self.del_item_from_list(self.ui.list_link0, self.job.link0_options))
        self.ui.comboBox_basis1.textActivated.connect(self.update_basis_boxes)
        self.ui.comboBox_job_type.textActivated.connect(self.update_job_checkBoxes)
        self.ui.button_cancel.clicked.connect(self.on_cancel)
        self.ui.button_write.clicked.connect(self.on_write)

        self.ui.button_add_freeze.clicked.connect(self.add_freeze_atoms)
        self.ui.button_delete_freeze.clicked.connect(self.remove_freeze_atoms)

        self.ui.list_model.itemSelectionChanged.connect(self.model_atom_clicked)
        self.ui.list_model.setSelectionMode(1)
        self.atoms_to_select = 1
        self.ui.comboBox_freezetype.currentTextChanged.connect(self.change_selection_mode)

        # Keep track of atoms selected (for multiple selection options)
        self.selected_indexes = list()

    def change_selection_mode(self):
        if self.ui.comboBox_freezetype.currentText() == "Atoms":
            self.ui.list_model.setSelectionMode(1)
        else:
            self.ui.list_model.setSelectionMode(2)

        select = {"Atom": 1, "Bond": 2, "Angle": 3, "Dihedral": 4}
        self.atoms_to_select = select[self.ui.comboBox_freezetype.currentText()]

    def model_atom_clicked(self):
        """
        When selection i atom list is changed, update, and communicate with pymol
        """

        sele = self.ui.list_model.selectedIndexes()

        while len(sele) > self.atoms_to_select:
            if len(self.selected_indexes) > 0:
                self.ui.list_model.item(self.selected_indexes.pop(0).row()).setSelected(False)
            else:
                self.ui.list_model.item(sele.pop(0).row()).setSelected(False)
            sele = self.ui.list_model.selectedIndexes()

        self.selected_indexes = sele

        atoms = list()
        for i in self.selected_indexes:
            if ".pdb" in self.filename:
                #atoms.append(i.text().split()[1])
                atoms.append(self.ui.list_model.item(i.row()).text().split()[1])
            else:
                atoms.append(str(i.row()+1))

        if self.pymol:
            self.update_pymol_selection(atoms=atoms)

    def update_pymol_selection(self, atoms):
        group = "state_%d" % self.react.get_current_state
        self.pymol.set_selection(atoms=atoms, sele_name="sele", object_name=self.filename.split(".")[0], group=group)

    def add_freeze_atoms(self):
        """
        Adds selected atoms to freeze section - append F to end of str for freeze
        """
        type = "F"
        g_cmd = {"Atom": "X", "Bond": "B", "Angle": "A", "Dihedral": "D"}
        atoms = ""
        for i in self.selected_indexes:
            atoms += f"{i.row()} "
            if self.pymol:
                if ".pdb" in self.filename:
                    atomnr = self.ui.list_model.item(i.row()).text().split()[1]
                else:
                    atomnr = i.row()
                self.pymol_spheres(atomnr)

        self.ui.list_freeze_atoms.insertItem(0, f"{g_cmd[self.ui.comboBox_freezetype.currentText()]} {atoms} {type}")

    def remove_freeze_atoms(self):
        """

        """
        # Get str from selection:
        to_del = self.ui.list_freeze_atoms.currentItem().text()
        print("To del")

    def pymol_spheres(self, atom_nr):
        """

        """
        group = "state_%d" % self.react.get_current_state
        self.pymol.pymol_cmd(f"show spheres, id {atom_nr} and {group} and {self.filename.split('.')[0]}")
        self.pymol.pymol_cmd(f"set sphere_scale, 0.3, id {atom_nr} and {group} and {self.filename.split('.')[0]}")

    def update_job_checkBoxes(self):
        """
        Update placeholder checkBoxes according to selected job type

        :return:
        """
        # TODO implement!
        pass

    def fill_main_tab(self):
        """
        Add all options to all comboBoxes + set current default settings

        :return:
        """

        self.ui.lineEdit_filename.setText(self.filename.split(".")[0] + ".com")
        self.ui.comboBox_job_type.addItems(self.react.settings.job_options)
        self.ui.comboBox_funct.addItems(self.react.settings.functional_options)
        self.ui.comboBox_basis1.addItems([x for x in self.react.settings.basis_options])
        #self.ui.List_add_job.addItems(self.)
        self.ui.list_link0.addItems(self.react.settings.link0_options)

        #self.ui.comboBox_job_type.setCurrentText()
        self.ui.comboBox_funct.setCurrentText(self.react.settings.functional)
        self.ui.comboBox_basis1.setCurrentText(self.react.settings.basis)

        self.update_basis_boxes()

    def update_basis_boxes(self):
        """
        Update basis functions comboBoxes according to current basis

        :return:
        """
        basis = self.ui.comboBox_basis1.currentText()

        self.ui.comboBox_basis2.clear()
        self.ui.comboBox_basis3.clear()
        self.ui.comboBox_basis4.clear()

        self.ui.comboBox_basis2.addItems(self.react.settings.basis_options[basis]['diff'])
        self.ui.comboBox_basis3.addItems(self.react.settings.basis_options[basis]['pol1'])
        self.ui.comboBox_basis4.addItems(self.react.settings.basis_options[basis]['pol2'])


    def read_selected_file(self):
        """

        :return:
        """
        xyz = self.mol_obj.get_formatted_xyz
        print(self.filepath)
        if "pdb" in self.filepath.split(".")[-1]:
            # insert pdb atoms in model atoms
            for i in range(len(self.mol_obj.atoms)):
                atom = self.mol_obj.atoms[i]
                print(atom.get_pdb_line)
                self.ui.list_model.insertItem(i, atom.get_pdb_line)

        else:
            # insert xyz atoms in model atoms
            self.ui.button_auto_freeze.setEnabled(False)

    def update_basis_options(self, basis):
        """
        # TODO delete, after moved/copied to Settings.
        """
        self.ui.basis2_comboBox.blockSignals(True)
        self.ui.basis3_comboBox.blockSignals(True)
        self.ui.basis4_comboBox.blockSignals(True)

        self.ui.basis2_comboBox.clear()
        self.ui.basis3_comboBox.clear()
        self.ui.basis4_comboBox.clear()

        basis = self.ui.comboBox_basis1.currentText()

        self.ui.basis2_comboBox.addItems(self.settings.basis_options[basis]['diff'])
        self.ui.basis3_comboBox.addItems(self.settings.basis_options[basis]['pol1'])
        self.ui.basis4_comboBox.addItems(self.settings.basis_options[basis]['pol2'])


        self.ui.basis2_comboBox.blockSignals(False)
        self.ui.basis3_comboBox.blockSignals(False)
        self.ui.basis4_comboBox.blockSignals(False)

        #self.curr_choices["diff"] = self.ui.basis2_comboBox.currentText()
        #self.curr_choices["diff"] = self.ui.basis2_comboBox.currentText()

    def add_item_to_list(self, Qtextinput, Qlist, job_list):
        """
        :param Qtextinput: QLineEdit
        :param Qlist: QListWidget
        :param original_list: list to store item
        Adds the text input from user (past to Qtextinput) to correct
        QlistWidget and append item to list.
        """
        user_input = Qtextinput.text()
        if user_input and user_input not in job_list:
            job_list.append(user_input)
            Qlist.addItem(user_input)

    def del_item_from_list(self, Qlist, job_list):
        """
        :param Qlist: QListWidget
        :param job_list: list to delete from
        Removes item in QlistWdiget and updates self.settings accordingly.
        """
        item_text = Qlist.currentItem().text()
        if item_text in job_list:
            job_list.remove(item_text)
        Qlist.takeItem(Qlist.currentRow())

    def on_cancel(self):
        self.close()

    def on_write(self):
        """
        Write all data to Inputfile object.
        # TODO how to return this object to react after closing the window?
        """

        self.job.filename = self.ui.lineEdit_filename.text()
        self.job.job_type = self.ui.comboBox_job_type.currentText()
        self.job.basis = self.ui.comboBox_basis1.currentText()
        self.job.basis_diff = self.ui.comboBox_basis2.currentText()
        self.job.basis_pol1 = self.ui.comboBox_basis3.currentText()
        self.job.basis_pol2 = self.ui.comboBox_basis4.currentText()
        self.react.states[self.react.get_current_state - 1].add_instance(self.job)
        

        self.close()



from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from UIs.SetupWindow import Ui_SetupWindow
from mods.GaussianFile import InputFile
from mods.common_functions import atom_distance, random_color


class CalcSetupWindow(QtWidgets.QMainWindow, Ui_SetupWindow):
    def __init__(self, parent, filepath):
        super(CalcSetupWindow, self).__init__(parent)
        self.react = parent
        self.filepath = filepath

        self.pymol = False
        if self.react.pymol:
            self.pymol = self.react.pymol
            self.pymol.pymol_cmd("set mouse_selection_mode, 0")
            self.pymol.pymol_cmd("hide cartoon")

            # Monitor clicks in pymol stdout_handler
            self.pymol.monitor_clicks()
            # Connect signals from pymol:
            self.pymol.atomsSelectedSignal.connect(self.pymol_atom_clicked)

        self.ui = Ui_SetupWindow()
        self.ui.setupUi(self)
        self.settings = self.react.settings

        # TODO optimize this?:
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        self.move(int(((screen_size.width() - window_size.width()) / 2)) - 250, 100)

        self.setWindowTitle("REACT - Calculation setup")

        self.mol_obj = self.react.states[self.react.state_index].get_molecule_object(self.filepath)

        self.filename = self.mol_obj.filename.split(".")[0] 


        self.insert_model_atoms()
        self.fill_main_tab()

        self.ui.Button_add_job.clicked.connect(lambda: self.add_item_to_list(self.ui.LineEdit_add_job, self.ui.List_add_job, self.mol_obj.job_options))
        self.ui.Button_del_job.clicked.connect(lambda:  self.del_item_from_list(self.ui.List_add_job, self.mol_obj.job_options))
        self.ui.button_add_link0.clicked.connect(lambda: self.add_item_to_list(self.ui.lineEdit_link0, self.ui.list_link0, self.mol_obj.link0_options))
        self.ui.button_del_link0.clicked.connect(lambda: self.del_item_from_list(self.ui.list_link0, self.mol_obj.link0_options))
        self.ui.comboBox_basis1.textActivated.connect(self.update_basis_boxes)
        self.ui.comboBox_job_type.textActivated.connect(self.update_job_details)
        self.ui.button_cancel.clicked.connect(self.on_cancel)
        self.ui.button_write.clicked.connect(self.on_write)
        self.ui.checkBox_mem.clicked.connect(lambda: self.route_checkboxes_update(self.ui.checkBox_mem, self.ui.lineEdit_mem))
        self.ui.checkBox_chk.clicked.connect(lambda: self.route_checkboxes_update(self.ui.checkBox_chk, self.ui.lineEdit_chk))
        self.ui.checkBox_schk.clicked.connect(lambda: self.route_checkboxes_update(self.ui.checkBox_schk, self.ui.lineEdit_schk))
        self.ui.checkBox_oldchk.clicked.connect(lambda: self.route_checkboxes_update(self.ui.checkBox_oldchk, self.ui.lineEdit_oldchk))
        self.ui.checkBox_rwf.clicked.connect(lambda: self.route_checkboxes_update(self.ui.checkBox_rwf, self.ui.lineEdit_rwf))
        self.ui.button_add_freeze.clicked.connect(self.add_freeze_atoms)
        self.ui.button_delete_freeze.clicked.connect(self.remove_freeze_atoms)
        self.ui.button_auto_freeze.clicked.connect(self.auto_freeze_atoms)
        self.ui.button_add_scan.clicked.connect(self.add_scan_atoms)
        self.ui.button_delete_scan.clicked.connect(self.remove_scan_atoms)
        self.ui.lineEdit_filename.textChanged.connect(self.filename_update)

        self.ui.list_model.itemSelectionChanged.connect(self.model_atom_clicked)
        self.ui.list_model.setSelectionMode(1)

        self.ui.list_freeze_atoms.itemSelectionChanged.connect(self.freeze_list_clicked)

        self.atoms_to_select = 1
        self.enable_scan(enable=False)
        self.ui.comboBox_freezetype.currentTextChanged.connect(self.change_selection_mode)

        # Keep track of atoms selected (for multiple selection options)
        self.selected_indexes = list()

        # Pymol returns ordered atom id list, so we need to keep track of click order
        self.selected_ids = list()

    def change_selection_mode(self):
        if self.ui.comboBox_freezetype.currentText() == "Atoms":
            self.ui.list_model.setSelectionMode(1)
        else:
            self.ui.list_model.setSelectionMode(2)

        select = {"Atom": 1, "Bond": 2, "Angle": 3, "Dihedral": 4}
        self.atoms_to_select = select[self.ui.comboBox_freezetype.currentText()]

    def enable_scan(self, enable=True):
        self.ui.button_add_scan.setEnabled(enable)
        #self.ui.button_delete_scan.setEnabled(enable)
        self.ui.spinbox_radius.setEnabled(enable)
        self.ui.spinbox_scan_pm.setEnabled(enable)
        self.ui.spinbox_scan_increment.setEnabled(enable)

    @pyqtSlot(list)
    def pymol_atom_clicked(self, ids):
        """
        Get atoms selected in pymol and select deselect in model atom listwidget
        """
        if not ids or None in ids:
            return

        ids = [int(x) - 1 for x in ids]

        # Effective when len(ids) > len(self.selected_ids)
        unsele = list(set(self.selected_ids) - set(ids))
        for id in unsele:
            self.ui.list_model.item(id).setSelected(False)
            self.selected_ids.pop(self.selected_ids.index(id))

        # Effective when len(ids) < len(self.selected_ids)
        new_select = list(set(ids) - set(self.selected_ids))
        for id in new_select:
            self.selected_ids.append(id)
            if len(self.selected_ids) > self.atoms_to_select:
                self.selected_ids.pop(0)
            self.ui.list_model.item(id).setSelected(True)

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
        coordinates = list()
        for i in self.selected_indexes:
            atoms.append(self.mol_obj.molecule[i.row() + 1].atom_index)
            coordinates.append(self.mol_obj.molecule[i.row() + 1].coordinate)

        if self.ui.comboBox_freezetype.currentText() == "Bond" and len(atoms) == 2:
            self.enable_scan(enable=True)
            r = atom_distance(coordinates[0], coordinates[1])
            self.ui.spinbox_radius.setValue(r)
        else:
            self.enable_scan(enable=False)

        if self.pymol:
            self.update_pymol_selection(atoms=atoms)

    def freeze_list_clicked(self):
        """
        When entry in "Atoms to freeze" is clicked, update to selected in "Atoms in model" list and pymol
        """
        try:
            indexes = [int(x) - 1 for x in self.ui.list_freeze_atoms.currentItem().text().split()[1:-1]]
        except AttributeError:
            return
        freeze_type = {1: "Atom", 2: "Bond", 3: "Angle", 4: "Dihedral"}
        self.ui.comboBox_freezetype.setCurrentText(freeze_type[len(indexes)])

        self.selected_indexes = indexes
        self.ui.list_model.clearSelection()

        for index in indexes:
            self.ui.list_model.item(index).setSelected(True)

    def update_pymol_selection(self, atoms):
        group = "state_%d" % self.react.get_current_state
        self.pymol.set_selection(atoms=atoms, sele_name="sele", object_name=self.mol_obj.molecule_name, group=group)

    def add_freeze_atoms(self):
        """
        Adds selected atoms to freeze section - append F to end of str for freeze
        """
        type = "F"
        g_cmd = {"Atom": "X", "Bond": "B", "Angle": "A", "Dihedral": "D"}
        atoms = ""
        for i in self.selected_indexes:
            atomnr = self.mol_obj.molecule[i.row() + 1].atom_index
            if self.pymol:
                self.pymol_spheres(atomnr)
            atoms += f"{atomnr } "

        self.ui.list_freeze_atoms.insertItem(0, f"{g_cmd[self.ui.comboBox_freezetype.currentText()]} {atoms} {type}")

    def remove_freeze_atoms(self):
        """
        Removes selected freeze atoms/bonds/angles/torsions
        """
        # Get rows for selected to delete:
        to_del = [self.ui.list_freeze_atoms.row(x) for x in self.ui.list_freeze_atoms.selectedItems()]
        for row in to_del:
            self.ui.list_freeze_atoms.takeItem(row)

    def add_scan_atoms(self):
        """
        Atom pair for BSB scan atom algorithm
        """
        freeze = "B "
        for i in self.selected_indexes:
            freeze += f"{self.mol_obj.molecule[i.row() + 1].atom_index} "

        freeze += f"{self.ui.spinbox_radius.value()} {self.ui.spinbox_scan_pm.value()} " \
                  f"{self.ui.spinbox_scan_increment.value()}"
        self.ui.list_freeze_atoms_2.insertItem(0, freeze)

    def remove_scan_atoms(self):
        try:
            self.ui.list_freeze_atoms_2.takeItem(self.ui.list_freeze_atoms_2.currentRow())
        except:
            pass
        
    def pymol_spheres(self, atom_nr):
        """
        Indicate withe spheres atoms to be frozen / modredundant
        """
        group = "state_%d" % self.react.get_current_state
        self.pymol.pymol_cmd(f"show spheres, id {atom_nr} and {group} and {self.mol_obj.filename.split('.')[0]}")
        self.pymol.pymol_cmd(f"set sphere_scale, 0.3, id {atom_nr} and {group} and {self.mol_obj.filename.split('.')[0]}")

    def update_job_details(self):
        """
        Update placeholder checkBoxes and additional-options-list according to selected job type

        :return:
        """
        job_type = self.ui.comboBox_job_type.currentText()
        self.add_details = []
        self.ui.checkBox_placeholder1.setChecked(False)
        self.ui.checkBox_placeholder2.setChecked(False)
        self.ui.checkBox_placeholder3.setChecked(False)
        self.ui.checkBox_placeholder4.setChecked(False)

        labels = {'Opt': ['tight', 'noeigentest', 'calcfc', 'Z-matrix'],
                          'Opt (TS)': ['temp1', 'temp2', 'temp3', 'temp4'], 
                          'Freq': ['noraman', 'temp2', 'temp3', 'temp4'], 
                          'IRC': ['temp1', 'temp2', 'temp3', 'temp4'],
                          'IRCMax': ['temp1', 'temp2', 'temp3', 'temp4'],
                          'Single point': ['temp1', 'temp2', 'temp3', 'temp4']} 
            
        self.ui.checkBox_placeholder1.setText(labels[job_type][0])
        self.ui.checkBox_placeholder2.setText(labels[job_type][1])
        self.ui.checkBox_placeholder3.setText(labels[job_type][2])
        self.ui.checkBox_placeholder4.setText(labels[job_type][3])

        for i in self.react.settings.job_options[job_type]:
            i = i.lower()

            if i == labels[job_type][0].lower():
                self.ui.checkBox_placeholder1.setChecked(True)
            elif i == labels[job_type][1].lower():
                self.ui.checkBox_placeholder2.setChecked(True)
            elif i == labels[job_type][2].lower():
                self.ui.checkBox_placeholder3.setChecked(True)
            elif i == labels[job_type][3].lower():
                self.ui.checkBox_placeholder4.setChecked(True)
            else:
                self.add_details.append(i)

        self.ui.List_add_job.clear()
        self.ui.List_add_job.addItems(self.add_details)

    def fill_main_tab(self):
        """
        Add all options to all comboBoxes + set current default settings

        :return:
        """
        self.ui.lineEdit_filename.setText(self.filename + '.com')
        self.ui.comboBox_job_type.addItems(self.react.settings.job_options)
        self.ui.comboBox_funct.addItems(self.react.settings.functional_options)
        self.ui.comboBox_basis1.addItems([x for x in self.react.settings.basis_options])

        #self.ui.comboBox_job_type.setCurrentText()
        self.ui.comboBox_funct.setCurrentText(self.react.settings.functional)
        self.ui.comboBox_basis1.setCurrentText(self.react.settings.basis)

        self.update_job_details()
        
        checkboxes = {self.ui.checkBox_chk: self.ui.lineEdit_chk,
                      self.ui.checkBox_mem: self.ui.lineEdit_mem,
                      self.ui.checkBox_schk: self.ui.lineEdit_schk,
                      self.ui.checkBox_oldchk: self.ui.lineEdit_oldchk,
                      self.ui.checkBox_rwf: self.ui.lineEdit_rwf,
                      self.ui.checkBox_save: None,
                      self.ui.checkBox_errorsave: None}

        link0_to_add_to_list = [x for x in self.settings.link0_options]

        print(link0_to_add_to_list)

        for checkbox, lineEdit in checkboxes.items():

            checkbox.setChecked(False)
            if lineEdit:
                lineEdit.setEnabled(False)

            found_keyword = False

            for keyword_0 in link0_to_add_to_list:

                keyword = keyword_0.lower()
                if "=" in keyword:
                    temp = keyword.split("=")
                    keyword = temp[0]
                    value = temp[1]
                else:
                    value = None

                if keyword == "mem" and checkbox.text() == "Memory":
                    found_keyword = True
                    value = value.upper()

                elif keyword == checkbox.text().lower():
                    found_keyword = True
                    if keyword == "chk" and not value:
                        value = self.filename + ".chk"
                    elif keyword == "schk" and not value:
                        value = self.filename + "_copy.chk"
                    elif keyword == "oldchk" and not value:
                        value = self.filename + "_old.chk"

                if found_keyword:
                    checkbox.setChecked(True)
                    link0_to_add_to_list.remove(keyword_0)
                    if value and lineEdit:
                        lineEdit.setEnabled(True)
                        lineEdit.setText(value)
                    
                    found_keyword = False

        self.ui.list_link0.addItems(link0_to_add_to_list)

    def route_checkboxes_update(self, checkbox, lineEdit):

        if checkbox.isChecked():
            lineEdit.setEnabled(True)
        else:
            lineEdit.setEnabled(False)
        
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

        self.ui.comboBox_basis2.setCurrentText(self.react.settings.basis_diff)
        self.ui.comboBox_basis3.setCurrentText(self.react.settings.basis_pol1)
        self.ui.comboBox_basis4.setCurrentText(self.react.settings.basis_pol2)

    def filename_update(self):
        
        self.filename = self.ui.lineEdit_filename.text()

        self.ui.lineEdit_chk.setText(self.filename + ".chk")
        self.ui.lineEdit_schk.setText(self.filename + "_copy.chk")
        self.ui.lineEdit_oldchk.setText(self.filename + "_old.chk")


    def insert_model_atoms(self):
        """
        :return:
        """

        if "pdb" in self.filepath.split(".")[-1]:
            atoms = self.mol_obj.formatted_pdb
        else:
            self.ui.button_auto_freeze.setEnabled(False)
            atoms = self.mol_obj.formatted_xyz

        for i in range(len(atoms)):
            self.ui.list_model.insertItem(i, atoms[i])

    def auto_freeze_atoms(self):
        """
        Goes through PDB atoms and tries to figure out base on pdb atom names and distances what atoms
        are terminal/chopped region atoms that should be frozen.
        """
        expected = ["CA", "C", "H", "N", "O"]
        atoms = self.mol_obj.atoms
        for atom in atoms:
            pdb_name = atom.get_pdb_atom_name
            if pdb_name in ["C", "N"]:
                atoms.pop(0)
                for next_atom in atoms:
                    radius = atom_distance(atom.get_coordinate, next_atom.get_coordinate)
                    if radius < 1.7:
                        if next_atom.get_pdb_atom_name not in expected:
                            atom_nr = next_atom.get_atom_index
                            self.ui.list_freeze_atoms.insertItem(0, f"X {atom_nr} F")
                            if self.pymol:
                                self.pymol_spheres(atom_nr)

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
        # TODO reply --> just open the .com file in the current state (tab) of REACT after write?
        # TODO on_write should probably just write whatever is in the preview window to a file.
        """

        self.mol_obj.filename = self.ui.lineEdit_filename.text()
        self.mol_obj.job_type = self.ui.comboBox_job_type.currentText()
        self.mol_obj.basis = self.ui.comboBox_basis1.currentText()
        self.mol_obj.basis_diff = self.ui.comboBox_basis2.currentText()
        self.mol_obj.basis_pol1 = self.ui.comboBox_basis3.currentText()
        self.mol_obj.basis_pol2 = self.ui.comboBox_basis4.currentText()
        self.react.states[self.react.state_index].add_instance(self.mol_obj)

        self.close()

    def closeEvent(self, event):
        if self.pymol:
            self.pymol.pymol_cmd("set mouse_selection_mode, 1")
            self.pymol.pymol_cmd("hide spheres,")
            self.pymol.unmonitor_clicks()


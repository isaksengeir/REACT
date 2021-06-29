from PyQt5 import QtWidgets
from UIs.SetupWindow import Ui_SetupWindow


class CalcSetupWindow(QtWidgets.QMainWindow, Ui_SetupWindow):
    def __init__(self, parent, DFT):
        super(CalcSetupWindow, self).__init__(parent)
        self.react = parent
        self.DFT = DFT
        self.ui = Ui_SetupWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REACT - Calculation setup")



        # TODO RE-implement these:
        #self.ui.add_button1.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_jobkey, self.ui.job_keys, "opt keys"))
        #self.ui.del_button1.clicked.connect(lambda: self.del_item_from_list(self.ui.job_keys, "opt keys"))
        #self.ui.add_button_2.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_addkeys, self.ui.add_keys, "additional keys"))
        #self.ui.del_button_2.clicked.connect(lambda: self.del_item_from_list(self.ui.add_keys, "additional keys"))
        #self.ui.add_button_3.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_link0, self.link0_keys, "link 0"))
        #self.ui.del_button_3.clicked.connect(lambda: self.del_item_from_list(self.ui.link0_keys, "link 0"))
        #self.ui.job_type_combobox.textActivated.connect(lambda: self.combobox_update(self.job_type_combobox, "job type"))
        #self.ui.func_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.func_comboBox, "functional"))
        #self.ui.basis1_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis1_comboBox, "basis"))
        #self.ui.basis2_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis2_comboBox, "diff"))
        #self.ui.basis3_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis3_comboBox, "pol1"))
        #self.ui.basis4_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis4_comboBox, "pol2"))

        self.read_selected_file()
        self.fill_main_tab()

        #self.ui.Button_add_job.clicked.connect(lambda: self.add_item_to_list())
        self.ui.comboBox_basis1.textActivated.connect(self.update_basis_boxes)
        self.ui.comboBox_job_type.textActivated.connect(self.update_job_checkBoxes)

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
        self.ui.comboBox_job_type.addItems(self.DFT.all_job_types)
        self.ui.comboBox_funct.addItems(self.DFT.all_functionals)
        self.ui.comboBox_basis1.addItems([x for x in self.DFT.all_basis])
        self.ui.List_add_job.addItems(self.DFT.job_options)
        self.ui.list_route.addItems(self.DFT.route_options)

        self.ui.comboBox_job_type.setCurrentText(self.DFT.job_type)
        self.ui.comboBox_funct.setCurrentText(self.DFT.functional)
        self.ui.comboBox_basis1.setCurrentText(self.DFT.basis)

        self.update_basis_boxes()

    def update_basis_boxes(self):
        """
        Update basis functions comboBoxes according to current basis

        :return:
        """

        self.ui.comboBox_basis2.clear()
        self.ui.comboBox_basis3.clear()
        self.ui.comboBox_basis4.clear()

        basis = self.ui.comboBox_basis1.currentText()

        self.ui.comboBox_basis2.addItems(self.DFT.all_basis[basis]["diff"])
        self.ui.comboBox_basis3.addItems(self.DFT.all_basis[basis]["pol1"])
        self.ui.comboBox_basis4.addItems(self.DFT.all_basis[basis]["pol2"])

        if basis == self.DFT.basis:
            self.ui.comboBox_basis2.setCurrentText(self.DFT.basis_funct["diff"])
            self.ui.comboBox_basis3.setCurrentText(self.DFT.basis_funct["pol1"])
            self.ui.comboBox_basis4.setCurrentText(self.DFT.basis_funct["pol2"])

    def read_selected_file(self):
        """

        :return:
        """

        state = self.react.get_current_state
        filepath = self.react.tabWidget.currentWidget().currentItem().text()

        #TODO can we remove this dependency of doing 'state - 1' ?
        mol_obj = self.react.states[state - 1].get_molecule_object(filepath)
        xyz = mol_obj.get_formatted_xyz
        print(filepath)
        if "pdb" in filepath.split(".")[-1]:
            # insert pdb atoms in model atoms
            for i in range(len(mol_obj.atoms)):
                atom = mol_obj.atoms[i]
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

        if basis in self.settings["user"]["basis"] and\
           basis in self.DFT_options["basis"]:
            #in case basis is in both, merge diff and pol options
            basis_options = {"diff": [], "pol1": [], "pol2": []}

            for key in ["diff", "pol1", "pol2"]:

                temp = self.DFT_options['basis'][basis][key]
                basis_options[key].extend(temp)

                temp = self.settings["user"]["basis"][basis][key]
                basis_options[key].extend(temp)

                # removes any duplicates in list
                basis_options[key] = list(set(basis_options[key]))

        elif basis in self.DFT_options['basis']:
            basis_options = self.DFT_options['basis'][basis]
        elif basis in self.settings["user"]["basis"]:
            basis_options = self.settings["user"]["basis"][basis]


        for item in basis_options.items():
            if item[0] == "diff":
                if item[1]:
                    self.ui.basis2_comboBox.addItems(item[1])
            if item[0] == "pol1":
                if item[1]:
                    self.ui.basis3_comboBox.addItems(item[1])
            if item[0] == "pol2":
                if item[1]:
                    self.ui.basis4_comboBox.addItems(item[1])


        self.ui.basis2_comboBox.blockSignals(False)
        self.ui.basis3_comboBox.blockSignals(False)
        self.ui.basis4_comboBox.blockSignals(False)

        #self.curr_choices["diff"] = self.ui.basis2_comboBox.currentText()
        #self.curr_choices["diff"] = self.ui.basis2_comboBox.currentText()

    def add_item_to_list(self, Qtextinput, Qlist, DFT_key):
        """
        :param Qtextinput: QLineEdit
        :param Qlist: QListWidget
        :param DFT_key: str: key to access correct variable in self.settings
        Adds the text input from user (past to Qtextinput) to correct
        QlistWidget and updates self.settings accordingly.
        """
        user_input = Qtextinput.text()
        if user_input and user_input not in self.curr_choices[DFT_key]:
            self.curr_choices[DFT_key].append(user_input)
            Qlist.addItem(user_input)

    def del_item_from_list(self, Qlist, DFT_key):
        """
        :param Qlist: QListWidget
        :param DFT_key: str: key to access correct variable in self.settings
        Removes item in QlistWdiget and updates self.settings accordingly.
        """
        item_text = Qlist.currentItem().text()
        if item_text in self.curr_choices[DFT_key]:
            self.curr_choices[DFT_key].remove(item_text)
        Qlist.takeItem(Qlist.currentRow())

    def on_cancel(self):
        self.close()


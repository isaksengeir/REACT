from PyQt5 import QtWidgets
from UIs.SetupWindow import Ui_SetupWindow
from mods.GaussianFile import InputFile


class CalcSetupWindow(QtWidgets.QMainWindow, Ui_SetupWindow):
    def __init__(self, parent, filepath):
        super(CalcSetupWindow, self).__init__(parent)
        self.react = parent
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
        self.ui.comboBox_job_type.addItems(self.DFT.all_job_types)
        self.ui.comboBox_funct.addItems(self.DFT.all_functionals)
        self.ui.comboBox_basis1.addItems([x for x in self.DFT.all_basis])
        self.ui.List_add_job.addItems(self.DFT.job_options)
        self.ui.list_link0.addItems(self.DFT.link0_options)

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
            self.ui.comboBox_basis2.setCurrentText(self.DFT.basis_diff)
            self.ui.comboBox_basis3.setCurrentText(self.DFT.basis_pol1)
            self.ui.comboBox_basis4.setCurrentText(self.DFT.basis_pol2)

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



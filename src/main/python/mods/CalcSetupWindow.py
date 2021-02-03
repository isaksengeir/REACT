from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from UIs.CalcSetupWindow import Ui_CalcSetupWindow
from UIs.CalcSetupMeny import Ui_setupMeny



class CalcSetupWindow(QtWidgets.QMainWindow, Ui_CalcSetupWindow):
    def __init__(self, parent):
        super(CalcSetupWindow, self).__init__(parent)
        self.react = parent
        self.ui = Ui_CalcSetupWindow()
        self.ui.setupUi(self)
        self.meny = CalcSetupMeny(self.react)
        self.meny.show()

        self.DFT_options = {'functional': ['B3LYP', 'rB3LYP', 'M062X'],
                    'basis': {'3-21G': {'pol1': [''], 'pol2': [''], 'diff': [' ', '+']},
                                  '6-21G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
                                  '4-31G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
                                  '6-31G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                            'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                            'diff': ['', '+', '++']},
                                  '6-311G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                             'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                             'diff': ['', '+', '++']},
                                  'D95': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                          'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                          'diff': ['', '+', '++']}
                                   }
                    }

        # Copy current DFT setings from REACT. 
        # Some of the values in this variable may be None or False, else, 
        # It should look like this:
        #
        # self.settings["DFT"]: {"functional"     : str(),
        #                        "basis"          : (str(), {"pol1": str(), "pol2": str(), "diff": str()}),
        #                        "additional keys": [],
        #                        "link 0"         : [],
        #                        "opt keys"       : [],
        #                        "user"           : {"functional": list(), "basis": dict()}}

        self.settings = parent.settings["DFT"]
        self.curr_choices = {"job type": "optimization", "job keys": self.settings["opt keys"],
                             "functional": self.settings["functional"], "basis": self.settings["basis"][0],
                             "pol1": self.settings["basis"][1]["pol1"], "pol2": self.settings["basis"][1]["pol2"],
                             "diff": self.settings["basis"][1]["diff"], "link 0": self.settings["link 0"],
                             "additional keys": self.settings["additional keys"]}

        self.read_settings_set_window()

        self.ui.add_button1.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_jobkey, self.ui.job_keys, "opt keys"))
        self.ui.del_button1.clicked.connect(lambda: self.del_item_from_list(self.ui.job_keys, "opt keys"))
        self.ui.add_button_2.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_addkeys, self.ui.add_keys, "additional keys"))
        self.ui.del_button_2.clicked.connect(lambda: self.del_item_from_list(self.ui.add_keys, "additional keys"))
        self.ui.add_button_3.clicked.connect(lambda: self.add_item_to_list(self.ui.linedit_link0, self.link0_keys, "link 0"))
        self.ui.del_button_3.clicked.connect(lambda: self.del_item_from_list(self.ui.link0_keys, "link 0"))
        self.ui.job_type_combobox.textActivated.connect(lambda: self.combobox_update(self.job_type_combobox, "job type"))
        self.ui.func_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.func_comboBox, "functional"))
        self.ui.basis1_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis1_comboBox, "basis"))
        self.ui.basis2_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis2_comboBox, "diff"))
        self.ui.basis3_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis3_comboBox, "pol1"))
        self.ui.basis4_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.basis4_comboBox, "pol2"))

        self.ui.cancel_button.clicked.connect(self.on_cancel)

    def combobox_update(self, widget, key):
        
        text = widget.currentText()

        self.curr_choices[key] = text
        if key == "basis":
            self.update_basis_options(text)

        print(self.curr_choices)

    def read_settings_set_window(self):
        """
        Checks for additional functional, basis sets or additional keys from
        self.react.settings. Will then fill all fields and set current options
        """
        self.ui.job_type_combobox.blockSignals(True)
        self.ui.func_comboBox.blockSignals(True)
        self.ui.basis1_comboBox.blockSignals(True)
        self.ui.basis2_comboBox.blockSignals(True)
        self.ui.basis3_comboBox.blockSignals(True)
        self.ui.basis4_comboBox.blockSignals(True)

        # fill comboboxes and lists
        self.ui.job_type_combobox.addItems(["Optimization (minimum)", "Optimization (TS)", "Frequency"])
        self.ui.func_comboBox.addItems(self.DFT_options["functional"] + self.settings["user"]["functional"])
        self.ui.basis1_comboBox.addItems([x for x in self.DFT_options['basis']])
        self.ui.basis1_comboBox.addItems([x for x in self.settings["user"]["basis"] if x not in self.DFT_options['basis']])
        self.ui.job_keys.addItems(self.curr_choices["job keys"])
        self.ui.add_keys.addItems(self.curr_choices["additional keys"])
        self.ui.link0_keys.addItems(self.curr_choices["link 0"])

        # set comboboxes according to current settings
        self.ui.func_comboBox.setCurrentText(self.settings["functional"])
        self.ui.basis1_comboBox.setCurrentText(self.settings["basis"][0])
        self.update_basis_options(self.settings["basis"][0])
        self.ui.basis2_comboBox.setCurrentText(self.settings["basis"][1]["diff"])
        self.ui.basis3_comboBox.setCurrentText(self.settings["basis"][1]["pol1"])
        self.ui.basis4_comboBox.setCurrentText(self.settings["basis"][1]["pol2"])

        self.ui.job_type_combobox.blockSignals(False)
        self.ui.func_comboBox.blockSignals(False)
        self.ui.basis1_comboBox.blockSignals(False)
        self.ui.basis2_comboBox.blockSignals(False)
        self.ui.basis3_comboBox.blockSignals(False)
        self.ui.basis4_comboBox.blockSignals(False)

    def update_basis_options(self, basis):
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
        self.meny.close()
        self.close()


class CalcSetupMeny(QtWidgets.QMainWindow, Ui_setupMeny):
    def __init__(self, parent):
        super(CalcSetupMeny, self).__init__(parent, Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.react = parent
        self.ui = Ui_setupMeny()
        self.ui.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.clicked = False
        self.move(300,300)

    def mousePressEvent(self, ev):
        self.old_pos = ev.screenPos()

    def mouseMoveEvent(self, ev):
        if self.clicked:
            dx = self.old_pos.x() - ev.screenPos().x()
            dy = self.old_pos.y() - ev.screenPos().y()
            self.move(self.pos().x() - dx, self.pos().y() - dy)
        self.old_pos = ev.screenPos()
        self.clicked = True
        return QtWidgets.QWidget.mouseMoveEvent(self, ev)
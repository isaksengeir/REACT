from PyQt5 import QtWidgets
from UIs.SettingsWindow import Ui_SettingsWindow


class GlobalSettings(QtWidgets.QMainWindow):
    """
    User window to interact with global settings (REACT attributes
    workdir, DFT_settings and Ui_stylemode)
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.react = parent
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.ui.add_DFT_button_1.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_1, self.ui.add_DFT_list_1, "additional keys"))
        self.ui.del_DFT_button_1.clicked.connect(lambda: self.del_item_from_list(self.ui.additionalKeys_1, self.ui.add_DFT_list_1, "additional keys"))
        self.ui.add_DFT_button_2.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_2, self.ui.add_DFT_list_2, "link 0"))
        self.ui.del_DFT_button_2.clicked.connect(lambda: self.del_item_from_list(self.ui.additionalKeys_2, self.ui.add_DFT_list_2, "link 0"))
        self.ui.add_DFT_button_4.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_3, self.ui.add_DFT_list_3, "opt keys"))
        self.ui.del_DFT_button_4.clicked.connect(lambda: self.del_item_from_list(self.ui.additionalKeys_3, self.ui.add_DFT_list_3, "opt keys"))
        #self.ui.change_cwd_button.clicked.connect(self.change_cwd)
        #self.ui.change_pymol_button.clicked.connect(self.change_pymol)

        

        # TODO: move this attribute to somewhere accessible for setup class
        self.DFT_options = {'functional': ['B3LYP', 'rB3LYP', 'M062X'],
                            'basis set': {'3-21G': {'pol1': None, 'pol2': None, 'diff': ['+', ' ']},
                                          '6-21G': {'pol1': ['d'], 'pol2': ['p'], 'diff': None},
                                          '4-31G': {'pol1': ['d'], 'pol2': ['p'], 'diff': None},
                                          '6-31G': {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                    'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                    'diff': ['+', '++', ' ']},
                                          '6-311G': {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                     'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                     'diff': ['+', '++', ' ']},
                                          'D95': {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                  'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                  'diff': ['+', '++', ' ']}
                                           }
                            }

        # Copy current setings from REACT. This variable will be modified
        # when the user makes changes to settings. On save, this variable
        # will replace the original settings variable beloning to REACT.
        # Some of the values in this variable may be None or False, else, 
        # It should look like this:
        #
        # self.settings = {"workdir": str(),
        #                  "DFT": {"functional"    : str(),
        #                          "basis"         : (str(), {"pol1": str(), "pol2": str(), "diff": str()}),
        #                          "additional keys": [],
        #                          "link 0"        : [],
        #                          "opt keys"      : [],
        #                          "user funct"    : [], 
        #                          "user basis": {}},
        #                  "pymolpath": str(),
        #                  "REACT pymol" : bool
        #                  "Ui": int()
        #                  }
        self.settings = parent.settings

        self.read_settings_set_window()

    def add_item_to_list(self, Qtextinput, Qlist, DFT_key):
        """
        """
        user_input = Qtextinput.text()
        if user_input and user_input not in self.settings["DFT"][DFT_key]:
            self.settings["DFT"][DFT_key].append(user_input)
            Qlist.addItem(user_input)
            print(self.settings["DFT"][DFT_key])

    def del_item_from_list(self, Qtextinput, Qlist, DFT_key):
        item_text = Qlist.currentItem().text()

        if item_text in self.settings["DFT"][DFT_key]:
            self.settings["DFT"][DFT_key].remove(item_text)

        Qlist.takeItem(Qlist.currentRow())


    def update_basis_options(self, basis):

        self.ui.basis2_comboBox_4.clear()
        self.ui.basis3_comboBox_6.clear()
        self.ui.basis4_comboBox_5.clear()

        if basis in self.DFT_options['basis set']:
            basis_options = self.DFT_options['basis set'][basis]
        elif basis in self.settings["user basis"]:
            basis_options = self.settings["user basis"][basis]
        else:
            self.react.append_text('Basis set is unknown to REACT. Add polarization and diffuse functions as needed.')
            return

        for item in basis_options.items():
            if item[0] == "diff":
                if item[1]:
                     self.ui.basis2_comboBox_4.addItems(item[1])
            if item[0] == "pol1":
                if item[1]:
                    self.ui.basis3_comboBox_6.addItems(item[1])
            if item[0] == "pol2":
                if item[1]:
                    self.ui.basis4_comboBox_5.addItems(item[1])

    def read_settings_set_window(self):
        """
        Checks for additional functional, basis sets or additional keys from
        self.react.settings. Will then fill all fields and set current options
        """

        # fill functional and basis set comboboxes
        self.ui.comboBox_funct.addItems(self.DFT_options['functional'])
        self.ui.comboBox_funct.addItems(self.settings["DFT"]["user funct"])
        self.ui.basis1_comboBox_3.addItems([x for x in self.DFT_options['basis set']])
        self.ui.basis1_comboBox_3.addItems([x for x in self.settings["DFT"]["user basis"]])

        # Read current settings, set window accordingly
        for item in self.settings.items():
            if item[0] == "DFT":
                self.ui.comboBox_funct.setCurrentText(item[1]["functional"])
                self.ui.basis1_comboBox_3.setCurrentText(item[1]["basis"][0])

                # update polarization and diffuse boxes, based on current basis
                self.update_basis_options(item[1]["basis"][0])

                #set current pol and diff functions
                self.ui.basis2_comboBox_4.setCurrentText(item[1]["basis"][1]["diff"])
                self.ui.basis3_comboBox_6.setCurrentText(item[1]["basis"][1]["pol1"])
                self.ui.basis4_comboBox_5.setCurrentText(item[1]["basis"][1]["pol2"])

                # Add all additional keys to appropriate QlistWidget
                self.ui.add_DFT_list_1.addItems(self.settings["DFT"]["additional keys"])
                self.ui.add_DFT_list_2.addItems(self.settings["DFT"]["link 0"])
                self.ui.add_DFT_list_3.addItems(self.settings["DFT"]["opt keys"])

            if item[0] == 'workdir':
                self.ui.cwd_lineEdit.setText(item[1])
            if item[0] == 'pymolpath':
                self.ui.pymol_lineEdit_2.setText(item[1])
            if item[0] == 'REACT pymol':
                if item[1]:
                    self.ui.checkBox.setChecked(True)
            if item[0] == 'Ui':
                if item[1] == 1:
                    self.ui.dark_button.setChecked(True)
                else:
                    self.ui.light_button.setChecked(True)
    
    def switch_Ui_colormode(self, color):
        """
        Switch Ui colormode. Darkmode: color = 1, lightmode: color = 0 
        """
        pass


    def add_keywords(self, keys, list):
        #
        pass



    def closeEvent(self, event):
        """
        When closing window, set to settings_window to None.
        :param event:
        """
        self.react.settings_window = None


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

        # TODO: move this attribute to somewhere accessible for setup class
        self.DFT_options = {'functional': ['B3LYP', 'rB3LYP', 'M062X'],
                            'basis set': {'3-21G': {'pol1': None, 'pol2': None, 'diff': ['+']},
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

        # list to store DFT data added by the user, either from self.setting or
        # user the graphical interface.
        self.additional_keys = []
        self.link_0 = []
        self.user_funct = []
        self.user_basis = {}

        self.read_settings_set_window()

    def update_basis_options(self, basis):

        self.ui.basis2_comboBox_4.clear()
        self.ui.basis3_comboBox_6.clear()
        self.ui.basis4_comboBox_5.clear()


        if basis in self.DFT_options['basis set']:
            basis_options = self.DFT_options['basis set'][basis]
        elif basis in self.user_basis:
            basis_options = self.user_basis[basis]
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

        if isinstance(self.react.settings["DFT"]["user funct"], list):
            self.user_funct.extend(self.react.settings["DFT"]["user funct"])

        if isinstance(self.react.settings["DFT"]["user basis"],dict):
            for item in self.react.settings["DFT"]["user basis"].items():
                if not item[0] in self.DFT_options:
                    #only add if this is a new basis set
                    self.user_basis[item[0]] = item[1]

        # fill functional and basis set comboboxes
        self.ui.comboBox_funct.addItems(self.DFT_options['functional'] + self.user_funct)
        self.ui.basis1_comboBox_3.addItems([x for x in self.DFT_options['basis set']])
        self.ui.basis1_comboBox_3.addItems([x for x in self.user_basis])

        for item in self.react.settings.items():
            if item[0] == "DFT":
                self.ui.comboBox_funct.setCurrentText(item[1]["functional"])
                self.ui.basis1_comboBox_3.setCurrentText(item[1]["basis"][0])
                # update polarization and diffuse boxes, based on current basis
                self.update_basis_options(item[1]["basis"][0])
                #dict that store current pol and diff functions
                pol_diff = item[1]["basis"][1]
                self.ui.basis2_comboBox_4.setCurrentText(pol_diff["diff"])
                self.ui.basis3_comboBox_6.setCurrentText(pol_diff["pol1"])
                self.ui.basis4_comboBox_5.setCurrentText(pol_diff["pol2"])


                self.add_additional_keywords(item[1]["additional keys"], self.ui.add_DFT_list_1)
                self.add_additional_keywords(item[1]["link 0"], self.ui.add_DFT_list_2)
                self.add_additional_keywords(item[1]["opt keys"], self.ui.add_DFT_list_3)
            if item[0] == 'workdir':
                self.ui.cwd_lineEdit.setText(item[1])
            if item[0] == 'pymol':
                self.ui.pymol_lineEdit_2.setText(item[1])
            if item[0] == 'Ui':
                if item[1] == 1:
                    self.ui.dark_button.setChecked(True)
                else:
                    self.ui.light_button.setChecked(True)

    def add_additional_keywords(self, keys, list):
        #TODO
        pass



    def closeEvent(self, event):
        """
        When closing window, set to settings_window to None.
        :param event:
        """
        self.react.settings_window = None


from PyQt5 import QtWidgets
from UIs.SettingsWindow import Ui_SettingsWindow
import os
import json


class Settings():
    def __init__(self, parent):

        self.react = parent

        self._workdir = None
        self._pymolpath = None
        self._REACT_pymol = None
        self._pymol_at_launch = None
        self._UI_mode = None
        
        #DFT settings
        self._functional = None
        self._basis = None
        self._basis_diff = None
        self._basis_pol1 = None
        self._basis_pol2 = None
        self._empiricaldispersion = None
        self._job_mem = None
        self._chk = None
        self._job_options = None
        self._link0_options = None
        self._basis_options = None
        self._functional_options = None

        try:
            with open('.custom_settings.json', 'r') as f:
                custom_data = json.load(f, object_hook=cf.json_hook_int_please)
                self.load_custom_settings(custom_data)
        except:
            self.set_default_settings()
   
    @property
    def workdir(self):
        return self._workdir

    @property
    def pymolpath(self):
        return self._pymolpath

    @property
    def REACT_pymol(self):
        return self._REACT_pymol
    
    @property
    def pymol_at_launch(self):
        return self._pymol_at_launch
    
    @property
    def UI_mode(self):
        return self._UI_mode

    @property
    def basis(self):
        return self._basis
    
    @property
    def basis_diff(self):
        return self._basis_diff

    @property
    def basis_pol1(self):
        return self._basis_pol1
    
    @property
    def basis_pol2(self):
        return self._basis_pol2

    @property
    def functional(self):
        return self._functional

    @property
    def job_mem(self):
        return self._job_mem

    @property
    def chk(self):
        return self._chk

    @property
    def empiricaldispersion(self):
        return self._empiricaldispersion

    @property
    def job_options(self):
        return self._job_options

    @property
    def link0_options(self):
        return self._link0_options

    @workdir.setter
    def workdir(self, value):
        self._workdir = value

    @pymolpath.setter
    def pymolpath(self, value):
        self._pymolpath = value

    @REACT_pymol.setter
    def REACT_pymol(self, value):
        self._REACT_pymol = value
    
    @pymol_at_launch.setter
    def pymol_at_launch(self, value):
        self._pymol_at_launch = value
    
    @UI_mode.setter
    def UI_mode(self, value):
        self._UI_mode = value

    @functional.setter
    def functional(self, value):
        self._functional = value

    @basis.setter
    def basis(self, value):
        self._basis = value

    @basis_diff.setter
    def basis_diff(self, value):
        self._basis_diff = value

    @basis_pol1.setter
    def basis_pol1(self, value):
        self._basis_pol1 = value
    
    @basis_pol2.setter
    def basis_pol2(self, value):
        self._basis_pol2 = value

    @job_mem.setter
    def job_mem(self, value):
        if type(value) == int:
            self._job_mem = value

    @chk.setter
    def chk(self, value):
        self._chk = value

    @empiricaldispersion.setter
    def empiricaldispersion(self, value):
        self._empiricaldispersion = value

    @job_options.setter
    def job_options(self, value):
        self._job_options = value

    @link0_options.setter
    def link0_options(self, value):
        self._link0_options = value
    
    def set_default_settings(self):
        self.workdir = os.getcwd()
        self.pymolpath = None
        self.REACT_pymol = True
        self.pymol_at_launch = True
        self.UI_mode = True
        
        #DFT settings
        self.functional = "B3LYP"
        self.basis = "6-31G"
        self.basis_diff = None
        self.basis_pol1 = "d"
        self.basis_pol2 = "p"
        self.empiricaldispersion = "gd3"
        self.job_mem = 6
        self.chk = True
        self.schk = False
        self.oldchk = False
        self.job_options = {"Opt (minimum)": ["noeigentest", "calcfc"], "Opt (TS)": [], "Freq": [], "IRC": [], "IRCMax": [], "SP": []}
        self.link0_options = []
        self.basis_options = {'3-21G': {'pol1': [''], 'pol2': [''], 'diff': [' ', '+']},
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
        self.functional_options = ['B3LYP', 'rB3LYP', 'M062X']


    def load_custom_settings(self, settings):
        for key in ['workdir', 'pymolpath', 'REACT_pymol', 'pymol_at_launch',
                    'UI_mode', 'functional', 'basis', 'basis_diff', 'basis_pol1'
                    'basis_pol2', 'empiricaldispersion', 'job_mem', 'chk', 'job_options',
                    'link0_options', 'basis_option', 'functional_options']:

            self._load_custom_settings(key)

    def _load_custom_settings(self, settings, key):
        try:
            item = settings.pop(key)

            if key == 'workdir':
                self.workdir = item
            if key == 'pymolpath':
                self.pymolpath = item
            if key == 'REACT_pymol':
                self.REACT_pymol = item
            if key == 'pymol_at_launch':
                self.pymol_at_launch = item
            if key == 'UI_mode':
                self.UI_mode = item    
            if key == 'functional':
                self.functional = item    
            if key == 'basis':
                self.basis = item
            if key == 'basis_diff':
                self.basis_diff = item
            if key == 'basis_pol1':
                self.basis_pol1 = item
            if key == 'basis_pol2':
                self.basis_pol2 = item
            if key == 'empiricaldispersion':
                self.empiricaldispersion = item
            if key == 'job_mem':
                self.job_mem = item
            if key == 'chk':
                self.chk = item
            if key == 'job_options':
                self.job_options = item
            if key == 'link0_options':
                self.link0_options = item
            if key == 'basis_options':
                self.basis_options = item
            if key == 'functional_options':
                self.functional_options = item
        except:
            self.react.append_text(f'Failed to load "{key}" from custom settings')

    def save_custom_settings(self):
        settings = {}
        
        settings['workdir'] = self.workdir
        settings['pymolpath'] = self.pymolpath
        settings['REACT_pymol'] = self.REACT_pymol
        settings['pymol_at_launch'] = self.pymol_at_launch
        settings['UI_mode'] = self.UI_mode
        settings['functional'] = self.functional
        settings['basis'] = self.basis
        settings['basis_diff'] = self.basis_diff
        settings['basis_pol1'] = self.basis_pol1
        settings['basis_pol2'] = self.basis_pol2
        settings['empiricaldispersion'] = self.empiricaldispersion
        settings['job_mem'] = self.job_mem
        settings['chk'] = self.chk
        settings['job_options'] = self.job_options
        settings['link0_options'] = self.link0_options
        settings['basis_option'] = self.basis_options
        settings['functional_options'] = self.functional_options
        
        with open(self.workdir + '.custom_settings.json', 'w+') as f:
            json.dump(settings, f)



class SettingsTheWindow(QtWidgets.QMainWindow):
    """
    User window to interact with instanse of Settings
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.react = parent
        self.settings = parent.settings
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        
    #    self.DFT_options = {'functional': ['B3LYP', 'rB3LYP', 'M062X'],
    #                        'basis': {'3-21G': {'pol1': [''], 'pol2': [''], 'diff': [' ', '+']},
    #                                      '6-21G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
    #                                      '4-31G': {'pol1': ['', 'd'], 'pol2': ['', 'p'], 'diff': ['']},
    #                                      '6-31G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
    #                                                'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
    #                                                'diff': ['', '+', '++']},
    #                                      '6-311G': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
    #                                                 'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
    #                                                 'diff': ['', '+', '++']},
    #                                      'D95': {'pol1': ['', 'd', '2d', '3d', 'df', '2df', '3df', '3d2f'],
    #                                              'pol2': ['', 'p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
    #                                              'diff': ['', '+', '++']}
    #                                       }
    #                        }
#
        # Copy current setings from REACT. This variable will be modified
        # when the user makes changes to settings. On save, this variable
        # will replace the original settings variable beloning to REACT.
        # Some of the values in this variable may be None or False, else, 
        # It should look like this:
        #
        # self.settings = {"workdir": os.getcwd(),
        #                  "DFT": {"functional": "B3LYP",
        #                  "basis": ("6-31G", {"pol1": "d", "pol2": 'p', "diff": None}),
        #                  "additional keys": ["empiricaldispersion=gd3"],
        #                  "link 0"        : [],
        #                  "job keys"      : {"Opt (minimum)": ["noeigentest", "calcfc"], "Opt (TS)": [], "Freq": [], "IRC": [], "IRCMax": [], "SP": []},
        #                  "user"    : {"functional": [], "basis": {}}}, 
        #                  "pymolpath": None,
        #                  "REACT pymol" : True,
        #                  "pymol at launch": True,
        #                  "Ui": 1
        #                  }
        #self.settings = copy.deepcopy(parent.settings)

        # fill functional and basis set comboboxes
        self.ui.comboBox_funct.addItems(self.settings.functional_options)
        self.ui.basis1_comboBox_3.addItems([x for x in self.settings.basis_options])
        self.ui.job_type_comboBox.addItems(["Opt (minimum)", "Opt (TS)", "Freq", "IRC", "IRCMax", "SP"])

        # Read current settings, set window accordingly

        self.ui.comboBox_funct.setCurrentText(self.settings.functional)
        self.ui.basis1_comboBox_3.setCurrentText(self.settings.basis)
        # update polarization and diffuse boxes, based on current basis
        self.update_basis_options(self.settings.basis)
        #set current pol and diff functions
        self.ui.basis2_comboBox_4.setCurrentText(self.settings.basis_diff)
        self.ui.basis3_comboBox_6.setCurrentText(self.settings.basis_pol1)
        self.ui.basis4_comboBox_5.setCurrentText(self.settings.basis_pol2)
        # Add all additional keys to appropriate QlistWidget
        #self.ui.add_DFT_list_1.addItems(self.settings["DFT"]["additional keys"])
        #self.ui.add_DFT_list_2.addItems(self.settings["DFT"]["link 0"])
        #self.ui.add_DFT_list_3.addItems(self.settings["DFT"]["job keys"]["Opt (minimum)"])

        self.ui.cwd_lineEdit.setText(self.settings.workdir)

        if self.settings.pymolpath != bool:
            self.ui.pymol_lineEdit_2.setText(self.settings.pymolpath)

        if self.settings.pymol_at_launch:
            self.ui.open_pymol_checkBox.setChecked(True)

        if self.settings.UI_mode == 1:
            self.ui.dark_button.setChecked(True)
        else:
            self.ui.light_button.setChecked(True)

        self.ui.label_2.hide()
        self.ui.dark_button.hide()
        self.ui.light_button.hide()

        self.ui.add_DFT_button_1.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_1, self.ui.add_DFT_list_1, "additional keys"))
        self.ui.del_DFT_button_1.clicked.connect(lambda: self.del_item_from_list(self.ui.add_DFT_list_1, "additional keys"))
        self.ui.add_DFT_button_2.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_2, self.ui.add_DFT_list_2, "link 0"))
        self.ui.del_DFT_button_2.clicked.connect(lambda: self.del_item_from_list(self.ui.add_DFT_list_2, "link 0"))
        self.ui.add_DFT_button_4.clicked.connect(lambda: self.add_item_to_list(self.ui.additionalKeys_3, self.ui.add_DFT_list_3, "job keys"))
        self.ui.del_DFT_button_4.clicked.connect(lambda: self.del_item_from_list(self.ui.add_DFT_list_3, "job keys"))
        self.ui.save_button.clicked.connect(self.save_settings)
        self.ui.cancel_button.clicked.connect(self.close)
        self.ui.comboBox_funct.textActivated.connect(lambda: self.combobox_update(self.ui.comboBox_funct, "functional"))
        self.ui.basis1_comboBox_3.textActivated.connect(lambda: self.combobox_update(self.ui.basis1_comboBox_3, "basis"))
        self.ui.basis2_comboBox_4.textActivated.connect(lambda: self.combobox_update(self.ui.basis2_comboBox_4, "diff"))
        self.ui.basis3_comboBox_6.textActivated.connect(lambda: self.combobox_update(self.ui.basis3_comboBox_6, "pol1"))
        self.ui.basis4_comboBox_5.textActivated.connect(lambda: self.combobox_update(self.ui.basis4_comboBox_5, "pol2"))
        self.ui.job_type_comboBox.textActivated.connect(lambda: self.combobox_update(self.ui.job_type_comboBox, "job type"))
        self.ui.change_cwd_button.clicked.connect(lambda: self.new_path_from_dialog(self.ui.cwd_lineEdit, "Select working directory"))
        self.ui.change_pymol_button.clicked.connect(lambda: self.new_path_from_dialog(self.ui.pymol_lineEdit_2,"select PyMOL path"))
        #self.ui.checkBox.stateChanged.connect(lambda: self.check_box_update(self.ui.checkBox, "REACT pymol"))
        #self.ui.open_pymol_checkBox.stateChanged.connect(lambda: self.check_box_update(self.ui.open_pymol_checkBox, "pymol at launch"))

    def new_path_from_dialog(self, textwidget, title_):
        """
        Changes text in work directory field using file dialog.
        No change saved in self.settings, this is handeled in save_settings. 
        """

        new_dir = QtWidgets.QFileDialog.getExistingDirectory(self, title_, self.settings.workdir, options=QtWidgets.QFileDialog.DontUseNativeDialog)
        
        # use this instead for native QfileDialog
        # files_, files_type = QtWidgets.QFileDialog.getOpenFileName(self, title_, self.settings["workdir"], "PyMOL app (*.app)",options=QtWidgets.QFileDialog.DontUseNativeDialog)
                                                                
        if new_dir:
            textwidget.setText(new_dir)

#    def check_box_update(self, checkbox, key):
#
#        if checkbox.isChecked():
#            self.settings[key] = True
#        else:
#            self.settings[key] = False

    def combobox_update(self, widget, key):
        """
        :param combobox: QComboBox
        :param key: str: key to identifu what combobox is changed

        Update window after a combobox is changed.
        """
        text = widget.currentText()

        if key == "job type":
            self.ui.add_DFT_list_3.clear()
            self.ui.add_DFT_list_3.addItems(self.settings.job_options[text])
    
        if key == "functional":
            if text not in self.settings.functional_options:
                # new functional not listed in settings from before

                self.settings.functional.append(text)
            
        if key == 'basis':
            if text not in self.settings.basis_options:
                # new basis not listed in settings from before

                self.settings.basis_options[text] = {"pol1": [], "pol2": [], "diff": []}
            self.update_basis_options(text)

        elif key in ["diff", "pol1", "pol2"]:
            basis = self.ui.basis1_comboBox_3.currentText()

            if text not in self.settings.basis_options[basis][key]:
                # diff, pol1 or pol2 not listed for current basis
                self.settings.basis_options[basis][key].append(text)


    def add_item_to_list(self, Qtextinput, Qlist, DFT_key):
        """
        :param Qtextinput: QLineEdit
        :param Qlist: QListWidget
        :param DFT_key: str: key to access correct variable in self.settings
        Adds the text input from user (past to Qtextinput) to correct
        QlistWidget and updates self.settings accordingly.
        """

        user_input = Qtextinput.text()
        Qlist.addItem(user_input)

        #if Qlist == self.ui.add_DFT_list_3:
        #    job_type = self.ui.job_type_comboBox.currentText()
        #    item_list = self.settings["DFT"]["job keys"][job_type]
        #else:
        #    item_list = self.settings["DFT"][DFT_key]

        #if user_input and user_input not in item_list:
        #    item_list.append(user_input)
        #    Qlist.addItem(user_input)

    def del_item_from_list(self, Qlist, DFT_key):
        """
        :param Qlist: QListWidget
        :param DFT_key: str: key to access correct variable in self.settings
        Removes item in QlistWdiget and updates self.settings accordingly.
        """
        item_text = Qlist.currentItem().text()
        Qlist.takeItem(Qlist.currentRow())

        #if Qlist == self.ui.add_DFT_list_3:
        #    job_type = self.ui.job_type_comboBox.currentText()
        #    item_list = self.settings["DFT"]["job keys"][job_type]
        #else:
        #    item_list = self.settings["DFT"][DFT_key]  

        #if item_text in item_list:
        #    item_list.remove(item_text)
        #Qlist.takeItem(Qlist.currentRow())


    def update_basis_options(self, basis):
        """
        :param basis: str: name current basis
        Updates polarization and diffuse functions avail for basis set
        """

        #self.block_all_combo_signals(True)

        self.ui.basis2_comboBox_4.clear()
        self.ui.basis3_comboBox_6.clear()
        self.ui.basis4_comboBox_5.clear()

        self.ui.basis2_comboBox_4.addItems(self.settings.basis_options[basis]['diff'])
        self.ui.basis3_comboBox_6.addItems(self.settings.basis_options[basis]['pol1'])
        self.ui.basis4_comboBox_5.addItems(self.settings.basis_options[basis]['pol2'])

        #self.block_all_combo_signals(False)

        #if basis in self.settings["DFT"]["user"]["basis"] and\
        #   basis in self.DFT_options["basis"]:
        #    # in case basis is in both, merge diff and pol options
        #    basis_options = {"diff": [], "pol1": [], "pol2": []}
#
        #    for key in ["diff", "pol1", "pol2"]:
#
        #        temp = self.DFT_options['basis'][basis][key]
        #        basis_options[key].extend(temp)
#
        #        temp = self.settings["DFT"]["user"]["basis"][basis][key]
        #        basis_options[key].extend(temp)
#
        #        # removes any duplicates in list
        #        basis_options[key] = list(set(basis_options[key]))
#
        #elif basis in self.DFT_options['basis']:
        #    basis_options = self.DFT_options['basis'][basis]
        #elif basis in self.settings["DFT"]["user"]["basis"]:
        #    basis_options = self.settings["DFT"]["user"]["basis"][basis]
        #else:
        #    self.react.append_text('Basis set is unknown to REACT. Add polarization and diffuse functions as needed.')
        #    return
#
        #for item in basis_options.items():
        #    if item[0] == "diff":
        #        if item[1]:
        #            self.ui.basis2_comboBox_4.addItems(item[1])
        #    if item[0] == "pol1":
        #        if item[1]:
        #            self.ui.basis3_comboBox_6.addItems(item[1])
        #    if item[0] == "pol2":
        #        if item[1]:
        #            self.ui.basis4_comboBox_5.addItems(item[1])



    def block_all_combo_signals(self, bool_):
        self.ui.comboBox_funct.blockSignals(bool_)
        self.ui.basis1_comboBox_3.blockSignals(bool_)
        self.ui.job_type_comboBox.blockSignals(bool_)
        self.ui.basis2_comboBox_4.blockSignals(bool_)
        self.ui.basis3_comboBox_6.blockSignals(bool_)
        self.ui.basis4_comboBox_5.blockSignals(bool_) 

    def save_settings(self):
        #self.settings["workdir"] = self.ui.cwd_lineEdit.text()
        #self.settings["pymolpath"] = self.ui.pymol_lineEdit_2.text()
        

        self.close()

    
    def switch_Ui_colormode(self, color):
        """
        Switch Ui colormode. Darkmode: color = 1, lightmode: color = 0 
        """
        pass


    def closeEvent(self, event):
        """
        When closing window, set to settings_window to None.
        :param event:
        """
        self.react.settings_window = None


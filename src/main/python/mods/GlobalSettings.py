from PyQt5 import QtWidgets
from UIs.SettingsWindow import Ui_SettingsWindow




class GlobalSettings(QtWidgets.QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        self.react = parent
        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)

        self.workdir = ''
        self.DFT_settings = {}

        self.DFT_options = {'Additional print' : [False, True],
                            'Functional' : ['B3LYP', 'rB3LYP', 'uB3LYP', 'M062X'],
                            'Basis set' : [{'3-31G' : { 'polarization1' : ['d', '2d','3d','df','2df','3df','3d2f'], 
                                                        'pol2': ['p','2p','3p','pd','2pd','3pd','3p2d'],
                                                        'diff' : ['+','++']
                                                        }
                                            },
                                            {'6-31G' : ''} 
                                            ],
                            'empiricaldispersion' : []
                            }

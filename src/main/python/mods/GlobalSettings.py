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
        self.DFT_options = {'Additional print': [False, True],
                            'Functional': ['B3LYP', 'rB3LYP', 'uB3LYP', 'M062X'],
                            'Basis set': {'3-21G':  {'pol1': None, 'pol2': None, 'diff': ['+']},
                                          '6-21G':  {'pol1': ['d'], 'pol2': ['p'], 'diff': None},
                                          '4-31G':  {'pol1': ['d'], 'pol2': ['p'], 'diff': None},
                                          '6-31G':  {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                     'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                     'diff': ['+', '++']},
                                          '6-311G': {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                     'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                     'diff': ['+', '++']},
                                          'D95':    {'pol1': ['d', '2d', '3d', 'df', '2df', '3df', '3d2f'],
                                                     'pol2': ['p', '2p', '3p', 'pd', '2pd', '3pd', '3p2d'],
                                                     'diff': ['+', '++']}
                                          },
                            'empiricaldispersion': ['gd3']
                            }

    def closeEvent(self, event):
        """
        When closing window, set to settings_window to None.
        :param event:
        """
        self.react.settings_window = None

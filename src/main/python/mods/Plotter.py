from PyQt5 import QtWidgets
from UIs.AnyPlot import Ui_AnyPlotter


class Plotter(QtWidgets.QMainWindow, Ui_AnyPlotter):
    def __init__(self, parent):
        super(Plotter, self).__init__(parent)

        self.ui = Ui_AnyPlotter()
        self.ui.setupUi(self)
        self.setWindowTitle("REACT - AnyPlot")
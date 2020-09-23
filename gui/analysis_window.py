import sys
from PyQt5 import QtWidgets, uic

from Analyse import Ui_analyse


class analyse(QtWidgets.QMainWindow, Ui_analyse):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__()
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

window = analyse()
window.show()
app.exec()

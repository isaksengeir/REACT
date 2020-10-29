
from PyQt5 import QtWidgets
from UIs.FileEditor_Window import Ui_Dialog
from UIs.FileEditorWindow import Ui_FileEditorWindow

class FileEditor(QtWidgets.QMainWindow):
    def __init__(self, parent, filepath):
        super().__init__(parent)

        with open(filepath,'r') as f:
            text = f.read()

        self.ui = Ui_FileEditorWindow()
        self.ui.setupUi(self)

        filename = filepath.split("/")[-1]
        self.setWindowTitle(filename)

        self.ui.FileEditorBox.setPlainText(text)

# TODO save changes to file after editing!!! 
# TODO if file is outputfile, make turn it in to a inputfile?
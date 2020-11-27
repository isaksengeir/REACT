
from PyQt5 import QtWidgets
import os
from UIs.FileEditorWindow import Ui_FileEditorWindow
from mods.DialogsAndExceptions import DialogMessage


class FileEditor(QtWidgets.QMainWindow):
    def __init__(self, parent, filepath, readonly=False):
        super().__init__(parent)

        if not os.path.isfile(filepath):
            dialog = DialogMessage(self, "File not found. Please check to see"
                                   "if file has been moved or deleted.")
            dialog.exec_()
            self.close

        self.react = parent
        self.ui = Ui_FileEditorWindow()
        self.ui.setupUi(self)
        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.setWindowTitle(self.filename)

        # True if a new file is created, instead of editing old file
        self.newfile = False

        # if readonly = True the FileEditor can be used to view any file
        self.save_file = True

        if readonly:
            # TODO toggle texteditor to not being editable
            # TODO OK button will not ask for save file name, just close window
            self.save_file = False

        # If file is input file or pdb, read it as it is
        elif self.filename.split(".")[-1] in ["inp", "com", "pdb"]:
            with open(filepath, 'r') as f:
                text = f.read()

        elif self.filename.split(".")[-1] in ["out", "log", "xyz"]:
            text = self.react.create_input_content(self.filepath)
            self.setWindowTitle(self.filename.split('.')[0] + '_new.com')
            self.newfile = True

        self.ui.textwindow.setPlainText(text)

        self.ui.save_button.clicked.connect(self.save_file_)
        self.ui.cancel_button.clicked.connect(self.close)

    def save_file_(self):

        if self.newfile:
            self.filepath = self.filepath.split('.')[0] + '_new.com'

        self.filepath, filter_ = QtWidgets.QFileDialog.getSaveFileName(
                                self, "Save file", self.filepath, "Gaussian input files (*.com *.inp)")

        if self.filepath == '':
            return

        with open(self.filepath, 'w') as f:
            f.write(self.ui.textwindow.toPlainText())

        self.react.add_files_to_list([self.filepath])
        self.setWindowTitle(self.filepath.split('/')[-1])

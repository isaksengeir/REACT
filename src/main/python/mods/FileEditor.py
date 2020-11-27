
from PyQt5 import QtWidgets
from UIs.FileEditorWindow import Ui_FileEditorWindow


class FileEditor(QtWidgets.QMainWindow):
    def __init__(self, parent, filepath, readonly=False):
        super().__init__(parent)
        self.react = parent
        self.ui = Ui_FileEditorWindow()
        self.ui.setupUi(self)

        self.filepath = filepath
        self.filename = self.filepath.split("/")[-1]
        self.setWindowTitle(self.filename)

        self.save_file = True
        # if readonly = True the FileEditor can be used to view any file

        if readonly:
            # TODO toggle texteditor to not being editable
            # TODO OK button will not ask for save file name, just close window
            self.save_file = False

        # If file is input file, xyz or pdb, read it as it is
        elif self.filename.split(".")[-1] in ["inp", "com", "xyz", "pdb"]:
            with open(filepath, 'r') as f:
                text = f.read()
            self.ui.textwindow.setPlainText(text)

        elif self.filename.split(".")[-1] in ["out", "log"]:

            self.file_content = self.react.create_input_content(self.filepath)
            self.setWindowTitle(self.filename.split('.')[0] + '_new.com')
            self.ui.textwindow.setPlainText(self.file_content)

    def save_file_(self):

        filepath, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", self.filepath.split('.')[0] + '_new.com', "Gaussian input files (*.com *.inp)")

        if filepath == '':
            return

        with open(filepath, 'w') as f:
            f.write(self.file_content)
        
        self.react.add_files_to_list([filepath])
        self.setWindowTitle(filepath.split('/')[-1])

# TODO save changes to file after editing!!! 

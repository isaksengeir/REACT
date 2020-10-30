
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

        # If file is input file, read it as it is
        elif self.filename.split(".")[-1] in ["inp", "com"]:
            with open(filepath, 'r') as f:
                text = f.read()
            self.ui.FileEditorBox.setPlainText(text)

        elif self.filename.split(".")[-1] in ["out", "log"]:
            # TODO read output file and get coordinates, basis set, etc....
            self.convert_out_to_inp()

    def convert_out_to_inp(self):
        """
        TODO
        :return:
        """
        print("Hello")
        xyz = self.react.states[self.react.tabWidget.currentIndex()].get_final_xyz(self.filepath)
        for line in xyz:
            self.ui.FileEditorBox.append(line)


# TODO save changes to file after editing!!! 
# TODO if file is outputfile, make turn it in to a inputfile?
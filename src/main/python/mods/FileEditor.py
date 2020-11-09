
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

            self.file_content = self.react.create_input_content(self.filepath)
            
            self.ui.OK_button.setText('Save')
            self.setWindowTitle(self.filename.split('.')[0] + '_new.com')
            self.ui.FileEditorBox.setPlainText(self.file_content)

            self.ui.OK_button.clicked.connect(self.save_file_)
        
        self.ui.Cancel_button.clicked.connect(self.close)

    def save_file_(self):

        filepath, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", self.filepath.split('.')[0] + '_new.com', "Gaussian input files (*.com *.inp)")

        if filepath == '':
            return

        with open(filepath, 'w') as f:
            f.write(self.file_content)
        
        self.react.add_files_to_list([filepath])
        self.setWindowTitle(filepath.split('/')[-1])


    def convert_out_to_inp(self):
        """
        TODO: this function is good for testing, but I (Bente) think the code should be moved to a 'create_InputObject'
        method, belonging to the State-class.
        :return:
        """
        xyz = self.react.states[self.react.tabWidget.currentIndex()].get_final_xyz(self.filepath)
        routecard = self.react.states[self.react.tabWidget.currentIndex()].get_routecard(self.filepath)

        self.ui.FileEditorBox.append(routecard)

        self.ui.FileEditorBox.append('\n')

        for line in xyz:
            self.ui.FileEditorBox.append(line)

        


# TODO save changes to file after editing!!! 

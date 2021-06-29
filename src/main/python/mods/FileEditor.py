
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

        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.save_button.clicked.connect(self.save_file_)
        self.ui.cancel_button.clicked.connect(self.close)
        self.orig_text = ""
        self.read_file()

    def read_file(self):
        """
        Reads file and filetype. comboBox is updated with filetypes in which
        the file can be converted into.
        """

        self.filetype = self.filename.split(".")[-1]

        if self.filetype in ['xyz']:
            self.ui.comboBox.addItems(['com', 'xyz'])

        elif self.filetype == 'out':
            self.ui.comboBox.addItems(['out', 'com', 'xyz'])

        else:
            self.ui.comboBox.addItem(self.filetype)

        # TODO We should utilize objects of Atom and Molecule here instead of reading a file
        with open(self.filepath, 'r') as f:
            text = f.read()

        self.orig_text = text
        self.ui.comboBox.setCurrentText(self.filetype)
        self.ui.textwindow.setPlainText(self.orig_text)

    def on_combobox_changed(self):
        """
        When combobox is changed, file is converted into the filetype of choice
        """

        new_filetype = self.ui.comboBox.currentText()

        if self.filetype in new_filetype:
            self.ui.textwindow.setPlainText(self.orig_text)
            self.setWindowTitle(self.filename)
            return

        elif new_filetype == 'com':
            try:
                text = self.react.create_input_content(self.filepath)
                new_filename = self.filename.split('.')[0] + '_new.com'
            except:
                dialog = DialogMessage(self, "Failed to convert file to com format")
                dialog.exec_()
                return

        elif new_filetype == 'xyz':
            try:
                text = self.react.create_xyz_filecontent(self.filepath)
                new_filename = self.filename.split('.')[0] + '_new.xyz'
            except:
                dialog = DialogMessage(self, "Failed to convert file to xyz format")
                dialog.exec_()
                return

        self.setWindowTitle(new_filename)
        self.ui.textwindow.setPlainText(text)

    def save_file_(self):
        """
        Save the content of the texteditor as a new file.
        """

        new_filename = self.windowTitle()

        new_filepath = self.filepath.replace(self.filename, new_filename)

        self.filepath, filter_ = QtWidgets.QFileDialog.getSaveFileName(
                                self, "Save file", new_filepath)

        if self.filepath == '':
            return

        with open(self.filepath, 'w') as f:
            f.write(self.ui.textwindow.toPlainText())

        self.react.add_files([self.filepath])
        self.close()

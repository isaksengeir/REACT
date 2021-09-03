from PyQt5 import QtWidgets
from UIs.DialogOK import Ui_DialogOK
from UIs.DialogSave import Ui_DialogSave

class DialogMessage(QtWidgets.QDialog):
    """
    Create simple dialog window with only a message.
    """

    def __init__(self, parent, messagestring):
        super().__init__(parent)
        self.custom_ui()
        self.ui.setupUi(self)
        self.ui.dialog_msg.setText(messagestring)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

    def custom_ui(self):
        """
        Assigns custom UI. Can be overwritten by child classes
        """
        self.ui = Ui_DialogOK()

class DialogSaveProject(DialogMessage):
    """
    child of DialogMessage. Gives the option to save or scratch project.
    """

    def __init__(self, parent):
        super().__init__(parent, 'Unsaved changes in project. Save changes to project before closing?')
    
    def custom_ui(self):
        """
        Assign custom UI.
        """
        self.ui = Ui_DialogSave()

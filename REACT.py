import sys
import os
from PyQt5 import QtWidgets, uic
from UIs.MainWindow import Ui_MainWindow

#from MainWindow import Ui_MainWindow

#methods --> Classes --> Modules --> Packages

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("REACT")
        self.add_state()

        self.tabWidget.currentChanged.connect(self.onChange)

        #MainWindow Buttons with methods:
        self.button_add_state.clicked.connect(self.add_state)
        self.button_delete_state.clicked.connect(self.delete_state)

        #self.button_add_file.clicked.connect(self.import_file_to_list)
        self.button_delete_file.clicked.connect(self.delete_file_from_list)

        self.button_add_file.clicked.connect(self.add_files_to_list)

    def add_files_to_list(self):
        """
        Adds filenames via self.import_files (QFileDialog) to current QtabWidget tab QListWidget.
        TODO should also be stored in dict for saving and loading project
        """
        # Avoid crash when no tabs exist
        if self.tabWidget.currentIndex() < 0:
            #TODO raise error in log window!
            return

        path = os.getcwd()  # wordkdir TODO
        filter_type = "Geometry files (*.pdb *.xyz);; Gaussian input files (*.com *.inp);; " \
                      "Gaussian output files (*.out)"
        title_ = "Import File"

        files_path, type = self.import_files(title_, filter_type,path)

        files_names = [x.split("/")[-1] for x in files_path]

        #Insert new items at the end of the list
        items_insert_index = self.tabWidget.currentWidget().count()

        self.tabWidget.currentWidget().insertItems(items_insert_index, files_names)

    def delete_file_from_list(self):
        """
        Deletes selected file(s) from QtabBarWidget-->Tab-->QListWdget-->item
        :return:
        """
        #Avoid crash when no tabs exist
        if self.tabWidget.currentIndex() < 0:
            return
        #Get the list displayed in the current tab (state)
        current_list = self.tabWidget.currentWidget()

        #Get the selected item(s) ---> returns a list of objects
        list_items = current_list.selectedItems()

        #Remove selected items from list:
        for item in list_items:
            current_list.takeItem(current_list.row(item))


    def import_files(self, title_="Import files", filter_type="Any files (*.*)", path=os.getcwd()):
        """
        Opens file dialog where multiple files can be selected.
        Return: files_ --> list of files (absolute path)
        Return: files_type --> string with the chosen filter_type
        """
        files_, files_type = QtWidgets.QFileDialog.getOpenFileNames(self, title_, path, filter_type)

        return files_, files_type

    def onChange(self):
        """
        Activated whenever tabs are changed --> TODO Rename tabs in accordance with current tab indexes
        """
        print("something changed!")
        #self.tabWidget.setTabText(0, "Hello")

    def add_state(self):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        state = self.tabWidget.count() + 1
        self.tabWidget.addTab(QtWidgets.QListWidget(self), f"{state}")

    def delete_state(self):
        """ 
        Deletes current state (tab) from tabBar widget together with QListWidget child.
        TODO
        """
        tab_index = self.tabWidget.currentIndex()

        #Avoid crash when there are not tabs
        if tab_index < 0:
            return

        self.tabWidget.widget(tab_index).deleteLater()
        print(self.tabWidget.currentWidget())



#    def append_text(self, text=str()):
#        """
#        :param text: text to be printed in ain window textBrowser
#        :return:
#        """
#        self.textBrowser.append(text)
#        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())



app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

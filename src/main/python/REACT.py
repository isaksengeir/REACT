import sys
import os
from PyQt5 import QtWidgets

from UIs.MainWindow import Ui_MainWindow
from mods.ReactWidgets import DragDropListWidget
from fbs_runtime.application_context.PyQt5 import ApplicationContext
#methods --> Classes --> Modules --> Packages


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setWindowTitle("REACT")
        self.add_state()

        self.tabWidget.currentChanged.connect(self.update_tab_names)

        #MainWindow Buttons with methods:
        self.button_add_state.clicked.connect(self.add_state)
        self.button_delete_state.clicked.connect(self.delete_state)

        self.button_add_file.clicked.connect(self.add_files_to_list)
        self.button_delete_file.clicked.connect(self.delete_file_from_list)

        self.button_print_file.clicked.connect(self.print_selected_file)


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

        #File names without path: TODO?
        #files_names = [x.split("/")[-1] for x in files_path]

        #Insert new items at the end of the list
        items_insert_index = self.tabWidget.currentWidget().count()

        #Insert files/filenames to project table:
        #TODO using entire path of file - maybe best this way?
        self.tabWidget.currentWidget().insertItems(items_insert_index, files_path)

        #Move horizontall scrollbar according to text
        self.tabWidget.currentWidget().repaint()
        scrollbar = self.tabWidget.currentWidget().horizontalScrollBar()
        scrollbar.setValue(self.tabWidget.currentWidget().horizontalScrollBar().maximum())

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
        files_, files_type = QtWidgets.QFileDialog.getOpenFileNames(self, title_, path, filter_type,
                                                                    options=QtWidgets.QFileDialog.DontUseNativeDialog)

        return files_, files_type

    def update_tab_names(self):
        """
        Activated whenever tabs are moved. Renames Tabs in correct order of states (1,2,3,4...)
        """
        for tab in range(self.tabWidget.count()):
            tab_name = self.tabWidget.tabText(tab)
            if tab_name != str(tab+1):
                self.tabWidget.setTabText(tab, str(tab+1))

    def add_state(self):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        state = self.tabWidget.count() + 1
        self.tabWidget.addTab(DragDropListWidget(self), f"{state}")

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

    def print_selected_file(self):
        """
        Will print the selected file to the main window.
        """
        #Avoid crash when no items in list:
        if not self.tabWidget.currentWidget().currentItem():
            return

        filename = self.tabWidget.currentWidget().currentItem().text()

        #check if file exist - if not - make user aware and remove from list
        if not os.path.exists(filename):
            self.append_text(f"{filename} does not exist. Removing from project list.")
            self.delete_file_from_list()
            return

        with open(filename, 'r') as pfile:
            for line in pfile:
                self.append_text(line.strip("\n"))

    def append_text(self, text=str()):
        """
        :param text: text to be printed in ain window textBrowser
        :return:
        """
        self.textBrowser.appendPlainText(text)
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

#Instantiate ApplicationContext https://build-system.fman.io/manual/#your-python-code
appctxt = ApplicationContext()

#Create window and show
window = MainWindow()
window.show()

#Invoke appctxt.app.exec_()
exit_code = appctxt.app.exec_()
sys.exit(exit_code)

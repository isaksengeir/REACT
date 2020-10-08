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

        self.button_add_file.clicked.connect(self.import_file_to_list)
        self.button_delete_file.clicked.connect(self.delete_file_from_list)

    def onChange(self):
        print("something changed!")
        #self.tabWidget.setTabText(0, "Hello")

    def add_state(self):
        """
        Add state to tabBar widget with a ListWidget
        """
        state = self.tabWidget.count() + 1
        self.tabWidget.addTab(QtWidgets.QListWidget(self), f"{state}")

        #self.tabWidget.currentWidget.connect(self.change)
        #self.tabWidget.currentChanged.connect(self.onChange)


    def import_file_to_list(self):
        """
        :return:
        """
        print(self.tabWidget.currentIndex())
        items_in_list = self.tabWidget.currentWidget().count()
        print(items_in_list)
        self.tabWidget.currentWidget().insertItem(items_in_list, "NEW FILE")

    def delete_file_from_list(self):
        """

        :return:
        """
        #Get the list displayed in the current tab (state)
        current_list = self.tabWidget.currentWidget()

        #Get the selected item(s) ---> returns a list of objects
        list_items = current_list.selectedItems()

        #Remove selected items from list:
        for item in list_items:
            current_list.takeItem(current_list.row(item))


    def delete_state(self):
        """ 
        Deletes curret state (tab) from tabBar widget
        TODO
        """
        print(self.tabWidget.currentIndex())

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

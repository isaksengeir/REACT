import sys
import os
import json
from PyQt5 import QtWidgets
import UIs.icons_rc
from UIs.MainWindow import Ui_MainWindow
from mods.ReactWidgets import DragDropListWidget
from mods.State import State
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time
#methods --> Classes --> Modules --> Packages


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("REACT")

        self.states = []
        self.proj_name = 'new_project.json'
        self.proj_path = ''

        self.add_state()

        self.tabWidget.tabBar().tabMoved.connect(self.update_tab_names)

        #MainWindow Buttons with methods:
        self.button_add_state.clicked.connect(self.add_state)
        self.button_delete_state.clicked.connect(self.delete_state)

        self.button_add_file.clicked.connect(self.add_files_to_list)
        self.button_delete_file.clicked.connect(self.delete_file_from_list)

        #self.button_print_file.clicked.connect(self.print_selected_file) #TODO I think we do not need this ....
        self.button_print_energy.clicked.connect(self.print_energy)
        self.button_print_scf.clicked.connect(self.print_scf)

        self.button_save_project.clicked.connect(self.save_project)
        self.button_open_project.clicked.connect(self.import_project)

        #Print welcome
        self.append_text("Welcome to REACT", True)

    def add_files_to_list(self):
        """
        Adds filenames via self.import_files (QFileDialog) to current QtabWidget tab QListWidget and selected state.
        """
        # Add state tab if not any exists...
        if self.tabWidget.currentIndex() < 0:
            self.append_text("No states exist - files must be assigned to a state.", True)
            self.append_text("Auto-creating state 1 - files will be added there")
            self.add_state(import_project=False)

        path = os.getcwd()  # wordkdir TODO
        filter_type = "Geometry files (*.pdb *.xyz);; Gaussian input files (*.com *.inp);; " \
                      "Gaussian output files (*.out)"
        title_ = "Import File"

        files_path, type_ = self.import_files(title_, filter_type,path)

        #File names without path: TODO?
        #files_names = [x.split("/")[-1] for x in files_path]

        #add new file to current state 
        self.add_file_to_state(files_path)

        #Insert new items at the end of the list
        items_insert_index = self.tabWidget.currentWidget().count()

        #Insert files/filenames to project table:
        #TODO using entire path of file - maybe best this way?
        self.tabWidget.currentWidget().insertItems(items_insert_index, files_path)

        #Move horizontall scrollbar according to text
        self.tabWidget.currentWidget().repaint()
        scrollbar = self.tabWidget.currentWidget().horizontalScrollBar()
        scrollbar.setValue(self.tabWidget.currentWidget().horizontalScrollBar().maximum())

    def add_file_to_state(self, files_path):

        if files_path:
            self.states[self.tabWidget.currentIndex()].add_gfiles(files_path)


    def delete_file_from_list(self):
        """
        Deletes selected file(s) from QtabBarWidget-->Tab-->QListWdget-->item
        :return:
        """
        #Avoid crash when no tabs exist
        if self.tabWidget.currentIndex() < 0:
            return

        #avid crash when no files exist in state:
        if self.tabWidget.currentWidget().count() < 1:
            return

        #Get the list displayed in the current tab (state)
        current_list = self.tabWidget.currentWidget()

        #Get the selected item(s) ---> returns a list of objects
        list_items = current_list.selectedItems()

        #delete files from state
        self.states[self.tabWidget.currentIndex()].del_gfiles([x.text() for x in list_items])

        #Remove selected items from list:
        for item in list_items:
            current_list.takeItem(current_list.row(item))

    def import_files(self, title_="Import files", filter_type="Any files (*.*)", path=os.getcwd()):
        """
        Opens file dialog where multiple files can be selected.
        Return: files_ --> list of files (absolute path)
        Return: files_type --> string with the chosen filter_type
        """
        #TODO this can be removed at some point - it is not readable on mac either. This is because of the DontUseNativeDialog (which will be removed)
        if 'linux' in sys.platform:
            files_, files_type = QtWidgets.QFileDialog.getOpenFileNames(self, title_, path, filter_type)
        else:
            files_, files_type = QtWidgets.QFileDialog.getOpenFileNames(self, title_, path, filter_type,
                                                                        options=QtWidgets.QFileDialog.DontUseNativeDialog)

        return files_, files_type

    def update_tab_names(self):
        """
        Activated whenever tabs are moved. Renames Tabs in correct order of states (1,2,3,4...)
        Algorithm for updating list of states: temporary new list is created, 

        """
        #new list of pointers to State-objects. Poiners are appened one by one by the followin for-loop,
        #thus, according to the new order of tabs. Tabs still have their original labels, which are used to retrive correct pointer.
        new_pointers = []

        for tab_index in range(self.tabWidget.count()):
            state = self.tabWidget.tabText(tab_index)

            new_pointers.append(self.states[int(state) - 1])
            if state != str(tab_index+1):
                self.tabWidget.setTabText(tab_index, str(tab_index+1))

        self.states = new_pointers

    def add_state(self, import_project=False):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        if import_project:
            #TODO code assumes that states are numbered correctly
            self.states.append(State(import_project[1]))
            print(f"added state {import_project[0]}, with files {import_project[1]}")

            tab_index = self.tabWidget.addTab(DragDropListWidget(self), f"{import_project[0]}")
            self.tabWidget.widget(tab_index).insertItems(-1, self.states[tab_index].get_filenames())

        else:
            self.states.append(State()) 

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

    def append_text(self, text=str(), date_time=False):
        """
        :param text: text to be printed in ain window textBrowser
        :return:
        """
        if date_time:
            text = "%s\n%s" % (time.asctime(time.localtime(time.time())), text)
        self.textBrowser.appendPlainText(text)
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

    def print_energy(self):
        """
        Takes the selected file and prints the final ENERGY (SCF Done) in hartree and kcal/mol.
        :return:
        """
        filepath = self.tabWidget.currentWidget().currentItem().text()
        filename = filepath.split('/')[-1]

        if filename.split('.')[-1] != "out":
            self.append_text("%s does not seem to be a Gaussian output file." % filename)
            return

        state_energy = self.states[self.tabWidget.currentIndex()].get_energy(filename)
        #energy_kcal = superfile.connvert_to_kcal(energy_au) TODO ?
        energy_kcal = 627.51 * state_energy

        self.append_text("\nFinal energy of %s:" % filename)
        self.append_text("%f a.u" % state_energy)
        self.append_text("%.4f kcal/mol" % energy_kcal)

    def print_scf(self):
        """
        Takes the selected file and prints the 4 Convergence criterias.
        :return:
        """
        self.append_text("Converged?...")


    def import_project(self):
        """
        Import project-file and creates new state instances accordingly. Deletes all states in workplace.
        TODO import logfile
        """

        self.proj_path, type_ = QtWidgets.QFileDialog.getOpenFileName(self, "Import project", self.proj_path, "Project/JSON (*.json)")
        
        #To avoid error if dialogwindow is opened, but no file is selected
        if self.proj_path == '':
            return
        
        if bool(self.states) == True:
            pass 
            #TODO raise some warning that workspace is not empty, save project before closing?
        
        #delete states currently in workspace
        self.states.clear()
        self.tabWidget.clear()

        self.proj_name = self.proj_path.split("/")[-1]  
  
        self.label_projectname.setText(self.proj_name.replace('.json', ''))

        with open(self.proj_path, 'r') as proj_file:
            proj = json.load(proj_file)

        try:
            settings = proj.pop('Settings')
            #TODO set settings
        except:
            pass

        try:
            log_text =proj.pop('Log_text')
            self.append_text(log_text)
        except:
            pass

        for state in proj.items():

            self.add_state(state)

    def save_project(self):
        """
        exports a JSON file including all states and list of associated gaussian files
        data = {1 : [file1,file2,..],
                2 : [file1,file2,..]
                }
        TODO add a 'Settings' item to JSON file 
        TODO save logfile 
        """

        project = {}

        for state_index in range(len(self.states)):
            project[state_index+1] = self.states[state_index].get_all_gpaths()

        project['Log_text'] = self.textBrowser.toPlainText()

        if self.proj_path == '':
            self.proj_path = os.getcwd() + '/' + self.proj_name

        new_proj_path, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save project", self.proj_path, "JSON (*.json)")

        if new_proj_path == '':
            return

        self.proj_name = new_proj_path.split("/")[-1]  
        self.proj_path = new_proj_path
        
        #change project name title in workspace
        new_proj_title = new_proj_path.split('/')[-1].replace('.json', '')    
        self.label_projectname.setText(new_proj_title)

        with open(self.proj_path, 'w') as f:
            json.dump(project, f)



#Instantiate ApplicationContext https://build-system.fman.io/manual/#your-python-code
appctxt = ApplicationContext()

#Create window and show
window = MainWindow()
window.show()

#Invoke appctxt.app.exec_()
exit_code = appctxt.app.exec_()
sys.exit(exit_code)

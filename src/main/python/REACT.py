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

        self.states = {}
        self.proj_name = 'new_project'

        self.add_state()

        self.tabWidget.currentChanged.connect(self.update_tab_names)

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
        # Avoid crash when no tabs exist
        if self.tabWidget.currentIndex() < 0:
            #TODO raise error in log window!
            return

        path = os.getcwd()  # wordkdir TODO
        filter_type = "Geometry files (*.pdb *.xyz);; Gaussian input files (*.com *.inp);; " \
                      "Gaussian output files (*.out)"
        title_ = "Import File"

        files_path, type_ = self.import_files(title_, filter_type,path)

        #File names without path: TODO?
        #files_names = [x.split("/")[-1] for x in files_path]

        #add new file to current state 
        if files_path:
            self.states[self.curr_state()].add_gfiles(files_path)

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

        #delete files from state
        self.states[self.curr_state()].del_gfiles([x.text() for x in list_items])

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
        #TODO this needs also to fix the correct tab index for the gaussian file objects...

    def add_state(self, import_project=False):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        #TODO BENTE why are you not using the DragDropListWidget ? I changed it back to DragDropListWidget (Geir)..
        if import_project:
            #TODO code assumes that states are numbered correctly
            tab_index = self.tabWidget.addTab(DragDropListWidget(self), f"{import_project[0]}")
            self.states[import_project[0]] = State(tab_index, import_project[1])

        else:
            state = self.tabWidget.count() + 1
            tab_index = self.tabWidget.addTab(DragDropListWidget(self), f"{state}")
            self.states[str(state)] = State(tab_index) # TODO buggy? State is created according to tab-count (ex. state 1 is now accessed with key = 1) If tabs are renumbered, key to access State has to be updated. 

    def delete_state(self):
        """
        Deletes current state (tab) from tabBar widget together with QListWidget child.
        TODO
        """
        tab_index = self.tabWidget.currentIndex()

        #Avoid crash when there are not tabs
        if tab_index < 0:
            return

        #remove current state
        self.states.pop(self.curr_state())

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
        

        self.states[str(self.curr_state())].gfiles[filename].read_dft_out(filepath)
        state_energy = self.states[str(self.curr_state())].gfiles[filename].ene["E_gas"]
        energy_kcal = 627.51 * state_energy

        #maybe not use fstrings to format here?
        self.append_text(f"Final Energy = {state_energy} a.u.\n")
        self.append_text(f"             = {energy_kcal:.2f} kcal/mol")

    def print_scf(self):
        """
        Takes the selected file and prints the 4 Convergence criterias.
        :return:
        """
        self.append_text("Converged?...")

    def curr_state(self):
        """
        Return: dict key to access current state.
        """
        return str(self.tabWidget.currentIndex()+1)

    def import_project(self):
        """
        Import project-file and creates new state instances accordingly. Deletes all states in workplace.
        TODO import logfile
        """

        proj_path, type_ = QtWidgets.QFileDialog.getOpenFileName(self, "Import project", os.getcwd(), "Project/JSON (*.json)")
        
        if proj_path == '':
            return
        
        if bool(self.states) == True:
            pass 
            #TODO raise some warning that workspace is not empty, save project before closing?
        
        #delete states currently in workspace
        self.states.clear()
        self.tabWidget.clear()
        #for tab_index in range(self.tabWidget.count()):
        #    self.tabWidget.widget(tab_index).deleteLater()

        self.proj_name = proj_path.split("/")[-1]  
  
        self.label_projectname.setText(self.proj_name.replace('.json', ''))

        with open(proj_path, 'r') as proj_file:
            proj = json.load(proj_file)

        try:
            settings = proj.pop('Settings')
            #TODO set settings
        except:
            pass

        for state in proj.items():

            self.add_state(state)
            self.tabWidget.widget(self.states[state[0]].get_tab_index()).insertItems(-1, self.states[state[0]].get_filenames())

    def save_project(self):
        """
        exports a JSON file including all states and list of associated gaussian files
        data = {1 : [file1,file2,..],
                2 : [file1,file2,..]
                }
        TODO add a 'Settings' item to JSON file (working path..)
        TODO save logfile 
        """

        project = {}

        for state in self.states.items():
            project[state[0]] = state[1].get_all_gpaths()

        #if not self.proj_name:
        #    self.proj_name = 'neww_project.json'

        new_file_path = os.getcwd() + '/' + self.proj_name

        proj_path, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save project", new_file_path, "JSON (*.json)")

        if proj_path == '':
            return

        self.proj_name = proj_path.split("/")[-1]  
        
        #change project name title in workspace
        new_proj_title = proj_path.split('/')[-1].replace('.json', '')    
        self.label_projectname.setText(new_proj_title)

        with open(proj_path, 'w') as f:
            json.dump(project, f)



#Instantiate ApplicationContext https://build-system.fman.io/manual/#your-python-code
appctxt = ApplicationContext()

#Create window and show
window = MainWindow()
window.show()

#Invoke appctxt.app.exec_()
exit_code = appctxt.app.exec_()
sys.exit(exit_code)

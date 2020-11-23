import sys
import os
import json
from PyQt5 import QtWidgets, QtGui
import UIs.icons_rc
import mods.common_functions as cf
from UIs.MainWindow import Ui_MainWindow
from mods.ReactWidgets import DragDropListWidget
from mods.State import State
from mods.FileEditor import FileEditor
from mods.AnalyseCalc import AnalyseCalc
from mods.GlobalSettings import GlobalSettings
from mods.ReactPlot import PlotGdata, PlotEnergyDiagram
from mods.MoleculeFile import XYZFile
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import time
import concurrent.futures
#methods --> Classes --> Modules --> Packages


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("REACT - Main")

        self.states = []
        self.proj_name = 'new_project'

        # Keep track of files to include for each state ... TODO implement this in States later instead?
        # state (int): main: path, frequency: path, solvation: path, big basis: path
        self.included_files = None

        # Since included files belong to project, and will be stored with project, we can only allow
        # one instance of the analyse window... TODO if we want this different
        self.analyse_window = None

        self.add_state()

        self.tabWidget.tabBar().tabMoved.connect(self.update_tab_names)

        #MainWindow Buttons with methods:
        self.button_add_state.clicked.connect(self.add_state)
        self.button_delete_state.clicked.connect(self.delete_state)

        self.button_add_file.clicked.connect(self.add_files_to_list)
        self.button_delete_file.clicked.connect(self.delete_file_from_list)
        self.button_edit_file.clicked.connect(self.edit_file)
        self.button_analyse_calc.clicked.connect(self.open_analyse)
        self.button_settings.clicked.connect(self.open_settings)

        self.button_print_energy.clicked.connect(self.print_energy)
        self.button_print_scf.clicked.connect(self.plot_scf)
        self.button_print_relativeE.clicked.connect(self.print_relative_energy)
        self.button_plot_ene_diagram.clicked.connect(self.plot_energy_diagram)

        self.button_save_project.clicked.connect(self.save_project)
        self.button_open_project.clicked.connect(self.import_project)

        #Print welcome
        self.append_text("Welcome to REACT", True)

    def add_files_to_list(self, paths=False):
        """
        Adds filenames via self.import_files (QFileDialog) to current QtabWidget tab QListWidget and selected state.
        """
        # Add state tab if not any exists...
        if self.tabWidget.currentIndex() < 0:
            self.append_text("No states exist - files must be assigned to a state.", True)
            self.append_text("Auto-creating state 1 - files will be added there")
            self.add_state(import_project=False)

        #path = os.getcwd()  # wordkdir TODO set this as global at some point
        path = "../resources/DFT_testfiles"
        filter_type = "Gaussian output files (*.out);; Gaussian input files (*.com *.inp);; " \
                      "Geometry files (*.pdb *.xyz)"
        title_ = "Import File"

        if paths:
            files_path = paths
        else:
            files_path, type_ = self.import_files(title_, filter_type,path)

        #File names without path: TODO?
        #files_names = [x.split("/")[-1] for x in files_path]

        #add new file to current state TODO this takes some time for large files...
        #with concurrent.futures.ThreadPoolExecutor() as executor:
        #    [executor.submit(self.add_file_to_state, filepath) for filepath in files_path]

        #Insert new items at the end of the list
        items_insert_index = self.tabWidget.currentWidget().count()

        #Insert files/filenames to project table:
        #TODO using entire path of file - maybe best this way?
        for file in files_path:
            self.tabWidget.currentWidget().insertItem(items_insert_index, file)
            self.add_file_to_state(file)
            #self.tabWidget.currentWidget().insertItem(items_insert_index, file)
            # Check if output file and if it has converged:
            if file.split(".")[-1] == "out":
                self.check_convergence(file, items_insert_index)
            items_insert_index += 1

        #Move horizontall scrollbar according to text
        self.tabWidget.currentWidget().repaint()
        scrollbar = self.tabWidget.currentWidget().horizontalScrollBar()
        scrollbar.setValue(self.tabWidget.currentWidget().horizontalScrollBar().maximum())

    def add_file_to_state(self, filepath):
        """
        :param filepath:
        :return:
        """
        self.states[self.tabWidget.currentIndex()].add_gfiles(filepath)

    def check_convergence(self, file_path, item_index):
        filename = file_path.split('/')[-1]
        converged = self.states[self.tabWidget.currentIndex()].check_convergence(file_path)
        if converged is False:
            #self.tabWidget.currentWidget(item_index).setForeground(Qt.red)
            self.tabWidget.currentWidget().item(item_index).setForeground(QtGui.QColor(100, 0, 0))
            self.append_text("\nWarning: %s seems to have not converged!" % filename)

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
        tab_index = self.tabWidget.currentIndex()
        self.states[tab_index].del_gfiles([x.text() for x in list_items])

        #Remove selected items from list:
        for item in list_items:
            current_list.takeItem(current_list.row(item))

            # Remove from included_files if existing:
            if self.included_files:
                for type_ in self.included_files[tab_index+1].keys():
                    if item.text() == self.included_files[tab_index + 1][type_]:
                        self.included_files[tab_index+1][type_] = ""
                        # Update analyse window, if active:
                        if self.analyse_window:
                            self.analyse_window.update_state_included_files()

    def import_files(self, title_="Import files", filter_type="Any files (*.*)", path=os.getcwd()):
        """
        Opens file dialog where multiple files can be selected.
        Return: files_ --> list of files (absolute path)
        Return: files_type --> string with the chosen filter_type
        """
        # TODO this can be removed at some point - it is not readable on mac either. This is because of the
        #  DontUseNativeDialog (which will be removed)
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
        new_included_files = dict()

        for tab_index in range(self.tabWidget.count()):
            state = self.tabWidget.tabText(tab_index)

            new_pointers.append(self.states[int(state) - 1])
            if state != str(tab_index+1):
                self.tabWidget.setTabText(tab_index, str(tab_index+1))
                # swap values of state and tab_index+1
                if self.included_files:
                    new_included_files[int(state)] = self.included_files[tab_index+1]

            else:
                if self.included_files:
                    new_included_files[int(state)] = self.included_files[int(state)]

        self.states = new_pointers
        self.included_files = new_included_files

    def add_state(self, import_project=False):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        if import_project:
            #TODO code assumes that states are numbered correctly
            self.states.append(State(import_project[1]))
            print(f"added state {import_project[0]}, with files {import_project[1]}")

            tab_index = self.tabWidget.addTab(DragDropListWidget(self), f"{import_project[0]}")
            self.tabWidget.widget(tab_index).insertItems(-1, self.states[tab_index].get_all_gpaths)

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

    def append_text(self, text=str(), date_time=False):
        """
        :param text: text to be printed in ain window textBrowser
        :return:
        """
        if date_time:
            text = "\n%s\n%s" % (time.asctime(time.localtime(time.time())), text)
        self.textBrowser.appendPlainText(text)
        self.textBrowser.verticalScrollBar().setValue(self.textBrowser.verticalScrollBar().maximum())

    def print_energy(self):
        """
        Takes the selected file and prints the final ENERGY (SCF Done) in hartree and kcal/mol.
        :return:
        """
        filepath = self.tabWidget.currentWidget().currentItem().text()
        filename = filepath.split('/')[-1]

        if filename.split('.')[-1] not in  ["out", "log"]:
            self.append_text("%s does not seem to be a Gaussian output file." % filename)
            return

        #this file --> State
        state_energy = self.states[self.tabWidget.currentIndex()].get_energy(filepath)
        #energy_kcal = superfile.connvert_to_kcal(energy_au) TODO ?

        energy_kcal = cf.hartree_to_kcal(state_energy)

        self.append_text("\nFinal energy of %s:" % filename)
        self.append_text("%f a.u" % state_energy)
        self.append_text("%.4f kcal/mol" % energy_kcal)

    def get_relative_energies(self):
        """
        :return: energies dict[state] = "dE": float, "file":path
        """
        energies = list()
        d_energies = dict()

        for tab_index in range(self.tabWidget.count()):
            if self.tabWidget.widget(tab_index).currentItem():
                file_path = self.tabWidget.widget(tab_index).currentItem().text()
                if file_path.split(".")[-1] in ["out", "log"]:
                    energies.append(self.states[tab_index].get_energy(file_path))
                    d_energies[tab_index + 1] = {"dE": energies[tab_index]-energies[0], "file": file_path}

                else:
                    self.append_text("%s does not seem to be Gaussian output" % file_path)
            else:
                self.append_text("No files selected for state %d" % (tab_index + 1))

        return d_energies

    def print_relative_energy(self):
        """
        calculates the relative energy (to state 1) for all states and prints it in the log window
        :return:
        """
        self.append_text("Relative energies", date_time=True)

        d_energies = self.get_relative_energies()

        for state in sorted(d_energies.keys()):
            self.append_text("%sE(%d): %.4f kcal/mol (%s)" % (cf.unicode_symbols["Delta"], state,
                                                              cf.hartree_to_kcal(d_energies[state]["dE"]),
                                                              d_energies[state]["file"].split("/")[-1]))

    def plot_energy_diagram(self):
        """

        :return:
        """
        d_ene = self.get_relative_energies()

        #Convert d_ene dict to list of energies in kcal/mol
        d_ene = [cf.hartree_to_kcal(d_ene[x]["dE"]) for x in sorted(d_ene.keys())]

        plot = PlotEnergyDiagram(d_ene, x_title="State", y_title="Relative energy", plot_legend=False)

    def plot_scf(self):
        """
        Takes the selected file and prints the 4 Convergence criterias.
        :return:
        """
        filepath = self.tabWidget.currentWidget().currentItem().text()

        # Can not plot? :
        if filepath.split(".")[-1] not in ["out", "log"]:
            return

        filename = filepath.split('/')[-1]

        scf_data = self.states[self.tabWidget.currentIndex()].get_scf(filepath)

        #Check if this is geometry optimization or not (None if not):
        converged = self.states[self.tabWidget.currentIndex()].check_convergence(filepath)
        plot = PlotGdata(scf_data, filename)

        if converged is None:
            plot.plot_scf_done()
            self.append_text("%s seem to not be a geometry optimisation ..." % filename)
        else:
            plot.plot_scf_convergence()
            if converged is False:
                self.append_text("%s has not converged successfully." % filename)

    def edit_file(self):
        """

        :return:
        """
        if not self.tabWidget.currentWidget().currentItem():
            self.append_text("\n No file selected for editing!")
            return

        filepath = self.tabWidget.currentWidget().currentItem().text()

        xyz = XYZFile(filepath)

        editor = FileEditor(self, filepath)
        editor.show()

        self.states[self.tabWidget.currentIndex()].update_fileobject(filepath)

    def create_input_content(self, filepath):
        '''
        :return: string -> content of new input file, based on outputfile given as argument
        '''
        return self.states[self.tabWidget.currentIndex()].create_input_content(filepath)

    def open_settings(self):
        Settings = GlobalSettings(self)
        Settings.show()

    def open_analyse(self):
        """

        :return:
        """
        if self.analyse_window:
            self.append_text("\nAnalyse Calculation is already running. \nPerhaps the window is hidden?")
            self.analyse_window.raise_()
            return

        if not self.tabWidget.currentWidget().currentItem():
            self.append_text("\n Nothing to analyse here ...")
            return
        self.analyse_window = AnalyseCalc(self)
        self.analyse_window.show()

    def import_project(self):
        """
        Import project-file and creates new state instances accordingly. Deletes all states in workplace.
        TODO import logfile
        """
        workdir = "../resources/DFT_testfiles"
        proj_path, type_ = QtWidgets.QFileDialog.getOpenFileName(self, "Import project", directory=workdir,
                                                                 filter="Project/JSON (*.json)")
        
        #To avoid error if dialogwindow is opened, but no file is selected
        if proj_path == '':
            return
        
        if bool(self.states) == True:
            pass 
            #TODO raise some warning that workspace is not empty, save project before closing?
        
        #delete states currently in workspace
        self.states.clear()
        self.tabWidget.clear()

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

        print(f"project looks like this{proj}")
        print(f"new self.states looks like this:{self.states}")

    def save_project(self):
        """
        exports a JSON file including all states and list of associated gaussian files
        data = {1 : [file1,file2,..],
                2 : [file1,file2,..]
                }
        TODO add a 'Settings' item to JSON file (working path..)
        TODO save logfile 
        TODO remember items colored red ? and recolor them when loading the project?
        """

        project = {}

        for state_index in range(len(self.states)):
            project[state_index+1] = self.states[state_index].get_all_gpaths

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

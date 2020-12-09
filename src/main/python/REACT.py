import sys
import os
import json
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThreadPool, QTimer
from mods.SplashScreen import SplashScreen
import UIs.icons_rc
import mods.common_functions as cf
from UIs.MainWindow import Ui_MainWindow
from mods.ReactWidgets import DragDropListWidget
from mods.State import State
from mods.FileEditor import FileEditor
from mods.AnalyseCalc import AnalyseCalc
from mods.GlobalSettings import GlobalSettings
from mods.ReactPlot import PlotGdata, PlotEnergyDiagram
from mods.Plotter import Plotter
from mods.DialogsAndExceptions import DialogMessage, DialogSaveProject
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from mods.ThreadWorkers import Worker
from threading import Lock
import time

#methods --> Classes --> Modules --> Packages


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):

        # SPLASH
        self.splash = SplashScreen(self)
        self.splash.show()

        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle("REACT - Main")

        # Global settings
        self.settings = {"workdir": os.getcwd(),
                         "DFT": {'functional'         : 'B3LYP',
                                 'basis'              : {'6-31G': {'pol1': 'd', 'pol2': 'p', 'diff': None}},
                                 'empiricaldispersion': 'gd3',
                                 'additonal keys'     : None,
                                 'link 0'             : None,
                                 'opt keys'           : ['noeigentest', 'calcfc']
                                 },
                         "Ui": 1
                         }
        self.states = []
        self.proj_name = 'new_project'
        
        # bool to keep track of unsaved changes to project.
        self.unsaved_proj = False

        # { state (int): main: path, frequency: path, solvation: path, big basis: path }
        self.included_files = None

        # Analyse window active or not:
        self.analyse_window = None

        # Bool allows only one instance of settings window at the time.
        self.settings_window = None

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
        self.button_create_cluster.clicked.connect(self.create_cluster)

        self.button_plotter.clicked.connect(self.open_plotter)

        # Print welcome
        self.append_text("Welcome to REACT", True)

        # Set progressbar to full:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progressbar)
        self.update_progressbar(100)

        # Threads for jobs take take time:
        self.threadpool = QThreadPool()

        # TODO put this some place in the UI bottom ?
        self.append_text("\nMultithreading with\nmaximum %d threads" % self.threadpool.maxThreadCount())

    def add_files_to_list(self, paths=False):
        """
        Adds filenames via self.import_files (QFileDialog) to current QtabWidget tab QListWidget and selected state.
        TODO: need to check if files exist in list from before! If file exist, 
        delete old and add again, since the user might have edited the file
        outside the app or using FileEditorWindow.

        """
        # Add state tab if not any exists...
        if self.tabWidget.currentIndex() < 0:
            self.append_text("No states exist - files must be assigned to a state.", True)
            self.append_text("Auto-creating state 1 - files will be added there")
            self.add_state()

        #path = os.getcwd()  # wordkdir TODO set this as global at some point
        path = "../resources/DFT_testfiles"
        filter_type = "Gaussian output files (*.out);; Gaussian input files (*.com *.inp);; " \
                      "Geometry files (*.pdb *.xyz)"
        title_ = "Import File"

        if isinstance(paths, list):
            files_path = paths
        else:
            files_path, type_ = self.import_files(title_, filter_type,path)

        if len(files_path) < 1:
            return

        # Where to start inserting files in project list:
        items_insert_index = self.tabWidget.currentWidget().count()

        # Start thread first:
        worker = Worker(self.thread_add_files, files_path, items_insert_index)
        #worker.signals.result.connect(self.print_result)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(worker)
        self.timer.start(10)

        # Insert files/filenames to project table:
        for file in files_path:
            self.tabWidget.currentWidget().insertItem(items_insert_index, file)
            self.tabWidget.currentWidget().item(items_insert_index).setForeground(QtGui.QColor(80, 80, 80))
            items_insert_index += 1

        # Move horizontall scrollbar according to text
        self.tabWidget.currentWidget().repaint()
        scrollbar = self.tabWidget.currentWidget().horizontalScrollBar()
        scrollbar.setValue(self.tabWidget.currentWidget().horizontalScrollBar().maximum())

    def thread_add_files(self, file_paths, item_index, progress_callback, results_callback):
        """
        :param file_paths:
        :param item_index: index where to start insertion of files in list
        :param progress_callback:
        :return:
        """
        # set progressbar to 1:
        self.update_progressbar(1)
        for n in range(len(file_paths)):
            file = file_paths[n]
            self.states[self.tabWidget.currentIndex()].add_gfiles(file)

            progress_callback.emit({self.update_progressbar: ((int(n+1) * 100 / len(file_paths)),),
                                    self.check_convergence: (file, item_index,
                                    self.tabWidget.currentIndex())})
            item_index += 1

        return "Done"

    def progress_fn(self, progress_stuff):
        """
        :param progress_stuff: {function : arguments}
        :return:
        """
        for func in progress_stuff.keys():
            args = progress_stuff[func]
            func(*args)

    def update_progressbar(self, val=None):
        """
        :param val:
        :return:
        """
        with Lock():
            if not val:
                val = self.progressBar.value()
                val += 1

            if val < 100:
                self.progressBar.setTextVisible(True)
            else:
                self.progressBar.setTextVisible(False)
                self.timer.stop()

            self.progressBar.setValue(int(val))

    def print_result(self, result):
        return result

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def add_file_to_state(self, filepath):
        """
        :param filepath:
        :return:
        redundant?
        """
        self.states[self.tabWidget.currentIndex()].add_gfiles(filepath)
        #

    def check_convergence(self, file_path, item_index, tab_index=None):
        filename = file_path.split('/')[-1]
        if tab_index is None:
            tab_index = self.tabWidget.currentIndex()
            tab_widget = self.tabWidget.currentWidget()
        else:
            tab_widget = self.tabWidget.widget(tab_index)

        if filename.split(".")[-1] not in ["out", "log"]:
            tab_widget.item(item_index).setForeground(QtGui.QColor(98, 114, 164))
        else:
            converged = self.states[tab_index].check_convergence(file_path)

            if isinstance(converged, bool) and not converged:
                tab_widget.item(item_index).setForeground(QtGui.QColor(195, 82, 52))
                self.append_text("\nWarning: %s seems to have not converged!" % filename)
            elif isinstance(converged, bool) and converged:
                tab_widget.item(item_index).setForeground(QtGui.QColor(117, 129, 104))
            elif not isinstance(converged, bool):
                tab_widget.item(item_index).setForeground(QtGui.QColor(117, 129, 104))

    def delete_file_from_list(self):
        """
        Deletes selected file(s) from QtabBarWidget-->Tab-->QListWdget-->item
        :return:
        """
        # Avoid crash when no tabs exist
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

    def add_state(self):
        """
        Add state (new tab) to tabBar widget with a ListWidget child.
        """
        self.states.append(State())

        state = self.tabWidget.count() + 1
        self.tabWidget.addTab(DragDropListWidget(self), f"{state}")
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(state-1))

    def delete_state(self):
        """
        Deletes current state (tab) from tabBar widget together with QListWidget child.
        TODO
        """
        tab_index = self.tabWidget.currentIndex()

        #Avoid crash when there are not tabs
        if tab_index < 0:
            return

        # Delete from self.included_files
        if self.included_files:
            self.included_files[tab_index+1] = {0: "", 1: "", 2: "", 3: ""}
            if self.analyse_window:
                self.analyse_window.update_state_included_files()

        self.tabWidget.widget(tab_index).deleteLater()
        self.states.pop(tab_index)

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

        editor = FileEditor(self, filepath)
        editor.show()

    def create_input_content(self, filepath):
        '''
        :return: string -> content of new input file, based on outputfile given as argument
        '''
        return self.states[self.tabWidget.currentIndex()].create_input_content(filepath)

    def open_settings(self):

        if self.settings_window:
            self.append_text("\nSettings window is already running."
                             "\nPerhaps the window is hidden?")
            self.settings_window.raise_()
        else:
            self.settings_window = GlobalSettings(self)
            self.settings_window.show()

    def open_analyse(self):
        """

        :return:
        """
        if self.analyse_window:
            self.append_text("\nAnalyse Calculation is already running. \nPerhaps the window is hidden?")
            self.analyse_window.raise_()
            return

        if not self.tabWidget.currentWidget().currentItem() and not self.included_files:
            self.append_text("\n Nothing to analyse here ...")
            return
        self.analyse_window = AnalyseCalc(self)
        self.analyse_window.show()

    def create_cluster(self):
        """
        """
        dialog = DialogMessage(self, "Create Cluster not yet available:(")
        dialog.exec_()

    def open_plotter(self):
        """

        :return:
        """

        self.plotter = Plotter(self)
        self.plotter.show()

    def import_project(self):
        """
        Import project-file and creates new state instances accordingly. Deletes all states in workplace.
        TODO import logfile
        """
        proj_path, type_ = QtWidgets.QFileDialog.getOpenFileName(self, "Import project",
                                                                 self.settings['workdir'], filter="Project (*.rxt)")

        #To avoid error if dialogwindow is opened, but no file is selected
        if proj_path == '':
            return
        
        if self.unsaved_proj:
            #TODO set self.unsaved_proj = True when approriate
            #when Save is clicked: signal = 1, else signal = 0. 
            #TODO save project when signal == 1, else: discard project
            dialog = DialogSaveProject(self)
            signal = dialog.exec_()
            
        #delete states currently in workspace
        self.states.clear()
        self.tabWidget.clear()
        self.textBrowser.clear()

        self.proj_name = proj_path.split("/")[-1]        
        self.workdir = proj_path.replace(self.proj_name, "")
        self.label_projectname.setText(self.proj_name.replace('.rxt', ''))

        with open(proj_path, 'r') as proj_file:
            proj = json.load(proj_file, object_hook=self.json_hook_int_please)

        for key in ['states', 'included files', 'workdir', 'DFT', 'log']:
            self._import_project_pop_and_assign(proj, key)

    def _import_project_pop_and_assign(self, project, key):

        try:
            proj_item = project.pop(key)

            if key == 'states':
                for state in proj_item.items():
                    self.add_state()
                    self.add_files_to_list(state[1])

                    # each state has to be completely loaded before moving on to text,
                    # to ensure the multithreading assigns files to correct state. 
                    self.threadpool.waitForDone()
            if key == 'included files':
                    self.included_files = proj_item
            if key == 'log':
                    self.textBrowser.appendPlainText(proj_item)
            else:
                    self.settings[key] = proj_item
        except:
            self.append_text(f'Failed to load "{key}" from "{self.proj_name}"')

    def save_project(self):
        """
        exports a *.rxt (identical to JSON) file containing:
        project = {'states'        : {1: [file1,file2,..],
                                      2: [file1,file2,..]
                                      },
                   'included files': self.included_files,
                   'settings'      : self.settings,
                   'log'           : self.textBrowser.toPlainText()
                   }
        """
        project = {}
        states = {}

        self.append_text("\nREACT project last saved: %s\n" % (time.asctime(time.localtime(time.time()))))

        for state_index in range(len(self.states)):      
            states[state_index+1] = self.states[state_index].get_all_gpaths
        
        project["states"] = states
        project["included files"] = self.included_files 
        project["workdir"] = self.settings["workdir"]
        project["DFT"] = self.settings["DFT"]
        project["log"] = self.textBrowser.toPlainText()

        temp_filepath = os.getcwd() + '/' + self.proj_name

        proj_path, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save project", temp_filepath, "REACT project (*.rxt)")

        if proj_path == '':
            return

        self.proj_name = proj_path.split("/")[-1]  
        
        #change project name title in workspace
        new_proj_title = proj_path.split('/')[-1].replace('.rxt', '')    
        self.label_projectname.setText(new_proj_title)

        with open(proj_path, 'w') as f:
            json.dump(project, f)

    def json_hook_int_please(self, obj):
        """
        Used as object hook when calling json.load()
        Will convert a key-object of type str into type int, if possible
        """
        new_dict = {}
        for k, v in obj.items():

            if isinstance(v,dict):
                new_dict_sub = {}
                for k_sub, v_sub in v.items():
                    try: 
                        new_k_sub = int(k_sub)
                        new_dict_sub[new_k_sub] = v[k_sub]
                    except ValueError:
                        new_dict_sub[k] = v[k_sub]

            try: 
                new_k = int(k)
                new_dict[new_k] = obj[k]
            except ValueError:
                new_dict[k] = obj[k]
            
        return new_dict


#Instantiate ApplicationContext https://build-system.fman.io/manual/#your-python-code
appctxt = ApplicationContext()

#Create window and show
window = MainWindow()
#window.show()

#Invoke appctxt.app.exec_()
exit_code = appctxt.app.exec_()
sys.exit(exit_code)

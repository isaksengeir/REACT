import sys
import os
import json
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThreadPool, QTimer
from mods.SplashScreen import SplashScreen
import UIs.icons_rc
import mods.common_functions as cf
from UIs.MainWindow import Ui_MainWindow
from mods.ReactWidgets import DragDropListWidget
from mods.State import State
from mods.PrintPlotOpen import PrintPlotOpen
from mods.DialogsAndExceptions import DialogMessage, DialogSaveProject
from mods.CalcSetupWindow import CalcSetupWindow

# from fbs_runtime.application_context.PyQt5 import ApplicationContext # fbs removed for good?
from mods.ThreadWorkers import Worker
from threading import Lock
import time
from mods.PymolProcess import PymolSession
from mods.ReactPlot import PlotGdata

#methods --> Classes --> Modules --> Packages


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow, PrintPlotOpen):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("REACT - Main")

        # Global settings
        self.settings = {"workdir": os.getcwd(),
                         "DFT": {"functional": "B3LYP",
                                 "basis": ("6-31G", {"pol1": "d", "pol2": 'p', "diff": None}),
                                 "additional keys": ["empiricaldispersion=gd3"],
                                 "link 0"        : [],
                                 "opt keys"      : ["noeigentest", "calcfc"],
                                 "user"    : {"functional": [], "basis": {}}}, 
                         "pymolpath": None,
                         "REACT pymol" : True,
                         "Ui": 1
                         }
        self.states = []
        self.proj_name = 'new_project'

        self.pymol = None

        #self.pymol_path = '/Applications/PyMOL.app/Contents/MacOS/pymol'

        # bool to keep track of unsaved changes to project.
        self.unsaved_proj = False

        # { state (int): main: path, frequency: path, solvation: path, big basis: path }
        self.included_files = None

        # Analyse window active or not:
        self.analyse_window = None

        # Create PDB cluster window active or not
        self.cluster_window = None

        # Bool allows only one instance of settings window at the time.
        self.settings_window = None

        self.add_state()

        self.tabWidget.tabBar().tabMoved.connect(self.update_tab_names)
        self.tabWidget.currentWidget().itemClicked.connect(self.change_pymol_structure)

        #MainWindow Buttons with methods:
        self.button_add_state.clicked.connect(self.add_state)
        self.button_delete_state.clicked.connect(self.delete_state)
        self.button_add_file.clicked.connect(self.add_files)
        self.button_delete_file.clicked.connect(self.delete_file)
        self.button_edit_file.clicked.connect(self.open_editfile)
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
        self.button_power_off.clicked.connect(self.power_off_on)
        self.button_pymol.clicked.connect(self.start_pymol)
        self.button_calc_setup.clicked.connect(self.calc_setup)

        self.power = True

        # Print welcome
        self.append_text("Welcome to REACT", True)

        # Set progressbar to full:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progressbar)
        self.update_progressbar(100)

        # Threads for jobs take take time:
        self.threadpool = QThreadPool()

        # SPLASH
        self.splash = SplashScreen(self)
        self.splash.show()

        # PyQt5.QtCore.QRect(0, 0, 5120, 1440)
        screen_size = QtWidgets.QDesktopWidget().screenGeometry()
        window_size = self.geometry()
        self.move(int(((screen_size.width() - window_size.width())/2)), 50)

        # TODO put this some place in the UI bottom ?
        self.append_text("\nMultithreading with\nmaximum %d threads" % self.threadpool.maxThreadCount())

    def calc_setup(self):
        self.setup_window = CalcSetupWindow(self)
        self.setup_window.show()


    def start_pymol(self, return_session=False):
        """
        Starts pymol sync to REACT
        :return_session: return the pymol session link
        :return: session (if return_session = True)
        """
        if self.pymol:
            self.pymol.close()
            return

        if self.settings['REACT pymol']:
            if os.path.isdir('OpenSourcePymol/dist/OpenSourcePymol.app'):
                pymol_path = 'OpenSourcePymol/dist/OpenSourcePymol.app'
            elif os.path.isdir("%s/OpenSourcePymol/dist/OpenSourcePymol.app" % '/'.join(sys.path[0].split('/')[0:-1])):
                pymol_path = "%s/OpenSourcePymol/dist/OpenSourcePymol.app" % '/'.join(sys.path[0].split('/')[0:-1])
            else:
                self.append_text("Can not find REACT Open Source Pymol")
                self.append_text(sys.path[0])
                return
        else:
            pymol_path = self.settings['pymolpath']

        if not pymol_path:
            self.append_text("No PyMol path set. Please see settings.")
            return

        self.pymol = PymolSession(parent=self, home=self, pymol_path=pymol_path)

        if return_session:
            return self.pymol

        self.tabWidget.tabBar().currentChanged.connect(self.pymol_view_current_state)
        self.connect_pymol_structures(connect=True)

        self.load_all_states_pymol()

    def connect_pymol_structures(self, connect=True):
        """
        Connect clicks in QListWidget to structure displayed in pymol
        :param connect: bool
        :return:
        """
        # on_off = {True:}
        for state in range(self.count_states):
            if connect:
                self.tabWidget.widget(state).itemClicked.connect(self.change_pymol_structure)
            else:
                self.tabWidget.widget(state).itemClicked.disconnect(self.change_pymol_structure)

    def pymol_view_current_state(self):
        """
        :return:
        """
        if not self.pymol:
            return
        state = self.get_current_state
        name = None
        if self.get_selected_filepath:
            name = self.get_selected_filepath.split("/")[-1].split(".")[0]
        self.pymol.pymol_cmd("group state_%d, toggle, open" % state)
        for i in range(1, self.count_states + 1):
            if i != state:
                self.pymol.pymol_cmd("group state_%d, toggle, close" % i)
                self.pymol.pymol_cmd("disable state_%d" % i)
        self.pymol.highlight(name=name, group="state_%d" % state)

    def file_to_pymol(self, filepath, state=1, set_defaults=True):
        """
        Takes any file and opens it in pymol
        :param filepath: path to file
        :param state: integer for state
        :param set_defaults: fix pymol representation
        :return:
        """
        if not self.pymol:
            return

        delete_after = False
        if filepath.split(".")[-1] not in ["xyz", "pdb"]:
            delete_after = True
            xyz = self.states[state - 1].get_final_xyz(filepath)
            filepath = "%s.xyz" % filepath.split(".")[0]
            cf.write_file(xyz, filepath)

        self.pymol.load_structure(filepath, delete_after=delete_after)
        self.pymol.pymol_cmd("group state_%d, %s" % (state, filepath.split("/")[-1].split(".")[0]))

        if set_defaults:
            self.pymol.set_default_rep()
            self.pymol.pymol_cmd("enable state_%d and %s" % (state, filepath.split("/")[-1].split(".")[0]))

    def load_all_states_pymol(self):
        """
        Loads all files from project table to pymol
        :return:
        """
        if not self.pymol:
            return

        for state in range(1, self.count_states + 1):
            for filepath in self.states[state-1].get_all_gpaths:
                self.file_to_pymol(filepath, state, set_defaults=False)

        self.pymol.set_default_rep()

        state = self.get_current_state
        self.pymol.pymol_cmd("group state_%d, toggle, open" % state)
        self.pymol.pymol_cmd("disable *")
        sel_file = self.get_selected_filepath
        if sel_file:
            self.pymol.pymol_cmd("enable state_%d and %s" % (state, sel_file.split("/")[-1].split(".")[0]))

    def load_scf_geometries(self):
        """
        Creates pymol object with all scf geometries
        :return:
        """
        state = self.get_current_state
        filepath = self.get_selected_filepath

        delete_after = True
        xyz_list = self.states[state - 1].get_all_xyz(filepath)
        del xyz_list[-1]
        i = 0
        base_path = "%s/%s" % (self.settings["workdir"], filepath.split("/")[-1].split(".")[0])

        for xyz in xyz_list:
            xyz_path = "%s_scf%03d.xyz" % (base_path, i)
            cf.write_file(xyz, xyz_path)
            self.pymol.load_structure(xyz_path, delete_after=delete_after)
            i += 1

        self.pymol.pymol_cmd("delete %s_scf" % base_path.split("/")[-1].split(".")[0])
        self.pymol.pymol_cmd("join_states %s_scf, %s_scf*, 0" % (base_path.split("/")[-1].split(".")[0],
                                                             base_path.split("/")[-1]))
        self.pymol.pymol_cmd("group state_%d, %s_scf" % (state, base_path.split("/")[-1].split(".")[0]))

        for j in range(0, i + 1):
            self.pymol.pymol_cmd("delete %s_scf%03d*" % (base_path.split("/")[-1], j))

        self.pymol.set_default_rep()
        self.pymol.pymol_cmd("disable *")
        self.pymol.pymol_cmd("enable state_%d and %s_scf" % (state, base_path.split("/")[-1].split(".")[0]))

    def change_pymol_structure(self):
        """
        displayes clicked entry in pymol
        :return:
        """
        if not self.pymol:
            return
        group = "state_%d" % self.get_current_state
        name = self.get_selected_filepath.split("/")[-1].split(".")[0]
        self.pymol.highlight(name=name, group=group)

    def plot_scf(self):
        """
        Takes the selected file and prints the 4 Convergence criterias.
        :return:
        """
        try:
            filepath = self.tabWidget.currentWidget().currentItem().text()
        except:
            return

        # Can not plot? :
        if filepath.split(".")[-1] not in ["out", "log"]:
            return

        # Sync with pymol
        if self.pymol:
            self.load_scf_geometries()

        filename = filepath.split('/')[-1]

        scf_data = self.states[self.tabWidget.currentIndex()].get_scf(filepath)

        #Check if this is geometry optimization or not (None if not):
        converged = self.states[self.tabWidget.currentIndex()].check_convergence(filepath)
        plot = PlotGdata(self, scf_data, filename)

        if converged is None:
            plot.plot_scf_done()
            self.append_text("%s seem to not be a geometry optimisation ..." % filename)
        else:
            plot.plot_scf_convergence()
            if converged is False:
                self.append_text("%s has not converged successfully." % filename)

    def add_files(self, paths=False):
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
        path = self.settings['workdir']
        filter_type = "Gaussian output files (*.out);; Gaussian input files (*.com *.inp);; " \
                      "Geometry files (*.pdb *.xyz)"
        title_ = "Import File"

        if isinstance(paths, list):
            files_path = paths
        else:
            files_path, type_ = self.import_files(title_, filter_type,path)

        if len(files_path) < 1:
            return

        # Remove file types not accepted by REACT
        accepted_files = ["inp", "com", "out", "xyz", "pdb"]
        files_path = [x for x in files_path if x.split(".")[-1] in accepted_files]

        # Where to start inserting files in project list:
        items_insert_index = self.tabWidget.currentWidget().count()

        # Start thread first:
        worker = Worker(self.thread_add_files, files_path, items_insert_index)
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
        pymol_defaults = False
        for n in range(len(file_paths)):
            file = file_paths[n]
            print(file)
            self.states[self.get_current_state - 1].add_gfile(file)
            if n == len(file_paths) - 1:
                pymol_defaults = True
            progress_callback.emit({self.update_progressbar: ((int(n+1) * 100 / len(file_paths)),),
                                    self.check_convergence: (file, item_index,
                                    self.tabWidget.currentIndex()),
                                    self.file_to_pymol: (file, self.get_current_state, pymol_defaults)})
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

    def update_progressbar(self, val=None, reverse=False):
        """
        :param val:
        :return:
        """
        with Lock():
            if not val:
                val = self.progressBar.value()
                if reverse:
                    val -= 1
                else:
                    val += 1
                if val > 80:
                    self.timer.setInterval(50)
                else:
                    self.timer.setInterval(10)

            if val < 100:
                self.progressBar.setTextVisible(True)

            if not reverse and val > 99:
                self.progressBar.setTextVisible(False)
                self.timer.stop()
            elif reverse and val < 1:
                self.timer2.stop()
                sys.exit()



            self.progressBar.setValue(int(val))

    def thread_complete(self):
        print("THREAD COMPLETE!")

        #if self.pymol:
        #    self.file_to_pymol(filepath=file, state=self.get_current_state, set_defaults=True)

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

    def delete_file(self):
        """
        Deletes selected file(s) from QtabBarWidget-->Tab-->QListWdget-->item
        :return:
        """
        # Avoid crash when no tabs exist
        if self.tabWidget.currentIndex() < 0:
            return

        # avoid crash when no files exist in state:
        if self.tabWidget.currentWidget().count() < 1:
            return

        # Get the list displayed in the current tab (state)
        current_list = self.tabWidget.currentWidget()

        # Get the selected item(s) ---> returns a list of objects
        list_items = current_list.selectedItems()

        # delete files from state
        tab_index = self.tabWidget.currentIndex()
        self.states[tab_index].del_gfiles([x.text() for x in list_items])

        # delete files from pymol
        if self.pymol:
            state = self.get_current_state
            [self.pymol.pymol_cmd("delete %s" % (x.text().split("/")[-1].split(".")[0]))
             for x in list_items]

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

    def update_tab_names(self):
        """
        Activated whenever tabs are moved. Renames Tabs in correct order of states (1,2,3,4...)
        Algorithm for updating list of states: temporary new list is created, 

        """
        # new list of pointers to State-objects. Poiners are appened one by one by the followin for-loop,
        # thus, according to the new order of tabs. Tabs still have their original labels, which are used to retrive correct pointer.
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

        #new state:
        state = self.count_states + 1
        self.tabWidget.addTab(DragDropListWidget(self), f"{state}")
        self.tabWidget.setCurrentWidget(self.tabWidget.widget(state - 1))
        if self.pymol:
            self.pymol.pymol_cmd("group state_%d" % state)
            self.tabWidget.widget(state - 1).itemClicked.connect(self.change_pymol_structure)


    def set_state(self, state):
        """
        Set tab to be displayed
        :param state: integer
        :return:
        """
        if int(state) <= self.count_states:
            self.tabWidget.setCurrentWidget(self.tabWidget.widget(state - 1))

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
        if self.pymol:
            self.pymol.pymol_cmd("delete state_%s" % str(tab_index + 1))

    def create_input_content(self, filepath):
        """
        :return: string -> content of new input file, based on outputfile given as argument
        """
        return self.states[self.tabWidget.currentIndex()].create_input_content(filepath)
    
    def create_xyz_filecontent(self, filepath):
        return self.states[self.tabWidget.currentIndex()].create_xyz_filecontent(filepath)

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
        if self.pymol:
            self.pymol.pymol_cmd("delete *")

        self.proj_name = proj_path.split("/")[-1]        
        self.workdir = proj_path.replace(self.proj_name, "")
        self.label_projectname.setText(self.proj_name.replace('.rxt', ''))

        with open(proj_path, 'r') as proj_file:
            proj = json.load(proj_file, object_hook=cf.json_hook_int_please)

        for key in ['states', 'included files', 'workdir', 'DFT', 'log']:
            self._import_project_pop_and_assign(proj, key)

    def _import_project_pop_and_assign(self, project, key):

        try:
            proj_item = project.pop(key)

            if key == 'states':
                for state in proj_item.items():
                    self.add_state()
                    self.add_files(state[1])

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

        temp_filepath = project["workdir"] + '/' + self.proj_name

        proj_path, filter_ = QtWidgets.QFileDialog.getSaveFileName(self, "Save project", temp_filepath, "REACT project (*.rxt)")

        if proj_path == '':
            return

        self.proj_name = proj_path.split("/")[-1]  
        
        #change project name title in workspace
        new_proj_title = proj_path.split('/')[-1].replace('.rxt', '')    
        self.label_projectname.setText(new_proj_title)

        with open(proj_path, 'w') as f:
            json.dump(project, f)

    def power_off_on(self):
        """
        power down when power button is clicked
        :return:
        """
        if self.power:
            self.button_power_off.setIcon(QtGui.QIcon('../resources/icons/power_off.png'))
            self.append_text("Powering down...", date_time=True)
            self.power = False
            self.timer2 = QTimer()
            self.timer2.timeout.connect(lambda: self.update_progressbar(reverse=True))
            self.timer2.start(5)

        else:
            self.button_power_off.setIcon(QtGui.QIcon('../resources/icons/power_on.png'))
            self.append_text("Powering down cancelled.")
            self.power = True
            self.timer2.stop()
            self.timer.start(5)

    @property
    def get_selected_filepath(self):
        """
        :return: path to selected file, str
        """
        try:
            return self.tabWidget.currentWidget().currentItem().text()
        except:
            return None

    @property
    def get_current_state(self):
        """
        :return: integer (state)
        """
        return self.tabWidget.currentIndex() + 1

    @property
    def count_states(self):
        """
        :return: integer (total number of states)
        """
        return self.tabWidget.count()

    def closeEvent(self, event):
        if self.pymol:
            try:
                # TODO this only partly works... QProcess: Destroyed while process ("OpenSourcePymol/dist/OpenSourcePymol.app") is still running.
                self.pymol.close()
            except:
                pass
### fbs code below not needed if we can not use fbs ###
# Instantiate ApplicationContext https://build-system.fman.io/manual/#your-python-code
#appctxt = ApplicationContext()
# Create window and show
#window = MainWindow()
# window.show() <- handled by splash screen - leave commented out

#exit_code = appctxt.app.exec_()
#sys.exit(exit_code)
### fbs code end ###


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # TODO transparent frameless main window? Maybe not, but maybe all the others?
    # window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    # window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    app.exec_()

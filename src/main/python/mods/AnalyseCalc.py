from PyQt5 import QtWidgets, QtGui
from UIs.AnalyseWindow import Ui_AnalyseWindow
import mods.common_functions as cf
from mods.ReactPlot import SpectrumIR


class AnalyseCalc(QtWidgets.QMainWindow, Ui_AnalyseWindow):
    def __init__(self, parent):
        super(AnalyseCalc, self).__init__(parent)

        self.react = parent

        self.ui = Ui_AnalyseWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("REACT - Analyse")
        
        self.ui.button_set_file.clicked.connect(self.set_file_included)
        self.ui.button_remove_file.clicked.connect(self.remove_file_included)

        self.ui.button_plot_frq.clicked.connect(self.plot_frequency)

        # Track State viewed in MainWindow:
        self.react.tabWidget.tabBar().currentChanged.connect(self.update_state_included_files)

        # Initialise dict of included files if it does not exist:
        self.energies = dict()
        state = self.react.tabWidget.currentIndex() + 1
        if not self.react.included_files or sum(len(x) for x in self.react.included_files[state].values()) < 4:
            self.init_included_files()
        self.update_state_included_files()

        self.ui.calctype.setCurrentRow(0)

    def init_included_files(self):
        """
        initialise dictionary with included files per state
        :return:
        """
        self.react.included_files = dict()
        for tab_index in range(self.react.tabWidget.count()):
            state = tab_index + 1

            self.react.included_files[state] = {0: "", 1: "", 2: "", 3: ""}
            if self.react.tabWidget.widget(tab_index).currentItem():
                file_path = self.react.tabWidget.widget(tab_index).currentItem().text()
                if file_path.split(".")[-1] in ["out", "log"]:

                    self.react.included_files[state][0] = file_path

                    # Check output file for frequencies
                    if self.react.states[tab_index].has_frequencies(file_path):
                        self.react.included_files[state][1] = file_path

                    # Check output file for Solvent
                    if self.react.states[tab_index].has_solvent(file_path):
                        self.react.included_files[state][2] = file_path

    def update_state_included_files(self):
        """
        When tabs are changed (state displayed) in main window, update correct files in list in analyse window
        TODO this function still exist after window is closed... need to kill it properly upon close
        :return:
        """
        tab_index = self.react.tabWidget.currentIndex()
        self.ui.label_state.setText(str(tab_index+1))

        # In case a new state has been added after initialising the analyse window:
        if tab_index + 1 not in self.react.included_files.keys():
            self.react.included_files[tab_index + 1] = {0: "", 1: "", 2: "", 3: ""}

        # Iterate through includes files and insert them into list:
        for index in sorted(self.react.included_files[tab_index+1].keys()):
            # If items exist in list, these must be removed before inserting new item:
            if self.ui.calc_files.count() > 0:
                self.ui.calc_files.takeItem(index)
            # Insert the new item:
            self.ui.calc_files.insertItem(index, self.react.included_files[tab_index+1][index])

            #Check if freq or solv is included in the main file:
            if index > 0:
                if self.react.included_files[tab_index+1][index] == self.react.included_files[1][0]:
                    self.ui.calc_files.item(index).setForeground(QtGui.QColor(70, 70, 70))

        # Move horizontal scrollbar according to text
        self.ui.calc_files.repaint()
        scrollbar = self.ui.calc_files.horizontalScrollBar()
        scrollbar.setValue(self.ui.calc_files.horizontalScrollBar().maximum())

        self.update_energies()
        self.update_absolute_values()
        self.update_relative_values()

    def update_energies(self):
        """

        :return:
        """
        for state in self.react.included_files.keys():
            if state not in self.energies.keys():
                self.energies[state] = {0: False, 1: False, 2: False, 3: False}

            for term in self.react.included_files[state].keys():
                # Check if state term has file (file length for now)
                if len(self.react.included_files[state][term]) > 2:
                    filepath = self.react.included_files[state][term]
                    state_object = self.react.states[state - 1]

                    # Include 3 corrections from frequency calculation
                    if term == 1:
                        self.energies[state][term] = dict()
                        self.energies[state][term]["dG"] = state_object.get_thermal_dg(filepath)
                        self.energies[state][term]["dH"] = state_object.get_thermal_dh(filepath)
                        self.energies[state][term]["dE"] = state_object.get_thermal_de(filepath)

                    else:
                        self.energies[state][term] = state_object.get_energy(filepath)
                else:
                    self.energies[state][term] = False

    def update_absolute_values(self):
        """

        :return:
        """
        self.ui.text_state_values.clear()
        self.ui.list_frequencies.clear()
        self.update_energies()
        D = cf.unicode_symbols["Delta"]
        d = cf.unicode_symbols["delta"]
        Dd = D+d
        DD = D+D

        state = self.react.tabWidget.currentIndex() + 1

        # If frequencies, insert them to list_frequencies:
        if self.energies[state][1]:
            insert_index = 0
            frequencies = self.react.states[state - 1].get_frequencies(str(self.react.included_files[state][1]))
            self.ui.list_frequencies.insertItem(insert_index, " Frequency IR Intensity")
            for freq in sorted(frequencies.keys()):
                insert_index += 1
                self.ui.list_frequencies.insertItem(insert_index, "%10.4f %10.4f" % (freq, frequencies[freq]))

    def update_relative_values(self):
        """

        :return:
        """
        self.ui.text_relative_values.clear()

        # Write header:
        D = cf.unicode_symbols["Delta"]
        d = cf.unicode_symbols["delta"]
        Dd = D + d
        DD = D + D

        self.ui.text_relative_values.appendPlainText("%5s%14s%14s%14s%14s%14s%14s%14s%14s%14s" %
                                                     ("State", D + "E(elec)", DD + "E(solv)", D + "E(big)", Dd + "G",
                                                      Dd + "H",
                                                      Dd + "E", D + "G", D + "H", D + "E",))

    def plot_frequency(self):
        """
        :return:
        """
        state = self.react.tabWidget.currentIndex() + 1
        if self.energies[state][1]:
            frequencies = self.react.states[state - 1].get_frequencies(str(self.react.included_files[state][1]))
            freq = list()
            inten = list()
            for x in sorted(frequencies.keys()):
                freq.append(x)
                inten.append(frequencies[x])
            SpectrumIR(freq, inten)

    def set_file_included(self):
        """
        Add file from main window to included_files and update list
        :return:
        """
        insert_index = self.ui.calctype.currentRow()
        filepath = self.react.tabWidget.currentWidget().currentItem().text()
        state = self.react.tabWidget.currentIndex() + 1

        if filepath.split(".")[-1] not in ["out", "log"]:
            self.react.append_text("File must be Gaussian output file")
            return

        #Check if file is what it is supposed to be:
        if insert_index == 1:
            if not self.react.states[state - 1].has_frequencies(filepath):
                self.react.append_text("\nNo frequencies found in %s" % filepath)
                return
        elif insert_index == 2:
            if not self.react.states[state - 1].has_solvent(filepath):
                self.react.append_text("\nNo solvent found in %s" % filepath)
                return

        # If no main file is set, automatically set the added file also as main:
        if insert_index != 0 and self.react.included_files[state][0] == "":
            self.react.included_files[state][0] = filepath

        self.react.included_files[state][insert_index] = filepath
        self.update_state_included_files()

    def remove_file_included(self):
        """
        Remove file from included_files and update list
        :return:
        """
        remove_index = self.ui.calctype.currentRow()
        state = self.react.tabWidget.currentIndex() + 1
        self.react.included_files[state][remove_index] = ""

        self.update_state_included_files()

    def closeEvent(self, event):
        """
        When closing window, set to analyse_window to None, so that window can be reopened again later.
        :param event:
        """
        self.react.analyse_window = None




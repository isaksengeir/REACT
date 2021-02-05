from PyQt5.QtCore import QProcess, Qt, pyqtSignal, pyqtSlot, QObject
import os


class PymolSession(QObject):
    # Signal to be emitted when pymol has returned all atom numbers of current selection
    atomsSelectedSignal = pyqtSignal(list)

    def __init__(self, parent=None, home=None, pymol_path=None):
        super(QObject, self).__init__(parent)
        self.parent = parent
        self.react = home
        self.pymol_path = pymol_path
        self.session = QProcess()
        self.session.setInputChannelMode(QProcess.ManagedInputChannel)
        self.session.setProcessChannelMode(QProcess.MergedChannels)

        # Connect Qprocess signals:
        self.session.finished.connect(self.pymol_finished)
        self.session.readyReadStandardOutput.connect(self.handle_stdout)
        self.session.stateChanged.connect(self.handle_state)

        # Delete file of loaded molecule after loading it:
        self.files_to_delete = list()
        self.collect_atoms = False
        self.iterate_found = False

        self.start_pymol()
        self.set_pymol_settings()

    def load_structure(self, file_=None, delete_after=False):
        """
        Load file in pymol
        :param file_: path to file (xyz, pdb, mae)
        """
        if delete_after:
            # filename as displayed in pymol : filepath
            self.files_to_delete.append(file_)

        if not file_:
            print("PymolProcess load_structure - No file given")
            return

        self.pymol_cmd("load %s" % file_)

    def start_pymol(self, external_gui=False):
        startup = ["-p"]
        if not external_gui:
            startup.append("-x")


        self.session.start(self.pymol_path, startup)
        print(self.session.waitForStarted())

        self.session.isWindowType()

    def pymol_cmd(self, cmd=""):
        """
        Write standard pymol commands to pymol
        :param cmd: pymol command
        :return:
        """
        cmd += "\n"
        self.session.write(cmd.encode())

    def set_pymol_settings(self):
        """
        :return:
        """
        if not self.session:
            return
        settings = ["space cmyk\n", "set stick_radius, 0.17\n", "set spec_power, 250\n", "set spec_reflect, 2\n"]
        for setting in settings:
            self.pymol_cmd(setting)

    def set_default_rep(self):
        """
        :return:
        """
        print("setting defaults")
        self.pymol_cmd("hide spheres")
        self.pymol_cmd("show sticks")
        self.pymol_cmd("color grey, name C*")

    def set_protein_ligand_rep(self, residues, pymol_name, group):
        """
        :param name: pymol pdb name (internal)
        :param group: pymol group where pdb is located
        :param residues: residue names to highlight
        :return:
        """
        # makes sure solvent is not represented by sticks
        self.pymol_cmd("hide sticks, %s and %s and sol." % (group, pymol_name))
        self.pymol_cmd("show lines, %s and %s" % (group, pymol_name))

        sel_str = "resname %s" % residues.pop(0)

        if len(residues) > 0:
            sel_str += " or resname ".join(residues)

        self.pymol_cmd("hide sticks, %s and %s and not %s" % (group, pymol_name, sel_str))
        self.pymol_cmd("color chartreuse, %s and %s and %s and name C*" % (group, pymol_name, sel_str))
        self.pymol_cmd("zoom %s and %s and %s, 10" % (group, pymol_name, sel_str))

    def highlight_atoms(self, atoms=list, color=str, name=str, group=None):
        """
        :param atoms:
        :param color:
        :param name:
        :param group:
        :return:
        """
        cmd = str()
        if group:
            cmd += "%s and " % group
        self.pymol_cmd("hide sticks, %s %s" % (cmd, name))

        self.pymol_cmd("color grey, %s %s and name C*" % (cmd, name))

        selection = "(id %s)" % (" or id ".join(atoms))
        self.pymol_cmd("show sticks, %s%s " % (cmd, selection))

        self.pymol_cmd("color %s, name C* and %s%s" % (color, cmd, selection))

    def highlight(self, name=None, group=None):
        """
        :param name: name of structure to be highlighted
        :param group: name of group, if used
        :return:
        """
        self.pymol_cmd("disable *")
        if group:
            self.pymol_cmd("group %s, toggle, open" % group)
        self.pymol_cmd("enable %s or %s" % (group, name))

    def set_selection(self, atoms, sele_name, object_name, group):
        """
        :param atoms: list of atom numbers
        :param sele_name: what to call selection (rather than (sele))
        :param object_name: What object to select from in pymol
        :param group: what group object belongs to
        :return:
        """
        self.pymol_cmd("delete %s" % sele_name)
        sel_str = "id "
        sel_str += " or id ".join(atoms)
        self.pymol_cmd("select %s, %s and %s and (%s)" % (sele_name, group, object_name, sel_str))
        self.pymol_cmd("group %s, %s" % (group, sele_name))

    def expand_sele(self, selection="sele", sele_name="new", group="", radius=5, by_res=True, include_solv=True):
        """
        :param selection:
        :param radius: radius around selection to select
        :return:
        """
        self.pymol_cmd("delete %s" % sele_name)
        cmd = "select %s, " % sele_name
        if by_res:
            cmd += "byres "
        cmd += "%s around %s " % (selection, str(radius))
        if not include_solv:
            cmd += "and not sol."

        self.pymol_cmd(cmd)

        self.pymol_cmd("group %s, %s" % (group, sele_name))

    def get_selected_atoms(self, sele="sele"):
        """
        Get PDB atom numbers for selection
        :return:
        """
        # iterate sele, rank
        self.atoms_selected = list()
        self.collect_atoms = True
        self.iterate_found = False
        self.pymol_cmd("iterate %s, ID" % sele)
        self.session.waitForReadyRead()

    def copy_sele_to_object(self, sele="sele", target_name="new_obj", group=None):
        """
        :param sele:
        :param target_name:
        :param group:
        :return:
        """
        self.pymol_cmd("delete %s" % target_name)
        self.pymol_cmd("create %s, %s" % (target_name, sele))
        if group:
            self.pymol_cmd("group %s, %s" % (group, target_name))

    def pymol_finished(self):
        self.parent.pymol = None
        print("Pymol session completed")

    def delete_all_files(self):
        """
        Iterates through self.delete_file and removes from disk
        :return:
        """
        for filename in self.files_to_delete:
            os.remove(filename)
        self.files_to_delete = list()

    def handle_stdout(self):
        """
        Reads output from Qprocess - this will be used to auto-decide handling REACT <--> Pymol
        :return:
        """
        data = self.session.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        if "CmdLoad:" in stdout:
            if len(self.files_to_delete) > 0:
                os.remove(self.files_to_delete.pop(0))
        if self.collect_atoms:
            if "Iterate:" in stdout:
                self.return_sel_atomnr()
                self.collect_atoms = False
            elif "iterate" in stdout:
                self.iterate_found = True
            if self.iterate_found:
                self.collect_iterate_rank(stdout)

    def collect_iterate_rank(self, stdout):
        """
        Read standard output from Qprocess pymol in the case of "iterate sele, rank" and collects atom numbers to
        self.atoms_selected
        :param stdout:
        :return:
        """
        for junk in stdout.split():
            for atomnr in junk.split("\n"):
                if atomnr.isnumeric():
                    self.atoms_selected.append(atomnr)

    @pyqtSlot()
    def return_sel_atomnr(self):
        self.atomsSelectedSignal.emit(self.atoms_selected)

    def handle_state(self, state):
        states = {
            QProcess.NotRunning: 'Exited',
            QProcess.Starting: 'Starting',
            QProcess.Running: 'Running',
        }
        state_name = states[state]
        print(f"Pymol: {state_name}")
        try:
            self.react.append_text(f"Pymol: {state_name}", date_time=True)
        except:
            pass
        if QProcess.NotRunning:
            self.disconnect_pymol()


    def handle_stderr(self):
        data = self.session.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def close(self):
        """
        Disconnect for a cleaner kill
        :return:
        """
        try:

            self.pymol_cmd("quit")
            self.session.kill()
            self.disconnect_pymol()
        except:
            pass

    def disconnect_pymol(self):
        self.react.tabWidget.tabBar().currentChanged.disconnect(self.react.pymol_view_current_state)
        self.react.connect_pymol_structures(connect=False)
        self.delete_all_files()




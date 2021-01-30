from PyQt5.QtCore import QProcess

import os

# https://www.learnpyqt.com/tutorials/qprocess-external-programs/


class PymolSession:
    def __init__(self, parent=None, home=None, pymol_path=None):
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

    def highlight(self, name=None, group=None):
        """
        :param name: name of structure to be highlighted
        :param group: name of group, if used
        :return:
        """
        self.pymol_cmd("disable *")
        self.pymol_cmd("enable %s or %s" % (group, name))

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
        if "CmdLoad: loaded as" in stdout:
            # Delete file?
            # print(stdout)
            print(stdout)
            if len(self.files_to_delete) > 0:
                os.remove(self.files_to_delete.pop(0))
                # remove left " and right ". from pymol string in filename
                #filename = stdout.split()[3][1:-2]

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
        if state == QProcess.NotRunning:
            self.close()

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
            self.react.tabWidget.tabBar().currentChanged.disconnect(self.react.pymol_view_current_state)
            self.react.connect_pymol_structures(connect=False)
            self.delete_all_files()

            self.close()
            self.session.kill()

        except:
            pass




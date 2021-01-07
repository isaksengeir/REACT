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
        self.delete_file = None

        self.start_pymol()
        self.set_pymol_settings()

    def load_structure(self, file_=None, delete_after=False):
        """
        Load file in pymol
        :param file_: path to file (xyz, pdb, mae)
        """
        if delete_after:
            self.delete_file = file_
        if not file_:
            print("PymolProcess load_structure - No file given")
            return
        text = 'load %s \n' % file_
        self.session.write(text.encode())

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
            self.session.write(setting.encode())

    def pymol_finished(self):
        self.parent.pymol = None
        print("Pymol session completed")

    def handle_stdout(self):
        """
        Reads output from Qprocess - this will be used to auto-decide handling REACT <--> Pymol
        :return:
        """
        data = self.session.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")

        # Delete file?
        if self.delete_file:
            if "CmdLoad: loaded as" in stdout:
                os.remove(self.delete_file)
                self.delete_file = None

        # TODO remove print statement
        print(stdout)

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

    def handle_stderr(self):
        data = self.session.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def close(self):
        self.session.kill()

from PyQt5.QtCore import QProcess, QIODevice

import sys

# https://www.learnpyqt.com/tutorials/qprocess-external-programs/


class PymolSession:
    def __init__(self, parent=None, home=None, pymol_path=None):
        self.parent = parent
        self.react = home
        self.pymol_path = pymol_path
        self.session = QProcess()
        # Connect Qprocess signals:
        self.session.finished.connect(self.pymol_finished)
        self.session.readyReadStandardOutput.connect(self.handle_stdout)
        self.session.stateChanged.connect(self.handle_state)

        self.start_pymol()

    def load_structure(self, file_=None):
        if not file_:
            print("PymolProcess load_structure - No file given")
            return
        #self.session.write(f"load {file_}\n".encode('utf-8'))
        text = u"load %s\n" % file_
        self.session.write(text.encode('utf-8'))
        self.session.waitForReadyRead()
        self.session.writeData(text)

        self.session.readAll()

    def start_pymol(self):
        self.session.start(self.pymol_path)
        self.session.waitForStarted()

    def pymol_finished(self):
        self.parent.pymol = None
        print("Pymol session completed")

    def handle_stdout(self):
        """
        Reads output from Qprocess
        :return:
        """
        data = self.session.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
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
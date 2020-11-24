
from UIs.SplashScreen import Ui_SplashScreen
from PyQt5 import QtWidgets, QtGui, QtCore

counter = 0


class SplashScreen(QtWidgets.QMainWindow, Ui_SplashScreen):
    def __init__(self, parent):
        QtWidgets.QMainWindow.__init__(self)
        self.parent = parent
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Remove title bar:
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Drop shadow effect:
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)


        # Start timer:
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)

        # Timer in milliseconds:
        self.timer.start(35)

        # Text in splash screen:
        #QtCore.QTimer.singleShot(1000, lambda: self.ui.label_loading.setText("<strong>loading...<strong>USER "
         #                                                                    "INTERFACE</strong>"))

    def progress(self):
        """
        :return:
        """
        global counter

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.parent.window().show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        counter += 1
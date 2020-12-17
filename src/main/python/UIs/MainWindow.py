# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 436)
        font = QtGui.QFont()
        font.setFamily("Courier")
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("\n"
"QMainWindow{\n"
"background-color:rgb(20, 20, 20);\n"
"color: rgb(98, 114, 164);\n"
"}\n"
"\n"
"\n"
"QScrollBar{\n"
"/*background-color:rgb(56,58,89);*/\n"
"background-color:rgb(30,30,30);\n"
"}\n"
"\n"
"QFrame {\n"
"/*background-color: rgb(56,58,89);*/\n"
"background-color: rgb(30,30,30);\n"
"/*border: 2px solid rgb(220,220,220);*/\n"
"/*border: 2px solid rgb(143, 23, 119);*/\n"
"border: 2px solid rgb(98, 114, 164);\n"
"/*border: 2px solid rgb(56,58,89);*/\n"
"\n"
"\n"
"border-radius:10px;\n"
"\n"
"}\n"
"\n"
"QLabel{\n"
"color:rgb(98, 114, 164);\n"
"border: 0px;\n"
"}\n"
"\n"
"QLineEdit{\n"
"color: rgb(220,220,220);\n"
"background-color: rgb(20,20,20);\n"
"border: None;\n"
"}\n"
"QLineEdit::hover {\n"
"border: 1px solid rgb(143,23,119);\n"
"}\n"
"\n"
"QRadioButton{\n"
"color: rgb(98, 114, 164);\n"
"\n"
"}\n"
"\n"
"QRadioButton::indicator::unchecked {\n"
"    background-color: rgb(20,20,20);\n"
"}\n"
"\n"
"\n"
"QRadioButton::indicator:unchecked:hover {\n"
"   background-color: rgb(143,23,119);\n"
"}\n"
"\n"
"QRadioButton::indicator::checked {\n"
"    background-color:  rgb(98, 114, 164);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked:hover {\n"
"    background-color: rgb(143,23,119);\n"
"}\n"
"\n"
"/*\n"
"\n"
"QRadioButton::indicator:unchecked:pressed {\n"
"    image: url(:/images/radiobutton_unchecked_pressed.png);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"QRadioButton::indicator:checked:pressed {\n"
"    image: url(:/images/radiobutton_checked_pressed.png);\n"
"}\n"
"\n"
"*/\n"
"\n"
"\n"
"/* IMPORTANT: 8< Add the code above here 8< */\n"
"QTabBar::tab:selected {\n"
"/* expand/overlap to the left and right by 4px */\n"
"margin-left: -4px;\n"
"margin-right: -4px;\n"
"}\n"
"QTabBar::tab:first:selected {\n"
"margin-left: 0; /* the first selected tab has nothing to overlap with on the left */\n"
"}\n"
"QTabBar::tab:last:selected {\n"
"margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"}\n"
"QTabBar::tab:only-one {\n"
"margin: 0; /* if there is only one tab, we don\'t want overlapping margins */\n"
"}\n"
"\n"
"QTabWidget::pane { /* The tab widget frame */\n"
"/*border-top: 2px solid #C2C7CB;*/\n"
"\n"
"/*border-top:4px solid rgb(56,58,89);*/\n"
"border-top:4px solid rgb(30,30,30);\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"left: 5px; /* move to the right by 5px */\n"
"}\n"
"\n"
"/* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QTabWidget */\n"
"QTabBar::tab {\n"
"/*border: 2px solid rgb(98, 114, 164);\n"
"\n"
"border-bottom-color: rgb(98, 114, 164);*/\n"
"border: 2px solid rgb(40, 40, 40);\n"
"\n"
"border-bottom-color: rgb(143, 23, 119);\n"
"border-top-left-radius: 4px;\n"
"border-top-right-radius: 4px;\n"
"min-width: 8ex;\n"
"padding: 2px;\n"
"color:rgb(143, 23, 119);\n"
"\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"/*background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #fafafa, stop: 0.4 #f4f4f4, stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);*/\n"
"background-color:rgb(42,42,42);\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"/*border-color: #9B9B9B;*/\n"
"\n"
"    border-color: rgb(143, 23, 119);\n"
"    border-bottom-color:  rgb(143,23,119);\n"
"    border-width: 3px;\n"
"    color:rgb(20,20,20);\n"
"    background-color: rgb(143,23,119);\n"
"\n"
"}\n"
"QTabBar::tab:!selected {\n"
"margin-top: 2px; /* make non-selected tabs look smaller */\n"
"}\n"
"\n"
"\n"
"QPushButton {\n"
"    /*background-color:rgb(98, 114, 164);*/\n"
"    background-color: rgb(30,30,30);\n"
"    color: rgb(143,23,119);\n"
"    \n"
"\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"       background-color: rgb(40, 40, 40);\n"
"    /*color:rgb(20,20,20);*/\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-color: rgb(143,23,119);\n"
"\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    color: rgb(143, 23, 119);\n"
"    background-color: rgb(20, 20, 20);\n"
"}\n"
"\n"
"QTableWidget QFrame{\n"
"border: None;\n"
"}\n"
"\n"
"QTableWidget {\n"
"color: rgb(98, 114, 164);\n"
"padding: 5px;\n"
"border-color: rgb(143, 23, 119);\n"
"selection-background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"QTableWidget::item:selected{\n"
"border: 1px solid rgb(143, 23, 119);\n"
"border-style: outset;\n"
"/* trying below, remove?*/\n"
"selection-background-color:transparent;\n"
"}\n"
"\n"
"\n"
"QTableView QTableCornerButton::section {\n"
"    background: rgb(30,30,30);\n"
"    border: None;\n"
"}\n"
"\n"
"QTableView QHeaderView::section {\n"
"color: rgb(143,23,119);\n"
"background-color: rgb(40,40,40);\n"
"\n"
"}\n"
"\n"
"\n"
"QListWidget{\n"
"border:None;\n"
"margin-top:5px;\n"
"margin-left:5px;\n"
"margin-right:5px;\n"
"\n"
"\n"
"background-color: rgb(30,30,30);\n"
"\n"
"color:rgb(98, 114, 164);\n"
"\n"
"}\n"
"\n"
"/* Works for both QListView and QListWidget */\n"
"QListView::item {\n"
"    /* Won\'t work without borders set */\n"
"    padding-left:1px;\n"
"    padding-right:10px;\n"
"    padding-top:1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"QListView::item:hover{\n"
"/*background-color: rgb(143,23,119);*/\n"
"border: 1px solid rgb(143, 23, 119);\n"
"border-style: outset;\n"
"background-color: rgb(40,40,40);\n"
"padding-left:5px;\n"
"padding-right:-10px;\n"
"}\n"
"\n"
"QListView::item:selected{\n"
"color: rgb(20,20,20);\n"
"background-color:rgb(98, 114, 164);\n"
"padding-left:10px;\n"
"padding-right:-10px;\n"
"\n"
"}\n"
"\n"
"QPlainTextEdit{\n"
"border: None;\n"
"color:rgb(98, 114, 164);\n"
"}\n"
"\n"
"\n"
"QFileDialog{\n"
"background-color:rgb(30,30,30);\n"
"border: 0px;\n"
"color: rgb(98,114,164);\n"
"}\n"
"\n"
"QTextEdit{\n"
"color: rgb(98, 114, 164);\n"
"border: None;\n"
"}\n"
"\n"
"QProgressBar {\n"
"    \n"
"    /*background-color: rgb(98, 114, 164);*/\n"
"    background-color: rgb(20,20,20);\n"
"    color: rgb(200, 200, 200);\n"
"    border-style: none;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"    border-radius: 10px;\n"
"    /*background-color: qlineargradient(spread:pad, x1:0, y1:0.511364, x2:1, y2:0.523, stop:0 rgba(254, 121, 199, 255), stop:1 rgba(170, 85, 255, 255));*/\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(170, 85, 255, 255), stop:1 rgba(143,23,119,255));\n"
"}\n"
"\n"
"\n"
"\n"
"QSpinBox {\n"
"/*padding-right: 15px; /* make room for the arrows */\n"
"background-color: rgb(20,20,20);\n"
"color: rgb(220,220,220);\n"
"border: 1px solid rgb(20, 20, 20);\n"
"}\n"
"\n"
"QSpinBox:hover\n"
"{\n"
"    border: 1px solid rgb(143, 23, 119);\n"
"}\n"
"\n"
"QSpinBox:focus\n"
"{\n"
"    border: 1px solid rgb(143, 23, 119);\n"
"}\n"
"\n"
"\n"
"QSpinBox::up-button {\n"
"    background-color: rgb(30,30,30);\n"
"    subcontrol-origin: border;\n"
"     subcontrol-position: top right; /* position at the top right corner */\n"
"\n"
"     width: 16px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */\n"
"    image: url(:/16x16/resources/icons/arrow-top.png) 1;\n"
"    border-width: 1px;\n"
"    top: 1px;\n"
"    right: 1px;\n"
"}\n"
"\n"
" QSpinBox::up-button:hover {\n"
"    background-color: rgb(143, 23, 119);\n"
"}\n"
"\n"
"QSpinBox::up-button:pressed  {\n"
"top: -1px;\n"
"right: 2px;\n"
"}\n"
"\n"
"\n"
"QSpinBox::down-button {\n"
"    background-color:rgb(30,30,30);\n"
"     subcontrol-origin: border;\n"
"     subcontrol-position: bottom right; /* position at bottom right corner */\n"
"\n"
"     width: 16px;\n"
"     image: url(:/16x16/resources/icons/arrow-bottom.png) 1;\n"
"     border-width: 1px;\n"
"     border-top-width: 0;\n"
"    top: -1px;\n"
"    right: 1px;\n"
" }\n"
"\n"
"QSpinBox::down-button:hover {\n"
"    background-color: rgb(143, 23, 119);\n"
"}\n"
"\n"
"QSpinBox::down-button:pressed  {\n"
"top: 1px;\n"
"right: 2px;\n"
"}\n"
"\n"
"\n"
"QComboBox {\n"
"    border: 1px solid rgb(30,30,30);\n"
"    border-radius: 3px;\n"
"    padding: 0px 3px 0px 3px;\n"
"    /*min-width: 6em;*/\n"
"}\n"
"\n"
"QComboBox:!editable::hover {\n"
"border: 1px solid rgb(143,23,119);\n"
"}\n"
"\n"
"QComboBox:!editable {\n"
"background: rgb(20,20,20);\n"
"color: rgb(220,220,220);\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: rgb(40,40,40);\n"
"}\n"
"\n"
"\n"
"/* QComboBox gets the \"on\" state when the popup is open */\n"
"QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"   /* background: rgb(20, 20, 20);*/\n"
"    background-color: rgb(143,23,119);\n"
"}\n"
"\n"
"QComboBox:!editable:off, QComboBox::drop-down:editable:off {\n"
"   /* background: rgb(20, 20, 20);*/\n"
"    background-color: rgb(143,23,119);\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"\n"
"}\n"
"\n"
"/* This controls the button*/\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    border-left-width: 1px;\n"
"    border-left-color:  rgb(20,20,20);\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"    background-color: rgb(40,40,40);\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/16x16/resources/icons/arrow-bottom.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid rgb(143,23,119);\n"
"    border-radius:0px;\n"
"    background-color: rgb(40,40,40);\n"
"    min-width: 150px;\n"
"\n"
"}\n"
"\n"
"\n"
"QCheckBox {\n"
"color: rgb(98, 114, 164);\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"image: url(:/24x24/resources/icons/toggle_on.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"image: url(:/24x24/resources/icons/toggle_off.png);\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(150, 300))
        self.frame.setMaximumSize(QtCore.QSize(150, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.frame)
        self.splitter.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter.setStyleSheet("QFrame {\n"
"border: None;\n"
"}\n"
"")
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(0)
        self.splitter.setObjectName("splitter")
        self.button_settings = QtWidgets.QPushButton(self.splitter)
        self.button_settings.setMinimumSize(QtCore.QSize(0, 30))
        self.button_settings.setObjectName("button_settings")
        self.button_calc_setup = QtWidgets.QPushButton(self.splitter)
        self.button_calc_setup.setMinimumSize(QtCore.QSize(0, 30))
        self.button_calc_setup.setObjectName("button_calc_setup")
        self.button_create_cluster = QtWidgets.QPushButton(self.splitter)
        self.button_create_cluster.setMinimumSize(QtCore.QSize(0, 30))
        self.button_create_cluster.setObjectName("button_create_cluster")
        self.button_analyse_calc = QtWidgets.QPushButton(self.splitter)
        self.button_analyse_calc.setMinimumSize(QtCore.QSize(0, 30))
        self.button_analyse_calc.setStyleSheet("QSplitter{border: 0px;}")
        self.button_analyse_calc.setObjectName("button_analyse_calc")
        self.button_plotter = QtWidgets.QPushButton(self.splitter)
        self.button_plotter.setMinimumSize(QtCore.QSize(0, 30))
        self.button_plotter.setObjectName("button_plotter")
        self.verticalLayout_2.addWidget(self.splitter)
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setMinimumSize(QtCore.QSize(500, 50))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.frame_3)
        self.progressBar.setMinimumSize(QtCore.QSize(300, 0))
        self.progressBar.setSizeIncrement(QtCore.QSize(0, 0))
        self.progressBar.setProperty("value", 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_4.addWidget(self.progressBar, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 2, 1, 1)
        self.button_power_off = QtWidgets.QPushButton(self.frame_3)
        self.button_power_off.setMinimumSize(QtCore.QSize(24, 24))
        self.button_power_off.setMaximumSize(QtCore.QSize(24, 24))
        self.button_power_off.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/power_on.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_power_off.setIcon(icon)
        self.button_power_off.setIconSize(QtCore.QSize(24, 24))
        self.button_power_off.setFlat(True)
        self.button_power_off.setObjectName("button_power_off")
        self.gridLayout_4.addWidget(self.button_power_off, 0, 3, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_4)
        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 3)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(500, 50))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_7.setContentsMargins(-1, 0, 12, 2)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/resources/icons/logo_blue.png"))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 3)
        self.frame_5 = QtWidgets.QFrame(self.centralwidget)
        self.frame_5.setMinimumSize(QtCore.QSize(200, 300))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.textBrowser = QtWidgets.QPlainTextEdit(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.textBrowser.setFont(font)
        self.textBrowser.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setPlainText("")
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_5.addWidget(self.textBrowser)
        self.gridLayout.addWidget(self.frame_5, 1, 2, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.centralwidget)
        self.frame_4.setMinimumSize(QtCore.QSize(300, 300))
        self.frame_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(143, 23, 119);\n"
"      color: white;\n"
"\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"       background-color:rgb(143, 23, 119);\n"
"\n"
"    border-style: outset;\n"
"    border-width: 0px;\n"
"    border-radius:10px;\n"
"\n"
"    \n"
"    /*border-color: rgb(12, 103, 213);*/\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"       /*background-color:rgb(17, 145, 255);\n"
"    color: black*/\n"
"    background-color: rgb(42, 42, 42);\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        self.label_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_2.setMaximumSize(QtCore.QSize(50, 20))
        self.label_2.setLineWidth(0)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label_projectname = QtWidgets.QLabel(self.frame_4)
        self.label_projectname.setMinimumSize(QtCore.QSize(50, 0))
        self.label_projectname.setMaximumSize(QtCore.QSize(16777215, 20))
        self.label_projectname.setStyleSheet("color:rgb(200,200,200);")
        self.label_projectname.setObjectName("label_projectname")
        self.horizontalLayout.addWidget(self.label_projectname)
        self.button_open_project = QtWidgets.QPushButton(self.frame_4)
        self.button_open_project.setMinimumSize(QtCore.QSize(24, 24))
        self.button_open_project.setMaximumSize(QtCore.QSize(24, 24))
        self.button_open_project.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_open_project.setIcon(icon1)
        self.button_open_project.setIconSize(QtCore.QSize(24, 24))
        self.button_open_project.setFlat(True)
        self.button_open_project.setObjectName("button_open_project")
        self.horizontalLayout.addWidget(self.button_open_project)
        self.button_save_project = QtWidgets.QPushButton(self.frame_4)
        self.button_save_project.setMinimumSize(QtCore.QSize(24, 24))
        self.button_save_project.setMaximumSize(QtCore.QSize(24, 24))
        self.button_save_project.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_save_project.setIcon(icon2)
        self.button_save_project.setIconSize(QtCore.QSize(24, 24))
        self.button_save_project.setFlat(True)
        self.button_save_project.setObjectName("button_save_project")
        self.horizontalLayout.addWidget(self.button_save_project)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setMinimumSize(QtCore.QSize(50, 0))
        self.label_3.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.button_add_state = QtWidgets.QPushButton(self.frame_4)
        self.button_add_state.setMinimumSize(QtCore.QSize(24, 24))
        self.button_add_state.setMaximumSize(QtCore.QSize(24, 24))
        self.button_add_state.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_add_state.setIcon(icon3)
        self.button_add_state.setIconSize(QtCore.QSize(24, 24))
        self.button_add_state.setFlat(True)
        self.button_add_state.setObjectName("button_add_state")
        self.horizontalLayout_2.addWidget(self.button_add_state)
        self.button_delete_state = QtWidgets.QPushButton(self.frame_4)
        self.button_delete_state.setMinimumSize(QtCore.QSize(24, 24))
        self.button_delete_state.setMaximumSize(QtCore.QSize(24, 24))
        self.button_delete_state.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_delete_state.setIcon(icon4)
        self.button_delete_state.setIconSize(QtCore.QSize(24, 24))
        self.button_delete_state.setFlat(True)
        self.button_delete_state.setObjectName("button_delete_state")
        self.horizontalLayout_2.addWidget(self.button_delete_state)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.frame_4)
        self.tabWidget.setStyleSheet("/*border-color:rgb(98, 114, 164);*/\n"
"\n"
"border-color:rgb(143, 23, 119);")
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 5, 1)
        self.button_delete_file = QtWidgets.QPushButton(self.frame_4)
        self.button_delete_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_delete_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_delete_file.setText("")
        self.button_delete_file.setIcon(icon4)
        self.button_delete_file.setIconSize(QtCore.QSize(24, 24))
        self.button_delete_file.setFlat(True)
        self.button_delete_file.setObjectName("button_delete_file")
        self.gridLayout_2.addWidget(self.button_delete_file, 2, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem5, 4, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem6, 0, 1, 1, 1)
        self.button_add_file = QtWidgets.QPushButton(self.frame_4)
        self.button_add_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_add_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_add_file.setText("")
        self.button_add_file.setIcon(icon3)
        self.button_add_file.setIconSize(QtCore.QSize(24, 24))
        self.button_add_file.setFlat(True)
        self.button_add_file.setObjectName("button_add_file")
        self.gridLayout_2.addWidget(self.button_add_file, 1, 1, 1, 1)
        self.button_edit_file = QtWidgets.QPushButton(self.frame_4)
        self.button_edit_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_edit_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_edit_file.setStyleSheet("")
        self.button_edit_file.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/edit-pencil.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_edit_file.setIcon(icon5)
        self.button_edit_file.setIconSize(QtCore.QSize(24, 24))
        self.button_edit_file.setFlat(True)
        self.button_edit_file.setObjectName("button_edit_file")
        self.gridLayout_2.addWidget(self.button_edit_file, 3, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 0, 0, 1, 1)
        self.button_print_scf = QtWidgets.QPushButton(self.frame_4)
        self.button_print_scf.setMinimumSize(QtCore.QSize(24, 24))
        self.button_print_scf.setMaximumSize(QtCore.QSize(24, 24))
        self.button_print_scf.setStyleSheet("")
        self.button_print_scf.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/quick_print_SCF.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_print_scf.setIcon(icon6)
        self.button_print_scf.setIconSize(QtCore.QSize(24, 24))
        self.button_print_scf.setFlat(True)
        self.button_print_scf.setObjectName("button_print_scf")
        self.gridLayout_3.addWidget(self.button_print_scf, 0, 1, 1, 1)
        self.button_plot_ene_diagram = QtWidgets.QPushButton(self.frame_4)
        self.button_plot_ene_diagram.setMinimumSize(QtCore.QSize(24, 24))
        self.button_plot_ene_diagram.setMaximumSize(QtCore.QSize(24, 24))
        self.button_plot_ene_diagram.setStyleSheet("")
        self.button_plot_ene_diagram.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/plot_enediagram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_plot_ene_diagram.setIcon(icon7)
        self.button_plot_ene_diagram.setIconSize(QtCore.QSize(24, 24))
        self.button_plot_ene_diagram.setFlat(True)
        self.button_plot_ene_diagram.setObjectName("button_plot_ene_diagram")
        self.gridLayout_3.addWidget(self.button_plot_ene_diagram, 0, 2, 1, 1)
        self.button_print_energy = QtWidgets.QPushButton(self.frame_4)
        self.button_print_energy.setMinimumSize(QtCore.QSize(24, 24))
        self.button_print_energy.setMaximumSize(QtCore.QSize(24, 24))
        self.button_print_energy.setStyleSheet("")
        self.button_print_energy.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/quick_print_E.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_print_energy.setIcon(icon8)
        self.button_print_energy.setIconSize(QtCore.QSize(24, 24))
        self.button_print_energy.setFlat(True)
        self.button_print_energy.setObjectName("button_print_energy")
        self.gridLayout_3.addWidget(self.button_print_energy, 0, 3, 1, 1)
        self.button_print_relativeE = QtWidgets.QPushButton(self.frame_4)
        self.button_print_relativeE.setMinimumSize(QtCore.QSize(24, 24))
        self.button_print_relativeE.setMaximumSize(QtCore.QSize(24, 24))
        self.button_print_relativeE.setStyleSheet("")
        self.button_print_relativeE.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/quick_delta_E.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_print_relativeE.setIcon(icon9)
        self.button_print_relativeE.setIconSize(QtCore.QSize(24, 24))
        self.button_print_relativeE.setFlat(True)
        self.button_print_relativeE.setObjectName("button_print_relativeE")
        self.gridLayout_3.addWidget(self.button_print_relativeE, 0, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_3)
        self.gridLayout.addWidget(self.frame_4, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_settings.setText(_translate("MainWindow", "Settings"))
        self.button_calc_setup.setText(_translate("MainWindow", "Calculation setup"))
        self.button_create_cluster.setText(_translate("MainWindow", "Create cluster"))
        self.button_analyse_calc.setText(_translate("MainWindow", "Analyse calculation"))
        self.button_plotter.setText(_translate("MainWindow", "Plotter"))
        self.label_2.setText(_translate("MainWindow", "Project:"))
        self.label_projectname.setText(_translate("MainWindow", "new_project"))
        self.label_3.setText(_translate("MainWindow", "States"))
        self.label_4.setText(_translate("MainWindow", "Quick launch"))
#import icons_rc

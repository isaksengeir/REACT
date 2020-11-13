# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AnalyseWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnalyseWindow(object):
    def setupUi(self, AnalyseWindow):
        AnalyseWindow.setObjectName("AnalyseWindow")
        AnalyseWindow.resize(704, 349)
        AnalyseWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(AnalyseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(331, 151))
        self.frame.setMaximumSize(QtCore.QSize(331, 151))
        self.frame.setStyleSheet("QListWidget{\n"
"\n"
"\n"
"}\n"
"QPushButton {\n"
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
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 5, 64, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.button_set_file = QtWidgets.QPushButton(self.layoutWidget)
        self.button_set_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_set_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_set_file.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_set_file.setIcon(icon)
        self.button_set_file.setIconSize(QtCore.QSize(24, 24))
        self.button_set_file.setFlat(True)
        self.button_set_file.setObjectName("button_set_file")
        self.gridLayout.addWidget(self.button_set_file, 0, 0, 1, 1)
        self.button_remove_file = QtWidgets.QPushButton(self.layoutWidget)
        self.button_remove_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_remove_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_remove_file.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove_file.setIcon(icon1)
        self.button_remove_file.setIconSize(QtCore.QSize(24, 24))
        self.button_remove_file.setFlat(True)
        self.button_remove_file.setObjectName("button_remove_file")
        self.gridLayout.addWidget(self.button_remove_file, 0, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(96, 10, 226, 18))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_state = QtWidgets.QLabel(self.layoutWidget1)
        self.label_state.setMinimumSize(QtCore.QSize(20, 0))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.label_state.setFont(font)
        self.label_state.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_state.setStyleSheet("color:rgb(143, 23, 119)")
        self.label_state.setObjectName("label_state")
        self.gridLayout_2.addWidget(self.label_state, 0, 1, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.frame)
        self.splitter.setGeometry(QtCore.QRect(5, 31, 315, 110))
        self.splitter.setMinimumSize(QtCore.QSize(0, 110))
        self.splitter.setStyleSheet("QSplitter {\n"
"border: None;\n"
"}")
        self.splitter.setLineWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(0)
        self.splitter.setObjectName("splitter")
        self.calctype = QtWidgets.QListWidget(self.splitter)
        self.calctype.setMinimumSize(QtCore.QSize(92, 110))
        self.calctype.setMaximumSize(QtCore.QSize(92, 110))
        self.calctype.setStyleSheet("QListWidget {\n"
"color: rgb(143, 23, 119);\n"
"\n"
"}\n"
"\n"
"QListWidget::item:hover{\n"
"/*background-color: rgb(143,23,119);*/\n"
"border: 1px solid rgb(143, 23, 119);\n"
"border-style: outset;\n"
"background-color: rgb(40,40,40);\n"
"padding-left:5px;\n"
"padding-right:-10px;\n"
"\n"
"}\n"
"\n"
"QListWidget::item:selected{\n"
"color: rgb(20,20,20);\n"
"background-color:rgb(98, 114, 164);\n"
"padding-left:10px;\n"
"padding-right:-10px;\n"
"\n"
"}\n"
"\n"
"QListWidget::item{\n"
"border: 1px solid rgb(20,20,20);\n"
"padding-right:-10px;\n"
"}\n"
"")
        self.calctype.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.calctype.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.calctype.setObjectName("calctype")
        item = QtWidgets.QListWidgetItem()
        self.calctype.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.calctype.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.calctype.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.calctype.addItem(item)
        self.calc_files = QtWidgets.QListWidget(self.splitter)
        self.calc_files.setMinimumSize(QtCore.QSize(225, 110))
        self.calc_files.setMaximumSize(QtCore.QSize(225, 110))
        self.calc_files.setStyleSheet("QListWidget {\n"
"color: rgb(220,220,220);\n"
"}\n"
"QListWidget::item:hover{\n"
"/*background-color: rgb(143,23,119);*/\n"
"\n"
"background-color: None;\n"
"\n"
"\n"
"}\n"
"\n"
"QListWidget::item{\n"
"border: 1px solid rgb(20,20,20);\n"
"}\n"
"")
        self.calc_files.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.calc_files.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.calc_files.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.calc_files.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.calc_files.setObjectName("calc_files")
        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 151))
        self.tabWidget.setStyleSheet("Qtabwidget {\n"
"margin: 0px, 0px,0px,0px;\n"
"\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.text_state_values = QtWidgets.QPlainTextEdit(self.tab)
        self.text_state_values.setMinimumSize(QtCore.QSize(0, 110))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.text_state_values.setFont(font)
        self.text_state_values.setReadOnly(True)
        self.text_state_values.setObjectName("text_state_values")
        self.verticalLayout_4.addWidget(self.text_state_values)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.list_frequencies = QtWidgets.QListWidget(self.tab_2)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.list_frequencies.setFont(font)
        self.list_frequencies.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.list_frequencies.setObjectName("list_frequencies")
        self.gridLayout_5.addWidget(self.list_frequencies, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.button_plot_frq = QtWidgets.QPushButton(self.tab_2)
        self.button_plot_frq.setObjectName("button_plot_frq")
        self.gridLayout_4.addWidget(self.button_plot_frq, 0, 0, 1, 1)
        self.button_frq_pymol = QtWidgets.QPushButton(self.tab_2)
        self.button_frq_pymol.setObjectName("button_frq_pymol")
        self.gridLayout_4.addWidget(self.button_frq_pymol, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 1, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(671, 151))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.text_relative_values = QtWidgets.QPlainTextEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.text_relative_values.setFont(font)
        self.text_relative_values.setReadOnly(True)
        self.text_relative_values.setObjectName("text_relative_values")
        self.verticalLayout_3.addWidget(self.text_relative_values)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout_3)
        AnalyseWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AnalyseWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(AnalyseWindow)

    def retranslateUi(self, AnalyseWindow):
        _translate = QtCore.QCoreApplication.translate
        AnalyseWindow.setWindowTitle(_translate("AnalyseWindow", "MainWindow"))
        self.button_remove_file.setShortcut(_translate("AnalyseWindow", "Ctrl+S"))
        self.label.setText(_translate("AnalyseWindow", "Included Calculation file(s) state"))
        self.label_state.setText(_translate("AnalyseWindow", "1"))
        __sortingEnabled = self.calctype.isSortingEnabled()
        self.calctype.setSortingEnabled(False)
        item = self.calctype.item(0)
        item.setText(_translate("AnalyseWindow", "Main:"))
        item = self.calctype.item(1)
        item.setText(_translate("AnalyseWindow", "Frequency:"))
        item = self.calctype.item(2)
        item.setText(_translate("AnalyseWindow", "Solvent:"))
        item = self.calctype.item(3)
        item.setText(_translate("AnalyseWindow", "Big basis:"))
        self.calctype.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AnalyseWindow", "Summary"))
        self.button_plot_frq.setText(_translate("AnalyseWindow", "Plot"))
        self.button_frq_pymol.setText(_translate("AnalyseWindow", "Pymol"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AnalyseWindow", "Frequencies"))
#import icons_rc
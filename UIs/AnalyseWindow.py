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
        AnalyseWindow.resize(739, 405)
        AnalyseWindow.setStyleSheet("")
        AnalyseWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(AnalyseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem, 0, 0, 1, 1)
        self.button_prev_state = QtWidgets.QPushButton(self.centralwidget)
        self.button_prev_state.setMinimumSize(QtCore.QSize(24, 24))
        self.button_prev_state.setMaximumSize(QtCore.QSize(24, 24))
        self.button_prev_state.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_prev_state.setIcon(icon)
        self.button_prev_state.setIconSize(QtCore.QSize(24, 24))
        self.button_prev_state.setFlat(True)
        self.button_prev_state.setObjectName("button_prev_state")
        self.gridLayout_6.addWidget(self.button_prev_state, 0, 1, 1, 1)
        self.button_next_state = QtWidgets.QPushButton(self.centralwidget)
        self.button_next_state.setMinimumSize(QtCore.QSize(24, 24))
        self.button_next_state.setMaximumSize(QtCore.QSize(24, 24))
        self.button_next_state.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_next_state.setIcon(icon1)
        self.button_next_state.setIconSize(QtCore.QSize(24, 24))
        self.button_next_state.setFlat(True)
        self.button_next_state.setObjectName("button_next_state")
        self.gridLayout_6.addWidget(self.button_next_state, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem1, 0, 3, 1, 1)
        self.unit_hartree = QtWidgets.QRadioButton(self.centralwidget)
        self.unit_hartree.setObjectName("unit_hartree")
        self.gridLayout_6.addWidget(self.unit_hartree, 0, 4, 1, 1)
        self.unit_kcal = QtWidgets.QRadioButton(self.centralwidget)
        self.unit_kcal.setObjectName("unit_kcal")
        self.gridLayout_6.addWidget(self.unit_kcal, 0, 5, 1, 1)
        self.unit_kj = QtWidgets.QRadioButton(self.centralwidget)
        self.unit_kj.setObjectName("unit_kj")
        self.gridLayout_6.addWidget(self.unit_kj, 0, 6, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem2, 0, 7, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_6)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_set_file.setIcon(icon2)
        self.button_set_file.setIconSize(QtCore.QSize(24, 24))
        self.button_set_file.setFlat(True)
        self.button_set_file.setObjectName("button_set_file")
        self.gridLayout.addWidget(self.button_set_file, 0, 0, 1, 1)
        self.button_remove_file = QtWidgets.QPushButton(self.layoutWidget)
        self.button_remove_file.setMinimumSize(QtCore.QSize(24, 24))
        self.button_remove_file.setMaximumSize(QtCore.QSize(24, 24))
        self.button_remove_file.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/24x24/resources/icons/arrow-minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_remove_file.setIcon(icon3)
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
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setMinimumSize(QtCore.QSize(671, 151))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_relative_values = QtWidgets.QPlainTextEdit(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.text_relative_values.setFont(font)
        self.text_relative_values.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.text_relative_values.setReadOnly(True)
        self.text_relative_values.setObjectName("text_relative_values")
        self.verticalLayout_2.addWidget(self.text_relative_values)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setVerticalSpacing(0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem3, 0, 0, 1, 1)
        self.checkBox_main = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_main.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_main.setCheckable(True)
        self.checkBox_main.setObjectName("checkBox_main")
        self.gridLayout_7.addWidget(self.checkBox_main, 0, 1, 1, 1)
        self.checkBox_big = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_big.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_big.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBox_big.setCheckable(True)
        self.checkBox_big.setObjectName("checkBox_big")
        self.gridLayout_7.addWidget(self.checkBox_big, 0, 2, 1, 1)
        self.checkBox_solvation = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_solvation.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_solvation.setCheckable(True)
        self.checkBox_solvation.setObjectName("checkBox_solvation")
        self.gridLayout_7.addWidget(self.checkBox_solvation, 0, 3, 1, 1)
        self.checkBox_gibbs = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_gibbs.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_gibbs.setCheckable(True)
        self.checkBox_gibbs.setObjectName("checkBox_gibbs")
        self.gridLayout_7.addWidget(self.checkBox_gibbs, 0, 4, 1, 1)
        self.checkBox_enthalpy = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_enthalpy.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_enthalpy.setCheckable(True)
        self.checkBox_enthalpy.setObjectName("checkBox_enthalpy")
        self.gridLayout_7.addWidget(self.checkBox_enthalpy, 0, 5, 1, 1)
        self.checkBox_energy = QtWidgets.QCheckBox(self.frame_2)
        self.checkBox_energy.setMinimumSize(QtCore.QSize(90, 0))
        self.checkBox_energy.setCheckable(True)
        self.checkBox_energy.setObjectName("checkBox_energy")
        self.gridLayout_7.addWidget(self.checkBox_energy, 0, 6, 1, 1)
        self.button_plot_energies = QtWidgets.QPushButton(self.frame_2)
        self.button_plot_energies.setObjectName("button_plot_energies")
        self.gridLayout_7.addWidget(self.button_plot_energies, 0, 7, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem4, 0, 8, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_7)
        self.gridLayout_3.addWidget(self.frame_2, 1, 0, 1, 3)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setMaximumSize(QtCore.QSize(16777215, 151))
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.text_state_values = QtWidgets.QPlainTextEdit(self.tab)
        self.text_state_values.setMinimumSize(QtCore.QSize(0, 115))
        font = QtGui.QFont()
        font.setFamily("Courier")
        self.text_state_values.setFont(font)
        self.text_state_values.setReadOnly(True)
        self.text_state_values.setObjectName("text_state_values")
        self.verticalLayout_4.addWidget(self.text_state_values)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
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
        self.verticalLayout_3.addLayout(self.gridLayout_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setVerticalSpacing(0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_2 = QtWidgets.QLabel(self.tab_3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_8.addWidget(self.label_2, 0, 0, 1, 1)
        self.lcdNumber_scale = QtWidgets.QLCDNumber(self.tab_3)
        self.lcdNumber_scale.setDigitCount(3)
        self.lcdNumber_scale.setProperty("value", 50.0)
        self.lcdNumber_scale.setProperty("intValue", 50)
        self.lcdNumber_scale.setObjectName("lcdNumber_scale")
        self.gridLayout_8.addWidget(self.lcdNumber_scale, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.tab_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_8.addWidget(self.label_3, 0, 2, 1, 1)
        self.horizontalSlider_scale = QtWidgets.QSlider(self.tab_3)
        self.horizontalSlider_scale.setStyleSheet("")
        self.horizontalSlider_scale.setMaximum(200)
        self.horizontalSlider_scale.setSingleStep(1)
        self.horizontalSlider_scale.setProperty("value", 50)
        self.horizontalSlider_scale.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_scale.setObjectName("horizontalSlider_scale")
        self.gridLayout_8.addWidget(self.horizontalSlider_scale, 1, 0, 1, 3)
        self.gridLayout_9.addLayout(self.gridLayout_8, 0, 0, 2, 1)
        self.checkBox_view_pymol = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_view_pymol.setChecked(True)
        self.checkBox_view_pymol.setObjectName("checkBox_view_pymol")
        self.gridLayout_9.addWidget(self.checkBox_view_pymol, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem5, 0, 2, 1, 1)
        self.checkBox_write_xyz = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_write_xyz.setChecked(False)
        self.checkBox_write_xyz.setObjectName("checkBox_write_xyz")
        self.gridLayout_9.addWidget(self.checkBox_write_xyz, 1, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem6, 1, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_9)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        AnalyseWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AnalyseWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AnalyseWindow)

    def retranslateUi(self, AnalyseWindow):
        _translate = QtCore.QCoreApplication.translate
        AnalyseWindow.setWindowTitle(_translate("AnalyseWindow", "MainWindow"))
        self.unit_hartree.setText(_translate("AnalyseWindow", "Hartree"))
        self.unit_kcal.setText(_translate("AnalyseWindow", "kcal/mol"))
        self.unit_kj.setText(_translate("AnalyseWindow", "kJ/mol"))
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
        self.checkBox_main.setText(_translate("AnalyseWindow", "Main"))
        self.checkBox_big.setText(_translate("AnalyseWindow", "Big"))
        self.checkBox_solvation.setText(_translate("AnalyseWindow", "Solvation"))
        self.checkBox_gibbs.setText(_translate("AnalyseWindow", "Gibbs"))
        self.checkBox_enthalpy.setText(_translate("AnalyseWindow", "Enthalpy"))
        self.checkBox_energy.setText(_translate("AnalyseWindow", "Energy"))
        self.button_plot_energies.setText(_translate("AnalyseWindow", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AnalyseWindow", "Summary"))
        self.button_plot_frq.setText(_translate("AnalyseWindow", "Plot"))
        self.button_frq_pymol.setText(_translate("AnalyseWindow", "Animate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AnalyseWindow", "Frequencies"))
        self.label_2.setText(_translate("AnalyseWindow", "Scale"))
        self.label_3.setText(_translate("AnalyseWindow", "%"))
        self.checkBox_view_pymol.setText(_translate("AnalyseWindow", "Open in Pymol"))
        self.checkBox_write_xyz.setText(_translate("AnalyseWindow", "Write xyz files"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("AnalyseWindow", "Animation settings"))
#import icons_rc

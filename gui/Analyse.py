# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'analyse.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_analyse(object):
    def setupUi(self, analyse):
        analyse.setObjectName("analyse")
        analyse.resize(643, 600)
        self.centralwidget = QtWidgets.QWidget(analyse)
        self.centralwidget.setObjectName("centralwidget")
        self.calcEnergies = QtWidgets.QPushButton(self.centralwidget)
        self.calcEnergies.setGeometry(QtCore.QRect(400, 260, 89, 25))
        self.calcEnergies.setObjectName("calcEnergies")
        self.geomConv = QtWidgets.QPushButton(self.centralwidget)
        self.geomConv.setGeometry(QtCore.QRect(400, 180, 89, 25))
        self.geomConv.setObjectName("geomConv")
        self.addState = QtWidgets.QPushButton(self.centralwidget)
        self.addState.setGeometry(QtCore.QRect(20, 70, 21, 21))
        icon = QtGui.QIcon.fromTheme("Arrow")
        self.addState.setIcon(icon)
        self.addState.setObjectName("addState")
        self.uploadState = QtWidgets.QPushButton(self.centralwidget)
        self.uploadState.setGeometry(QtCore.QRect(60, 260, 101, 25))
        self.uploadState.setObjectName("uploadState")
        self.freqCorr = QtWidgets.QCheckBox(self.centralwidget)
        self.freqCorr.setGeometry(QtCore.QRect(400, 50, 92, 23))
        self.freqCorr.setObjectName("freqCorr")
        self.energyTable = QtWidgets.QTableWidget(self.centralwidget)
        self.energyTable.setGeometry(QtCore.QRect(30, 360, 590, 161))
        self.energyTable.setObjectName("energyTable")
        self.energyTable.setColumnCount(5)
        self.energyTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.energyTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.energyTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.energyTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.energyTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.energyTable.setHorizontalHeaderItem(4, item)
        self.bbsCorr = QtWidgets.QCheckBox(self.centralwidget)
        self.bbsCorr.setGeometry(QtCore.QRect(400, 90, 92, 23))
        self.bbsCorr.setObjectName("bbsCorr")
        self.moveStateDown = QtWidgets.QPushButton(self.centralwidget)
        self.moveStateDown.setGeometry(QtCore.QRect(20, 200, 21, 21))
        self.moveStateDown.setObjectName("moveStateDown")
        self.delState = QtWidgets.QPushButton(self.centralwidget)
        self.delState.setGeometry(QtCore.QRect(20, 110, 21, 21))
        icon = QtGui.QIcon.fromTheme("Arrow")
        self.delState.setIcon(icon)
        self.delState.setObjectName("delState")
        self.statesLabel = QtWidgets.QLabel(self.centralwidget)
        self.statesLabel.setGeometry(QtCore.QRect(140, 20, 71, 17))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.statesLabel.setFont(font)
        self.statesLabel.setObjectName("statesLabel")
        self.deleteState = QtWidgets.QPushButton(self.centralwidget)
        self.deleteState.setGeometry(QtCore.QRect(200, 260, 101, 25))
        self.deleteState.setObjectName("deleteState")
        self.moveStateUp = QtWidgets.QPushButton(self.centralwidget)
        self.moveStateUp.setGeometry(QtCore.QRect(20, 160, 21, 21))
        icon = QtGui.QIcon.fromTheme("Arrow")
        self.moveStateUp.setIcon(icon)
        self.moveStateUp.setObjectName("moveStateUp")
        self.normalMode = QtWidgets.QPushButton(self.centralwidget)
        self.normalMode.setGeometry(QtCore.QRect(400, 220, 89, 25))
        self.normalMode.setObjectName("normalMode")
        self.correctionsLabel = QtWidgets.QLabel(self.centralwidget)
        self.correctionsLabel.setGeometry(QtCore.QRect(380, 20, 131, 17))
        font = QtGui.QFont()
        font.setPointSize(17)
        self.correctionsLabel.setFont(font)
        self.correctionsLabel.setObjectName("correctionsLabel")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(280, 540, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.stateTree = QtWidgets.QTreeView(self.centralwidget)
        self.stateTree.setGeometry(QtCore.QRect(50, 50, 256, 192))
        self.stateTree.setObjectName("stateTree")
        self.solvCorr = QtWidgets.QCheckBox(self.centralwidget)
        self.solvCorr.setGeometry(QtCore.QRect(400, 130, 92, 23))
        self.solvCorr.setObjectName("solvCorr")
        self.tableInfo = QtWidgets.QComboBox(self.centralwidget)
        self.tableInfo.setGeometry(QtCore.QRect(30, 540, 171, 25))
        self.tableInfo.setObjectName("tableInfo")
        self.tableInfo.addItem("")
        self.tableInfo.addItem("")
        self.tableInfo.addItem("")
        analyse.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(analyse)
        self.statusbar.setObjectName("statusbar")
        analyse.setStatusBar(self.statusbar)

        self.retranslateUi(analyse)
        QtCore.QMetaObject.connectSlotsByName(analyse)

    def retranslateUi(self, analyse):
        _translate = QtCore.QCoreApplication.translate
        analyse.setWindowTitle(_translate("analyse", "MainWindow"))
        self.calcEnergies.setText(_translate("analyse", "Calculate"))
        self.geomConv.setText(_translate("analyse", "Geom. Conv."))
        self.addState.setText(_translate("analyse", "+"))
        self.uploadState.setText(_translate("analyse", "Load file"))
        self.freqCorr.setText(_translate("analyse", "Frequency"))
        item = self.energyTable.horizontalHeaderItem(0)
        item.setText(_translate("analyse", "States"))
        item = self.energyTable.horizontalHeaderItem(1)
        item.setText(_translate("analyse", "dE"))
        item = self.energyTable.horizontalHeaderItem(2)
        item.setText(_translate("analyse", "solv"))
        item = self.energyTable.horizontalHeaderItem(3)
        item.setText(_translate("analyse", " dG"))
        item = self.energyTable.horizontalHeaderItem(4)
        item.setText(_translate("analyse", "Hi"))
        self.bbsCorr.setText(_translate("analyse", "Big Basis"))
        self.moveStateDown.setText(_translate("analyse", "D"))
        self.delState.setText(_translate("analyse", "-"))
        self.statesLabel.setText(_translate("analyse", "States"))
        self.deleteState.setText(_translate("analyse", "Delete file"))
        self.moveStateUp.setText(_translate("analyse", "U"))
        self.normalMode.setText(_translate("analyse", "Norm. Mode"))
        self.correctionsLabel.setText(_translate("analyse", "Corrections"))
        self.solvCorr.setText(_translate("analyse", "Solvation"))
        self.tableInfo.setItemText(0, _translate("analyse", "Energies"))
        self.tableInfo.setItemText(1, _translate("analyse", "Absolute Energies"))
        self.tableInfo.setItemText(2, _translate("analyse", "Job Details"))

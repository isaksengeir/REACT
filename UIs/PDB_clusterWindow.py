# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PDB_clusterWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ClusterPDB(object):
    def setupUi(self, ClusterPDB):
        ClusterPDB.setObjectName("ClusterPDB")
        ClusterPDB.resize(618, 330)
        self.centralwidget = QtWidgets.QWidget(ClusterPDB)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.select = QtWidgets.QWidget()
        self.select.setObjectName("select")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.select)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_pdb_file = QtWidgets.QLabel(self.select)
        self.label_pdb_file.setMaximumSize(QtCore.QSize(61, 32))
        self.label_pdb_file.setObjectName("label_pdb_file")
        self.gridLayout.addWidget(self.label_pdb_file, 0, 0, 1, 1)
        self.lineEdit_pdb_file = QtWidgets.QLineEdit(self.select)
        self.lineEdit_pdb_file.setDragEnabled(True)
        self.lineEdit_pdb_file.setReadOnly(True)
        self.lineEdit_pdb_file.setObjectName("lineEdit_pdb_file")
        self.gridLayout.addWidget(self.lineEdit_pdb_file, 0, 1, 1, 1)
        self.button_load_pdb = QtWidgets.QPushButton(self.select)
        self.button_load_pdb.setMaximumSize(QtCore.QSize(71, 32))
        self.button_load_pdb.setObjectName("button_load_pdb")
        self.gridLayout.addWidget(self.button_load_pdb, 0, 2, 1, 1)
        self.button_pdb_from_table = QtWidgets.QPushButton(self.select)
        self.button_pdb_from_table.setMaximumSize(QtCore.QSize(181, 32))
        self.button_pdb_from_table.setObjectName("button_pdb_from_table")
        self.gridLayout.addWidget(self.button_pdb_from_table, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.select)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.button_set_cluster_center = QtWidgets.QPushButton(self.select)
        self.button_set_cluster_center.setObjectName("button_set_cluster_center")
        self.gridLayout_2.addWidget(self.button_set_cluster_center, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.select)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_inclusion_radius = QtWidgets.QLineEdit(self.select)
        self.lineEdit_inclusion_radius.setMaximumSize(QtCore.QSize(30, 16777215))
        self.lineEdit_inclusion_radius.setDragEnabled(True)
        self.lineEdit_inclusion_radius.setReadOnly(True)
        self.lineEdit_inclusion_radius.setObjectName("lineEdit_inclusion_radius")
        self.gridLayout_3.addWidget(self.lineEdit_inclusion_radius, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.select)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)
        self.slider_inclusion_size = QtWidgets.QSlider(self.select)
        self.slider_inclusion_size.setMaximum(20)
        self.slider_inclusion_size.setProperty("value", 5)
        self.slider_inclusion_size.setOrientation(QtCore.Qt.Horizontal)
        self.slider_inclusion_size.setObjectName("slider_inclusion_size")
        self.gridLayout_3.addWidget(self.slider_inclusion_size, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.select_byres = QtWidgets.QCheckBox(self.select)
        self.select_byres.setChecked(True)
        self.select_byres.setObjectName("select_byres")
        self.gridLayout_6.addWidget(self.select_byres, 0, 0, 1, 1)
        self.include_solvent = QtWidgets.QCheckBox(self.select)
        self.include_solvent.setChecked(True)
        self.include_solvent.setObjectName("include_solvent")
        self.gridLayout_6.addWidget(self.include_solvent, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_6)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem, 0, 0, 1, 1)
        self.button_create_model = QtWidgets.QPushButton(self.select)
        self.button_create_model.setMinimumSize(QtCore.QSize(150, 0))
        self.button_create_model.setObjectName("button_create_model")
        self.gridLayout_5.addWidget(self.button_create_model, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 0, 3, 1, 1)
        self.button_update_manual_selection = QtWidgets.QPushButton(self.select)
        self.button_update_manual_selection.setObjectName("button_update_manual_selection")
        self.gridLayout_5.addWidget(self.button_update_manual_selection, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_5)
        self.tabWidget.addTab(self.select, "")
        self.validate = QtWidgets.QWidget()
        self.validate.setObjectName("validate")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.validate)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_5 = QtWidgets.QLabel(self.validate)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 0, 0, 1, 1)
        self.nterm_capping = QtWidgets.QComboBox(self.validate)
        self.nterm_capping.setMinimumSize(QtCore.QSize(0, 0))
        self.nterm_capping.setObjectName("nterm_capping")
        self.nterm_capping.addItem("")
        self.nterm_capping.addItem("")
        self.nterm_capping.addItem("")
        self.gridLayout_7.addWidget(self.nterm_capping, 0, 1, 1, 1)
        self.button_auto_nterm = QtWidgets.QPushButton(self.validate)
        self.button_auto_nterm.setObjectName("button_auto_nterm")
        self.gridLayout_7.addWidget(self.button_auto_nterm, 0, 2, 2, 1)
        self.label_6 = QtWidgets.QLabel(self.validate)
        self.label_6.setObjectName("label_6")
        self.gridLayout_7.addWidget(self.label_6, 1, 0, 1, 1)
        self.cterm_capping = QtWidgets.QComboBox(self.validate)
        self.cterm_capping.setObjectName("cterm_capping")
        self.cterm_capping.addItem("")
        self.cterm_capping.addItem("")
        self.cterm_capping.addItem("")
        self.gridLayout_7.addWidget(self.cterm_capping, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_7)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem2, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.validate)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem3, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_9)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.button_delete_selected = QtWidgets.QPushButton(self.validate)
        self.button_delete_selected.setObjectName("button_delete_selected")
        self.gridLayout_10.addWidget(self.button_delete_selected, 0, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_10.addItem(spacerItem4, 0, 2, 1, 1)
        self.groups_to_add = QtWidgets.QComboBox(self.validate)
        self.groups_to_add.setMinimumSize(QtCore.QSize(150, 0))
        self.groups_to_add.setObjectName("groups_to_add")
        self.groups_to_add.addItem("")
        self.groups_to_add.addItem("")
        self.groups_to_add.addItem("")
        self.groups_to_add.addItem("")
        self.gridLayout_10.addWidget(self.groups_to_add, 0, 0, 1, 1)
        self.button_add_group = QtWidgets.QPushButton(self.validate)
        self.button_add_group.setMinimumSize(QtCore.QSize(150, 0))
        self.button_add_group.setObjectName("button_add_group")
        self.gridLayout_10.addWidget(self.button_add_group, 0, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_10)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.button_finalize = QtWidgets.QPushButton(self.validate)
        self.button_finalize.setObjectName("button_finalize")
        self.gridLayout_8.addWidget(self.button_finalize, 0, 0, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_8)
        self.tabWidget.addTab(self.validate, "")
        self.finalize = QtWidgets.QWidget()
        self.finalize.setObjectName("finalize")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.finalize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem5, 0, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.finalize)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_11.addWidget(self.label_8, 0, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_11.addItem(spacerItem6, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_11)
        self.list_model_summary = QtWidgets.QListWidget(self.finalize)
        self.list_model_summary.setObjectName("list_model_summary")
        self.verticalLayout_4.addWidget(self.list_model_summary)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem7, 0, 0, 1, 1)
        self.copy_to_project = QtWidgets.QCheckBox(self.finalize)
        self.copy_to_project.setMinimumSize(QtCore.QSize(200, 0))
        self.copy_to_project.setChecked(True)
        self.copy_to_project.setObjectName("copy_to_project")
        self.gridLayout_12.addWidget(self.copy_to_project, 0, 1, 1, 1)
        self.button_export_model = QtWidgets.QPushButton(self.finalize)
        self.button_export_model.setObjectName("button_export_model")
        self.gridLayout_12.addWidget(self.button_export_model, 0, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_12)
        self.tabWidget.addTab(self.finalize, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem8, 0, 0, 1, 1)
        self.lineEdit_atoms_in_model = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_atoms_in_model.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_atoms_in_model.setDragEnabled(True)
        self.lineEdit_atoms_in_model.setReadOnly(True)
        self.lineEdit_atoms_in_model.setObjectName("lineEdit_atoms_in_model")
        self.gridLayout_4.addWidget(self.lineEdit_atoms_in_model, 0, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_4)
        ClusterPDB.setCentralWidget(self.centralwidget)

        self.retranslateUi(ClusterPDB)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ClusterPDB)

    def retranslateUi(self, ClusterPDB):
        _translate = QtCore.QCoreApplication.translate
        ClusterPDB.setWindowTitle(_translate("ClusterPDB", "MainWindow"))
        self.label_pdb_file.setText(_translate("ClusterPDB", "PDB file:"))
        self.button_load_pdb.setText(_translate("ClusterPDB", "Load"))
        self.button_pdb_from_table.setText(_translate("ClusterPDB", "Import from project table"))
        self.label.setText(_translate("ClusterPDB", "Select central molecule/ligand/reactant to build model around"))
        self.button_set_cluster_center.setText(_translate("ClusterPDB", "Set central selection"))
        self.label_2.setText(_translate("ClusterPDB", "Include surrounding residues within"))
        self.label_3.setText(_translate("ClusterPDB", "Å"))
        self.select_byres.setText(_translate("ClusterPDB", "Select by residue (recomended)"))
        self.include_solvent.setText(_translate("ClusterPDB", "Include solvent"))
        self.button_create_model.setText(_translate("ClusterPDB", "Create model"))
        self.button_update_manual_selection.setText(_translate("ClusterPDB", "Update manual selection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.select), _translate("ClusterPDB", "Select"))
        self.label_5.setText(_translate("ClusterPDB", "N-terminal capping:"))
        self.nterm_capping.setItemText(0, _translate("ClusterPDB", "ace"))
        self.nterm_capping.setItemText(1, _translate("ClusterPDB", "methyl"))
        self.nterm_capping.setItemText(2, _translate("ClusterPDB", "H"))
        self.button_auto_nterm.setText(_translate("ClusterPDB", "Auto add"))
        self.label_6.setText(_translate("ClusterPDB", "C-terminal capping:"))
        self.cterm_capping.setItemText(0, _translate("ClusterPDB", "nme"))
        self.cterm_capping.setItemText(1, _translate("ClusterPDB", "methyl"))
        self.cterm_capping.setItemText(2, _translate("ClusterPDB", "H"))
        self.label_7.setText(_translate("ClusterPDB", "Manual edits to selected atom(s):"))
        self.button_delete_selected.setText(_translate("ClusterPDB", "Delete selected"))
        self.groups_to_add.setItemText(0, _translate("ClusterPDB", "ace"))
        self.groups_to_add.setItemText(1, _translate("ClusterPDB", "nme"))
        self.groups_to_add.setItemText(2, _translate("ClusterPDB", "methyl"))
        self.groups_to_add.setItemText(3, _translate("ClusterPDB", "H"))
        self.button_add_group.setText(_translate("ClusterPDB", "Add"))
        self.button_finalize.setText(_translate("ClusterPDB", "Finalize"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.validate), _translate("ClusterPDB", "Validate"))
        self.label_8.setText(_translate("ClusterPDB", "Summary"))
        self.copy_to_project.setText(_translate("ClusterPDB", "Copy to project table"))
        self.button_export_model.setText(_translate("ClusterPDB", "Export model"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.finalize), _translate("ClusterPDB", "Finalize"))
        self.label_4.setText(_translate("ClusterPDB", "Atoms in model:"))

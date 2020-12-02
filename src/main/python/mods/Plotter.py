from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from UIs.AnyPlot import Ui_AnyPlotter


class Plotter(QtWidgets.QMainWindow, Ui_AnyPlotter):
    def __init__(self, parent):
        super(Plotter, self).__init__(parent, Qt.WindowStaysOnTopHint)

        self.ui = Ui_AnyPlotter()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle("REACT - AnyPlot")

        self.ui.tableWidget.cellDoubleClicked.connect(self.set_colour)
        self.ui.button_plot.clicked.connect(self.make_plot)

        # Insert first colour menu
        #self.add_color_menu(1)

    def set_colour(self):
        """

        :return:
        """
        # row column
        row = self.ui.tableWidget.currentRow()
        if row != 0:
            return None

        column = self.ui.tableWidget.currentColumn()

        #Open colour selector:
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            # color name in hex:
            print(color.name())
            self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem())
            self.ui.tableWidget.item(row, column).setBackground(QColor(color))


    def make_plot(self):
        """

        :return:
        """
        colors = list()
        titles = list()
        plots = list()
        for column in range(self.ui.tableWidget.columnCount()):
            energies = list()
            for row in range(self.ui.tableWidget.rowCount()):
                if row == 0:
                    colors.append(self.ui.tableWidget.item(row, column))
                elif row == 1:
                    titles.append(self.ui.tableWidget.item(row, column))
                else:
                    value = self.ui.tableWidget.item(row, column)

                    if self.is_number(value):
                        energies.append(float)
                    else:
                        pass
            plots.append(energies)

        print(colors, titles, plots)

    def is_number(self, s):
        """
        :param s: string or anything
        :return: True/False for s is float
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

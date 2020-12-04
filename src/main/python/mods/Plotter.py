from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from UIs.AnyPlot import Ui_AnyPlotter
from mods.ReactPlot import PlotEnergyDiagram
from mods.common_functions import random_color, select_color, is_number


class Plotter(QtWidgets.QMainWindow, Ui_AnyPlotter):
    def __init__(self, parent):
        super(Plotter, self).__init__(parent)
        # find better alternative to , Qt.WindowStaysOnTopHint
        self.ui = Ui_AnyPlotter()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowTitle("REACT - AnyPlot")

        self.ui.tableWidget.cellDoubleClicked.connect(self.double_click_color)
        self.ui.button_plot.clicked.connect(self.make_plot)

        self.ui.button_set_rows_columns.clicked.connect(self.update_table)

        # Set a random color for the first column
        self.set_colour(0, random_color())
        self.set_title(0, "Title")

    def update_table(self):
        """
        :return:
        """
        # -2 because the 2 first entries are reserved for color and title
        rows_old = int(self.ui.tableWidget.rowCount() - 2)
        rows_new = int(self.ui.spinBox_rows.value())

        columns_old = int(self.ui.tableWidget.columnCount())
        columns_new = int(self.ui.spinBox_columns.value())

        # Add or delete rows?
        if rows_new > rows_old:
            self.add_rows(rows_old+2, rows_new)
        elif rows_new < rows_old:
            self.delete_rows(rows_old+2, rows_new)
        else:
            pass

        # Add or delete columns?
        if columns_new > columns_old:
            self.add_columns(columns_old, columns_new)
        elif columns_new < columns_old:
            self.delete_columns(columns_old, columns_new)
        else:
            pass

    def add_columns(self, insert_index, columns_total):
        """
        :param insert_index:
        :param columns_total:
        :return:
        """
        while int(self.ui.tableWidget.columnCount()) < columns_total:
            self.ui.tableWidget.insertColumn(insert_index)
            self.set_colour(insert_index, random_color())
            self.set_title(insert_index, "Title")
            insert_index += 1

    def delete_columns(self, delete_index, columns_total):
        """
        :param delete_index:
        :param columns_total:
        :return:
        """
        while int(self.ui.tableWidget.columnCount()) > columns_total:
            self.ui.tableWidget.removeColumn(delete_index)
            delete_index -= 1

    def add_rows(self, insert_index, rows_total):
        """
        :param insert_index: Where to insert new row(s)
        :param rows_total: Final number of rows in table
        """
        while int(self.ui.tableWidget.rowCount() - 2) < rows_total:
            self.ui.tableWidget.insertRow(insert_index)
            insert_index += 1

    def delete_rows(self, delete_index, rows_total):
        """
        :param delete_index: Index to delete
        :param rows_total: Final number of rows in table
        """

        while int(self.ui.tableWidget.rowCount() - 2) > rows_total:
            self.ui.tableWidget.removeRow(delete_index)
            delete_index -= 1

    def double_click_color(self):
        """
        If color row is double-clicked, open color selector, and color row.
        :return:
        """
        # row column
        row = self.ui.tableWidget.currentRow()
        if row != 0:
            return None

        column = self.ui.tableWidget.currentColumn()
        color = select_color()

        self.set_colour(column, color)

    def set_colour(self, column=None, color=None):
        """
        Sets color of row=0 for column.
        :return:
        """
        row = 0

        # color name in hex:
        self.ui.tableWidget.setItem(row, column, QtWidgets.QTableWidgetItem())
        self.ui.tableWidget.item(row, column).setBackground(QColor(color))

    def set_title(self, column=0, title="Title"):
        """
        Set title for plot in column
        :param column:
        :param title:
        """
        self.ui.tableWidget.setItem(1, column, QtWidgets.QTableWidgetItem("Title"))

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
                print(self.ui.tableWidget.item(row, column).text())
                if row == 0:
                    color = self.ui.tableWidget.item(row, column).background().color().name()
                    colors.append(color)
                elif row == 1:
                    print(self.ui.tableWidget.item(row, column))
                    titles.append(self.ui.tableWidget.item(row, column).text())
                else:
                    value = self.ui.tableWidget.item(row, column).text()

                    if is_number(value):
                        energies.append(float(value))
                    else:
                        pass
            plots.append(energies)

        print(colors, titles, plots)

        PlotEnergyDiagram(ene_array=plots, legends=titles, line_colors=colors, y_title="Relative Energy",
                          plot_legend=True)



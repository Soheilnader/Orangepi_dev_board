import os
import sys
from i2c import *

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"main.ui"
        uic.loadUi(ts_ui, self)

        self.button_read.clicked.connect(self.button_read_clicked)
        self.button_write.clicked.connect(self.button_write_clicked)
        self.button_exit.clicked.connect(self.exit)

        self.table_data.setRowCount(128)
        self.table_data.setColumnCount(4)
        self.data = ['Unknown' for i in range(128)]
        row = 0
        for i in range(128):

            self.table_data.setItem(row, 0, QTableWidgetItem(str(hex(i))))
            self.table_data.setItem(row, 1, QTableWidgetItem(str(self.data[i])))
            self.table_data.setItem(row, 1, QTableWidgetItem(str(self.data[i])))
            self.table_data.setItem(row, 3, QTableWidgetItem(str(self.data[i])))

            row+=1

        self.show()

    def button_read_clicked(self):
        print("read")
        self.data = read_eeprom(0x50, 0, 128)
        row = 0
        for i in range(128):

            self.table_data.setItem(row, 0, QTableWidgetItem(str(hex(i))))
            self.table_data.setItem(row, 1, QTableWidgetItem(str(self.data[i])))
            self.table_data.setItem(row, 2, QTableWidgetItem(str(hex(self.data[i]))))
            self.table_data.setItem(row, 3, QTableWidgetItem(str(chr(self.data[i]))))
            row += 1
    def button_write_clicked(self):
        print("write")
        for i in range(128):
            if int(self.table_data.item(i, 1).text()) == self.data[i]:
                pass
            else:
                print("block %d changed to %d" %(i, int(self.table_data.item(i, 1).text())))
                self.data[i] =  int(self.table_data.item(i, 1).text())
                write_eeprom(0x50, i, int(self.table_data.item(i, 1).text()))



    def bool_to_01(self, bool_input):
        if bool_input == True:
            return 1
        else:
            return 0

    def str_2_char(self, string):
        if len(string) == 2:
            return string
        else:
            return "0" + string

    def exit(self):
        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()

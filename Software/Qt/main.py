import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"D:\Work\Uni\Project\Software\Qt\main.ui"
        uic.loadUi(ts_ui, self)
        self.button_relay1.clicked.connect(self.button_relay1_func)
        self.button_relay2.clicked.connect(self.button_relay2_func)
        self.button_relay3.clicked.connect(self.button_relay3_func)
        self.button_exit.clicked.connect(self.exit)


        self.dial_pwm.valueChanged.connect(self.dial_pwm_change)
        self.show()

    def dial_pwm_change(self):
        print("Dial value = %i" % (self.dial_pwm.value()*10))
        self.lcd_pwm.display(self.dial_pwm.value()*10)

    def button_relay1_func(self):
        print(self.button_relay1.isChecked())

    def button_relay2_func(self):
        print(self.button_relay2.isChecked())

    def button_relay3_func(self):
        print(self.button_relay3.isChecked())

    def exit(self):
        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()

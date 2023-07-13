import os
import sys
import time
from random import randint

from pyA20.gpio import gpio
from pyA20.gpio import port
from pyA20.gpio import connector

from orangepwm import *

from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

import camera
#import weather

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        ts_ui = r"main.ui"
        uic.loadUi(ts_ui, self)
        self.setFixedSize(1024, 600)

        gpio.init() #Initialize module. Always called first
        self.pwm = OrangePwm(100, port.PA7)
        self.pwm.start(0)

        gpio.setcfg(port.PA10, gpio.OUTPUT)  #Configure LED1 as output
        gpio.setcfg(port.PA9, gpio.OUTPUT)
        gpio.setcfg(port.PA21, gpio.OUTPUT)
        
        self.button_lamp1.clicked.connect(self.button_lamp1_clicked)
        self.button_lamp2.clicked.connect(self.button_lamp2_clicked)
        self.button_fan.clicked.connect(self.button_fan_clicked)
        self.button_exit.clicked.connect(self.exit)


        # creating a timer object
        timer = QTimer(self)
        # adding action to timer
        timer.timeout.connect(self.clock)
        # update the timer every second
        timer.start(1000)

        self.x = list(range(100))  # 100 time points
        self.y = [0 for _ in range(100)]  # 100 data points

        #self.graphWidget.setBackground('b')

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graphWidget.plot(self.x, self.y, pen=pen)
        # ... init continued ...
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # self.frame.setStyleSheet("background-image: url(pic/background/main.jpg)")
        self.button_lamp1.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/lamp1_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/lamp1_on.png);}
    """)

        self.button_lamp2.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/lamp2_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/lamp2_on.png);}
        """)

        self.button_fan.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/fan_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/fan_on.png);}
        """)

        self.button_heater.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/heater_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/heater_on.png);}
        """)

        self.button_cooler.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/cooler_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/cooler_on.png);}
        """)


        self.button_exit.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/exit_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/exit_on.png);}
    """)

        self.button_cam.setStyleSheet("""
            QPushButton {border-image: url(pic/buttons/cam_off.png);}
            QPushButton:hover {border-image: url(pic/buttons/cam_on.png);}
        """)

        self.slider_fan.setStyleSheet("""
        QSlider::groove:vertical {
    background: white;
    position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */
    left: 4px; right: 4px;
}

QSlider::handle:vertical {
    height: 40px;
    background: white;
    margin: 0 -4px; /* expand outside the groove */
}

QSlider::add-page:vertical {
    background: white;
}

QSlider::sub-page:vertical {
    background: grey;
}
        """)

        self.progress_adc.setStyleSheet("""
 QProgressBar::chunk {
     background-color: #ef1d1e;
 }
        """)

        back_img = QPixmap(r"pic/background/main.jpg")
        self.label.setPixmap(back_img)

        thermo_img = QPixmap(r"pic/background/thermo.png")
        self.label_thermo.setPixmap(thermo_img)

        usc_img = QPixmap(r"pic/background/usc.png")
        self.img_usc.setPixmap(usc_img)

        self.button_lamp1.clicked.connect(self.button_lamp1_clicked)
        self.button_lamp2.clicked.connect(self.button_lamp2_clicked)
        self.button_fan.clicked.connect(self.button_fan_clicked)
        self.button_cam.clicked.connect(self.button_cam_clicked)
        self.button_heater.clicked.connect(self.button_heater_clicked)
        self.button_cooler.clicked.connect(self.button_cooler_clicked)
        self.slider_fan.valueChanged.connect(self.slider_fan_change)

        self.button_exit.clicked.connect(self.exit)

        self.show()

    def button_lamp1_clicked(self):
        print(self.button_lamp1.isChecked())

        if (self.button_lamp1.isChecked()):
            self.button_lamp1.setStyleSheet("border-image: url(pic/buttons/lamp1_on.png);")
            gpio.output(port.PA9, self.bool_to_01(self.button_lamp1.isChecked()))
        if (not self.button_lamp1.isChecked()):
            self.button_lamp1.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/lamp1_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/lamp1_on.png);}
    """)
        gpio.output(port.PA9, self.bool_to_01(self.button_lamp1.isChecked()))

    def button_lamp2_clicked(self):
        print(self.button_lamp2.isChecked())

        if (self.button_lamp2.isChecked()):
            self.button_lamp2.setStyleSheet("border-image: url(pic/buttons/lamp2_on.png);")

        if (not self.button_lamp2.isChecked()):
            self.button_lamp2.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/lamp2_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/lamp2_on.png);}
    """)
        gpio.output(port.PA10, self.bool_to_01(self.button_lamp2.isChecked()))
        

    def button_fan_clicked(self):
        print(self.button_fan.isChecked())

        if (self.button_fan.isChecked()):
            self.button_fan.setStyleSheet("border-image: url(pic/buttons/fan_on.png);")
            print(self.slider_fan.value())
            gpio.output(port.PA21, self.bool_to_01(self.button_fan.isChecked()))
            self.pwm.changeDutyCycle(self.slider_fan.value()*20)
            self.lcd_fan.display(self.slider_fan.value())
        if (not self.button_fan.isChecked()):
            self.button_fan.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/fan_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/fan_on.png);}
    """)
            self.lcd_fan.display(0)
            gpio.output(port.PA21, self.bool_to_01(self.button_fan.isChecked()))
            self.pwm.changeDutyCycle(0)

    def button_heater_clicked(self):
        print(self.button_heater.isChecked())

        if (self.button_heater.isChecked()):
            self.button_heater.setStyleSheet("border-image: url(pic/buttons/heater_on.png);")
        if (not self.button_heater.isChecked()):
            self.button_heater.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/heater_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/heater_on.png);}
    """)

    def button_cooler_clicked(self):
        print(self.button_cooler.isChecked())

        if (self.button_cooler.isChecked()):
            self.button_cooler.setStyleSheet("border-image: url(pic/buttons/cooler_on.png);")
        if (not self.button_cooler.isChecked()):
            self.button_cooler.setStyleSheet("""
        QPushButton {border-image: url(pic/buttons/cooler_off.png);}
        QPushButton:hover {border-image: url(pic/buttons/cooler_on.png);}
    """)

    def slider_fan_change(self):
        # print(self.slider_fan.value())
        if (self.button_fan.isChecked()):
            print(self.slider_fan.value())
            self.lcd_fan.display(self.slider_fan.value())
            self.pwm.changeDutyCycle(self.slider_fan.value()*20)
        else:
            self.lcd_fan.display(0)
            gpio.output(port.PA21, self.bool_to_01(self.button_fan.isChecked()))
            self.pwm.changeDutyCycle(0)

    def button_cam_clicked(self):
        print("Cam")
        self.dialog = camera.Camera()
        self.dialog.show()

    def button_weather_clicked(self):
        print("Weather")
        self.dialog = weather.Weather()
        self.dialog.show()

    def clock(self):
        # self.lcd_hour.display("%02d" %(time.localtime()[3]))
        # self.lcd_min.display(time.localtime()[4])
        self.label_clock.setText("{:02d}:{:02d}".format(time.localtime()[3], time.localtime()[4]))

    # "{:4d}{:02d}{:02d}".format(int(year), int(month), int(day))

    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100) * 3.3 / 100)  # Add a new random value.
        self.progress_adc.setValue(int(self.y[-1] * 100 / 3.3))
        self.lcd_adc.display(self.y[-1])
        self.data_line.setData(self.x, self.y)  # Update the data.

    def bool_to_01(self, bool_input):
        if bool_input == True:
            return 1
        else:
            return 0

    def exit(self):

        gpio.output(port.PA9, 0)
        gpio.output(port.PA10, 0)
        gpio.output(port.PA21, 0)
        self.pwm.stop()

        sys.exit()


app = QApplication(sys.argv)
UIWindow = UI()
app.exec()

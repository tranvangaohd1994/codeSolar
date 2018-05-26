import Config
from PyQt5.QtWidgets import (QWidget, QLabel, QGraphicsDropShadowEffect,QFrame)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal,QRect,QDateTime,QDate
from PyQt5.QtGui import QIcon, QPixmap,QColor,QTransform
from time import strftime
import sys, random

class App(QWidget):
    def __init__(self,height,width):
        super().__init__()
        self.initUI(height,width)

    def closeEvent(self, event):
        global isRead,ser,threadRead
        print("------------------closing")
        """
        isRead =False
        threadRead.join()
        ser.close()
        """
    def initUI(self,height,width):
        self.setWindowTitle('Slova')
        self.setGeometry(0,0,width,height)
        #background
       
        xscale = float(width) / 1024.0
        yscale = float(height) / 600.0
        frames = []
        framep = 0

        frame1 = QFrame(self)
        frame1.setObjectName("frame1")
        frame1.setGeometry(0, 0, width, height)
        frame1.setStyleSheet("#frame1 { background-color: black; border-image: url(" +
                            Config.background + ") 0 0 0 0 stretch stretch;}")
        frames.append(frame1)

        ypos=0
       
        self.power = QLabel(frame1)
        self.power.setObjectName("power")
        self.power.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textcolor +"; font-size: " +str(int(10 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power.setGeometry(0, height *0.53 , 300 * xscale, 100)

        self.energyDay = QLabel(frame1)
        self.energyDay.setObjectName("power")
        self.energyDay.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textcolor +"; font-size: " +str(int(40 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.energyDay.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.energyDay.setGeometry(0, height *0.68 , 300 * xscale, 500)

        self.energyAcc = QLabel(frame1)
        self.energyAcc.setObjectName("power")
        self.energyAcc.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textcolor +"; font-size: " +str(int(40 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.energyAcc.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.energyAcc.setGeometry(0, height *0.84 , 300 * xscale, 100)


        self._date = QLabel(frame1)
        self._date.setObjectName("temper2")
        self._date.setStyleSheet("#temper2 { background-color: transparent; color: " +
                            Config.textWhite +
                            "; font-size: " +
                            str(int(40 * xscale)) +
                            "px; " +
                            Config.fontattr +
                            "}")
        self._date.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self._date.setGeometry(width*0.25, 0.03*height, 750 * xscale, 100)
        #print(xscale)
        self.temper = QLabel(frame1)
        self.temper.setObjectName("temper")
        self.temper.setStyleSheet("#temper { background-color: transparent; color: " +
                            Config.textOut +
                            "; font-size: " +
                            str(int(40 * xscale)) +
                            "px; " +
                            Config.fontattr +
                            "}")
        self.temper.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.temper.setGeometry(width * 0.67, height *0.26 , 300 * xscale, 100)

        self.humidity = QLabel(frame1)
        self.humidity.setObjectName("humidity")
        self.humidity.setStyleSheet("#humidity { background-color: transparent; color: " +
                            Config.textOut +
                            "; font-size: " +
                            str(int(30 * xscale)) +
                            "px; " +
                            Config.fontattr +
                            "}")
        self.humidity.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        self.humidity.setGeometry(width * 0.73,height*0.34, 300 * xscale, 100)

        self.indoorTemp = QLabel(frame1)
        self.indoorTemp.setObjectName("indoorTemp")
        self.indoorTemp.setStyleSheet("#indoorTemp { background-color: transparent; color: " +
                            Config.textcolor +
                            "; font-size: " +
                            str(int(40 * xscale)) +
                            "px; " +
                            Config.fontattr +
                            "}")
        self.indoorTemp.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.indoorTemp.setGeometry(width * 0.05,height*0.26, 150 * xscale, 50*yscale)

        ypos += 75
        self.indoorHumi = QLabel(frame1)
        self.indoorHumi.setObjectName("indoorHumi")
        self.indoorHumi.setStyleSheet("#indoorHumi { background-color: transparent; color: " +
                        Config.textcolor +
                        "; font-size: " +
                        str(int(30* xscale)) +
                        "px; " +
                        Config.fontattr +
                        "}")
        self.indoorHumi.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.indoorHumi.setGeometry(width * 0.11,height*0.33, 150 * xscale, 50*yscale)

        self.money = QLabel(frame1)
        self.money.setObjectName("money")
        self.money.setStyleSheet("#money { background-color: transparent; color: " +
                        Config.textWhite +
                        "; font-size: " +
                        str(int(80* xscale)) +
                        "px; " +
                        Config.fontattr +
                        "}")
        self.money.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.money.setGeometry(width * 0.4,height*0.55, 380 * xscale, 100*yscale)

        self.showTemp()
        #self.tick()
        ctimer = QTimer(self)
        ctimer.timeout.connect(self.showTemp)
        ctimer.start(1000)
        self.show()
        self.showFullScreen()


    def showTemp(self):
        _date = strftime("%Y-%d-%B  %H:%M:%S")
        
        
        """
        DATA_PIN = 18
        SCK_PIN = 21
        with SHT1x(DATA_PIN, SCK_PIN, gpio_mode=GPIO.BCM) as sensor:
            nhiet_do = sensor.read_temperature()
            do_am= sensor.read_humidity(nhiet_do)
        """
        do_am,nhiet_do = 90.32,40.05
        _power,energyDay,energyAccumulation = 50,1,25
        self._date.setText(str(_date))
        self.energyAcc.setText(str(energyAccumulation))
        self.energyDay.setText(str(energyDay))
        self.power.setText(str(_power))
        if(nhiet_do < 0):
            return
        self.temper.setText(str(nhiet_do))
        #self.temper2.setText(str(100) + u'°C')
        self.humidity.setText(str(do_am))
        self.indoorHumi.setText('45.23')
        self.indoorTemp.setText('34.45')
        self.money.setText('200.000')
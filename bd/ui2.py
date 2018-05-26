import Config
from PyQt5.QtWidgets import (QWidget,QDialog , QLabel,QPushButton, QGraphicsDropShadowEffect,QFrame)
from PyQt5.QtCore import Qt,QSize, QTimer, pyqtSignal,QRect,QDateTime,QDate
from PyQt5.QtGui import QIcon, QPixmap,QColor,QTransform
from time import strftime
import sys, random
import setting
import readData
import threading

class App(QWidget):
    def __init__(self,height,width):
        super().__init__()
        self.initUI(height,width)
        self.threadRead = readData.readUart(1,"readUart",1)
        self.threadRead.start()

    def closeEvent(self, event):
        readData.isRead = False
        print("-------------closing")
       
    
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
                            Config.bg2 + ") 0 0 0 0 stretch stretch;}")
        frames.append(frame1)

        ypos=0
       
        self.power = QLabel(frame1)
        self.power.setObjectName("power")
        self.power.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textblack +"; font-size: " +str(int(70 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power.setGeometry(0.35*width, height *0.34 , 50 * xscale, 100*yscale)

        self.power1 = QLabel(frame1)
        self.power1.setObjectName("power1")
        self.power1.setStyleSheet("#power1 { background-color: transparent; color: " +
                            Config.textblack +"; font-size: " +str(int(70 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power1.setGeometry(0.41*width, height *0.34 , 50 * xscale, 100*yscale)

        self.power2 = QLabel(frame1)
        self.power2.setObjectName("power2")
        self.power2.setStyleSheet("#power2 { background-color: transparent; color: " +
                            Config.textblack +"; font-size: " +str(int(70 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power2.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power2.setGeometry(0.48*width, height *0.34 , 50 * xscale, 100*yscale)

        self.power3 = QLabel(frame1)
        self.power3.setObjectName("power3")
        self.power3.setStyleSheet("#power3 { background-color: transparent; color: " +
                            Config.textblack +"; font-size: " +str(int(70 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power3.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power3.setGeometry(0.545*width, height *0.34 , 50 * xscale, 100*yscale)

        self.power4 = QLabel(frame1)
        self.power4.setObjectName("power4")
        self.power4.setStyleSheet("#power4 { background-color: transparent; color: " +
                            Config.textblack +"; font-size: " +str(int(70 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.power4.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.power4.setGeometry(0.61*width, height *0.34 , 50 * xscale, 100*yscale)

        self.HaNoi = QLabel(frame1)
        self.HaNoi.setObjectName("HaNoi")
        self.HaNoi.setStyleSheet("#HaNoi { background-color: transparent; color: " +
                            Config.textWhite +"; font-size: " +str(int(40 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.HaNoi.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.HaNoi.setGeometry(0*width, height *0.0 , 200 * xscale, 100*yscale)
        self.HaNoi.setText('Hà Tĩnh')

        self.energyDay = QLabel(frame1)
        self.energyDay.setObjectName("power")
        self.energyDay.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textcolor +"; font-size: " +str(int(36 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.energyDay.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.energyDay.setGeometry(0.15*width, height *0.545 , 300 * xscale, 100)

        self.energyAcc = QLabel(frame1)
        self.energyAcc.setObjectName("power")
        self.energyAcc.setStyleSheet("#power { background-color: transparent; color: " +
                            Config.textcolor +"; font-size: " +str(int(36 * xscale)) +
                            "px; " +Config.fontattr +"}")
        self.energyAcc.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.energyAcc.setGeometry(0.58*width, height *0.545 , 300 * xscale, 100)


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
        self._date.setGeometry(width*0.25, 0*height, 750 * xscale, 100)
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
        self.temper.setGeometry(width * 0.65, height *0.19 , 300 * xscale, 100)

        self.humidity = QLabel(frame1)
        self.humidity.setObjectName("humidity")
        self.humidity.setStyleSheet("#humidity { background-color: transparent; color: " +
                            Config.textOut +
                            "; font-size: " +
                            str(int(26 * xscale)) +
                            "px; " +
                            Config.fontattr +
                            "}")
        self.humidity.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        self.humidity.setGeometry(width * 0.68,height*0.26, 300 * xscale, 100)

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
        self.indoorTemp.setGeometry(width * 0.12,height*0.19, 150 * xscale, 50*yscale)

        self.indoorHumi = QLabel(frame1)
        self.indoorHumi.setObjectName("indoorHumi")
        self.indoorHumi.setStyleSheet("#indoorHumi { background-color: transparent; color: " +
                        Config.textcolor +
                        "; font-size: " +
                        str(int(26* xscale)) +
                        "px; " +
                        Config.fontattr +
                        "}")
        self.indoorHumi.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.indoorHumi.setGeometry(width * 0.15,height*0.26, 150 * xscale, 50*yscale)

        self.money = QLabel(frame1)
        self.money.setObjectName("money")
        self.money.setStyleSheet("#money { background-color: transparent; color: " +
                        Config.textcolor +
                        "; font-size: " +
                        str(int(60* xscale)) +
                        "px; " +
                        Config.fontattr +
                        "}")
        self.money.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.money.setGeometry(width * 0.3,height*0.8, 450 * xscale, 100*yscale)
        
        self.btnSetting = QPushButton(frame1)
        self.btnSetting.setGeometry(QRect(width-48, height-48, 48, 48))
        self.btnSetting.setToolTip("setting button")
        icon = QIcon()
        icon.addPixmap(QPixmap(Config.imgButton), QIcon.Normal, QIcon.On)
        self.btnSetting.setIcon(icon)
        self.btnSetting.setIconSize(QSize(48, 48))
        self.btnSetting.setAutoDefault(False)
        self.btnSetting.setObjectName("btnSetting")
        self.btnSetting.clicked.connect(self.on_click)
        
        
        self.btnExit = QPushButton(frame1)
        self.btnExit.setGeometry(QRect(0, height-48, 48, 48))
        self.btnExit.setToolTip("Exit button")
        iconExit = QIcon()
        iconExit.addPixmap(QPixmap(Config.imgButtonExit), QIcon.Normal, QIcon.On)
        self.btnExit.setIcon(iconExit)
        self.btnExit.setIconSize(QSize(48, 48))
        self.btnExit.setAutoDefault(False)
        self.btnExit.setObjectName("btnExit")
        self.btnExit.clicked.connect(self.close)

        self.showTemp()
        #self.tick()
        ctimer = QTimer(self)
        ctimer.timeout.connect(self.showTemp)
        ctimer.start(1000)
        self.show()
        self.showFullScreen()
    
    def showTemp(self):
        _date = strftime("%H:%M:%S   %A,%d-%m-%Y")
        _s = strftime("%S")
        data = readData.oldData
        if(int(_s) % 10 == 0) :
            try:
                while readData.isAvailbal == False :
                    pass
                readData.sent2Arduino()
            except KeyboardInterrupt:
                readData.ser.close()
                print("ser.close()")
        humiOut,tempOut,moneyV = data[0],data[1],data[6]
        humiIn,tempIn = data[3],data[2]
        _power,energyDay,energyTotal=data[7],data[4],data[5]
        self._date.setText(str(_date))
        self.energyAcc.setText(str(energyTotal))
        self.energyDay.setText(str(energyDay))
        
        self.temper.setText(str(tempOut))
        #self.temper2.setText(str(100) + u'°C')
        self.humidity.setText(str(humiOut))
        self.indoorHumi.setText(str(humiIn))
        self.indoorTemp.setText(str(tempIn))
        self.money.setText(moneyV)

        self.power.setText(str(data[12]))
        self.power1.setText(str(data[11]))
        self.power2.setText(str(data[10]))
        self.power3.setText(str(data[9]))
        self.power4.setText(str(data[8]))

    def on_click(self):
        self.DialogSetting = QDialog()
        ui = setting.Ui_DialogSetting()
        ui.setupUi(self.DialogSetting)
        self.DialogSetting.show()
        print('PyQt5 button click')
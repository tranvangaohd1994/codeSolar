# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setting.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogSetting(object):
    def setupUi(self, DialogSetting):
        DialogSetting.setObjectName("DialogSetting")
        DialogSetting.resize(451, 209)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogSetting)
        self.buttonBox.setGeometry(QtCore.QRect(-20, 150, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.SldBrightless = QtWidgets.QSlider(DialogSetting)
        self.SldBrightless.setGeometry(QtCore.QRect(150, 10, 291, 29))
        self.SldBrightless.setOrientation(QtCore.Qt.Horizontal)
        self.SldBrightless.setObjectName("SldBrightless")
        self.label = QtWidgets.QLabel(DialogSetting)
        self.label.setGeometry(QtCore.QRect(10, 0, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStatusTip("")
        self.label.setWhatsThis("")
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")
        self.timeEdit = QtWidgets.QTimeEdit(DialogSetting)
        self.timeEdit.setGeometry(QtCore.QRect(150, 80, 118, 27))
        self.timeEdit.setObjectName("timeEdit")
        self.label_2 = QtWidgets.QLabel(DialogSetting)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStatusTip("")
        self.label_2.setWhatsThis("")
        self.label_2.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(DialogSetting)
        self.buttonBox.accepted.connect(DialogSetting.accept)
        self.buttonBox.rejected.connect(DialogSetting.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogSetting)

    def retranslateUi(self, DialogSetting):
        _translate = QtCore.QCoreApplication.translate
        DialogSetting.setWindowTitle(_translate("DialogSetting", "Dialog"))
        self.label.setText(_translate("DialogSetting", "Brightless"))
        self.label_2.setText(_translate("DialogSetting", "Timer up date"))

# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     DialogSetting = QtWidgets.QDialog()
#     ui = Ui_DialogSetting()
#     ui.setupUi(DialogSetting)
#     DialogSetting.show()
#     sys.exit(app.exec_())


import ui2
from PyQt5.QtWidgets import QApplication
import sys


global isRead,myApp,threadRead

# chan DATA duoc noi vao chan GPIO25 cua PI
if __name__ == '__main__':
    #threadRead=readUart(1,"readUart",1)
    #threadRead.start()
    app = QApplication(sys.argv)
    desktop = app.desktop()
    rec = desktop.screenGeometry()
    height = rec.height()
    width = rec.width()
    myApp = ui2.App(height,width)
    sys.exit(app.exec_())    
import sys
from time import time, sleep
from PyQt4.QtGui import QApplication, QSplashScreen, QPixmap

from frmMain import MainWindow
# from gui.gui import MainWindow

def main():
    app = QApplication(sys.argv)
    start = time() 
    splash = QSplashScreen(QPixmap("images/login.png"))
    splash.show()
    while time() - start < 1:
        sleep(0.001)
        app.processEvents()
    win = MainWindow()
    splash.finish(win)
    win.show()
    app.exec_()

if __name__ == "__main__":
    main()
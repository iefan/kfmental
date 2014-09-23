# from PyQt4 import 
from myimport import *
from resources import *
from frmMain import MainWindow

class Login(QDialog):
    def __init__(self, db=""):
        QDialog.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = {}

        lbl1 = QLabel("用户名：")
        lbl2 = QLabel("密  码：")

        self.textName = QLineEdit()
        self.textPass = QLineEdit()
        self.textPass.setEchoMode(QLineEdit.Password)
        self.buttonLogin = QPushButton('登录')

        self.textName.setFixedWidth(150)
        self.textPass.setFixedWidth(150)
        self.buttonLogin.setFixedWidth(100)
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QGridLayout()
        layout.addWidget(lbl1, 0, 0, Qt.AlignRight)
        layout.addWidget(self.textName, 0, 1)
        layout.addWidget(lbl2, 1, 0, Qt.AlignRight)
        layout.addWidget(self.textPass, 1, 1)
        layout.addWidget(self.buttonLogin, 2, 1, Qt.AlignRight)

        bitmaplbl = QLabel()
        bitmaplbl.setPixmap(QPixmap("images/login.png"))
        hlayout = QHBoxLayout()
        hlayout.addWidget(bitmaplbl)
        hlayout.addLayout(layout)

        self.setLayout(hlayout)

        self.setWindowTitle("汕头市残联精防基金结算系统")
        self.setWindowIcon(QIcon("images/login.png"))
        self.setStyleSheet("font-size:16px;")

        self.setMinimumSize(380,180)
        self.setMaximumSize (380,180)
        self.resize(380,180)

    def handleLogin(self):
        username = self.textName.text()
        passwd   = self.textPass.text().encode()

        tmppwd = hashlib.md5()
        tmppwd.update(passwd)
        # print(passwd, tmppwd.hexdigest())

        query = QSqlQuery(self.db)
        strsql = "SELECT unitsn, unitname, unitgroup,unitman FROM User where unitsn='%s' and passwd='%s'" % (username, tmppwd.hexdigest())
        ret= query.exec_(strsql);
        # print(ret, "~~~~~~~", strsql, query.isValid())
        # print(ret, query.isValid(), query.next(),)
        if query.next():
            self.curuser['unitsn']      = query.value(0)
            self.curuser['unitname']    = query.value(1)
            self.curuser['unitgroup']   = query.value(2)
            self.curuser['unitman']     = query.value(3)
            # print(1)
            # print("user", self.curuser)
            self.accept()
            # print(2)
        else:
            QMessageBox.warning(self, '错误', '请输入正确的用户名和密码')

def DispLogin():
    import sys
    app = QApplication(sys.argv)

    db = globaldb()
    loginwin = Login(db)
    # print(loginwin.curuser)
    if loginwin.exec_() == QDialog.Accepted:
        # print(loginwin.curuser)
        # print(3)
        window = MainWindow(db, loginwin.curuser)
        window.show()
        db.close()
        sys.exit(app.exec_())
    db.close()


def DispSplash():
    import sys
    from time import time, sleep
    app = QApplication(sys.argv)

    start = time() 
    splash = QSplashScreen(QPixmap("images/splash.png"))
    splash.show()
    while time() - start < 1:
        sleep(0.001)
        app.processEvents()
    
    db = globaldb()
    loginwin = Login(db)
    splash.finish(loginwin)
    
    if loginwin.exec_() == QDialog.Accepted:
        # print(loginwin.curuser)
        # print(3)
        window = MainWindow(db, loginwin.curuser)
        window.show()
        db.close()
        sys.exit(app.exec_())
    db.close()
                
if __name__ == '__main__':
    # DispLogin()
    DispSplash()
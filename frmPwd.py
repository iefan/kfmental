from myimport import *
from resources import *

class frmPwd(QDialog):
    def __init__(self, parent=None, db="", curuser={}):
        super(frmPwd,self).__init__(parent)
        # QDialog.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        lbl1 = QLabel("原来密码：")
        lbl2 = QLabel("新设密码：")
        lbl3 = QLabel("重输密码：")
        # self.mmm = "mmm"

        self.textOldPwd  = QLineEdit()
        self.textNewPwd  = QLineEdit()
        self.textNewPwd2 = QLineEdit()
        self.textOldPwd.setEchoMode(QLineEdit.Password)
        self.textNewPwd.setEchoMode(QLineEdit.Password)
        self.textNewPwd2.setEchoMode(QLineEdit.Password)
        self.buttonOk       = QPushButton('确认修改')
        self.buttonCancel   = QPushButton('取消修改')

        self.textOldPwd.setFixedWidth(150)
        self.textNewPwd.setFixedWidth(150)
        self.textNewPwd2.setFixedWidth(150)
        self.buttonOk.setFixedWidth(100)
        self.buttonCancel.setFixedWidth(100)
        self.buttonOk.clicked.connect(self.modifyPwd)
        self.buttonCancel.clicked.connect(self.close)

        layout = QGridLayout()
        layout.addWidget(lbl1, 0, 0, Qt.AlignRight)
        layout.addWidget(self.textOldPwd, 0, 1)
        layout.addWidget(lbl2, 1, 0, Qt.AlignRight)
        layout.addWidget(self.textNewPwd, 1, 1)
        layout.addWidget(lbl3, 2, 0, Qt.AlignRight)
        layout.addWidget(self.textNewPwd2, 2, 1)
        layout.addWidget(self.buttonOk, 3, 0, Qt.AlignRight)
        layout.addWidget(self.buttonCancel, 3, 1, Qt.AlignRight)

        self.setLayout(layout)

        self.setWindowTitle("修改密码")
        self.setWindowIcon(QIcon("images/login.png"))
        self.setStyleSheet("font-size:14px;")

        self.setMinimumSize(280,180)
        self.setMaximumSize (280,180)
        self.resize(280,180)

    def modifyPwd(self):
        oldpwd  = self.textOldPwd.text()
        newpwd  = self.textNewPwd.text()
        newpwd2 = self.textNewPwd2.text()

        if oldpwd ==  "" or newpwd == "" or newpwd2 == "":
             QMessageBox.warning(self, '错误', '请输入原始密码及重置密码！')
             return
        if newpwd != newpwd2:
             QMessageBox.warning(self, '错误', '两次输入密码不一致！')
             return
        if len(newpwd) < 3:
             QMessageBox.warning(self, '错误', '请输入大于2位的密码！')
             return

        username = self.curuser["unitsn"]

        tmppwd = hashlib.md5()
        tmppwd.update(oldpwd.encode())
        tmppwd2 = hashlib.md5()
        tmppwd2.update(newpwd.encode())

        query = QSqlQuery(self.db)
        strsql = "SELECT * FROM User where unitsn='%s' and passwd='%s'" % (username, tmppwd.hexdigest())
        ret= query.exec_(strsql);
        # print(ret, "~~~~~~~", strsql, query.isValid())
        # print(ret, query.isValid(), query.next(),)
        if query.next():
            tmppwd.update(newpwd.encode())
            # print(newpwd, tmppwd2.hexdigest())
            strsql = "UPDATE User SET passwd='%s' where unitsn='%s'" % (tmppwd2.hexdigest(), username)
            # print(ret, "~~~~~~~", strsql, query.isValid())
            ret = query.exec_(strsql)
            if ret:
                QMessageBox.warning(self, '密码修改成功', '密码修改成功！\n\n系统自动退出！\n\n请重新登录！')
                self.accept()
            else:
                QMessageBox.warning(self, '错误', '密码未修改成功！')
                self.reject()
                
            # self.accept()
            # print(2)
        else:
            QMessageBox.warning(self, '错误', '请输入正确的原始密码')

                
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    db = globaldb()

    dialog=frmPwd(db=db)
    dialog.show()
    app.exec_()

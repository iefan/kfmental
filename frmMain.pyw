#!/usr/bin/env python
from myimport import *
from resources import *

from frmUser import UserDlg
from frmMental import MentalDlg
from frmPwd import frmPwd

class MainWindow(QMainWindow):
    def __init__(self, db="", curuser = {}):
        super(MainWindow, self).__init__()
        # print(1)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tabWidget=QTabWidget(self)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        # self.db.close()

        # print(self.db.connectionName())
        # self.closeEvent.connect(self.closeWindow())
        
        self.curuser = curuser

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeMyTab)

        self.setCentralWidget(self.tabWidget)

        self.createActions()
        self.createMenus()

        message = "欢迎使用汕头市残联康复业务管理系统！"
        self.statusBar().showMessage(message)

        if self.curuser == {}:
            userInfoStr = "当前登录属于调试操作！"
        else:
            userInfoStr = "当前用户编码：%s，单位：%s，操作人员姓名：%s" % (self.curuser["unitsn"], self.curuser["unitname"], self.curuser["unitman"])
        self.userlabel = QLabel(userInfoStr)
        self.statusBar().addPermanentWidget(self.userlabel)

        self.setWindowIcon(QIcon("images/login.png"))
        self.setWindowTitle("康复业务系统")
        self.setMinimumSize(480,320)
        self.resize(720,600)

        self.setStyleSheet("font-size:14px;")
        
        # self.createDb()

    def closeEvent(self, event):
        # pass
        # print(1)
        self.db.close()
        # QSqlDatabase.removeDatabase(self.db.connectionName())
        # print(2)

    def closeMyTab(self, tabindx):
        self.tabWidget.removeTab (tabindx)
        # print(tabindx)

    def createDb(self):
        query = QSqlQuery(self.db)
        strsqlUser = "create table User (id int not null primary key auto_increment,\
            unitsn char(20) not null, \
            passwd char(40) not null, \
            unitname char(40) not null, \
            unitclass char(40) not null, \
            unitman  char(30) not null);"
        
        strsqlAdapt = "create table Adaptstat(id int not null primary key auto_increment,\
            adaptdate date not null, \
            adaptpersons int default 0, \
            adapttools int default 0, \
            isover char(10) default '否');"
        # strsql = "create table MyClass(id int(4) not null primary key auto_increment, name char(20) not null, sex int(4) not null default '0', degree double(16,2));"

        ret = query.exec_(strsqlAdapt)
        print(ret)
        # query.exec_("insert into user values(101, 'aa', 'bb', 'cc', 'dd', 'ee')")
        # query.exec_("select * from recipes")
        # while query.next():
        #     print(query.value(0), query.value(1), query.value(2))
            # starttime DATETIME NOT NULL,
        # print("createdb")

    # def contextMenuEvent(self, event):
    #     menu = QMenu(self)
    #     menu.addAction(self.cutAct)
    #     menu.addAction(self.copyAct)
    #     menu.addAction(self.pasteAct)
    #     menu.exec_(event.globalPos())

    # def refreshTable(self):
    #     print("a")
    # def resetMain(self):
    #     .textOldPwd
    #     print(12)

    def modifyPwd(self):
        dialog=frmPwd(self, db=self.db, curuser=self.curuser)
        # dialog.show()
        # dialog.accepted.connect(self.resetMain)
        # self.connect(dialog, SIGNAL("accepted"), self.refreshTable)
        dialog.show()
        if dialog.exec_() == QDialog.Accepted:
            self.close()
            # print(1)
            # print(dialog.mmm)

    def userManage(self):
        if self.curuser != {}:
            if self.curuser["unitclass"] != "市残联":
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "用户管理"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = UserDlg(db=self.db)
        self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)
        # self.lstTab.append(tabindx)
        # self.infoLabel.setText("Invoked <b>File|New</b>")

    def ToolManage(self):
        if self.curuser != {}:
            if self.curuser["unitclass"] != "市残联" and self.curuser["unitclass"] != "辅具中心":
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "适配器管理"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget2 = AdaptDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget2,curTabText)
        self.tabWidget.setCurrentWidget(widget2)
        # self.lstTab.append(tabindx)
        # self.infoLabel.setText("Invoked <b>File|Open</b>")
        	
    def about(self):
        # self.infoLabel.setText("Invoked <b>Help|About</b>")
        QMessageBox.about(self, "关于...",
                "本程序完成康复科日常业务数据管理! \n\n%s \n\n%s " % (CUR_VERSION, CUR_CONTACT))

    def aboutQt(self):
        pass
        # self.infoLabel.setText("Invoked <b>Help|About Qt</b>")


    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action

    def createActions(self):
        self.userAct        = self.createAction("用户管理(&U)", self.userManage,   "", "", "用户管理")
        self.modifyPwdAct   = self.createAction("修改密码", self.modifyPwd,   "", "", "修改用户密码")
        self.toolAct        = self.createAction("辅具用品(&M)", self.ToolManage,   "", "", "辅具用品数量统计")
        self.exitAct        = self.createAction("退出(&X)", self.close,   "Ctrl+Q", "", "退出系统")
        self.aboutAct       = self.createAction("关于(&A)", self.about,   "", "", "显示当前系统的基本信息")
        self.aboutQtAct     = self.createAction("关于Qt(&Q)", self.aboutQt,   "", "", "显示Qt库的基本信息")
        self.aboutQtAct.triggered.connect(qApp.aboutQt)
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("系统管理(&S)")
        self.fileMenu.addAction(self.userAct)        
        self.fileMenu.addAction(self.modifyPwdAct)        
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("业务管理(&F)")
        self.editMenu.addAction(self.toolAct)
        
        self.helpMenu = self.menuBar().addMenu("关于(&H)")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # app.setStyle(QStyleFactory.create('cleanlooks'))
    window = MainWindow()
    # app.lastWindowClosed.connect(window.closeWindow())
    window.show()
    sys.exit(app.exec_())

#!/usr/bin/env python
from myimport import *
from resources import *

from frmUser import UserDlg
from frmMentalInfo import MentalDlg
from frmApproval import ApprovalDlg
from frmApply import ApplyDlg
from frmPwd import frmPwd
from frmHospital import HospitalDlg
from frmCalc import CalcDlg
from frmFinish import FinishDlg

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

        message = "欢迎使用汕头市精神残疾人住院医疗救助结算业务系统！"
        self.statusBar().showMessage(message)

        if self.curuser == {}:
            userInfoStr = "当前登录属于调试操作！"
        else:
            userInfoStr = "当前用户编码：%s，单位：%s，操作人员姓名：%s" % (self.curuser["unitsn"], self.curuser["unitname"], self.curuser["unitman"])
        self.userlabel = QLabel(userInfoStr)
        self.statusBar().addPermanentWidget(self.userlabel)

        # dispSystemInfo = QLabel("汕头市残联精防基金结算\n\n       业务系统", self)
        # dispSystemInfo.setGeometry(300,200,820,200)
        # dispSystemInfo.setStyleSheet("font-size:60px; color:blue;font-weight:bold;")
        # self.setStyleSheet("background-color:red;")

        self.setWindowIcon(QIcon("images/login.png"))
        self.setWindowTitle("汕头市精神残疾人住院医疗救助结算业务系统")
        self.setMinimumSize(480,320)
        self.showMaximized()
        # self.resize(720,600)

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
            if self.curuser["unitgroup"] != "市残联":
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

    def ApplyManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "区残联":
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "住院申请"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = ApplyDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    def FinishManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" :
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "市残联核结"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = FinishDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)
      
    def ApprovalManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" :
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "市残联申核"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget3 = ApprovalDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget3,curTabText)
        self.tabWidget.setCurrentWidget(widget3)

    def CalcManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "医院" :
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "出院费用结算"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = CalcDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    
    def HospitalManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "医院" :
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "确认出入院"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget = HospitalDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget,curTabText)
        self.tabWidget.setCurrentWidget(widget)

    def MentalManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "区残联":
                QMessageBox.warning(self, "没有授权", "当前用户没有权限进行该操作！")
                return

        curTabText = "精神病人基础信息库"
        for tabindx in list(range(0, self.tabWidget.count())):
            if self.tabWidget.tabText(tabindx) == curTabText:
                self.tabWidget.setCurrentIndex(tabindx)
                return

        widget2 = MentalDlg(db=self.db, curuser=self.curuser)
        tabindx = self.tabWidget.addTab(widget2,curTabText)
        self.tabWidget.setCurrentWidget(widget2)


    def ToolManage(self):
        if self.curuser != {}:
            if self.curuser["unitgroup"] != "市残联" and self.curuser["unitgroup"] != "辅具中心":
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
                	
    def about(self):
        QMessageBox.about(self, "关于...",
                "本程序完成汕头市精防基金结算! \n\n%s \n\n%s " % (CUR_VERSION, CUR_CONTACT))

    def aboutQt(self):
        pass
        

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
        # self.toolAct        = self.createAction("辅具用品(&M)", self.ToolManage,   "", "", "辅具用品数量统计")
        self.mentalAct      = self.createAction("基础信息库(&M)", self.MentalManage,   "", "", "精神病人基础信息库")
        self.applyAct       = self.createAction("住院申请(&I)", self.ApplyManage,   "", "", "住院申请")
        self.approvalAct    = self.createAction("市残联申核(&A)", self.ApprovalManage,   "", "", "市残联申核")
        self.finishAct    = self.createAction("市残联核结(&A)", self.FinishManage,   "", "", "市残联核结")
        self.hospitalAct    = self.createAction("确认出入院(&A)", self.HospitalManage,   "", "", "确认出入院")
        self.calcAct        = self.createAction("出院费用结算(&A)", self.CalcManage,   "", "", "出院费用结算")
        self.exitAct        = self.createAction("退出(&X)", self.close,   "Ctrl+Q", "", "退出系统")
        self.aboutAct       = self.createAction("关于(&A)", self.about,   "", "", "显示当前系统的基本信息")
        self.aboutQtAct     = self.createAction("关于Qt(&Q)", self.aboutQt,   "", "", "显示Qt库的基本信息")
        self.aboutQtAct.triggered.connect(qApp.aboutQt)
        
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("系统管理(&S)")
        self.fileMenu.addAction(self.userAct)        
        self.fileMenu.addAction(self.modifyPwdAct)        
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("基础信息及申请(&F)")
        self.editMenu.addAction(self.mentalAct)
        self.editMenu.addAction(self.applyAct)
        
        self.approvalMenu = self.menuBar().addMenu("市残联申核(&A)")
        self.approvalMenu.addAction(self.approvalAct)
        self.approvalMenu.addAction(self.finishAct)

        self.hospitalMenu = self.menuBar().addMenu("医院确认结算(&P)")
        self.hospitalMenu.addAction(self.hospitalAct)
        self.hospitalMenu.addAction(self.calcAct)

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

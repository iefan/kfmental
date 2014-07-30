from resources import *

from cc_delegate import ComboBoxDelegate

class UserDlg(QDialog):
    def __init__(self,parent=None, db=""):
        super(UserDlg,self).__init__(parent)

        # widget = QWidget()               

        # self.setCentralWidget(widget)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        # headers = ["单位编码", "单位名称", "单位类别", "姓名"]

        self.userView = QTableView()
        self.userModel = QSqlTableModel(self.userView)
        self.userModel.setTable("user")
        self.userModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.userModel.setQuery(QSqlQuery("select unitsn, unitname, unitclass, unitpp from user"))
        self.userModel.select()
        # self.userModel.removeColumn(2)
        # self.userModel.removeColumn(0)
        self.userModel.setHeaderData(1, Qt.Horizontal, "单位编码")
        self.userModel.setHeaderData(3, Qt.Horizontal, "单位名称")
        self.userModel.setHeaderData(4, Qt.Horizontal, "单位类别")
        self.userModel.setHeaderData(5, Qt.Horizontal, "操作人员")

        # self.userModel = QStandardItemModel(0, 0, self.userView)
        # self.userModel.setHorizontalHeaderLabels(headers)
        self.userView.setModel(self.userModel)
        self.userView.setColumnHidden(0, True) # hide sn
        self.userView.setColumnHidden(2, True) # hide password
        # print(2)
        lstUnitName = ["市残联", "金平区残联", "龙湖区残联","濠江区残联","澄海区残联","潮阳区残联","潮南区残联","南澳县残联", \
                '市四本部' ,'礐石','红莲池','汕大']
        combodelegate = ComboBoxDelegate(self, lstUnitName)
        combodelegate2 = ComboBoxDelegate(self, ["市残联", "区残联", "医院"])
        self.userView.setItemDelegateForColumn(3, combodelegate)
        self.userView.setItemDelegateForColumn(4, combodelegate2)


        self.userView.setStyleSheet("QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        # self.userView.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.userView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.userView.horizontalHeader().setStyleSheet("color: red");
        # self.userView.verticalHeader().hide()
        self.userView.verticalHeader().setFixedWidth(30)
        self.userView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.userView.setStyleSheet("font-size:14px; ");
        # print(4)
        # self.userView.show()

        # topFiller = QTableWidget()
        # topFiller.clear()
        # topFiller.setSortingEnabled(False)
        # topFiller.setRowCount(10)
        # topFiller.setColumnCount(len(headers))
        # topFiller.setHorizontalHeaderLabels(headers)
        # topFiller.setItem(1, 1, QTableWidgetItem("1"))
        # topFiller.resizeColumnsToContents()

        # topFiller = QWidget()
        self.userView.setSizePolicy(QSizePolicy.Expanding,
                QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        resetPwdbtn    = QPushButton("重置密码")
        btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(resetPwdbtn, QDialogButtonBox.ActionRole);

        # self.infoLabel = QLabel(
        #         "<i>Choose a menu option, or right-click to invoke a context menu</i>",
        #         alignment=Qt.AlignCenter)
        # self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        # bottomFiller = QWidget()
        # bottomFiller.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Expanding)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addWidget(self.userView)
        vbox.addWidget(btnbox)
        # vbox.addWidget(self.infoLabel)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveUser)
        newusrbtn.clicked.connect(self.newUser)
        revertbtn.clicked.connect(self.revertUser)
        removebtn.clicked.connect(self.removeUser)
        resetPwdbtn.clicked.connect(self.resetPwd)
        # self.userView.clicked.connect(self.tableClick)

    def closeEvent(self, event):
        self.db.close()

    def resetPwd(self):
        index = self.userView.currentIndex()
        row = index.row()
        tmppwd = hashlib.md5()
        tmppwd.update(b"123456")
        self.userModel.setData(self.userModel.index(row, 2), tmppwd.hexdigest()) #set default password
        a = self.userModel.submitAll()
        b = self.userModel.database().commit()
        QMessageBox.warning(self, '成功', '重置密码完成，当前密码:123456！')

        
    def removeUser(self):
        index = self.userView.currentIndex()
        row = index.row()
        # print(index.isValid(), index.row())
        
        # nameid = self.userModel.data(self.userModel.index(row, 0))

        # self.userModel.setFilter("id = 10");
        # self.userModel.select();
        # if self.userModel.rowCount() == 1:
        #     model.removeRows(0,1) // 如果要删除所有满足条件的记录则把1改成model.rowCount()
        #     model.submitAll();
        # if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
      
        if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？", "确定", "取消") == 0:
            self.userModel.removeRows(row, 1)
            self.userModel.submitAll()
            self.userModel.database().commit()
            # print("nameid")
            

    def revertUser(self):
        self.userModel.revertAll()
        self.userModel.database().rollback()

    def newUser(self):
        row = self.userModel.rowCount()
        self.userModel.insertRow(row)
        tmppwd = hashlib.md5()
        tmppwd.update(b"123456")
        self.userModel.setData(self.userModel.index(row, 2), tmppwd.hexdigest()) #set default password

    def saveUser(self):
        self.userModel.database().transaction()
        if self.userModel.submitAll():
            self.userModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.userModel.revertAll()
            self.userModel.database().rollback()
            # print("save fail!  ->rollback")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.userModel.setItem(0, 0, tmpitem)
        # print(self.userModel.database())
        # print("saveUser")
       
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=UserDlg()
    dialog.show()
    app.exec_()
from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate, PhoneDelegate, PersonIdDelegate

class ApplyDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(ApplyDlg,self).__init__(parent)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser
        self.willApply = []

        self.ApplyView = QTableView()
        self.ApplyModel = QSqlRelationalTableModel(self.ApplyView)
        self.ApplyModel.setTable("approvalmodel")
        self.ApplyModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.ApplyModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.ApplyModel.select()
        for indx, iheader in enumerate(LST_APPROVALHEADER):
            self.ApplyModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.ApplyView.setModel(self.ApplyModel)
        self.ApplyView.setColumnHidden(0, True) # hide sn

        hideColList = list(range(8,43))
        hideColList.remove(15)
        for icol in hideColList:
            self.ApplyView.setColumnHidden(icol, True) # hide sn

        self.ApplyView.setColumnWidth(1, 150)
        self.ApplyView.setColumnWidth(4, 120)

        self.ApplyView.setItemDelegateForColumn(3, ComboBoxDelegate(self, CERT1_CHOICES))
        self.ApplyView.setItemDelegateForColumn(4, ComboBoxDelegate(self, CERT2_CHOICES))
        self.ApplyView.setItemDelegateForColumn(5, ComboBoxDelegate(self, CERT3_CHOICES))
        self.ApplyView.setItemDelegateForColumn(6, DateDelegate(self))
       
        self.ApplyView.setAlternatingRowColors(True)
        self.ApplyView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 
       
        self.ApplyView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.ApplyView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.ApplyView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        # newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        # Applybtn     = QPushButton("批准")

        # btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(Applybtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel("", alignment=Qt.AlignLeft)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)


        nameLabel       = QLabel("姓名:")
        self.nameEdit   = QLineEdit()
        regExp = QRegExp("[^']*")
        self.nameEdit.setValidator(QRegExpValidator(regExp, self))
        nameLabel.setBuddy(self.nameEdit)

        # personIdLabel   = QLabel("身份证号:")
        # self.ppidEdit   = QLineEdit()
        # personIdLabel.setBuddy(self.ppidEdit)
        # regExp = QRegExp("^[0-9]{8,12}$")
        # self.ppidEdit.setValidator(QRegExpValidator(regExp, self))
        
        applyresultLabel      = QLabel("审核结果:")
        self.applyresultCombo = QComboBox(self)
        self.applyresultCombo.addItems(ISAPPROVAL_CHOICES)
        self.applyresultCombo.insertItem(0, "")
        self.applyresultCombo.setCurrentIndex(0)
        applyresultLabel.setBuddy(self.applyresultCombo)


        findbutton = QPushButton("查询")
        # findbutton.setIcon(QIcon(":/first.png"))

        findbox = QHBoxLayout()
        findbox.setMargin(10)
        findbox.setAlignment(Qt.AlignHCenter);
        # findbox.addWidget(self.callerEdit)
        findbox.addStretch (10)
        findbox.addWidget(nameLabel)
        findbox.addWidget(self.nameEdit)
        findbox.addStretch (10)
        # findbox.addWidget(personIdLabel)
        # findbox.addWidget(self.ppidEdit)
        # findbox.addStretch (10)
        findbox.addWidget(applyresultLabel)
        findbox.addWidget(self.applyresultCombo)
        findbox.addWidget(findbutton)
        findbox.addStretch (10)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addLayout(findbox)
        vbox.addWidget(self.ApplyView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveApply)
        revertbtn.clicked.connect(self.revertApply)
        removebtn.clicked.connect(self.removeApply)
        # Applybtn.clicked.connect(self.okApply)

        findbutton.clicked.connect(self.findApply)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.ApplyView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveApply)
        # self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ApplyView.doubleClicked.connect(self.dbclick)


    def setWillApply(self, lstwillapply):
        self.willApply = lstwillapply

    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        if indx.sibling(indx.row(),15).data() != "待审":
            self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            if indx.column() in [1,2,7,15]:
                self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)
            else:
                self.ApplyView.setEditTriggers(QAbstractItemView.DoubleClicked)

        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitgroup"] == "市残联":
                if indx.column() == 1:
                    self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.ApplyView.setEditTriggers(QAbstractItemView.DoubleClicked)
            else:
                self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # if indx.sibling(indx.row(),4).data() == "是":
                #     self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # else:
                #     self.ApplyView.setEditTriggers(QAbstractItemView.DoubleClicked)

                # if indx.column() == 4:
                #     self.ApplyView.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def findApply(self):
        name        = self.nameEdit.text()
        # ppid        = self.ppidEdit.text()
        applyresult      = self.applyresultCombo.currentText()
        strwhere    = "relTblAl_2.name like '%%%s%%' and isapproval like '%%%s%%'" % (name, applyresult)

        self.ApplyModel.setFilter(strwhere)
        # print("~~~", self.ApplyModel.selectStatement())
        self.ApplyModel.select()
        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(self.ApprovalModel.rowCount()))


    def removeApply(self):
        index = self.ApplyView.currentIndex()
        row = index.row()
        if row != -1:
            ppname = self.ApplyModel.data(self.ApplyModel.index(row, 1))
            if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？\n\n姓名：%s\n\n" % ppname, "确定", "取消") == 0:
                self.ApplyModel.removeRows(row, 1)
                self.ApplyModel.submitAll()
                self.ApplyModel.database().commit()

                self.infoLabel.setText("")

        # print("nameid")
        
    def revertApply(self):
        self.ApplyModel.revertAll()
        self.ApplyModel.database().rollback()
        self.infoLabel.setText("")

    def newApply(self):
        # self.ApplyModel.setFilter("1=1")
        if self.curuser == {}:
            applyman = "某某"
        else:
            applyman = self.unitman

        for iwillapply in self.willApply:
            row = self.ApplyModel.rowCount()
            self.ApplyModel.insertRow(row)
            # print(self.ApplyModel.data(self.ApplyModel.index(row, 0)), 'id=========')
            self.ApplyModel.setData(self.ApplyModel.index(row, 2), iwillapply) #set default password
            self.ApplyModel.setData(self.ApplyModel.index(row, 7), applyman) #set default password
            self.ApplyModel.setData(self.ApplyModel.index(row, 15), '待审') #set default password
            self.ApplyView.scrollToBottom()
        
        self.infoLabel.setText("")

        # theLastIndex = self.ApplyModel.index(row, 1)
        # self.ApplyView.scrollTo(theLastIndex)
        
        # self.ApplyModel.setData(self.ApplyModel.index(row, 2), "123456") #set default password

    def saveApply(self):
        self.ApplyModel.database().transaction()
        if self.ApplyModel.submitAll():
            self.ApplyModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.ApplyModel.revertAll()
            self.ApplyModel.database().rollback()
            # print("save fail!  ->rollback")

        self.ApplyModel.setFilter("1=1")
        self.infoLabel.setText("")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.ApplyModel.setItem(0, 0, tmpitem)
        # print(self.ApplyModel.database())
        # print("saveApply")
       
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=ApplyDlg()
    dialog.show()
    app.exec_()
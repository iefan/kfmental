from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate, PhoneDelegate, PersonIdDelegate

class ApprovalDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(ApprovalDlg,self).__init__(parent)

        # widget = QWidget()               

        # self.setCentralWidget(widget)
        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        # headers = ["月份", "适配人数", "适配件数", "是否确认"]

        self.ApprovalView = QTableView()
        self.ApprovalModel = QSqlRelationalTableModel(self.ApprovalView)
        self.ApprovalModel.setTable("approvalmodel")
        self.ApprovalModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.ApprovalModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.ApprovalModel.select()
        for indx, iheader in enumerate(LST_APPROVALHEADER):
            self.ApprovalModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.ApprovalView.setModel(self.ApprovalModel)
        self.ApprovalView.setColumnHidden(0, True) # hide sn

        hideColList = list(range(18,43))
        for icol in hideColList:
            self.ApprovalView.setColumnHidden(icol, True) # hide sn

        self.ApprovalView.setColumnWidth(1, 150)
        self.ApprovalView.setColumnWidth(4, 120)
        # self.ApprovalView.setColumnHidden(15, True) # hide sn

        # sexDelegate = ComboBoxDelegate(self, SEX_CHOICES)
        # self.ApprovalView.setItemDelegateForColumn(2, sexDelegate)
        # countyDelegate = ComboBoxDelegate(self, COUNTY_CHOICES)
        # self.ApprovalView.setItemDelegateForColumn(3, countyDelegate)
        # ppidDelegate = PersonIdDelegate(self)
        # self.ApprovalView.setItemDelegateForColumn(4, ppidDelegate)
        # disDelegate = ComboBoxDelegate(self, DISLEVEL_CHOICES)
        # self.ApprovalView.setItemDelegateForColumn(5, disDelegate)
        # dateDelegate = DateDelegate(self)
        # self.ApprovalView.setItemDelegateForColumn(6, dateDelegate)
        # econDelegate = ComboBoxDelegate(self, ECON_CHOICES)
        # self.ApprovalView.setItemDelegateForColumn(7, econDelegate)
        # cityDelegate = ComboBoxDelegate(self, CITY_CHOICE)
        # self.ApprovalView.setItemDelegateForColumn(8, cityDelegate) 
        # relaDelegate = ComboBoxDelegate(self, RELASHIP_CHOICES)
        # self.ApprovalView.setItemDelegateForColumn(11, relaDelegate)

        # phoneDelegate = PhoneDelegate(self)
        # self.ApprovalView.setItemDelegateForColumn(12, phoneDelegate)
        # phone2Delegate = PhoneDelegate(self)
        # self.ApprovalView.setItemDelegateForColumn(13, phone2Delegate)

        # date2Delegate = DateDelegate(self)
        # self.ApprovalView.setItemDelegateForColumn(14, date2Delegate)
        
        self.ApprovalView.setAlternatingRowColors(True)
        self.ApprovalView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 

        # self.ApprovalView.setStyleSheet()
        # self.ApprovalView.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.ApprovalView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.ApprovalView.horizontalHeader().setStyleSheet("color: red");
        # self.ApprovalView.verticalHeader().hide()
        # self.ApprovalView.verticalHeader().setFixedWidth(30)
        self.ApprovalView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.ApprovalView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.ApprovalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        approvalbtn     = QPushButton("批准")

        btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(approvalbtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel("", alignment=Qt.AlignLeft)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)


        nameLabel       = QLabel("姓名:")
        self.nameEdit   = QLineEdit()
        regExp = QRegExp("[^']*")
        self.nameEdit.setValidator(QRegExpValidator(regExp, self))
        nameLabel.setBuddy(self.nameEdit)

        personIdLabel   = QLabel("身份证号:")
        self.ppidEdit   = QLineEdit()
        personIdLabel.setBuddy(self.ppidEdit)
        regExp = QRegExp("^[0-9]{8,12}$")
        self.ppidEdit.setValidator(QRegExpValidator(regExp, self))
        
        countyLabel      = QLabel("区县名称:")
        self.countyCombo = QComboBox(self)
        self.countyCombo.addItems(COUNTY_CHOICES)
        self.countyCombo.insertItem(0, "")
        self.countyCombo.setCurrentIndex(0)
        countyLabel.setBuddy(self.countyCombo)


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
        findbox.addWidget(personIdLabel)
        findbox.addWidget(self.ppidEdit)
        findbox.addStretch (10)
        findbox.addWidget(countyLabel)
        findbox.addWidget(self.countyCombo)
        findbox.addWidget(findbutton)
        findbox.addStretch (10)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addLayout(findbox)
        vbox.addWidget(self.ApprovalView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveApproval)
        newusrbtn.clicked.connect(self.newApproval)
        revertbtn.clicked.connect(self.revertApproval)
        removebtn.clicked.connect(self.removeApproval)
        approvalbtn.clicked.connect(self.okApproval)

        findbutton.clicked.connect(self.findApproval)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.ApprovalView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveApproval)
        # self.dispTotalnums()
        # self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ApprovalView.doubleClicked.connect(self.dbclick)


    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        if indx.column() in [1,2,3,4,5,6,7]:
            self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.ApprovalView.setEditTriggers(QAbstractItemView.DoubleClicked)


        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitgroup"] == "市残联":
                if indx.column() == 1:
                    self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.ApprovalView.setEditTriggers(QAbstractItemView.DoubleClicked)
            else:
                self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # if indx.sibling(indx.row(),4).data() == "是":
                #     self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # else:
                #     self.ApprovalView.setEditTriggers(QAbstractItemView.DoubleClicked)

                # if indx.column() == 4:
                #     self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def dispTotalnums(self, strwhere="1=1"):
        query = QSqlQuery(self.db)
        strsql = "SELECT count(*) FROM Approvalmodel where " + strwhere
        ret= query.exec_(strsql);
        query.next()
        # print(ret, "~~~~~~~", strsql)
        # total_personnums = 0
        # total_toolnums = 0
        # while query.next():
        #     if type(query.value(0))== QPyNullVariant:
        #         break
        #     total_personnums += query.value(0)
        #     total_toolnums   += query.value(1)
            # print(query.value(0), query.value(1))

        # print(total_personnums, total_toolnums, "==")
        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(query.value(0)))

    def findApproval(self):
        name        = self.nameEdit.text()
        ppid        = self.ppidEdit.text()
        county      = self.countyCombo.currentText()
        strwhere    = "name like '%%%s%%' and ppid like '%%%s%%' and county like '%%%s%%'" % (name, ppid, county)

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Approvaldate)=%d" % yeardate
        # else:
        #     strwhere = "Approvaldate > '%s' and Approvaldate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.ApprovalModel.setFilter(strwhere)
        self.ApprovalModel.select()

        self.dispTotalnums(strwhere)

        # self.ApprovalModel.setFilter("")

    def okApproval(self):
        index = self.ApprovalView.currentIndex()
        row = index.row()

    def removeApproval(self):
        index = self.ApprovalView.currentIndex()
        row = index.row()
        if row != -1:
            ppname = self.ApprovalModel.data(self.ApprovalModel.index(row, 1))
            if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？\n\n姓名：%s\n\n" % ppname, "确定", "取消") == 0:
                self.ApprovalModel.removeRows(row, 1)
                self.ApprovalModel.submitAll()
                self.ApprovalModel.database().commit()

                self.infoLabel.setText("")

        # print("nameid")
        
    def revertApproval(self):
        self.ApprovalModel.revertAll()
        self.ApprovalModel.database().rollback()
        self.infoLabel.setText("")

    def newApproval(self):
        # self.ApprovalModel.setFilter("1=1")
        row = self.ApprovalModel.rowCount()
        self.ApprovalModel.insertRow(row)

        # theLastIndex = self.ApprovalModel.index(row, 1)
        # self.ApprovalView.scrollTo(theLastIndex)
        self.ApprovalView.scrollToBottom()
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 15), "某某") #set default password
        self.infoLabel.setText("")
        # self.ApprovalModel.setData(self.ApprovalModel.index(row, 2), "123456") #set default password

    def saveApproval(self):
        self.ApprovalModel.database().transaction()
        if self.ApprovalModel.submitAll():
            self.ApprovalModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.ApprovalModel.revertAll()
            self.ApprovalModel.database().rollback()
            # print("save fail!  ->rollback")

        self.ApprovalModel.setFilter("1=1")
        self.infoLabel.setText("")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.ApprovalModel.setItem(0, 0, tmpitem)
        # print(self.ApprovalModel.database())
        # print("saveApproval")
       
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=ApprovalDlg()
    dialog.show()
    app.exec_()
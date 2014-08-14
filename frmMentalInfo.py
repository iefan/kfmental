from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate, PhoneDelegate, PersonIdDelegate
from frmApply import ApplyDlg

class MentalDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(MentalDlg,self).__init__(parent)

        # widget = QWidget()               

        # self.setCentralWidget(widget)
        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        # headers = ["月份", "适配人数", "适配件数", "是否确认"]

        self.MentalView = QTableView()
        self.MentalModel = QSqlTableModel(self.MentalView)
        self.MentalModel.setTable("mentalmodel")
        self.MentalModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.MentalModel.setQuery(QSqlQuery("select unitsn, unitname, unitgroup, unitpp from Mental"))
        self.MentalModel.select()
        # self.MentalModel.removeColumn(2)
        # self.MentalModel.removeColumn(0)
        for indx, iheader in enumerate(LST_MENTALHEADER):
            self.MentalModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        # self.MentalModel = QStandardItemModel(0, 0, self.MentalView)
        # self.MentalModel.setHorizontalHeaderLabels(headers)
        self.MentalView.setModel(self.MentalModel)
        self.MentalView.setColumnHidden(0, True) # hide sn
        self.MentalView.setColumnHidden(15, True) # hide sn

        sexDelegate = ComboBoxDelegate(self, SEX_CHOICES)
        self.MentalView.setItemDelegateForColumn(2, sexDelegate)
        countyDelegate = ComboBoxDelegate(self, COUNTY_CHOICES)
        self.MentalView.setItemDelegateForColumn(3, countyDelegate)
        ppidDelegate = PersonIdDelegate(self)
        self.MentalView.setItemDelegateForColumn(4, ppidDelegate)
        disDelegate = ComboBoxDelegate(self, DISLEVEL_CHOICES)
        self.MentalView.setItemDelegateForColumn(5, disDelegate)
        dateDelegate = DateDelegate(self)
        self.MentalView.setItemDelegateForColumn(6, dateDelegate)
        econDelegate = ComboBoxDelegate(self, ECON_CHOICES)
        self.MentalView.setItemDelegateForColumn(7, econDelegate)
        cityDelegate = ComboBoxDelegate(self, CITY_CHOICE)
        self.MentalView.setItemDelegateForColumn(8, cityDelegate) 
        relaDelegate = ComboBoxDelegate(self, RELASHIP_CHOICES)
        self.MentalView.setItemDelegateForColumn(11, relaDelegate)

        phoneDelegate = PhoneDelegate(self)
        self.MentalView.setItemDelegateForColumn(12, phoneDelegate)
        phone2Delegate = PhoneDelegate(self)
        self.MentalView.setItemDelegateForColumn(13, phone2Delegate)

        date2Delegate = DateDelegate(self)
        self.MentalView.setItemDelegateForColumn(14, date2Delegate)
        
        self.MentalView.setAlternatingRowColors(True)
        self.MentalView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 

        # self.MentalView.setStyleSheet()
        # self.MentalView.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.MentalView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.MentalView.horizontalHeader().setStyleSheet("color: red");
        # self.MentalView.verticalHeader().hide()
        # self.MentalView.verticalHeader().setFixedWidth(30)
        self.MentalView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.MentalView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.MentalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        applybtn        = QPushButton("申请")

        btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(applybtn, QDialogButtonBox.ActionRole);

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
        vbox.addWidget(self.MentalView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveMental)
        newusrbtn.clicked.connect(self.newMental)
        revertbtn.clicked.connect(self.revertMental)
        removebtn.clicked.connect(self.removeMental)
        applybtn.clicked.connect(self.applyMental)

        findbutton.clicked.connect(self.findMental)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.MentalView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveMental)
        self.dispTotalnums()
        # self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.MentalView.doubleClicked.connect(self.dbclick)


    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitgroup"] == "市残联" or self.curuser["unitgroup"] == "区残联":
                self.MentalView.setEditTriggers(QAbstractItemView.DoubleClicked)
            else:
                self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # if indx.sibling(indx.row(),4).data() == "是":
                #     self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # else:
                #     self.MentalView.setEditTriggers(QAbstractItemView.DoubleClicked)

                # if indx.column() == 4:
                #     self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def dispTotalnums(self, strwhere="1=1"):
        query = QSqlQuery(self.db)
        strsql = "SELECT count(*) FROM mentalmodel where " + strwhere
        ret= query.exec_(strsql)
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

    def findMental(self):
        name        = self.nameEdit.text()
        ppid        = self.ppidEdit.text()
        county      = self.countyCombo.currentText()
        strwhere    = "name like '%%%s%%' and ppid like '%%%s%%' and county like '%%%s%%'" % (name, ppid, county)

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Mentaldate)=%d" % yeardate
        # else:
        #     strwhere = "Mentaldate > '%s' and Mentaldate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.MentalModel.setFilter(strwhere)
        self.MentalModel.select()

        self.dispTotalnums(strwhere)

        # self.MentalModel.setFilter("")

    def applyMental(self):
        index = self.MentalView.currentIndex()
        row = index.row()
        mentalid = self.MentalModel.data(self.MentalModel.index(row, 0))

        lstwillapply = [mentalid]

        curTabText = "住院申请"

        parentTabWidget = self.parent().parentWidget()
        for tabindx in list(range(0, parentTabWidget.count())):
            widget = parentTabWidget.widget(tabindx)            
            if type(widget)==ApplyDlg:
                widget.setWillApply(lstwillapply) #设置即将申请的人员id
                widget.newApply()
                parentTabWidget.setCurrentIndex(tabindx)
                return

        widget = ApplyDlg(db=self.db, curuser=self.curuser)
        widget.setWillApply(lstwillapply) #设置即将申请的人员id
        widget.newApply()
        tabindx = parentTabWidget.addTab(widget,curTabText)
        parentTabWidget.setCurrentWidget(widget)

        # query = QSqlQuery(self.db)
        # strsql = "insert into approvalmodel (mental_id) VALUES (%d) " % mentalid
        # ret= query.exec_(strsql)

        # print(mentalid)
        # print(mentalid, ret, '---', strsql)

    def removeMental(self):
        index = self.MentalView.currentIndex()
        row = index.row()
        if row != -1:
            ppname = self.MentalModel.data(self.MentalModel.index(row, 1))
            if QMessageBox.question(self, "删除确认", "是否要删除当前选中记录？\n\n姓名：%s\n\n" % ppname, "确定", "取消") == 0:
                self.MentalModel.removeRows(row, 1)
                self.MentalModel.submitAll()
                self.MentalModel.database().commit()

                self.infoLabel.setText("")

        # print("nameid")
        
    def revertMental(self):
        self.MentalModel.revertAll()
        self.MentalModel.database().rollback()
        self.infoLabel.setText("")

    def newMental(self):
        # self.MentalModel.setFilter("1=1")
        row = self.MentalModel.rowCount()
        self.MentalModel.insertRow(row)

        # theLastIndex = self.MentalModel.index(row, 1)
        # self.MentalView.scrollTo(theLastIndex)
        self.MentalView.scrollToBottom()
        self.MentalModel.setData(self.MentalModel.index(row, 15), "某某") #set default password
        self.infoLabel.setText("")
        # self.MentalModel.setData(self.MentalModel.index(row, 2), "123456") #set default password

    def saveMental(self):
        self.MentalModel.database().transaction()
        if self.MentalModel.submitAll():
            self.MentalModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.MentalModel.revertAll()
            self.MentalModel.database().rollback()
            # print("save fail!  ->rollback")

        self.MentalModel.setFilter("1=1")
        self.infoLabel.setText("")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.MentalModel.setItem(0, 0, tmpitem)
        # print(self.MentalModel.database())
        # print("saveMental")
       
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=MentalDlg()
    dialog.show()
    app.exec_()
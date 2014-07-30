from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate

class AdaptDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(AdaptDlg,self).__init__(parent)

        # widget = QWidget()               

        # self.setCentralWidget(widget)
        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        # headers = ["月份", "适配人数", "适配件数", "是否确认"]

        self.AdaptView = QTableView()
        self.AdaptModel = QSqlTableModel(self.AdaptView)
        self.AdaptModel.setTable("Adaptstat")
        self.AdaptModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.AdaptModel.setQuery(QSqlQuery("select unitsn, unitname, unitclass, unitpp from Adapt"))
        self.AdaptModel.select()
        # self.AdaptModel.removeColumn(2)
        # self.AdaptModel.removeColumn(0)
        self.AdaptModel.setHeaderData(1, Qt.Horizontal, "截止日期")
        self.AdaptModel.setHeaderData(2, Qt.Horizontal, "适配人数")
        self.AdaptModel.setHeaderData(3, Qt.Horizontal, "适配件数")
        self.AdaptModel.setHeaderData(4, Qt.Horizontal, "是否确认")

        # self.AdaptModel = QStandardItemModel(0, 0, self.AdaptView)
        # self.AdaptModel.setHorizontalHeaderLabels(headers)
        self.AdaptView.setModel(self.AdaptModel)
        self.AdaptView.setColumnHidden(0, True) # hide sn
        # self.AdaptView.setColumnHidden(4, True) # hide over
        # print(2)
        dateDelegate = DateDelegate(self)
        yesnoDelegate = ComboBoxDelegate(self, ["是", "否"])
        self.AdaptView.setItemDelegateForColumn(1, dateDelegate)
        # self.AdaptView.setItemDelegateForColumn(4, yesnodelegate)

        self.AdaptView.setItemDelegateForColumn(4, yesnoDelegate)
        # print(yesnodelegate)


        self.AdaptView.setStyleSheet("QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        # self.AdaptView.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.AdaptView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.AdaptView.horizontalHeader().setStyleSheet("color: red");
        # self.AdaptView.verticalHeader().hide()
        self.AdaptView.verticalHeader().setFixedWidth(30)
        self.AdaptView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.AdaptView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.AdaptView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        newusrbtn       = QPushButton("新增")
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        btnbox.addButton(newusrbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel("", alignment=Qt.AlignLeft)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

        # bottomFiller = QWidget()
        # bottomFiller.setSizePolicy(QSizePolicy.Expanding,
        #         QSizePolicy.Expanding)

        # callerLabel = QLabel("&Caller:")
        # self.callerEdit = QLineEdit()
        # callerLabel.setBuddy(self.callerEdit)
        today = QDate.currentDate()

        self.yearCheckbox = QCheckBox("按年份")
        # self.yearCheckbox.setStyleSheet("font-size:14px; text-align:right;")
        self.yearDateTime = QDateTimeEdit()
        self.yearDateTime = QDateTimeEdit()
        self.yearDateTime.setDate(today)
        self.yearDateTime.setDisplayFormat('yyyy')
        self.yearDateTime.setEnabled(False)

        startLabel = QLabel("起始月份:")
        self.startDateTime = QDateTimeEdit()
        startLabel.setBuddy(self.startDateTime)
        # self.startDateTime.setSelectedSection(QDateTimeEdit.MonthSection | QDateTimeEdit.YearSection)
        self.startDateTime.setDate(today)
        # self.startDateTime.setDateRange(today, today)
        self.startDateTime.setDisplayFormat(DATETIME_FORMAT)
        # self.startDateTime.setCalendarPopup(True)
        # self.startDateTime.setCurrentSection(QDateTimeEdit.MonthSection)

        endLabel = QLabel("截止月份:")
        self.endDateTime = QDateTimeEdit()
        endLabel.setBuddy(self.endDateTime)
        self.endDateTime.setDate(today)
        # self.endDateTime.setCalendarPopup(True)
        # self.endDateTime.setDateRange(today, today)
        self.endDateTime.setDisplayFormat(DATETIME_FORMAT)
        findbutton = QPushButton("查询")
        # findbutton.setIcon(QIcon(":/first.png"))

        findbox = QHBoxLayout()
        findbox.setMargin(10)
        findbox.setAlignment(Qt.AlignHCenter);
        # findbox.addWidget(self.callerEdit)
        findbox.addWidget(self.yearCheckbox)
        findbox.addWidget(self.yearDateTime)
        findbox.addSpacing(20)
        findbox.addWidget(startLabel)
        findbox.addWidget(self.startDateTime)
        findbox.addWidget(endLabel)
        findbox.addWidget(self.endDateTime)
        findbox.addWidget(findbutton)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addLayout(findbox)
        vbox.addWidget(self.AdaptView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveAdapt)
        newusrbtn.clicked.connect(self.newAdapt)
        revertbtn.clicked.connect(self.revertAdapt)
        removebtn.clicked.connect(self.removeAdapt)
        findbutton.clicked.connect(self.findAdapt)
        self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.AdaptView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveAdapt)
        self.dispTotalnums()
        # self.AdaptView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.AdaptView.doubleClicked.connect(self.dbclick)

    def dbclick(self, indx):
        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitclass"] == "辅具中心":
                if indx.sibling(indx.row(),4).data() == "是":
                    self.AdaptView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.AdaptView.setEditTriggers(QAbstractItemView.DoubleClicked)

                if indx.column() == 4:
                    self.AdaptView.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def yearCheck(self):
        if self.yearCheckbox.isChecked():
            self.startDateTime.setEnabled(False)
            self.endDateTime.setEnabled(False)
            self.yearDateTime.setEnabled(True)
        else:
            self.startDateTime.setEnabled(True)
            self.endDateTime.setEnabled(True)
            self.yearDateTime.setEnabled(False)

    def dispTotalnums(self, strwhere="1=1"):
        query = QSqlQuery(self.db)
        strsql = "SELECT sum(adaptpersons), sum(adapttools) FROM Adaptstat where " + strwhere
        ret= query.exec_(strsql);
        # print(ret, "~~~~~~~", strsql)
        total_personnums = 0
        total_toolnums = 0
        while query.next():
            if type(query.value(0))== QPyNullVariant:
                break
            total_personnums += query.value(0)
            total_toolnums   += query.value(1)
            # print(query.value(0), query.value(1))

        # print(total_personnums, total_toolnums, "==")
        self.infoLabel.setText("合计：适配人数 <font color='red'>%d</font> ，总件数 <font color='red'>%d</font> 。" % (int(total_personnums), int(total_toolnums)))

    def findAdapt(self):
        yeardate  = self.yearDateTime.date().year()
        startdate = self.startDateTime.date().toPyDate()
        # print(startdate)
        startdate = (startdate - datetime.timedelta(startdate.day-1)).isoformat()
        enddate   = self.endDateTime.date().addMonths(1).toPyDate()
        enddate   = (enddate - datetime.timedelta(enddate.day-1)).isoformat()

        if self.yearCheckbox.isChecked():
            strwhere = "year(adaptdate)=%d" % yeardate
        else:
            strwhere = "adaptdate > '%s' and adaptdate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.AdaptModel.setFilter(strwhere)
        self.AdaptModel.select()

        self.dispTotalnums(strwhere)

        # self.AdaptModel.setFilter("")

    def removeAdapt(self):
        index = self.AdaptView.currentIndex()
        row = index.row()
        nameid = self.AdaptModel.data(self.AdaptModel.index(row, 0))
        self.AdaptModel.removeRows(row, 1)
        self.AdaptModel.submitAll()
        self.AdaptModel.database().commit()

        self.infoLabel.setText("")

        # print("nameid")
        
    def revertAdapt(self):
        self.AdaptModel.revertAll()
        self.AdaptModel.database().rollback()
        self.infoLabel.setText("")

    def newAdapt(self):
        # self.AdaptModel.setFilter("1=1")
        row = self.AdaptModel.rowCount()
        self.AdaptModel.insertRow(row)
        self.AdaptModel.setData(self.AdaptModel.index(row, 4), "否") #set default password
        self.infoLabel.setText("")
        # self.AdaptModel.setData(self.AdaptModel.index(row, 2), "123456") #set default password

    def saveAdapt(self):
        self.AdaptModel.database().transaction()
        if self.AdaptModel.submitAll():
            self.AdaptModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.AdaptModel.revertAll()
            self.AdaptModel.database().rollback()
            # print("save fail!  ->rollback")

        self.AdaptModel.setFilter("1=1")
        self.infoLabel.setText("")
        # model->database().transaction();
        # tmpitem = QStandardItem("张三")
        # self.AdaptModel.setItem(0, 0, tmpitem)
        # print(self.AdaptModel.database())
        # print("saveAdapt")
       
        
if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=AdaptDlg()
    dialog.show()
    app.exec_()
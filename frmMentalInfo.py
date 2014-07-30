from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate

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
        # self.MentalModel.setHeaderData(1, Qt.Horizontal, "截止日期")
        # self.MentalModel.setHeaderData(2, Qt.Horizontal, "适配人数")
        # self.MentalModel.setHeaderData(3, Qt.Horizontal, "适配件数")
        # self.MentalModel.setHeaderData(4, Qt.Horizontal, "是否确认")

        # self.MentalModel = QStandardItemModel(0, 0, self.MentalView)
        # self.MentalModel.setHorizontalHeaderLabels(headers)
        self.MentalView.setModel(self.MentalModel)
        self.MentalView.setColumnHidden(0, True) # hide sn
        # self.MentalView.setColumnHidden(4, True) # hide over
        # print(2)
        dateDelegate = DateDelegate(self)
        yesnoDelegate = ComboBoxDelegate(self, ["是", "否"])
        self.MentalView.setItemDelegateForColumn(1, dateDelegate)
        # self.MentalView.setItemDelegateForColumn(4, yesnodelegate)

        self.MentalView.setItemDelegateForColumn(4, yesnoDelegate)
        # print(yesnodelegate)


        self.MentalView.setStyleSheet("QTableView::item:hover {background-color: rgba(100,200,220,100);} ")
        # self.MentalView.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.MentalView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.MentalView.horizontalHeader().setStyleSheet("color: red");
        # self.MentalView.verticalHeader().hide()
        self.MentalView.verticalHeader().setFixedWidth(30)
        self.MentalView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.MentalView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.MentalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        vbox.addWidget(self.MentalView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveMental)
        newusrbtn.clicked.connect(self.newMental)
        revertbtn.clicked.connect(self.revertMental)
        removebtn.clicked.connect(self.removeMental)
        findbutton.clicked.connect(self.findMental)
        self.yearCheckbox.stateChanged.connect(self.yearCheck)
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
            if self.curuser["unitgroup"] == "辅具中心":
                if indx.sibling(indx.row(),4).data() == "是":
                    self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.MentalView.setEditTriggers(QAbstractItemView.DoubleClicked)

                if indx.column() == 4:
                    self.MentalView.setEditTriggers(QAbstractItemView.NoEditTriggers)


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
        strsql = "SELECT sum(Mentalpersons), sum(Mentaltools) FROM Mentalstat where " + strwhere
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

    def findMental(self):
        yeardate  = self.yearDateTime.date().year()
        startdate = self.startDateTime.date().toPyDate()
        # print(startdate)
        startdate = (startdate - datetime.timedelta(startdate.day-1)).isoformat()
        enddate   = self.endDateTime.date().addMonths(1).toPyDate()
        enddate   = (enddate - datetime.timedelta(enddate.day-1)).isoformat()

        if self.yearCheckbox.isChecked():
            strwhere = "year(Mentaldate)=%d" % yeardate
        else:
            strwhere = "Mentaldate > '%s' and Mentaldate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.MentalModel.setFilter(strwhere)
        self.MentalModel.select()

        self.dispTotalnums(strwhere)

        # self.MentalModel.setFilter("")

    def removeMental(self):
        index = self.MentalView.currentIndex()
        row = index.row()
        nameid = self.MentalModel.data(self.MentalModel.index(row, 0))
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
        self.MentalModel.setData(self.MentalModel.index(row, 4), "否") #set default password
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
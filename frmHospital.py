from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate, PhoneDelegate, PersonIdDelegate, HospitalOkDelegate, HospitalOutDateDelegate

class HospitalDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(HospitalDlg,self).__init__(parent)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        self.HospitalView = QTableView()
        self.HospitalModel = QSqlRelationalTableModel(self.HospitalView)
        self.HospitalModel.setTable("approvalmodel")
        self.HospitalModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.HospitalModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.HospitalModel.select()
        for indx, iheader in enumerate(LST_APPROVALHEADER):
            self.HospitalModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.HospitalView.setModel(self.HospitalModel)
        self.HospitalView.setColumnHidden(0, True) # hide sn

        hideColList = [3,4,5,6,7,11,12,15,16,17]
        hideColList.extend(list(range(23,43)))
        for icol in hideColList:
            self.HospitalView.setColumnHidden(icol, True) # hide sn

        self.HospitalView.setColumnWidth(1, 150)
        # self.HospitalView.setColumnWidth(4, 120)
        # self.HospitalView.setColumnHidden(15, True) # hide sn

        # self.HospitalView.setItemDelegateForColumn(18, DateDelegate(self))
        self.HospitalView.setItemDelegateForColumn(18, HospitalOutDateDelegate(self, {19:"已确认", 20:'ccc'}))
        # self.HospitalView.setItemDelegateForColumn(19, HospitalOkDelegate(self, SAVEOK_CHOICES, {20:'aaa'}))
        self.HospitalView.setItemDelegateForColumn(19, ComboBoxDelegate(self, SAVEOK_CHOICES))
        self.HospitalView.setItemDelegateForColumn(21, HospitalOutDateDelegate(self, {22:'ccc'}, 'calc'))
        
        self.HospitalView.setAlternatingRowColors(True)
        self.HospitalView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 

        # self.HospitalView.setStyleSheet()
        # self.HospitalView.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.HospitalView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.HospitalView.horizontalHeader().setStyleSheet("color: red");
        # self.HospitalView.verticalHeader().hide()
        # self.HospitalView.verticalHeader().setFixedWidth(30)
        self.HospitalView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.HospitalView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.HospitalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        # removebtn       = QPushButton("删除")
        # Hospitalbtn     = QPushButton("批准")

        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(Hospitalbtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel("", alignment=Qt.AlignLeft)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)


        nameLabel       = QLabel("姓名:")
        self.nameEdit   = QLineEdit()
        regExp = QRegExp("[^']*")
        self.nameEdit.setValidator(QRegExpValidator(regExp, self))
        nameLabel.setBuddy(self.nameEdit)

        periodLabel      = QLabel("救助疗程:")
        self.periodCombo = QComboBox(self)
        self.periodCombo.addItems(PERIOD_CHOICES)
        self.periodCombo.insertItem(0, "")
        self.periodCombo.setCurrentIndex(0)
        periodLabel.setBuddy(self.periodCombo)

        isInHospitalLabel      = QLabel("是否入院:")
        self.isInHospitalCombo = QComboBox(self)
        self.isInHospitalCombo.addItems(SAVEOK_CHOICES)
        self.isInHospitalCombo.insertItem(0, "")
        self.isInHospitalCombo.setCurrentIndex(0)
        isInHospitalLabel.setBuddy(self.isInHospitalCombo)


        findbutton = QPushButton("查询")
        # findbutton.setIcon(QIcon(":/first.png"))

        findbox = QHBoxLayout()
        findbox.setMargin(10)
        findbox.setAlignment(Qt.AlignHCenter);
        findbox.addStretch (10)
        findbox.addWidget(nameLabel)
        findbox.addWidget(self.nameEdit)
        findbox.addStretch (10)
        findbox.addWidget(periodLabel)
        findbox.addWidget(self.periodCombo)
        findbox.addStretch (10)
   
        findbox.addWidget(isInHospitalLabel)
        findbox.addWidget(self.isInHospitalCombo)
        findbox.addWidget(findbutton)
        findbox.addStretch (10)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addLayout(findbox)
        vbox.addWidget(self.HospitalView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveHospital)
        revertbtn.clicked.connect(self.revertHospital)
        # removebtn.clicked.connect(self.removeHospital)

        findbutton.clicked.connect(self.findHospital)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.HospitalView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveHospital)
        # self.dispTotalnums()
        # self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.HospitalView.doubleClicked.connect(self.dbclick)

        # self.HospitalModel.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), self.HospitalModel.index(1, 5), self.HospitalModel.index(1, 5))

        # self.HospitalView.dataChanged.connect(self.HospitalItemChange)

    # def dataChanged(self, topleft, bottomright):
    #     print(topleft.data())
        # QAbstractItemView.dataChanged(topleft, bottomright)
        # print(topleft, '2')
        # print(topleft.column() )
        # print(topleft.data(), bottomright.sibling(indx.row(),15))

    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        # print(indx)
        
        if indx.column() in [1,2,8,9,10,11,12,13,14,20,22]:
            self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.HospitalView.setEditTriggers(QAbstractItemView.DoubleClicked)

        # self.connect(self.HospitalModel, SIGNAL('dataChanged(QModelIndex,QModelIndex)'), SLOT(self.dataChanged(indx,indx)))
        # if indx.sibling(indx.row(),15).data() == "同意":
        #     self.HospitalModel.setData(self.HospitalModel.index(indx.row(), 1), 'aaaa2004')



        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitgroup"] == "市残联":
                if indx.column() == 1:
                    self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.HospitalView.setEditTriggers(QAbstractItemView.DoubleClicked)
            else:
                self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # if indx.sibling(indx.row(),4).data() == "是":
                #     self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # else:
                #     self.HospitalView.setEditTriggers(QAbstractItemView.DoubleClicked)

                # if indx.column() == 4:
                #     self.HospitalView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def findHospital(self):
        name                = self.nameEdit.text()
        period              = self.periodCombo.currentText()
        isInHospital        = self.isInHospitalCombo.currentText()

        strwhere0 = " relTblAl_2.name like '%%%s%%' " % name

        if period == "":
            strwhere1 = " 1=1 "
        else:
            strwhere1 = " period = '%s' " % period

        if isInHospital == "":
            strwhere2 = " 1=1 "
        else:
            if isInHospital == "未确认":
                strwhere2 = " saveok = '%s' or saveok is NULL " % isInHospital 
            else:
                strwhere2 = " saveok = '%s' " % isInHospital

        strwhere    = " and ".join([strwhere0, strwhere1, strwhere2])

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Hospitaldate)=%d" % yeardate
        # else:
        #     strwhere = "Hospitaldate > '%s' and Hospitaldate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.HospitalModel.setFilter(strwhere)
        self.HospitalModel.select()
        # print(self.HospitalModel.selectStatement())

        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(self.HospitalModel.rowCount()))

        # self.HospitalModel.setFilter("")


    def revertHospital(self):
        self.HospitalModel.revertAll()
        self.HospitalModel.database().rollback()
        self.infoLabel.setText("")

    def saveHospital(self):
        self.HospitalModel.database().transaction()
        if self.HospitalModel.submitAll():
            # print(self.HospitalModel.selectStatement(), "--")
            self.HospitalModel.database().commit()
            # print("save success!  ->commit")
            # print(12131)
        else:
            # print(2)
            self.HospitalModel.revertAll()
            self.HospitalModel.database().rollback()
            # print("save fail!  ->rollback")

        self.findHospital()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=HospitalDlg()
    dialog.show()
    app.exec_()
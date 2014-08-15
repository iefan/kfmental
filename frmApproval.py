from resources import *

from cc_delegate import ComboBoxDelegate, DateDelegate, PhoneDelegate, PersonIdDelegate

class ApprovalDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(ApprovalDlg,self).__init__(parent)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

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

        self.ApprovalView.setItemDelegateForColumn(8,  ComboBoxDelegate(self, HOSPITAL_CHOICES))
        self.ApprovalView.setItemDelegateForColumn(9,  ComboBoxDelegate(self, PERIOD_CHOICES))
        self.ApprovalView.setItemDelegateForColumn(10, ComboBoxDelegate(self, YESNO_CHOICES))
        self.ApprovalView.setItemDelegateForColumn(12, ComboBoxDelegate(self, CONTINUE_CHOICES))
        self.ApprovalView.setItemDelegateForColumn(13, DateDelegate(self))
        self.ApprovalView.setItemDelegateForColumn(14, DateDelegate(self))
        self.ApprovalView.setItemDelegateForColumn(15, ComboBoxDelegate(self, ISAPPROVAL_CHOICES))
        self.ApprovalView.setItemDelegateForColumn(16, DateDelegate(self))
        
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
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        removebtn       = QPushButton("删除")
        approvalbtn     = QPushButton("批准")

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
        
        hospitalLabel      = QLabel("医疗机构:")
        self.hospitalCombo = QComboBox(self)
        self.hospitalCombo.addItems(HOSPITAL_CHOICES)
        self.hospitalCombo.insertItem(0, "")
        self.hospitalCombo.setCurrentIndex(0)
        hospitalLabel.setBuddy(self.hospitalCombo)

        periodLabel      = QLabel("救助疗程:")
        self.periodCombo = QComboBox(self)
        self.periodCombo.addItems(PERIOD_CHOICES)
        self.periodCombo.insertItem(0, "")
        self.periodCombo.setCurrentIndex(0)
        periodLabel.setBuddy(self.periodCombo)

        foodLabel      = QLabel("伙食补助:")
        self.foodCombo = QComboBox(self)
        self.foodCombo.addItems(YESNO_CHOICES)
        self.foodCombo.insertItem(0, "")
        self.foodCombo.setCurrentIndex(0)
        foodLabel.setBuddy(self.hospitalCombo)

        approvalresultLabel      = QLabel("审核结果:")
        self.approvalresultCombo = QComboBox(self)
        self.approvalresultCombo.addItems(ISAPPROVAL_CHOICES)
        self.approvalresultCombo.insertItem(0, "")
        self.approvalresultCombo.setCurrentIndex(0)
        approvalresultLabel.setBuddy(self.approvalresultCombo)


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
        findbox.addWidget(hospitalLabel)
        findbox.addWidget(self.hospitalCombo)
        findbox.addStretch (10)
        findbox.addWidget(periodLabel)
        findbox.addWidget(self.periodCombo)
        findbox.addStretch (10)
        findbox.addWidget(foodLabel)
        findbox.addWidget(self.foodCombo)
        findbox.addStretch (10)
        findbox.addWidget(approvalresultLabel)
        findbox.addWidget(self.approvalresultCombo)
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

        # self.ApprovalModel.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), self.ApprovalModel.index(1, 5), self.ApprovalModel.index(1, 5))

        # self.ApprovalView.dataChanged.connect(self.approvalItemChange)

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
        
        if indx.column() in [1,2,3,4,5,6,7,17]:
            self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.ApprovalView.setEditTriggers(QAbstractItemView.DoubleClicked)

        # self.connect(self.ApprovalModel, SIGNAL('dataChanged(QModelIndex,QModelIndex)'), SLOT(self.dataChanged(indx,indx)))
        # if indx.sibling(indx.row(),15).data() == "同意":
        #     self.ApprovalModel.setData(self.ApprovalModel.index(indx.row(), 1), 'aaaa2004')



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

    def findApproval(self):
        name                = self.nameEdit.text()
        hospital            = self.hospitalCombo.currentText()
        period              = self.periodCombo.currentText()
        foodallow           = self.foodCombo.currentText()
        approvalresult      = self.approvalresultCombo.currentText()
        strwhere    = "relTblAl_2.name like '%%%s%%' and \
                (hospital like '%%%s%%' or hospital is NULL) and \
                (period like '%%%s%%' or period is NULL) and \
                (foodallow like '%%%s%%' or foodallow is NULL ) and \
                (isapproval like '%%%s%%' or isapproval is NULL)" % \
                (name, hospital, period, foodallow, approvalresult)

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Approvaldate)=%d" % yeardate
        # else:
        #     strwhere = "Approvaldate > '%s' and Approvaldate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.ApprovalModel.setFilter(strwhere)
        self.ApprovalModel.select()

        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(self.ApprovalModel.rowCount()))

        # self.ApprovalModel.setFilter("")

    def okApproval(self):
        index = self.ApprovalView.currentIndex()
        row = index.row()
        hospital = self.ApprovalModel.data(self.ApprovalModel.index(row, 8))
        period   = self.ApprovalModel.data(self.ApprovalModel.index(row, 9))
        food     = self.ApprovalModel.data(self.ApprovalModel.index(row, 10))
        startdate= self.ApprovalModel.data(self.ApprovalModel.index(row, 13))
        enddate  = self.ApprovalModel.data(self.ApprovalModel.index(row, 14))
        if type(hospital)==QPyNullVariant or type(period)==QPyNullVariant or type(food)==QPyNullVariant or type(startdate)==QDate or type(enddate)==QDate:
            QMessageBox.warning(self, "提醒", "仍有审批项目未正确填写!")
            return
        if self.curuser == {}:
            approvalman = "某某"
        else:
            approvalman = self.unitman
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 1), datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 11), 1) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 12), "") 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 15), '同意') #set default password
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 16), QDate.currentDate()) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 17), approvalman) 

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

    def saveApproval(self):
        self.ApprovalModel.database().transaction()
        if self.ApprovalModel.submitAll():
            self.ApprovalModel.database().commit()
            # print("save success!  ->commit")
        else:
            self.ApprovalModel.revertAll()
            self.ApprovalModel.database().rollback()
            # print("save fail!  ->rollback")

        self.findApproval()

        # self.ApprovalModel.setFilter("1=1")
        # self.infoLabel.setText("")
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
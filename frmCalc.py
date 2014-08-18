from resources import *
from cc_delegate import *

class CalcDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(CalcDlg,self).__init__(parent)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        self.CalcView = QTableView()
        self.CalcModel = QSqlRelationalTableModel(self.CalcView)
        self.CalcModel.setTable("approvalmodel")
        self.CalcModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.CalcModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.CalcModel.select()
        for indx, iheader in enumerate(LST_APPROVALHEADER):
            self.CalcModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.CalcView.setModel(self.CalcModel)
        self.CalcView.setColumnHidden(0, True) # hide sn

        hideColList = [3,4,5,6,7,8,9,11,12,13,14,15,16,17,19,20,22]
        # hideColList.extend(list(range(25,43)))
        for icol in hideColList:
            self.CalcView.setColumnHidden(icol, True) # hide sn

        self.CalcView.setColumnWidth(1, 150)
        # self.CalcView.setColumnWidth(4, 120)
        # self.CalcView.setColumnHidden(15, True) # hide sn

        self.CalcView.setItemDelegateForColumn(31, ComboBoxDelegate(self, INSU_CHOICES))
        self.CalcView.setItemDelegateForColumn(35, HospitalOutDateDelegate(self, {36:'ddd'}))
        
        self.CalcView.setAlternatingRowColors(True)
        self.CalcView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 

        self.CalcView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.CalcView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.CalcView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        # removebtn       = QPushButton("删除")
        # Calcbtn     = QPushButton("批准")

        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(Calcbtn, QDialogButtonBox.ActionRole);

        self.infoLabel = QLabel("", alignment=Qt.AlignLeft)
        self.infoLabel.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)


        nameLabel       = QLabel("姓名:")
        self.nameEdit   = QLineEdit()
        regExp = QRegExp("[^']*")
        self.nameEdit.setValidator(QRegExpValidator(regExp, self))
        nameLabel.setBuddy(self.nameEdit)

        isEnterFileLabel      = QLabel("是否核结:")
        self.isEnterFileCombo = QComboBox(self)
        self.isEnterFileCombo.addItems(YESNO_CHOICES)
        self.isEnterFileCombo.insertItem(0, "")
        self.isEnterFileCombo.setCurrentIndex(0)
        isEnterFileLabel.setBuddy(self.isEnterFileCombo)


        findbutton = QPushButton("查询")
        # findbutton.setIcon(QIcon(":/first.png"))

        findbox = QHBoxLayout()
        findbox.setMargin(10)
        findbox.setAlignment(Qt.AlignHCenter);
        findbox.addStretch (10)
        findbox.addWidget(nameLabel)
        findbox.addWidget(self.nameEdit)
        findbox.addStretch (10)
        findbox.addWidget(isEnterFileLabel)
        findbox.addWidget(self.isEnterFileCombo)
        findbox.addWidget(findbutton)
        findbox.addStretch (10)

        vbox = QVBoxLayout()
        vbox.setMargin(5)
        vbox.addLayout(findbox)
        vbox.addWidget(self.CalcView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveCalc)
        revertbtn.clicked.connect(self.revertCalc)
        # removebtn.clicked.connect(self.removeCalc)

        findbutton.clicked.connect(self.findCalc)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.CalcView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveCalc)
        # self.dispTotalnums()
        # self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.CalcView.doubleClicked.connect(self.dbclick)

        # self.CalcModel.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), self.CalcModel.index(1, 5), self.CalcModel.index(1, 5))

        # self.CalcView.dataChanged.connect(self.CalcItemChange)

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
        
        if indx.column() in [1,2,8,9,10,11,12,13,14,18,20,36,37,38,39,40,41,42,43]:
            self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.CalcView.setEditTriggers(QAbstractItemView.DoubleClicked)

        # self.connect(self.CalcModel, SIGNAL('dataChanged(QModelIndex,QModelIndex)'), SLOT(self.dataChanged(indx,indx)))
        # if indx.sibling(indx.row(),15).data() == "同意":
        #     self.CalcModel.setData(self.CalcModel.index(indx.row(), 1), 'aaaa2004')



        #当已经申核完结时，锁定当前item，禁止编辑，主要通过全局的 setEditTriggers 来设置。
        if self.curuser != {}:
            if self.curuser["unitgroup"] == "市残联":
                if indx.column() == 1:
                    self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                else:
                    self.CalcView.setEditTriggers(QAbstractItemView.DoubleClicked)
            else:
                self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)

                # if indx.sibling(indx.row(),4).data() == "是":
                #     self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # else:
                #     self.CalcView.setEditTriggers(QAbstractItemView.DoubleClicked)

                # if indx.column() == 4:
                #     self.CalcView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def findCalc(self):
        name                = self.nameEdit.text()
        isEnterFile         = self.isEnterFileCombo.currentText()

        strwhere0 = " relTblAl_2.name like '%%%s%%' " % name

        if isEnterFile == "":
            strwhere1 = " 1=1 "
        else:
            if isEnterFile == "是":
                strwhere1 = " enterfiledate IS NOT NULL "
            else:
                strwhere1 = " enterfiledate IS NULL "

        strwhere    = " and ".join([strwhere0,  strwhere2])

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Calcdate)=%d" % yeardate
        # else:
        #     strwhere = "Calcdate > '%s' and Calcdate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.CalcModel.setFilter(strwhere)
        self.CalcModel.select()
        # print(self.CalcModel.selectStatement())

        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(self.CalcModel.rowCount()))

        # self.CalcModel.setFilter("")


    def revertCalc(self):
        self.CalcModel.revertAll()
        self.CalcModel.database().rollback()
        self.infoLabel.setText("")

    def saveCalc(self):
        self.CalcModel.database().transaction()
        if self.CalcModel.submitAll():
            # print(self.CalcModel.selectStatement(), "--")
            self.CalcModel.database().commit()
            # print("save success!  ->commit")
            # print(12131)
        else:
            # print(2)
            self.CalcModel.revertAll()
            self.CalcModel.database().rollback()
            # print("save fail!  ->rollback")

        self.findCalc()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=CalcDlg()
    dialog.show()
    app.exec_()
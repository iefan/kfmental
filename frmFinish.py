from resources import *
from cc_delegate import *

class FinishDlg(QDialog):
    def __init__(self,parent=None, db="", curuser={}):
        super(FinishDlg,self).__init__(parent)

        if db == "":
            self.db = globaldb()
        else:
            self.db = db

        self.curuser = curuser

        self.FinishView = QTableView()
        self.FinishModel = QSqlRelationalTableModel(self.FinishView)
        self.FinishModel.setTable("approvalmodel")
        self.FinishModel.setRelation(2, QSqlRelation("mentalmodel", "id", "name"));
        self.FinishModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        # self.FinishModel.select()
        for indx, iheader in enumerate(LST_APPROVALHEADER):
            self.FinishModel.setHeaderData(indx+1, Qt.Horizontal, iheader)
    
        self.FinishView.setModel(self.FinishModel)
        self.FinishView.setColumnHidden(0, True) # hide sn

        hideColList = [3,4,5,6,7,8,9,11,12,13,14,15,16,17,19,20,22]
        # hideColList.extend(list(range(25,43)))
        for icol in hideColList:
            self.FinishView.setColumnHidden(icol, True) # hide sn

        self.FinishView.setColumnWidth(1, 150)
        [self.FinishView.setColumnWidth(icol, 70) for icol in [2,10,23,24,25,26,27,28,29,30,32,33,34]]
        # self.FinishView.setColumnWidth(4, 120)
        # self.FinishView.setColumnHidden(15, True) # hide sn

        # self.FinishView.setItemDelegateForColumn(31, ComboBoxDelegate(self, INSU_CHOICES))
        self.FinishView.setItemDelegateForColumn(41, HospitalOutDateDelegate(self, {42:'ddd'}))
        
        self.FinishView.setAlternatingRowColors(True)
        self.FinishView.setStyleSheet("QTableView{background-color: rgb(250, 250, 115);"  
                    "alternate-background-color: rgb(141, 163, 215);}"
                    "QTableView::item:hover {background-color: rgba(100,200,220,100);} ") 

        self.FinishView.verticalHeader().setStyleSheet("color: red;font-size:20px; ");
        self.FinishView.setStyleSheet("font-size:14px; ");
        # print(4)
       
        self.FinishView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        btnbox = QDialogButtonBox(Qt.Horizontal)
        savebtn         = QPushButton("保存")
        revertbtn       = QPushButton("撤销")
        # removebtn       = QPushButton("删除")
        # Finishbtn     = QPushButton("批准")

        btnbox.addButton(savebtn, QDialogButtonBox.ActionRole);
        btnbox.addButton(revertbtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(removebtn, QDialogButtonBox.ActionRole);
        # btnbox.addButton(Finishbtn, QDialogButtonBox.ActionRole);

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
        vbox.addWidget(self.FinishView)
        vbox.addWidget(self.infoLabel)
        vbox.addWidget(btnbox)
        self.setLayout(vbox)

        savebtn.clicked.connect(self.saveFinish)
        revertbtn.clicked.connect(self.revertFinish)
        # removebtn.clicked.connect(self.removeFinish)

        findbutton.clicked.connect(self.findFinish)
        # self.yearCheckbox.stateChanged.connect(self.yearCheck)
        # self.FinishView.clicked.connect(self.tableClick)
        # self.connect(savebtn, SIGNAL('clicked()'), self.saveFinish)
        # self.dispTotalnums()
        # self.FinishView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.FinishView.doubleClicked.connect(self.dbclick)
        self.findFinish()

    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        lstnotedit = list(range(1,43))
        lstnotedit.remove(41)
        # print(indx.column())
        if indx.column() in lstnotedit:
            self.FinishView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.FinishView.setEditTriggers(QAbstractItemView.DoubleClicked)
       

    def findFinish(self):
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

        strwhere    = " and ".join([strwhere0,  strwhere1])
        strwhere    += " and dateclose IS NOT NULL "

        # if self.yearCheckbox.isChecked():
        #     strwhere = "year(Finishdate)=%d" % yeardate
        # else:
        #     strwhere = "Finishdate > '%s' and Finishdate < '%s' " % (startdate, enddate)
        # print(strwhere)
        # print(startdate, enddate, yeardate)
        self.FinishModel.setFilter(strwhere)
        self.FinishModel.select()
        # print(self.FinishModel.selectStatement())

        self.infoLabel.setText("合计：当前查询人数 <font color='red'>%d</font> " % int(self.FinishModel.rowCount()))

        # self.FinishModel.setFilter("")


    def revertFinish(self):
        self.FinishModel.revertAll()
        self.FinishModel.database().rollback()
        self.infoLabel.setText("")

    def saveFinish(self):
        self.FinishModel.database().transaction()
        if self.FinishModel.submitAll():
            # print(self.FinishModel.selectStatement(), "--")
            self.FinishModel.database().commit()
            # print("save success!  ->commit")
            # print(12131)
        else:
            # print(2)
            self.FinishModel.revertAll()
            self.FinishModel.database().rollback()
            # print("save fail!  ->rollback")

        self.findFinish()

if __name__ == "__main__":
    import sys
    app=QApplication(sys.argv)
    dialog=FinishDlg()
    dialog.show()
    app.exec_()
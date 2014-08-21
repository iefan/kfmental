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

        self.ApprovalView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self.ApprovalView, SIGNAL("customContextMenuRequested(const QPoint &)"), self.show_contextmenu)

        self.popMenu = QMenu(self)
        entry1 = self.popMenu.addAction("导出医疗救助通知单")
        entry1.triggered.connect(self.exportNotice)
        # self.connect(entry1, SIGNAL('triggered()'), self.exportNotice())
        # self.connect(self.ApprovalView.horizontalHeader(), SIGNAL("customContextMenuRequested(QPoint)"), SLOT(self.show_contextmenu))
        # self.ApprovalView.customContextMenuRequested.connect(self.show_contextmenu)

        self.ApprovalView.setColumnHidden(0, True) # hide sn

        hideColList = list(range(18,43))
        hideColList.remove(19)
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

    def exportNotice(self):
        indx = self.ApprovalView.currentIndex()
        # print(indx)
        approvalsn  = indx.sibling(indx.row(),1).data()
        
        # self.ApprovalModel.setQuery()
        query = QSqlQuery(self.db)
        strsql = "select M.county, M.name, M.economic, M.sex, A.period, M.ppid, A.foodallow, A.notifystart, A.notifyend  \
            from mentalmodel as M, approvalmodel as A where M.id=A.mental_id and A.approvalsn='%s'" % approvalsn
        ret= query.exec_(strsql)
        while query.next():
            county      = query.value(0)
            name        = query.value(1)
            economic    = query.value(2)
            sex         = query.value(3)
            period      = query.value(4)
            ppid        = query.value(5)
            foodallow   = query.value(6)
            notifystart = query.value(7).toString('yyyy年MM月dd日')
            notifyend   = query.value(8).toString('yyyy年MM月dd日')


        # from xlrd import open_workbook
        # from xlutils.copy import copy
        # mentalmodel = self.ApprovalModel.relationModel(2)
        # mentalmodel.setFilter('id=%s' % name)

        # record  = self.ApprovalModel.database().record(self.ApprovalModel.tableName())
        # field   = record.field(2);
        # print(record
        # field.value())
        # print('---', self.ApprovalModel.relationModel(2), self.ApprovalModel.relationModel(2).fieldIndex("id"))

        print(approvalsn, county, name,economic, sex, period, ppid, foodallow, notifystart, notifyend)

        from xlwt import Workbook,easyxf
        book = Workbook(encoding='ascii')
            # 'pattern: pattern solid,  fore_colour white;'
        style = easyxf(
            'font: height 280, name 黑体;'
            'align: vertical center, horizontal center;'
            )
        style2 = easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal left;')

        sheet1 = book.add_sheet('住院通知单',cell_overwrite_ok=True)
        sheet1.write(0,7,'存根联', easyxf('font: height 200, name 黑体;align: vertical center, horizontal right;'))
        sheet1.col(7).width = 25*256
        sheet1.write_merge(1,1,1,7, '汕头市残疾人医疗康复救助基金贫困精神病人医疗救助通知单',style)
        sheet1.col(1).width = 26*256
        sheet1.row(1).height_mismatch = 1
        sheet1.row(1).height = 5*256
        sheet1.col(0).width = 10
        sheet1.write(2,1,'医院（中心）：', easyxf('font: height 260, name 仿宋_GB2312; align: vertical center, horizontal right'))
        sheet1.write(3,1,'　　经审核，下列人员符合汕头市残疾人医疗康复救助基金精神病患者住院医疗救助条件，请按照有关规定确认接收治疗：')
        sheet1.row(3).height_mismatch = 1
        sheet1.row(3).height = 4*220
        sheet1.write(4,1,'审批编号：', style2)
        sheet1.row(4).height_mismatch = 1
        sheet1.row(4).height = 3*200
        sheet1.write(5,1,'区县：', style2)
        sheet1.write(6,1,'姓名：', style2)
        sheet1.write(7,1,'性别：', style2)
        sheet1.write(8,1,'通知单有效期：', style2)
        sheet1.write(9,1,'备    注：', style2)
        sheet1.write(10,1,'签发：', style2)
        sheet1.write(6,4,'经济状况：', style2)
        sheet1.write(7,4,'救助疗程：', style2)
        sheet1.write(8,4,'伙食补助：', style2)
        sheet1.write(10,3,'审批时间', style2)
        sheet1.write(10,7,'残联基金专用印章', style2)
        for indx in list(range(5,11)):
            sheet1.row(indx).height_mismatch =1 
            sheet1.row(indx).height=2*256

        book.save('d:/simple.xls')
        



    def show_contextmenu(self,point):
        # print(point, self.mapToParent(point), self.mapToParent(point), self.mapToGlobal(point))
        # print(point, self.mapFromParent(point), self.mapFromParent(point), self.mapFromGlobal(point))
        # print(point, self.ApprovalView.mapToParent(point), self.ApprovalView.mapToParent(point), self.ApprovalView.mapToGlobal(point))
        # print(point, self.ApprovalView.mapFromParent(point), self.ApprovalView.mapFromParent(point), self.ApprovalView.mapFromGlobal(point))
        # indx = self.ApprovalView.indexAt(point)
        # point.setX(point.x()+self.popMenu.width()-10);
        # point.setY(point.y()+self.popMenu.height());
        self.popMenu.exec_(self.ApprovalView.mapToGlobal(point))

    def closeEvent(self, event):
        self.db.close()

    def dbclick(self, indx):
        # print(indx)
        
        if indx.column() in [1,2,3,4,5,6,7,17, 21]:
            self.ApprovalView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            if indx.sibling(indx.row(),21).data() == "已确认":
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

        issaveok = self.ApprovalModel.data(self.ApprovalModel.index(row, 19))
        # print(issaveok)
        if issaveok == "已确认":
            return

        savetimes = self.ApprovalModel.data(self.ApprovalModel.index(row, 11))
        if type(savetimes)== QPyNullVariant:
            savetimes = 1
        else:
            savetimes += 1

        hospital = self.ApprovalModel.data(self.ApprovalModel.index(row, 8))
        period   = self.ApprovalModel.data(self.ApprovalModel.index(row, 9))
        food     = self.ApprovalModel.data(self.ApprovalModel.index(row, 10))
        startdate= self.ApprovalModel.data(self.ApprovalModel.index(row, 13))
        enddate  = self.ApprovalModel.data(self.ApprovalModel.index(row, 14))
        # print(hospital, period, food, startdate, enddate)
        # print(type(startdate)==QDate )
        if type(hospital)==QPyNullVariant or type(period)==QPyNullVariant or type(food)==QPyNullVariant or (type(startdate)==QDate and startdate.isNull()) or (type(enddate)==QDate and enddate.isNull()):
            QMessageBox.warning(self, "提醒", "仍有审批项目未正确填写!")
            return
        if self.curuser == {}:
            approvalman = "某某"
        else:
            approvalman = self.unitman
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 1), datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 11), savetimes) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 12), "") 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 15), '同意') 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 16), QDate.currentDate()) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 17), approvalman) 
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 19), '未确认') 

        if period == "急性":
            self.ApprovalModel.setData(self.ApprovalModel.index(row, 38), 64) #急性64/天，慢性57/天
        else:
            self.ApprovalModel.setData(self.ApprovalModel.index(row, 38), 57) #急性64/天，慢性57/天
        self.ApprovalModel.setData(self.ApprovalModel.index(row, 39), 14) #每天伙食补助14


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
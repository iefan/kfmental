from myimport import *

class PersonIdDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.parent = parent

    def createEditor(self,parent,option,index):
        editor = QLineEdit(parent)
        regExp = QRegExp("^[0-9]{15,17}X?x?$")
        editor.setValidator(QRegExpValidator(regExp, parent))
        editor.installEventFilter(self)
        return editor

    def setEditorData(self,editor,index):        
        # print('---', index.data(Qt.DisplayRole))
        # text = index.data(Qt.DisplayRole)
        text = index.model().data(index)
        if type(text)== QPyNullVariant:
            text = ""
        edit = editor
        edit.setText(text)

    def setModelData(self,editor,model,index):
        text = editor.text()        
        model.setData(index,text)


class PhoneDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.parent = parent

    def createEditor(self,parent,option,index):
        editor = QLineEdit(parent)
        regExp = QRegExp("^[0-9]{8,12}$")
        editor.setValidator(QRegExpValidator(regExp, parent))
        editor.installEventFilter(self)
        return editor

    def setEditorData(self,editor,index):        
        # print('---', index.data(Qt.DisplayRole))
        # text = index.data(Qt.DisplayRole)
        text = index.model().data(index)
        if type(text)== QPyNullVariant:
            text = ""
        edit = editor
        edit.setText(text)

    def setModelData(self,editor,model,index):
        text = editor.text()        
        model.setData(index,text)

    # def updateEditorGeometry(self, editor, option, index):
    #     self.editor.setGeometry(option.rect)


class DateDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.parent = parent

    def createEditor(self,parent,option,index):
        editor = QDateTimeEdit(parent)
        # curdate = datetime.date.today()
        # curdate = QDate.fromString(curdate.isoformat(),  Qt.ISODate)

        # curdate = QDate.currentDate()
        # editor.setDate(curdate)

        # editor.setDisplayFormat("yyyy-MM")
        editor.setDisplayFormat("yyyy-MM-dd")
        editor.setCalendarPopup(True)
        editor.installEventFilter(self)
        return editor
                
    def setEditorData(self,editor,index):        
        # print('---', index.data(Qt.DisplayRole))
        dateStr = index.data(Qt.DisplayRole)
        # date = QDate.currentDate()
        # print(1, type(dateStr))
        if type(dateStr) == type(str("abc")):
            date = QDate.fromString(dateStr,  Qt.ISODate)
            # date = QDate.currentDate()
            # print(2, date, dateStr)
        elif type(dateStr) == QDate:
            # print(3, dateStr)
            if dateStr.isNull():
                date = QDate.currentDate()
                # print(4, date)
            else:
                date = index.model().data(index)
                # print(5, date)
        edit = editor
            # edit.setDisplayFormat("yyyy-MM")
        edit.setDate(date)
   
    def setModelData(self,editor,model,index):
        date = editor.date().toString(Qt.ISODate)
        # print(date)
        # newdate = date.addMonths(1).toPyDate()
        
        # text = (newdate - datetime.timedelta(newdate.day)).isoformat()
        # print(text)

        # print(date, text, type(text))
        model.setData(index,date)

class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent, itemslist=["a", "b", "c"]):
        QItemDelegate.__init__(self, parent)
        # itemslist = ["a", "b", "c"]
        self.itemslist = itemslist
        self.parent = parent

    # def paint(self, painter, option, index):        
    #     # Get Item Data
    #     value = index.data(Qt.DisplayRole).toInt()[0]
    #     # value = self.itemslist[index.data(QtCore.Qt.DisplayRole).toInt()[0]]
    #     # fill style options with item data
    #     style = QApplication.style()
    #     opt = QStyleOptionComboBox()
    #     opt.currentText = str(self.itemslist[value])
    #     opt.rect = option.rect


    #     # draw item data as ComboBox
    #     style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
    #     self.parent.openPersistentEditor(index)

    def createEditor(self, parent, option, index):

        ##get the "check" value of the row
        # for row in range(self.parent.model.rowCount(self.parent)):
            # print row

        self.editor = QComboBox(parent)
        self.editor.addItems(self.itemslist)
        self.editor.setCurrentIndex(0)
        self.editor.installEventFilter(self)    
        # self.connect(self.editor, SIGNAL("currentIndexChanged(int)"), self.editorChanged)

        return self.editor

    # def setEditorData(self, editor, index):
        # value = index.data(QtCore.Qt.DisplayRole).toInt()[0]
        # editor.setCurrentIndex(value)

    def setEditorData(self, editor, index): 
        curtxt = index.data(Qt.DisplayRole)
        # print(type(curtxt)== QPyNullVariant )
        if type(curtxt) == type(1):
            curindx = int(index.data(Qt.DisplayRole))
            curtxt = self.itemslist[curindx]
        elif type(curtxt)== QPyNullVariant:
            curtxt = ""
        pos = self.editor.findText(curtxt)
        if pos == -1:  
            pos = 0
        self.editor.setCurrentIndex(pos)


    def setModelData(self,editor,model,index):
        curindx = self.editor.currentIndex()
        text = self.itemslist[curindx]
        model.setData(index, text)
        # print(text, '-----delegate----')
        # model.emit(SIGNAL('dataChanged(QModelIndex,QModelIndex)'), model.index(1, 8), model.index(1, 8))


    # def updateEditorGeometry(self, editor, option, index):
    #     self.editor.setGeometry(option.rect)

    # def editorChanged(self, index):
    #     check = self.editor.itemText(index)
    #     id_seq = self.parent.selectedIndexes[0][0]
    #     update.updateCheckSeq(self.parent.db, id_seq, check)


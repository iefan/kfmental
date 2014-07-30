from myimport import *
import sys

DATETIME_FORMAT = "yyyy-MM"
CUR_VERSION = "版本：2014.0725.1.0"
CUR_CONTACT = "如有任何问题请联系康复科：88611869"

def globaldb():
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName("")
    db.setHostName("127.0.0.1")
    # db.setHostName("218.16.248.155")
    db.setDatabaseName("kfmental")
    # db.setDatabaseName("kfother")
    db.setUserName("root")
    # db.setUserName("kfk")
    db.setPassword("stcl789456")
    # db.setPassword("kfk123456")
    # db.setDatabaseName("caracate.db")
    if not db.open():
        QMessageBox.warning(None, "错误",  "数据库连接失败: %s" % db.lastError().text())
        sys.exit(1)
    return db
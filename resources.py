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

LST_MENTALHEADER = ["姓名", "性别", "区县", "身份证号", "残疾类别", "办证日期", "经济状况", "户口类别",\
            "住址", "监护人", "监护关系", "固定电话", "手机", "建档时间", '操作人员']
COUNTY_CHOICES = ['金平区','龙湖区','濠江区','澄海区','潮阳区','潮南区','南澳县']
SEX_CHOICES = ['男','女']
ECON_CHOICES = ['低保','五保','特困','困难']
CITY_CHOICE = ['非农','农业']
RELASHIP_CHOICES = ['配偶','子女','孙子女','父母','祖父母','兄弟姐妹','其他']
DISLEVEL_CHOICES = ["61","62","63","64",'其他']
INSU_CHOICES = ['职工医保','城乡医保']
CERT1_CHOICES = ['身份证','户口本']
CERT2_CHOICES = ['精神残疾证', '精神障碍诊断证明', '非精神残疾证']
CERT3_CHOICES = ['低保证','五保证','特困证','困难证明']
HOSPITAL_CHOICES = ['市四本部','礐石',    '红莲池',  '汕大']
PERIOD_CHOICES = ['急性', '慢性']
CONTINUE_CHOICES = ['间隔救助','续院救助']
ISAPPROVAL_CHOICES = ['待审','退审','同意','作废']
SAVEOK_CHOICES = ['已确认','过期']
ISCAL_CHOICES = ['已结算','待结算']

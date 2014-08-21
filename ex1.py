from xlwt import Workbook,easyxf
book = Workbook(encoding='ascii')
    # 'pattern: pattern solid,  fore_colour white;'
style = easyxf(
    'font: height 280, name 黑体;'
    'align: vertical center, horizontal center;'
    )
style2 = easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal left;')
style3 = easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal left, wrap True;')

sheet1 = book.add_sheet('住院通知单',cell_overwrite_ok=True)

sheet1.col(0).width = 5*256
sheet1.col(1).width = 32*256
sheet1.col(7).width = 15*256
for irow in [0, 12]:
    if irow == 0:
        flagtxt = '存根联'
    else:
        flagtxt = "核报联"
    sheet1.write(0+irow,7,flagtxt, easyxf('font: height 200, name 黑体;align: vertical center, horizontal right;'))
    sheet1.write_merge(1+irow,1+irow,0,7, '汕头市残疾人医疗康复救助基金贫困精神病人医疗救助通知单',style)
    sheet1.row(1+irow).height_mismatch = 1
    sheet1.row(1+irow).height = 5*256
    sheet1.write_merge(2+irow,2+irow,0,1,'医院（中心）：', easyxf('font: height 260, name 仿宋_GB2312; align: vertical center, horizontal right'))
    # sheet1.col(1).width = 30*256
    sheet1.write_merge(3+irow,3+irow,0,7,'　　经审核，下列人员符合汕头市残疾人医疗康复救助基金精神病患者住院医疗救助条件，请按照有关规定确认接收治疗：', style3)
    sheet1.row(3+irow).height_mismatch = 1
    sheet1.row(3+irow).height = 5*220
    sheet1.write_merge(4+irow,4+irow,1,3,'审批编号：', style2)
    sheet1.row(4+irow).height_mismatch = 1
    sheet1.row(4+irow).height = 3*200
    sheet1.write(5+irow,1,'区县：', style2)
    sheet1.write(6+irow,1,'姓名：', style2)
    sheet1.write(7+irow,1,'性别：', style2)
    sheet1.write_merge(8+irow,8+irow,1,3,'通知单有效期：', style2)
    sheet1.write(9+irow,1,'备    注：', style2)
    sheet1.write(10+irow,1,'签发：', style2)
    sheet1.write(6+irow,4,'经济状况：', style2)
    sheet1.write(7+irow,4,'救助疗程：', style2)
    sheet1.write(8+irow,4,'伙食补助：', style2)
    sheet1.write(10+irow,3,'审批时间', style2)
    sheet1.write_merge(10+irow,10+irow,5,7,'残联基金专用印章', easyxf('font: height 260, name 仿宋_GB2312, bold True; align: vertical center, horizontal center;'))
    for indx in list(range(5,11)):
        sheet1.row(indx+irow).height_mismatch =1 
        sheet1.row(indx+irow).height=2*256
sheet1.write_merge(11,11,0,7,'………………………………………………………………………………………………………………', easyxf('font: height 240, name 宋体; align: vertical center, horizontal center;'))
sheet1.row(11).height_mismatch = 1
sheet1.row(11).height = 6*200
sheet1.footer_str = "".encode()
# book.save('d:/simple.xls')
try:
    book.save('d:/simple.xls')
except  Exception as e:
    print(e.errno, e.strerror)
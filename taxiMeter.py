
#!usr/bin/python
# Author:DBUCK
# -*- coding: utf-8 -*-
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWinExtras import QtWin
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import QCheckBox, QLineEdit, QMessageBox, QWidget, QPushButton, QApplication, QGridLayout, QLabel
from PyQt5.QtCore import QRegExp, QTimer, QDateTime
import pyperclip
import sys
myappid = 'dbuck.taximeter.cab.0.1'
QtWin.setCurrentProcessExplicitAppUserModelID(myappid)


class WinForm(QWidget):

    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.time_display = 0
        self.setWindowTitle('市政出租车计价器')
        # 设置标签
        self.label_driver_name = QLabel('司机姓名:')
        self.label_driver_name.setFont(QFont('SimHei', 12))  # 设置标签字体
        self.label_pax_name = QLabel('乘客姓名:')
        self.label_pax_name.setFont(QFont('SimHei', 12))
        self.label_time = QLabel('驾驶时间:0秒')
        self.label_time.setFont(QFont('SimHei', 12))
        self.label_drop_charge = QLabel('起步价格:$7')
        self.label_drop_charge.setFont(QFont('SimHei', 12))
        self.label_time_charge = QLabel('行程收费:$0')
        self.label_time_charge.setFont(QFont('SimHei', 12))
        self.label_money = QLabel('收费金额:$0')
        self.label_money.setFont(QFont('SimHei', 12))
        # 设置按键
        self.start_btn = QPushButton('开始/继续打表')
        self.start_btn.setFont(QFont('SimHei', 10))  # 设置按键字体
        self.end_btn = QPushButton('结束/暂停打表')
        self.end_btn.setFont(QFont('SimHei', 10))
        self.print_btn = QPushButton('重置并导出此单信息')
        self.print_btn.setFont(QFont('SimHei', 10))
        self.readme_btn = QPushButton('如何使用？')
        self.readme_btn.setFont(QFont('SimHei', 10))
        # 设置文本输入框
        self.input_driver_name = QLineEdit()
        self.input_driver_name.setFont(QFont('SimHei', 8))  # 设置文本输入框字体
        self.input_driver_name.setPlaceholderText('例:Ronald Barnard')  # 设置例子
        self.input_driver_name.setValidator(QRegExpValidator(QRegExp('^[A-Za-z ]+$')))  # 限制文本框输入内容仅为英文字母与空格
        self.input_pax1_name = QLineEdit()
        self.input_pax1_name.setFont(QFont('SimHei', 8))
        self.input_pax1_name.setPlaceholderText('例:Michael De Santa')
        self.input_pax1_name.setValidator(QRegExpValidator(QRegExp('^[A-Za-z ]+$')))
        self.input_pax2_name = QLineEdit()
        self.input_pax2_name.setFont(QFont('SimHei', 8))
        self.input_pax2_name.setPlaceholderText('例:Franklin Clinton')
        self.input_pax2_name.setValidator(QRegExpValidator(QRegExp('^[A-Za-z ]+$')))
        self.input_pax3_name = QLineEdit()
        self.input_pax3_name.setFont(QFont('SimHei', 8))
        self.input_pax3_name.setPlaceholderText('例:Trevor Philips')
        self.input_pax3_name.setValidator(QRegExpValidator(QRegExp('^[A-Za-z ]+$')))
        # 设置复选框
        self.check_box = QCheckBox('一直保持在最上层')
        self.check_box.setFont(QFont('SimHei', 10))
        # 设置界面结构
        layout = QGridLayout(self)
        # 标签
        layout.addWidget(self.label_driver_name, 0, 0, 1, 2)
        layout.addWidget(self.label_pax_name, 1, 0, 1, 2)
        layout.addWidget(self.label_time, 2, 0, 1, 2)
        layout.addWidget(self.label_drop_charge, 3, 0, 1, 2)
        layout.addWidget(self.label_time_charge, 4, 0, 1, 4)
        layout.addWidget(self.label_money, 5, 0, 1, 2)
        # 文本输入框
        layout.addWidget(self.input_driver_name, 0, 1, 1, 1)
        layout.addWidget(self.input_pax1_name, 1, 1, 1, 1)
        layout.addWidget(self.input_pax2_name, 1, 2, 1, 1)
        layout.addWidget(self.input_pax3_name, 1, 3, 1, 1)
        # 按钮
        layout.addWidget(self.end_btn, 6, 0, 1, 1)
        layout.addWidget(self.start_btn, 6, 1, 1, 2)
        layout.addWidget(self.print_btn, 6, 3, 1, 1)
        layout.addWidget(self.readme_btn, 5, 3, 1, 1)
        self.end_btn.setEnabled(False)
        # 复选框
        layout.addWidget(self.check_box, 4, 3, 1, 1)
        self.setLayout(layout)
        self.setFixedSize(1000, 400)
        # 初始化一个定时器
        self.timer = QTimer(self)
        # 将定时器超时信号与槽函数showContents()连接
        self.timer.timeout.connect(self.showContents)
        # 连接按键操作和槽函数
        self.start_btn.clicked.connect(self.startTimer)
        self.end_btn.clicked.connect(self.endTimer)
        self.print_btn.clicked.connect(self.printInfo)
        self.readme_btn.clicked.connect(self.readMe)
        # 连接文本输入框和槽函数
        self.dic = {
            'driver': '',
            'pax1': '',
            'pax2': '',
            'pax3': '',
            'time': '',
            'money_total': '',
            'money': ''
        }
        self.money = 0
        self.min2 = 0
        self.min3 = 0
        self.c0 = 0
        self.c1 = 0
        self.input_driver_name.editingFinished.connect(self.saveInfo)
        self.input_pax1_name.editingFinished.connect(self.saveInfo)
        self.input_pax2_name.editingFinished.connect(self.saveInfo)
        self.input_pax3_name.editingFinished.connect(self.saveInfo)
        # 连接复选框和槽函数
        self.check_box.toggled.connect(self.alwaysOnTop)
        self.check_box.toggled.connect(self.notAlwaysOnTop)

    def showContents(self):
        # 标签上显示内容
        self.time_display = self.time_display + 1
        self.label_time.setText(f'驾驶时间:{self.time_display}秒')
        if 0 < self.time_display < 60:
            min1 = self.time_display * 0.3
        if 60 <= self.time_display < 120:
            self.min2 = (self.time_display - 60) * 0.9 + 18
            min1 = 0
        if self.time_display >= 120:
            self.min3 = (self.time_display - 120) * 1.3 + 72
            min1 = 0
            self.min2 = 0
        if self.time_display == 300:
            self.c0 = 1
        if self.time_display % 600 == 0:
            self.c1 = self.c1 + 1
        self.money = round(min1 + self.min2 + self.min3 +
                           10 * self.c0 + 100 * self.c1, 2)
        self.money_total = 7 + self.money
        self.label_time_charge.setText(f'行程收费:${self.money}')
        self.label_money.setText(f'收费金额:${self.money_total}')

    def startTimer(self):
        # 设置计时间隔并启动，每隔1000ms（1秒）发送一次超时信号，循环进行
        self.timer.start(1000)
        self.start_btn.setEnabled(False)
        self.end_btn.setEnabled(True)
        self.print_btn.setEnabled(False)

    def endTimer(self):
        self.timer.stop()
        self.print_btn.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.end_btn.setEnabled(False)

    def saveInfo(self):
        self.dic['driver'] = self.input_driver_name.text()
        self.dic['pax1'] = self.input_pax1_name.text()
        self.dic['pax2'] = self.input_pax2_name.text()
        self.dic['pax3'] = self.input_pax3_name.text()

    def printInfo(self):
        try:
            self.label_money.setText('收费金额:$0')
            self.label_time.setText('驾驶时间:0秒')
            self.label_time_charge.setText('行程收费:$0')
            self.dic['time'] = str(self.time_display) + 's'
            self.dic['money_total'] = '$' + str(self.money_total)
            self.dic['money'] = '$' + str(self.money)
            self.money = 0
            self.min2 = 0
            self.min3 = 0
            self.time_display = 0
            self.input_pax1_name.setText('')
            self.input_pax2_name.setText('')
            self.input_pax3_name.setText('')
            driver = self.dic['driver']
            pax1 = self.dic['pax1']
            pax2 = self.dic['pax2']
            pax3 = self.dic['pax3']
            time = self.dic['time']
            money = self.dic['money']
            money_total = self.dic['money_total']
            date = QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm')
            pyperclip.copy(f'/do 感谢你搭乘洛圣都出租车,计价器显示信息:起步费$7 行程收费{money} 总共消耗时间:{time} 总计费:{money_total} 请向出租车司机支付车费,检查随身携带物品,祝你有美好的一天。')
            QMessageBox.information(self, '注意', '/do内容已复制到剪切板', QMessageBox.Yes)
            with open('接单信息.txt', 'a') as f:
                f.write(f'''——————————————————————————————
日期：{date}
司机：{driver}
客人：{pax1} {pax2} {pax3}
消耗时间：{time}
起步价格：7$
行程收费：{money}
总计费：{money_total}
——————————————————————————————\n''')            
            self.money = 0
            self.money_total = 0
            self.print_btn.setEnabled(False)
        except:
            QMessageBox.warning(self, '注意', '并没有输入信息以导出', QMessageBox.Yes)

    def readMe(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('「市政出租车计价器」使用说明')
        msg_box.setStyleSheet('''
                    QLabel{"
                      "min-width: 500px;"
                      "min-height: 300px; "
                      "}
                      ''')
        msg_box.setText('''
        欢迎使用「市政出租车计价器」 本计价器由罗纳德(DBUCK)制作[出租车员工除了开出租车什么都会]
        #准备工作
        你最好将游戏设置为「无边框窗口化」模式,这样切屏就不会有中间的卡顿了
        当你准备开始工作前，请在计价器中输入你的名字，注意不要加下横杠(其实你也输入不了，不信你可以试试)
        随后你需要按照手册的无线电口令来宣布你开始上班，驾驶你的出租车开始工作
        #开始工作
        当你接到单子后你需要填写你本次乘客的游戏ID，注意他们也不要加下横杠，并且每个空槽只能写一个人名
        然后你需要问他们去哪儿，知道目的地后切出屏幕，点击「开始/继续打表」按钮(注意，你需要在游戏里扮演计价器启动并运行的扮演)
        当你将客人送达到目的地附近时切出屏幕点击「结束/暂停打表」
        最后你需要点击右边的「重置并导出本单信息」点击后你本次接单的信息就会被导出保存至本程序所在的同一目录下,计价器信息就会粘贴到你到剪切板里了,你只需要粘贴(ctrl+v)发到ic中让他们进行付款。(建议将此软件放在一个你找得到的文件夹中)\n祝你工作愉快！ ———— 市政出租车办公室全体人员致意
        #测试版  完整版请等待后续更新 —— R.B
        ''')
        msg_box.setStandardButtons(QMessageBox.Yes)
        msg_box.button(QMessageBox.Yes).setText('我知道了，开始工作！')
        msg_box.exec_()

    def alwaysOnTop(self):
        if self.check_box.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.show()

    def notAlwaysOnTop(self):
        if not self.check_box.isChecked():
            self.setWindowFlags(QtCore.Qt.Window)
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('Cab.ico'))
    form = WinForm()
    form.show()
    sys.exit(app.exec_())

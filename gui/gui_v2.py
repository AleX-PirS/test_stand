# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connecting_measuse.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(455, 551)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 451, 381))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.connecting_tab = QtWidgets.QWidget()
        self.connecting_tab.setObjectName("connecting_tab")
        self.frame_2 = QtWidgets.QFrame(self.connecting_tab)
        self.frame_2.setGeometry(QtCore.QRect(10, 10, 431, 111))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.oscilloscope_addr = QtWidgets.QLineEdit(self.frame_2)
        self.oscilloscope_addr.setGeometry(QtCore.QRect(12, 30, 311, 20))
        self.oscilloscope_addr.setClearButtonEnabled(True)
        self.oscilloscope_addr.setObjectName("oscilloscope_addr")
        self.oscilloscope_butt = QtWidgets.QPushButton(self.frame_2)
        self.oscilloscope_butt.setGeometry(QtCore.QRect(330, 30, 91, 21))
        self.oscilloscope_butt.setObjectName("oscilloscope_butt")
        self.oscilloscope_info = QtWidgets.QLineEdit(self.frame_2)
        self.oscilloscope_info.setGeometry(QtCore.QRect(12, 70, 311, 20))
        self.oscilloscope_info.setReadOnly(True)
        self.oscilloscope_info.setObjectName("oscilloscope_info")
        self.oscilloscope_ping_butt = QtWidgets.QPushButton(self.frame_2)
        self.oscilloscope_ping_butt.setGeometry(QtCore.QRect(330, 69, 91, 21))
        self.oscilloscope_ping_butt.setObjectName("oscilloscope_ping_butt")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(20, 49, 231, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(20, 11, 231, 20))
        self.label_4.setObjectName("label_4")
        self.frame_3 = QtWidgets.QFrame(self.connecting_tab)
        self.frame_3.setGeometry(QtCore.QRect(10, 120, 431, 111))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.generator_60_addr = QtWidgets.QLineEdit(self.frame_3)
        self.generator_60_addr.setGeometry(QtCore.QRect(12, 30, 311, 20))
        self.generator_60_addr.setClearButtonEnabled(True)
        self.generator_60_addr.setObjectName("generator_60_addr")
        self.generator_60_butt = QtWidgets.QPushButton(self.frame_3)
        self.generator_60_butt.setGeometry(QtCore.QRect(330, 30, 91, 21))
        self.generator_60_butt.setObjectName("generator_60_butt")
        self.generator_60_info = QtWidgets.QLineEdit(self.frame_3)
        self.generator_60_info.setGeometry(QtCore.QRect(12, 70, 311, 20))
        self.generator_60_info.setReadOnly(True)
        self.generator_60_info.setObjectName("generator_60_info")
        self.generator_60_ping_butt = QtWidgets.QPushButton(self.frame_3)
        self.generator_60_ping_butt.setGeometry(QtCore.QRect(330, 69, 91, 21))
        self.generator_60_ping_butt.setObjectName("generator_60_ping_butt")
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(20, 49, 231, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(20, 11, 231, 20))
        self.label_6.setObjectName("label_6")
        self.frame = QtWidgets.QFrame(self.connecting_tab)
        self.frame.setGeometry(QtCore.QRect(10, 230, 431, 111))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.generator_50_addr = QtWidgets.QLineEdit(self.frame)
        self.generator_50_addr.setGeometry(QtCore.QRect(12, 30, 311, 20))
        self.generator_50_addr.setClearButtonEnabled(True)
        self.generator_50_addr.setObjectName("generator_50_addr")
        self.generator_50_butt = QtWidgets.QPushButton(self.frame)
        self.generator_50_butt.setGeometry(QtCore.QRect(330, 30, 91, 21))
        self.generator_50_butt.setObjectName("generator_50_butt")
        self.generator_50_info = QtWidgets.QLineEdit(self.frame)
        self.generator_50_info.setGeometry(QtCore.QRect(12, 70, 311, 20))
        self.generator_50_info.setReadOnly(True)
        self.generator_50_info.setObjectName("generator_50_info")
        self.generator_50_ping_butt = QtWidgets.QPushButton(self.frame)
        self.generator_50_ping_butt.setGeometry(QtCore.QRect(330, 69, 91, 21))
        self.generator_50_ping_butt.setObjectName("generator_50_ping_butt")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(20, 49, 231, 21))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 11, 231, 20))
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.connecting_tab, "")
        self.measure_tab = QtWidgets.QWidget()
        self.measure_tab.setObjectName("measure_tab")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.measure_tab)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 451, 361))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget_2.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(3, 70, 431, 231))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setGeometry(QtCore.QRect(10, 0, 291, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 291, 41))
        self.label_9.setObjectName("label_9")
        self.tabWidget_2.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.tabWidget.addTab(self.measure_tab, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(10, 0, 81, 21))
        self.label_7.setObjectName("label_7")
        self.signals_box = QtWidgets.QComboBox(self.tab)
        self.signals_box.setGeometry(QtCore.QRect(10, 20, 81, 22))
        self.signals_box.setObjectName("signals_box")
        self.signals_box.addItem("")
        self.signals_box.addItem("")
        self.signals_box.addItem("")
        self.signals_box.addItem("")
        self.signals_box.addItem("")
        self.tabWidget.addTab(self.tab, "")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(110, 390, 271, 81))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(4, 390, 101, 23))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.oscilloscope_butt.setText(_translate("MainWindow", "connect"))
        self.oscilloscope_info.setText(_translate("MainWindow", "no data"))
        self.oscilloscope_ping_butt.setText(_translate("MainWindow", "ping"))
        self.label_3.setText(_translate("MainWindow", "Device info"))
        self.label_4.setText(_translate("MainWindow", "Oscilloscope"))
        self.generator_60_butt.setText(_translate("MainWindow", "connect"))
        self.generator_60_info.setText(_translate("MainWindow", "no data"))
        self.generator_60_ping_butt.setText(_translate("MainWindow", "ping"))
        self.label_5.setText(_translate("MainWindow", "Device info"))
        self.label_6.setText(_translate("MainWindow", "Generator 81160A"))
        self.generator_50_butt.setText(_translate("MainWindow", "connect"))
        self.generator_50_info.setText(_translate("MainWindow", "no data"))
        self.generator_50_ping_butt.setText(_translate("MainWindow", "ping"))
        self.label_2.setText(_translate("MainWindow", "Device info"))
        self.label.setText(_translate("MainWindow", "Generator 81150A"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.connecting_tab), _translate("MainWindow", "Connecting"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "Parameter"))
        self.label_8.setText(_translate("MainWindow", "Insert data: delay,width,lead,trail,amplitude<new line>"))
        self.label_9.setText(_translate("MainWindow", "EXAMPLE:\n"
"10,14.5,24.5,23,204\n"
"12,14.5,24.5,23,204"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Text sweep"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Sweep"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.measure_tab), _translate("MainWindow", "Pulse"))
        self.label_7.setText(_translate("MainWindow", "Signal type"))
        self.signals_box.setItemText(0, _translate("MainWindow", "Sine"))
        self.signals_box.setItemText(1, _translate("MainWindow", "Square"))
        self.signals_box.setItemText(2, _translate("MainWindow", "Ramp"))
        self.signals_box.setItemText(3, _translate("MainWindow", "Arb"))
        self.signals_box.setItemText(4, _translate("MainWindow", "Noise"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Other measures"))
        self.pushButton.setText(_translate("MainWindow", "show devices"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

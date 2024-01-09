# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rc/rc.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(343, 653)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 341, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.oscilloscope_addr = QtWidgets.QLineEdit(self.frame)
        self.oscilloscope_addr.setGeometry(QtCore.QRect(10, 49, 231, 20))
        self.oscilloscope_addr.setObjectName("oscilloscope_addr")
        self.oscilloscope_conn_butt = QtWidgets.QPushButton(self.frame)
        self.oscilloscope_conn_butt.setGeometry(QtCore.QRect(250, 49, 61, 21))
        self.oscilloscope_conn_butt.setObjectName("oscilloscope_conn_butt")
        self.oscilloscope_radio = QtWidgets.QRadioButton(self.frame)
        self.oscilloscope_radio.setGeometry(QtCore.QRect(320, 49, 21, 21))
        self.oscilloscope_radio.setText("")
        self.oscilloscope_radio.setCheckable(False)
        self.oscilloscope_radio.setChecked(False)
        self.oscilloscope_radio.setObjectName("oscilloscope_radio")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 181, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 181, 20))
        self.label_4.setObjectName("label_4")
        self.generator_conn_butt = QtWidgets.QPushButton(self.frame)
        self.generator_conn_butt.setGeometry(QtCore.QRect(250, 89, 61, 21))
        self.generator_conn_butt.setObjectName("generator_conn_butt")
        self.generator_addr = QtWidgets.QLineEdit(self.frame)
        self.generator_addr.setGeometry(QtCore.QRect(10, 89, 231, 20))
        self.generator_addr.setObjectName("generator_addr")
        self.generator_radio = QtWidgets.QRadioButton(self.frame)
        self.generator_radio.setGeometry(QtCore.QRect(320, 89, 21, 21))
        self.generator_radio.setText("")
        self.generator_radio.setCheckable(False)
        self.generator_radio.setChecked(False)
        self.generator_radio.setObjectName("generator_radio")
        self.logs_plain_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.logs_plain_text.setGeometry(QtCore.QRect(3, 510, 341, 141))
        self.logs_plain_text.setReadOnly(False)
        self.logs_plain_text.setObjectName("logs_plain_text")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(6, 491, 71, 20))
        self.label_2.setObjectName("label_2")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(-1, 129, 341, 111))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(10, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setTextFormat(QtCore.Qt.AutoText)
        self.label_5.setWordWrap(False)
        self.label_5.setObjectName("label_5")
        self.reset_osc_butt = QtWidgets.QPushButton(self.frame_2)
        self.reset_osc_butt.setGeometry(QtCore.QRect(10, 30, 321, 23))
        self.reset_osc_butt.setObjectName("reset_osc_butt")
        self.reset_gen_butt = QtWidgets.QPushButton(self.frame_2)
        self.reset_gen_butt.setGeometry(QtCore.QRect(10, 60, 321, 23))
        self.reset_gen_butt.setObjectName("reset_gen_butt")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(-1, 239, 341, 241))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(10, 0, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setTextFormat(QtCore.Qt.AutoText)
        self.label_6.setWordWrap(False)
        self.label_6.setObjectName("label_6")
        self.freq = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.freq.setGeometry(QtCore.QRect(50, 30, 101, 22))
        self.freq.setDecimals(5)
        self.freq.setMaximum(999999.99)
        self.freq.setSingleStep(0.01)
        self.freq.setObjectName("freq")
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(10, 31, 47, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(10, 61, 47, 21))
        self.label_8.setObjectName("label_8")
        self.delay = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.delay.setGeometry(QtCore.QRect(50, 60, 101, 22))
        self.delay.setDecimals(5)
        self.delay.setMaximum(999.99)
        self.delay.setSingleStep(0.01)
        self.delay.setObjectName("delay")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(160, 30, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.frame_3)
        self.label_10.setGeometry(QtCore.QRect(160, 60, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(160, 90, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_15 = QtWidgets.QLabel(self.frame_3)
        self.label_15.setGeometry(QtCore.QRect(160, 120, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.frame_3)
        self.label_16.setGeometry(QtCore.QRect(160, 150, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.frame_3)
        self.label_17.setGeometry(QtCore.QRect(160, 180, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.start_butt = QtWidgets.QPushButton(self.frame_3)
        self.start_butt.setGeometry(QtCore.QRect(190, 90, 131, 51))
        self.start_butt.setObjectName("start_butt")
        self.signal_type_box = QtWidgets.QComboBox(self.frame_3)
        self.signal_type_box.setGeometry(QtCore.QRect(190, 30, 131, 22))
        self.signal_type_box.setObjectName("signal_type_box")
        self.signal_type_box.addItem("")
        self.signal_type_box.addItem("")
        self.signal_type_box.addItem("")
        self.signal_type_box.addItem("")
        self.signal_type_box.addItem("")
        self.signal_type_box.addItem("")
        self.label_18 = QtWidgets.QLabel(self.frame_3)
        self.label_18.setGeometry(QtCore.QRect(159, 208, 47, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.trig = QtWidgets.QDoubleSpinBox(self.frame_3)
        self.trig.setGeometry(QtCore.QRect(50, 209, 101, 22))
        self.trig.setDecimals(5)
        self.trig.setMaximum(9999.99)
        self.trig.setSingleStep(0.01)
        self.trig.setObjectName("trig")
        self.Ampl_2 = QtWidgets.QLabel(self.frame_3)
        self.Ampl_2.setGeometry(QtCore.QRect(10, 210, 47, 21))
        self.Ampl_2.setObjectName("Ampl_2")
        self.isScreenshotable = QtWidgets.QCheckBox(self.frame_3)
        self.isScreenshotable.setGeometry(QtCore.QRect(189, 70, 131, 20))
        self.isScreenshotable.setObjectName("isScreenshotable")
        self.width = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.width.setGeometry(QtCore.QRect(50, 329, 101, 22))
        self.width.setDecimals(5)
        self.width.setMaximum(999.99)
        self.width.setSingleStep(0.01)
        self.width.setObjectName("width")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 330, 47, 21))
        self.label_12.setObjectName("label_12")
        self.lead = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.lead.setGeometry(QtCore.QRect(50, 359, 101, 22))
        self.lead.setDecimals(5)
        self.lead.setMaximum(999.99)
        self.lead.setSingleStep(0.01)
        self.lead.setObjectName("lead")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 360, 47, 21))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 391, 47, 21))
        self.label_14.setObjectName("label_14")
        self.trail = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.trail.setGeometry(QtCore.QRect(50, 390, 101, 22))
        self.trail.setDecimals(5)
        self.trail.setMaximum(999.99)
        self.trail.setSingleStep(0.01)
        self.trail.setObjectName("trail")
        self.Ampl = QtWidgets.QLabel(self.centralwidget)
        self.Ampl.setGeometry(QtCore.QRect(10, 421, 47, 21))
        self.Ampl.setObjectName("Ampl")
        self.ampl = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.ampl.setGeometry(QtCore.QRect(50, 420, 101, 22))
        self.ampl.setDecimals(5)
        self.ampl.setMaximum(9999.99)
        self.ampl.setSingleStep(0.01)
        self.ampl.setObjectName("ampl")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Connecting"))
        self.oscilloscope_conn_butt.setText(_translate("MainWindow", "connect"))
        self.label_3.setText(_translate("MainWindow", "Oscilloscope"))
        self.label_4.setText(_translate("MainWindow", "Generator"))
        self.generator_conn_butt.setText(_translate("MainWindow", "connect"))
        self.label_2.setText(_translate("MainWindow", "Logs"))
        self.label_5.setText(_translate("MainWindow", "Control"))
        self.reset_osc_butt.setText(_translate("MainWindow", "Reset oscilloscope"))
        self.reset_gen_butt.setText(_translate("MainWindow", "Reset generator"))
        self.label_6.setText(_translate("MainWindow", "Signal settings"))
        self.label_7.setText(_translate("MainWindow", "Freq:"))
        self.label_8.setText(_translate("MainWindow", "Delay:"))
        self.label_9.setText(_translate("MainWindow", "Hz"))
        self.label_10.setText(_translate("MainWindow", "s"))
        self.label_11.setText(_translate("MainWindow", "ns"))
        self.label_15.setText(_translate("MainWindow", "ns"))
        self.label_16.setText(_translate("MainWindow", "ns"))
        self.label_17.setText(_translate("MainWindow", "mV"))
        self.start_butt.setText(_translate("MainWindow", "Start"))
        self.signal_type_box.setItemText(0, _translate("MainWindow", "PULSE"))
        self.signal_type_box.setItemText(1, _translate("MainWindow", "SQUARE"))
        self.signal_type_box.setItemText(2, _translate("MainWindow", "SINE"))
        self.signal_type_box.setItemText(3, _translate("MainWindow", "RAMP"))
        self.signal_type_box.setItemText(4, _translate("MainWindow", "NOISE"))
        self.signal_type_box.setItemText(5, _translate("MainWindow", "ARB"))
        self.label_18.setText(_translate("MainWindow", "mV"))
        self.Ampl_2.setText(_translate("MainWindow", "Trig"))
        self.isScreenshotable.setText(_translate("MainWindow", "Take screenshot"))
        self.label_12.setText(_translate("MainWindow", "Width:"))
        self.label_13.setText(_translate("MainWindow", "Lead:"))
        self.label_14.setText(_translate("MainWindow", "Trail:"))
        self.Ampl.setText(_translate("MainWindow", "Ampl:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
from PyQt5 import QtWidgets
import sys
import datetime
import regex
from pytz import timezone

from ui_gen import Ui_MainWindow
from pkg import RegData


class Ui(object):
    def __init__(self) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def logging(self, *messages: str):
        date = str(datetime.datetime.now(tz=timezone('Europe/Moscow')))
        history = self.ui.logs_plain_text.toPlainText()
        if history != "":
            history += "\n"

        res = date + "| "
        for i in messages:
            res += str(i)

        self.ui.logs_plain_text.setPlainText(history+res)

    def log_registers(self, data: str):
        date = str(datetime.datetime.now(tz=timezone('Europe/Moscow')))
        self.ui.regs_plain_text.setPlainText("Date: " + date + '\n' + data)

    def log_resources(self, data: list[tuple[str, str]]):
        str_data = "---------------\n"
        for i in data:
            str_data += i[0]+'\n'+i[1]+'\n'+'---------------\n'
        self.ui.res_plain_text.setPlainText(str_data[:-1])

    def get_com_port_address(self) -> str:
        address = regex.findall("^COM([0-9]+)", self.ui.com_addr.text().strip().upper())
        if len(address) != 1:
            raise Exception(
                "Invalid COM PORT address. Need address like 'COMi' where 'i' is 1, 2, ... n.")

        return "COM" + address[0]

    def get_w_registers_data(self) -> RegData:
        return RegData(
            CCAL=self.get_code_from_box(self.ui.comboBox_CCAL.currentText()),
            CCSA=self.get_code_from_box(self.ui.comboBox_CCSA.currentText()),
            GAIN=self.get_code_from_box(self.ui.comboBox_GAIN.currentText()),
            ICSA=self.get_code_from_box(self.ui.comboBox_ICSA.currentText()),
            SHA=self.get_code_from_box(self.ui.comboBox_SHA.currentText()),
            SHTR=self.get_code_from_box(self.ui.comboBox_SHTR.currentText()),
            POL=self.get_code_from_box(self.ui.comboBox_POL.currentText()),
            BIAS_CORE_CUR=self.get_code_from_box(
                self.ui.comboBox_BIAS_CORE_CUR.currentText()),
            DAC_CAL=self.ui.spinBox_DAC_CAL.value(),
            REZ=self.ui.spinBox_REZ.value(),
            CAL_EN_CH=self.ui.spinBox_CAL_EN_CH.value(),
            AN_CH_DISABLE=self.ui.spinBox_AN_CH_DISABLE.value(),
            CMP_TH=self.get_code_from_box(
                self.ui.comboBox_CMP_TH.currentText()),
            CFG_p1_in_time=self.ui.spinBox_CFG_p1_in_time.value(),
            CFG_p1_L0_over=self.ui.spinBox_CFG_p1_L0_over.value(),
            CFG_p2_plus_SOC=self.ui.spinBox_CFG_p2_puls_SOC.value(),
            CFG_p2_plus_SWM=self.ui.spinBox_CFG_p2_puls_SWM.value(),
            CFG_p2_plus_EOC=self.ui.spinBox_CFG_p2_puls_EOC.value(),
            CFG_p3_L1_over=self.ui.spinBox_CFG_p3_L1_over.value(),
            CFG_rst_plus_EOC=self.ui.spinBox_CFG_rst_puls_EOC.value(),
            CFG_SW_force_num=self.ui.spinBox_CFG_SW_force_num.value(),
            CFG_SW_force_EN=self.get_code_from_box(
                self.ui.comboBox_CFG_SW_force_EN.currentText()),
            CFG_OUT_INT=self.ui.spinBox_CFG_OUT_INT.value(),
            ADC_EMU_CFG=self.ui.spinBox_ADC_EMU_CFG.value(),
            EMUL_DATA_i=self.ui.spinBox_EMUL_DATA_i.value(),
            EMUL_ADDR_i=self.get_code_from_box(
                self.ui.comboBox_EMUL_ADDR_i.currentText()),
            EMUL_EN_L0=self.get_code_from_box(
                self.ui.comboBox_EMUL_EN_L0.currentText()),
            EMUL_EN_L1=self.get_code_from_box(
                self.ui.comboBox_EMUL_EN_L1.currentText()),
            EMUL_tau_v=self.get_code_from_box(
                self.ui.comboBox_EMUL_tau_v.currentText()),
            EMUL_L0_v=self.get_code_from_box(
                self.ui.comboBox_EMUL_L0_v.currentText()),
            EMUL_L1_v=self.ui.spinBox_EMUL_L1_v.value(),
        )

    def set_reg_values(self, regs:RegData):
        self.ui.comboBox_CCAL.setCurrentIndex(0)
        self.ui.comboBox_CCSA.setCurrentIndex(0)
        self.ui.comboBox_GAIN.setCurrentIndex(0)
        self.ui.comboBox_ICSA.setCurrentIndex(0)
        self.ui.comboBox_SHA.setCurrentIndex(0)
        self.ui.comboBox_SHTR.setCurrentIndex(0)
        self.ui.comboBox_POL.setCurrentIndex(0)
        self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(0)
        self.ui.spinBox_DAC_CAL.setValue(regs.DEFAULT_DAC_CAL)
        self.ui.spinBox_REZ.setValue(regs.DEFAULT_REZ)
        self.ui.spinBox_CAL_EN_CH.setValue(regs.DEFAULT_CAL_EN_CH)
        self.ui.spinBox_AN_CH_DISABLE.setValue(regs.DEFAULT_AN_CH_DISABLE)
        self.ui.comboBox_CMP_TH.setCurrentIndex(0)
        self.ui.spinBox_CFG_p1_in_time.setValue(regs.DEFAULT_CFG_p1_in_time)
        self.ui.spinBox_CFG_p1_L0_over.setValue(regs.DEFAULT_CFG_p1_L0_over)
        self.ui.spinBox_CFG_p2_puls_SOC.setValue(regs.DEFAULT_CFG_p2_plus_SOC)
        self.ui.spinBox_CFG_p2_puls_SWM.setValue(regs.DEFAULT_CFG_p2_plus_SWM)
        self.ui.spinBox_CFG_p2_puls_EOC.setValue(regs.DEFAULT_CFG_p2_plus_EOC)
        self.ui.spinBox_CFG_p3_L1_over.setValue(regs.DEFAULT_CFG_p3_L1_over)
        self.ui.spinBox_CFG_rst_puls_EOC.setValue(regs.DEFAULT_CFG_rst_plus_EOC)
        self.ui.spinBox_CFG_SW_force_num.setValue(regs.DEFAULT_CFG_SW_force_num)
        self.ui.comboBox_CFG_SW_force_EN.setCurrentIndex(0)
        self.ui.spinBox_CFG_OUT_INT.setValue(regs.DEFAULT_CFG_OUT_INT)
        self.ui.spinBox_ADC_EMU_CFG.setValue(regs.DEFAULT_ADC_EMU_CFG)
        self.ui.spinBox_EMUL_DATA_i.setValue(regs.DEFAULT_EMUL_DATA_i)
        self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(0)
        self.ui.comboBox_EMUL_EN_L0.setCurrentIndex(0)
        self.ui.comboBox_EMUL_EN_L1.setCurrentIndex(0)
        self.ui.comboBox_EMUL_tau_v.setCurrentIndex(0)
        self.ui.comboBox_EMUL_L0_v.setCurrentIndex(0)
        self.ui.spinBox_EMUL_L1_v.setValue(regs.DEFAULT_EMUL_L1_v)

    def get_code_from_box(self, data: str) -> int:
        try:
            code = int(regex.findall(".*\(([0-9]*)\)", data)[0], base=2)
        except Exception as e:
            print('Bad data!', e)
            return

        return code

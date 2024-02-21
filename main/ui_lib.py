from re import M
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QObject
import sys
import datetime
import regex
from pytz import timezone
import math
from itertools import product

from ui_gen import Ui_MainWindow
from pkg import Channel, RegData, GeneratorSample, Scenario
from pkg import registers_metadata_name_to_addr
from pkg import process_signal_type


class Ui(QObject):
    is_regs_readonly = False
    is_env_readonly = False
    is_uart_readonly = False
    is_testing_readonly = False
    is_logs_readonly = False
    is_gui_buttons_readonly = False
    is_triggs_readonly = False
    is_channels_readonly = False
    is_gen_readonly = False

    def __init__(self) -> None:
        super(Ui, self).__init__()
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def logging(self, *messages: str):
        date = str(datetime.datetime.now(tz=timezone('Europe/Moscow')))
        # history = self.ui.logs_plain_text.toPlainText()
        # if history != "":
        #     history += "\n"

        res = date + "| "
        for i in messages:
            res += str(i)

        self.ui.logs_plain_text.appendPlainText(res)
        self.ui.logs_plain_text.repaint()

    def clear_log(self):
        self.ui.logs_plain_text.setPlainText("")

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

    def set_default_reg_values(self, regs:RegData):
        self.ui.comboBox_CCAL.setCurrentIndex(0)
        self.ui.comboBox_CCAL.repaint()
        self.ui.comboBox_CCSA.setCurrentIndex(0)
        self.ui.comboBox_CCSA.repaint()
        self.ui.comboBox_GAIN.setCurrentIndex(0)
        self.ui.comboBox_GAIN.repaint()
        self.ui.comboBox_ICSA.setCurrentIndex(0)
        self.ui.comboBox_ICSA.repaint()
        self.ui.comboBox_SHA.setCurrentIndex(0)
        self.ui.comboBox_SHA.repaint()
        self.ui.comboBox_SHTR.setCurrentIndex(0)
        self.ui.comboBox_SHTR.repaint()
        self.ui.comboBox_POL.setCurrentIndex(0)
        self.ui.comboBox_POL.repaint()
        self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(0)
        self.ui.comboBox_BIAS_CORE_CUR.repaint()
        self.ui.spinBox_DAC_CAL.setValue(regs.DEFAULT_DAC_CAL)
        self.ui.spinBox_DAC_CAL.repaint()
        self.ui.spinBox_REZ.setValue(regs.DEFAULT_REZ)
        self.ui.spinBox_REZ.repaint()
        self.ui.spinBox_CAL_EN_CH.setValue(regs.DEFAULT_CAL_EN_CH)
        self.ui.spinBox_CAL_EN_CH.repaint()
        self.ui.spinBox_AN_CH_DISABLE.setValue(regs.DEFAULT_AN_CH_DISABLE)
        self.ui.spinBox_AN_CH_DISABLE.repaint()
        self.ui.comboBox_CMP_TH.setCurrentIndex(0)
        self.ui.comboBox_CMP_TH.repaint()
        self.ui.spinBox_CFG_p1_in_time.setValue(regs.DEFAULT_CFG_p1_in_time)
        self.ui.spinBox_CFG_p1_in_time.repaint()
        self.ui.spinBox_CFG_p1_L0_over.setValue(regs.DEFAULT_CFG_p1_L0_over)
        self.ui.spinBox_CFG_p1_L0_over.repaint()
        self.ui.spinBox_CFG_p2_puls_SOC.setValue(regs.DEFAULT_CFG_p2_plus_SOC)
        self.ui.spinBox_CFG_p2_puls_SOC.repaint()
        self.ui.spinBox_CFG_p2_puls_SWM.setValue(regs.DEFAULT_CFG_p2_plus_SWM)
        self.ui.spinBox_CFG_p2_puls_SWM.repaint()
        self.ui.spinBox_CFG_p2_puls_EOC.setValue(regs.DEFAULT_CFG_p2_plus_EOC)
        self.ui.spinBox_CFG_p2_puls_EOC.repaint()
        self.ui.spinBox_CFG_p3_L1_over.setValue(regs.DEFAULT_CFG_p3_L1_over)
        self.ui.spinBox_CFG_p3_L1_over.repaint()
        self.ui.spinBox_CFG_rst_puls_EOC.setValue(regs.DEFAULT_CFG_rst_plus_EOC)
        self.ui.spinBox_CFG_rst_puls_EOC.repaint()
        self.ui.spinBox_CFG_SW_force_num.setValue(regs.DEFAULT_CFG_SW_force_num)
        self.ui.spinBox_CFG_SW_force_num.repaint()
        self.ui.comboBox_CFG_SW_force_EN.setCurrentIndex(0)
        self.ui.comboBox_CFG_SW_force_EN.repaint()
        self.ui.spinBox_CFG_OUT_INT.setValue(regs.DEFAULT_CFG_OUT_INT)
        self.ui.spinBox_CFG_OUT_INT.repaint()
        self.ui.spinBox_ADC_EMU_CFG.setValue(regs.DEFAULT_ADC_EMU_CFG)
        self.ui.spinBox_ADC_EMU_CFG.repaint()
        self.ui.spinBox_EMUL_DATA_i.setValue(regs.DEFAULT_EMUL_DATA_i)
        self.ui.spinBox_EMUL_DATA_i.repaint()
        self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(0)
        self.ui.comboBox_EMUL_ADDR_i.repaint()
        self.ui.comboBox_EMUL_EN_L0.setCurrentIndex(0)
        self.ui.comboBox_EMUL_EN_L0.repaint()
        self.ui.comboBox_EMUL_EN_L1.setCurrentIndex(0)
        self.ui.comboBox_EMUL_EN_L1.repaint()
        self.ui.comboBox_EMUL_tau_v.setCurrentIndex(0)
        self.ui.comboBox_EMUL_tau_v.repaint()
        self.ui.comboBox_EMUL_L0_v.setCurrentIndex(0)
        self.ui.comboBox_EMUL_L0_v.repaint()
        self.ui.spinBox_EMUL_L1_v.setValue(regs.DEFAULT_EMUL_L1_v)
        self.ui.spinBox_EMUL_L1_v.repaint()

    def set_reg_values(self, regs:RegData):
        # Analog
        self.ui.spinBox_DAC_CAL.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['dac_cal']], "big"))
        self.ui.spinBox_DAC_CAL.repaint()
        self.ui.spinBox_REZ.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['rez']], "big"))
        self.ui.spinBox_REZ.repaint()
        self.ui.spinBox_CAL_EN_CH.setValue((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cal_en_0']], "big")<<2)+(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cal_en_1']], "big")>>6))
        self.ui.spinBox_CAL_EN_CH.repaint()
        self.ui.spinBox_AN_CH_DISABLE.setValue((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['an_ch_disable_15']], "big")<<2)+(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['an_ch_disable_16']], "big")>>6))
        self.ui.spinBox_AN_CH_DISABLE.repaint()
        
        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']], "big")&0b1100_0000)>>6):
            case 0b00:
                self.ui.comboBox_CCAL.setCurrentIndex(1)
            case 0b01:
                self.ui.comboBox_CCAL.setCurrentIndex(0)
            case 0b10:
                self.ui.comboBox_CCAL.setCurrentIndex(2)
            case 0b11:
                self.ui.comboBox_CCAL.setCurrentIndex(3)
        self.ui.comboBox_CCAL.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']], "big")&0b0011_0000)>>4):
            case 0b00:
                self.ui.comboBox_CCSA.setCurrentIndex(1)
            case 0b01:
                self.ui.comboBox_CCSA.setCurrentIndex(0)
            case 0b10:
                self.ui.comboBox_CCSA.setCurrentIndex(2)
            case 0b11:
                self.ui.comboBox_CCSA.setCurrentIndex(3)
        self.ui.comboBox_CCSA.repaint()
        
        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']], "big")&0b0000_1000)>>3):
            case 0b0:
                self.ui.comboBox_GAIN.setCurrentIndex(0)
            case 0b1:
                self.ui.comboBox_GAIN.setCurrentIndex(1)
        self.ui.comboBox_GAIN.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']], "big")&0b0000_0100)>>2):
            case 0b0:
                self.ui.comboBox_ICSA.setCurrentIndex(0)
            case 0b1:
                self.ui.comboBox_ICSA.setCurrentIndex(1)
        self.ui.comboBox_ICSA.repaint()

        match (int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_0']], "big")&0b0000_0011):
            case 0b11:
                self.ui.comboBox_SHA.setCurrentIndex(0)
            case 0b00:
                self.ui.comboBox_SHA.setCurrentIndex(1)
            case 0b01:
                self.ui.comboBox_SHA.setCurrentIndex(2)
        self.ui.comboBox_SHA.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_1']], "big")&0b1100_0000)>>6):
            case 0b10:
                self.ui.comboBox_SHTR.setCurrentIndex(0)
            case 0b11:
                self.ui.comboBox_SHTR.setCurrentIndex(1)
            case 0b00:
                self.ui.comboBox_SHTR.setCurrentIndex(2)
        self.ui.comboBox_SHTR.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_1']], "big")&0b0010_0000)>>5):
            case 0b1:
                self.ui.comboBox_POL.setCurrentIndex(0)
            case 0b0:
                self.ui.comboBox_POL.setCurrentIndex(1)
        self.ui.comboBox_POL.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['analog_ctrl_1']], "big")&0b0001_1000)>>3):
            case 0b00:
                self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(0)
            case 0b01:
                self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(1)
            case 0b10:
                self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(2)
            case 0b11:
                self.ui.comboBox_BIAS_CORE_CUR.setCurrentIndex(3)
        self.ui.comboBox_BIAS_CORE_CUR.repaint()

        # Analog-digital
        match (int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['digit_analog_ctrl_0']], "big")&0b0000_1111):
            case 0b0001:
                self.ui.comboBox_CMP_TH.setCurrentIndex(0)
            case 0b0000:
                self.ui.comboBox_CMP_TH.setCurrentIndex(1)
            case 0b0011:
                self.ui.comboBox_CMP_TH.setCurrentIndex(2)
            case 0b0111:
                self.ui.comboBox_CMP_TH.setCurrentIndex(3)
            case 0b1111:
                self.ui.comboBox_CMP_TH.setCurrentIndex(4)
        self.ui.comboBox_CMP_TH.repaint()
        
        # Digital
        self.ui.spinBox_CFG_p1_in_time.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p1_in_time']], "big"))
        self.ui.spinBox_CFG_p1_in_time.repaint()
        self.ui.spinBox_CFG_p1_L0_over.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p1_l0_over']], "big"))
        self.ui.spinBox_CFG_p1_L0_over.repaint()
        self.ui.spinBox_CFG_p2_puls_SOC.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_soc']], "big"))
        self.ui.spinBox_CFG_p2_puls_SOC.repaint()
        self.ui.spinBox_CFG_p2_puls_SWM.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_swm']], "big"))
        self.ui.spinBox_CFG_p2_puls_SWM.repaint()
        self.ui.spinBox_CFG_p2_puls_EOC.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p2_plus_eoc']], "big"))
        self.ui.spinBox_CFG_p2_puls_EOC.repaint()
        self.ui.spinBox_CFG_rst_puls_EOC.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_rst_plus_eoc']], "big"))
        self.ui.spinBox_CFG_rst_puls_EOC.repaint()
        self.ui.spinBox_CFG_SW_force_num.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_sw_force_num']], "big"))
        self.ui.spinBox_CFG_SW_force_num.repaint()
        self.ui.spinBox_CFG_OUT_INT.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_out_int']], "big"))
        self.ui.spinBox_CFG_OUT_INT.repaint()
        self.ui.spinBox_CFG_p3_L1_over.setValue((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p3_l1_over_0']], "big")<<5)+(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_p3_l1_over_1']], "big")))
        self.ui.spinBox_CFG_p3_L1_over.repaint()
        self.ui.spinBox_ADC_EMU_CFG.setValue((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_clk_gen_0']], "big")<<2)+(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_clk_gen_1']], "big")>>6))
        self.ui.spinBox_ADC_EMU_CFG.repaint()
        self.ui.spinBox_EMUL_L1_v.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_2']], "big"))
        self.ui.spinBox_EMUL_L1_v.repaint()
        self.ui.spinBox_EMUL_DATA_i.setValue(int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_4']], "big")&0b0001_1111)
        self.ui.spinBox_EMUL_DATA_i.repaint()

        match (int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_sw_force_en']], "big")&0b0000_0001):
            case 0b0:
                self.ui.comboBox_CFG_SW_force_EN.setCurrentIndex(0)
            case 0b1:
                self.ui.comboBox_CFG_SW_force_EN.setCurrentIndex(1)
        self.ui.comboBox_CFG_SW_force_EN.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_4']], "big")&0b1110_0000)>>5):
            case 0b000:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(0)
            case 0b001:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(1)
            case 0b010:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(2)
            case 0b011:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(3)
            case 0b100:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(4)
            case 0b101:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(5)
            case 0b110:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(6)
            case 0b111:
                self.ui.comboBox_EMUL_ADDR_i.setCurrentIndex(7)
        self.ui.comboBox_EMUL_ADDR_i.repaint()

        match (int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_3']], "big")&0b0000_0001):
            case 0b0:
                self.ui.comboBox_EMUL_EN_L0.setCurrentIndex(0)
            case 0b1:
                self.ui.comboBox_EMUL_EN_L0.setCurrentIndex(1)
        self.ui.comboBox_EMUL_EN_L0.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_3']], "big")&0b0000_0010)>>1):
            case 0b0:
                self.ui.comboBox_EMUL_EN_L1.setCurrentIndex(0)
            case 0b1:
                self.ui.comboBox_EMUL_EN_L1.setCurrentIndex(1)
        self.ui.comboBox_EMUL_EN_L1.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_3']], "big")&0b0000_1100)>>2):
            case 0b00:
                self.ui.comboBox_EMUL_tau_v.setCurrentIndex(0)
            case 0b01:
                self.ui.comboBox_EMUL_tau_v.setCurrentIndex(1)
            case 0b10:
                self.ui.comboBox_EMUL_tau_v.setCurrentIndex(2)
            case 0b11:
                self.ui.comboBox_EMUL_tau_v.setCurrentIndex(3)
        self.ui.comboBox_EMUL_tau_v.repaint()

        match ((int.from_bytes(regs.reg_data[registers_metadata_name_to_addr['cfg_ch_emul_3']], "big")&0b0011_0000)>>4):
            case 0b00:
                self.ui.comboBox_EMUL_L0_v.setCurrentIndex(0)
            case 0b01:
                self.ui.comboBox_EMUL_L0_v.setCurrentIndex(1)
            case 0b10:
                self.ui.comboBox_EMUL_L0_v.setCurrentIndex(2)
            case 0b11:
                self.ui.comboBox_EMUL_L0_v.setCurrentIndex(3)
        self.ui.comboBox_EMUL_L0_v.repaint()

        return

    def get_averaging_value(self) -> int:
        return self.ui.peak_measure_times.value()
    
    def is_char_test(self) -> bool:
        return self.ui.is_char_test.isChecked()

    def get_consts_status(self):
        return self.ui.is_analog_use.isChecked(), self.ui.is_analog_digit_use.isChecked(), self.ui.is_digit_use.isChecked()

    def get_code_from_box(self, data: str) -> int:
        try:
            code = int(regex.findall(".*\(([0-9]*)\)", data)[0], base=2)
        except Exception as e:
            print('Bad data!', e)
            return

        return code
    
    def get_testing_settings_checks(self):
        return self.ui.Is_send_consts.isChecked(), self.ui.is_read_consts.isChecked(), self.ui.is_read_interface_data.isChecked()

    def process_value_power(self, value:float|int, power:str) -> int|float:
        match power:
            case "MHz":
                return value*10**(3)
            case "kHz":
                return value*10**(3)
            case "V" | "s" | "Hz":
                return value
            case "mV" | "ms":
                return value*10**(-3)
            case "us":
                return value*10**(-6)
            case "ns":
                return value*10**(-9)
            case _:
                raise Exception("Bad dimension.")
            
    def process_signal_type_to_ui(self, signal) -> int:
        match signal:
            case "PULS":
                return 0
            case "SQU":
                return 1
            case "SIN":
                return 2
            case "RAMP":
                return 3
            case "NOIS":
                return 4
            case "USER":
                return 5
            case _:
                raise Exception("Bad signal type.")
            
    def get_polarity_status(self):
        match self.ui.comboBox_POL.currentIndex():
            case 0:
                return 1 
            case 1:
                return -1

    def process_power_to_value(self, value:float, type:str):
        match type:
            case "Hz":
                if 0<=value and value<1_000:
                    return value, 0
                elif 1_000<=value and value<1_000_000:
                    return value*10**(-3), 1
                elif 1_000_000<=value:
                    return value*10**(-6), 2
            case "V":
                if 0<=value and value<1:
                    return value*10**(3), 0
                elif 1<=value:
                    return value, 1
            case "s":
                if 0<=value and value<0.000001:
                    return value*10**(9), 0
                elif 0.000001<=value and value<0.001:
                    return value*10**(6), 3
                elif 0.001<=value and value<1:
                    return value*10**(3), 2
                elif 1<=value:
                    return value, 1

    def get_emulation_data(self):
        return self.ui.is_EM_ADC_EN.isChecked(),self.ui.is_EM_L0_L1.isChecked()

    def get_raw_data(self):
        return self.ui.lineEdit_raw_SPI.text().rstrip().lower()

    def change_emulation_state(self, state):
        self.ui.CH_EM_status.setValue(int(state))

    def change_CS_state(self, state):
        self.ui.CS_status.setValue(int(state))

    def change_rw_CS(self, state):
        self.ui.CS_status.setEnabled(not state)
        self.ui.toggle_CS_butt.setEnabled(not state)

    def get_auto_cs_status(self):
        return self.ui.is_auto_CS.isChecked()

    def get_generator_data_manual(self)-> GeneratorSample:
        return GeneratorSample(
            signal_type=process_signal_type(self.ui.signal_type_box.currentText()),
            ampl=self.process_value_power(self.ui.ampl.value(), self.ui.comboBox_ampl.currentText()),
            delay=self.process_value_power(self.ui.delay.value(), self.ui.comboBox_delay.currentText()),
            freq=self.process_value_power(self.ui.freq.value(), self.ui.comboBox_freq.currentText()),
            is_triggered=self.ui.checkBox_is_triggered.isChecked(),
            lead=self.process_value_power(self.ui.lead.value(), self.ui.comboBox_lead.currentText()),
            offset=self.process_value_power(self.ui.offset.value(), self.ui.comboBox_offset.currentText()),
            trail=self.process_value_power(self.ui.trail.value(), self.ui.comboBox_trail.currentText()),
            trig_lvl=self.process_value_power(self.ui.trig_lvl.value(), self.ui.comboBox_trig_lvl.currentText()),
            width=self.process_value_power(self.ui.width.value(), self.ui.comboBox_width.currentText()),
        )

    def create_sequence_samples(self, start, finish, count, rule) -> list[float] | list[int]:
        match count:
            case 1:
                return [start]
            case 2:
                return [start, finish]
            
        if finish==start or finish==0.0:
            return [start]
        
        # if finish<start:
        #     raise Exception("Finish value less than start value.")

        result = []
        match rule:
            case "linear":
                step = (finish-start)/(count-1)
                for i in range(count):
                    result.append(i*step+start)
                return result
            case "logarithmic":
                if start == 0.0 or finish == 0.0:
                    raise Exception("Forbidden to use zero value with logarithmic scale.")
                step = (finish/start)**(1/(count-1))
                for i in range(count):
                    result.append(start*step**i)
                return result
            case _:
                raise Exception("Bad sequence rule.")

    def get_regs_comm_data(self):
        return self.ui.comboBox_read_write.currentIndex(), self.ui.spinBox_reg_addr.value(), self.ui.spinBox_reg_value.value()

    def get_triggers_data(self) -> list[tuple[int, int]]:
        L0_sequence = self.create_sequence_samples(
            start=self.ui.L0.value(),
            finish=self.ui.L0_2.value(),
            count=self.ui.spinBox_L0_times.value(),
            rule=self.ui.comboBox_L0_delta.currentText(),
        )
        L1_sequence = self.create_sequence_samples(
            start=self.ui.L1.value(),
            finish=self.ui.L1_2.value(),
            count=self.ui.spinBox_L1_times.value(),
            rule=self.ui.comboBox_L1_delta.currentText(),
        )

        for idx, val in enumerate(L0_sequence):
            L0_sequence[idx] = val//5

        for idx, val in enumerate(L1_sequence):
            L1_sequence[idx] = val//5

        return list(product(
            L0_sequence,
            L1_sequence,
        )), self.ui.delay_trig.value()

    def get_generator_data_scenario(self)-> list[GeneratorSample]:
        sig_type = process_signal_type(self.ui.signal_type_box.currentText())
        offset = self.process_value_power(self.ui.offset.value(), self.ui.comboBox_offset.currentText())
        delay = self.process_value_power(self.ui.delay.value(), self.ui.comboBox_delay.currentText())
        trig = self.process_value_power(self.ui.trig_lvl.value(), self.ui.comboBox_trig_lvl.currentText())
        is_triggered = self.ui.checkBox_is_triggered.isChecked()

        width_sequence = self.create_sequence_samples(
            start=self.process_value_power(self.ui.width.value(), self.ui.comboBox_width.currentText()),
            finish=self.process_value_power(self.ui.width_2.value(), self.ui.comboBox_width_2.currentText()),
            count=self.ui.spinBox_width_times.value(),
            rule=self.ui.comboBox_width_delta.currentText(),
        )
        lead_sequence = self.create_sequence_samples(
            start=self.process_value_power(self.ui.lead.value(), self.ui.comboBox_lead.currentText()),
            finish=self.process_value_power(self.ui.lead_2.value(), self.ui.comboBox_lead_2.currentText()),
            count=self.ui.spinBox_lead_times.value(),
            rule=self.ui.comboBox_lead_delta.currentText(),
        )
        trail_sequence = self.create_sequence_samples(
            start=self.process_value_power(self.ui.trail.value(), self.ui.comboBox_trail.currentText()),
            finish=self.process_value_power(self.ui.trail_2.value(), self.ui.comboBox_trail_2.currentText()),
            count=self.ui.spinBox_trail_times.value(),
            rule=self.ui.comboBox_trail_delta.currentText(),
        )
        ampl_sequence = self.create_sequence_samples(
            start=self.process_value_power(self.ui.ampl.value(), self.ui.comboBox_ampl.currentText()),
            finish=self.process_value_power(self.ui.ampl_2.value(), self.ui.comboBox_ampl_2.currentText()),
            count=self.ui.spinBox_ampl_times.value(),
            rule=self.ui.comboBox_ampl_delta.currentText(),
        )
        freq_sequence = self.create_sequence_samples(
            start=self.process_value_power(self.ui.freq.value(), self.ui.comboBox_freq.currentText()),
            finish=self.process_value_power(self.ui.freq_2.value(), self.ui.comboBox_freq_2.currentText()),
            count=self.ui.spinBox_freq_times.value(),
            rule=self.ui.comboBox_freq_delta.currentText(),
        )
        parameters_lists = list(product(
            width_sequence,
            lead_sequence,
            trail_sequence,
            ampl_sequence,
            freq_sequence,
        ))

        scenario_samples = []
        for sample in parameters_lists:
            scenario_samples.append(GeneratorSample(
                signal_type=sig_type,
                is_triggered=is_triggered,
                trig_lvl=trig,
                offset=offset,
                delay=delay,
                width=sample[0],
                lead=sample[1],
                trail=sample[2],
                ampl=sample[3],
                freq=sample[4],
            ))

        if len(scenario_samples) == 1:
            if scenario_samples[0].width+scenario_samples[0].ampl+scenario_samples[0].lead+scenario_samples[0].trail== 0:
                return []
        return scenario_samples

    def set_triggers_data_zero(self):
        self.ui.L0.setValue(500)
        self.ui.L0.repaint()
        self.ui.L0_2.setValue(0)
        self.ui.L0_2.repaint()
        self.ui.spinBox_L0_times.setValue(1)
        self.ui.spinBox_L0_times.repaint()
        self.ui.comboBox_L0_delta.setCurrentIndex(0)
        self.ui.comboBox_L0_delta.repaint()
        self.ui.L1.setValue(10000)
        self.ui.L1.repaint()
        self.ui.L1_2.setValue(0)
        self.ui.L1_2.repaint()
        self.ui.spinBox_L1_times.setValue(1)
        self.ui.spinBox_L1_times.repaint()
        self.ui.comboBox_L1_delta.setCurrentIndex(0)
        self.ui.comboBox_L1_delta.repaint()

    def set_triggers_data(self, l0, l1):
        self.set_triggers_data_zero()
        self.ui.L0.setValue(l0)
        self.ui.L1.setValue(l1)

    def set_generator_data_zero(self) -> None:
        self.ui.signal_type_box.setCurrentIndex(0)
        self.ui.signal_type_box.repaint()
        self.ui.offset.setValue(0)
        self.ui.offset.repaint()
        self.ui.delay.setValue(0)
        self.ui.delay.repaint()
        self.ui.comboBox_offset.setCurrentIndex(0)
        self.ui.comboBox_offset.repaint()
        self.ui.comboBox_delay.setCurrentIndex(0)
        self.ui.comboBox_delay.repaint()
        self.ui.width.setValue(0)
        self.ui.width.repaint()
        self.ui.width_2.setValue(0)
        self.ui.width_2.repaint()
        self.ui.spinBox_width_times.setValue(0)
        self.ui.spinBox_width_times.repaint()
        self.ui.comboBox_width.setCurrentIndex(0)
        self.ui.comboBox_width.repaint()
        self.ui.comboBox_width_2.setCurrentIndex(0)
        self.ui.comboBox_width_2.repaint()
        self.ui.comboBox_width_delta.setCurrentIndex(0)
        self.ui.comboBox_width_delta.repaint()
        self.ui.lead.setValue(0)
        self.ui.lead.repaint()
        self.ui.lead_2.setValue(0)
        self.ui.lead_2.repaint()
        self.ui.spinBox_lead_times.setValue(0)
        self.ui.spinBox_lead_times.repaint()
        self.ui.comboBox_lead.setCurrentIndex(0)
        self.ui.comboBox_lead.repaint()
        self.ui.comboBox_lead_2.setCurrentIndex(0)
        self.ui.comboBox_lead_2.repaint()
        self.ui.comboBox_lead_delta.setCurrentIndex(0)
        self.ui.comboBox_lead_delta.repaint()
        self.ui.trail.setValue(0)
        self.ui.trail.repaint()
        self.ui.trail_2.setValue(0)
        self.ui.trail_2.repaint()
        self.ui.spinBox_trail_times.setValue(0)
        self.ui.spinBox_trail_times.repaint()
        self.ui.comboBox_trail.setCurrentIndex(0)
        self.ui.comboBox_trail.repaint()
        self.ui.comboBox_trail_2.setCurrentIndex(0)
        self.ui.comboBox_trail_2.repaint()
        self.ui.comboBox_trail_delta.setCurrentIndex(0)
        self.ui.comboBox_trail_delta.repaint()
        self.ui.ampl.setValue(0)
        self.ui.ampl.repaint()
        self.ui.ampl_2.setValue(0)
        self.ui.ampl_2.repaint()
        self.ui.spinBox_ampl_times.setValue(0)
        self.ui.spinBox_ampl_times.repaint()
        self.ui.comboBox_ampl.setCurrentIndex(0)
        self.ui.comboBox_ampl.repaint()
        self.ui.comboBox_ampl_2.setCurrentIndex(0)
        self.ui.comboBox_ampl_2.repaint()
        self.ui.comboBox_ampl_delta.setCurrentIndex(0)
        self.ui.comboBox_ampl_delta.repaint()
        self.ui.freq.setValue(0)
        self.ui.freq.repaint()
        self.ui.freq_2.setValue(0)
        self.ui.freq_2.repaint()
        self.ui.spinBox_freq_times.setValue(0)
        self.ui.spinBox_freq_times.repaint()
        self.ui.comboBox_freq.setCurrentIndex(0)
        self.ui.comboBox_freq.repaint()
        self.ui.comboBox_freq_2.setCurrentIndex(0)
        self.ui.comboBox_freq_2.repaint()
        self.ui.comboBox_freq_delta.setCurrentIndex(0)
        self.ui.comboBox_freq_delta.repaint()
        self.ui.checkBox_is_triggered.setChecked(True)
        self.ui.checkBox_is_triggered.repaint()
        self.ui.trig_lvl.setValue(200)
        self.ui.trig_lvl.repaint()
        self.ui.comboBox_trig_lvl.setCurrentIndex(0)
        self.ui.comboBox_trig_lvl.repaint()

    def reset_scenario_data(self)->None:
        self.ui.scenario_name.setText("")
        self.ui.scenario_desc_plain_text_input.setPlainText("")
        self.ui.spinBox_layer_count.setValue(0)
        self.ui.scenario_status_plain_text.setPlainText("")

    def get_scenario_data(self):
        return self.ui.scenario_name.text(), self.ui.scenario_desc_plain_text_input.toPlainText(), self.ui.spinBox_layer_count.value()

    def increase_layer_count(self) -> None:
        self.ui.spinBox_layer_count.setValue(self.ui.spinBox_layer_count.value() + 1)

    def decrease_layer_count(self) -> None:
        self.ui.spinBox_layer_count.setValue(self.ui.spinBox_layer_count.value() - 1)

    def add_log_layer_data(self, layer_count, test_count) -> None:
        history = self.ui.scenario_status_plain_text.toPlainText()
        self.ui.scenario_status_plain_text.setPlainText(history+f"layer:{layer_count}, tests:{test_count};\n")

    def set_channels_data_zero(self):
        self.ui.trigger_src_box.setCurrentIndex(0)
        self.ui.trigger_src_box.repaint()
        self.ui.trig_lvl_oscilloscope.setValue(200)
        self.ui.trig_lvl_oscilloscope.repaint()
        self.ui.comboBox_trig_lvl_oscilloscope.setCurrentIndex(0)
        self.ui.comboBox_trig_lvl_oscilloscope.repaint()

        self.ui.scale_time.setValue(100)
        self.ui.scale_time.repaint()
        self.ui.comboBox_time_scale.setCurrentIndex(0)
        self.ui.comboBox_time_scale.repaint()
        
        self.ui.checkBox_is_use_chan_1.setChecked(False)
        self.ui.checkBox_is_use_chan_1.repaint()
        self.ui.line_chan_1_name.setText("")
        self.ui.line_chan_1_name.repaint()
        self.ui.scale_ch_1.setValue(200)
        self.ui.scale_ch_1.repaint()
        self.ui.scale_ch_1_power.setCurrentIndex(0)
        self.ui.scale_ch_1_power.repaint()
        self.ui.checkBox_is_use_chan_2.setChecked(False)
        self.ui.checkBox_is_use_chan_2.repaint()
        self.ui.line_chan_2_name.setText("")
        self.ui.line_chan_2_name.repaint()
        self.ui.scale_ch_2.setValue(200)
        self.ui.scale_ch_2.repaint()
        self.ui.scale_ch_2_power.setCurrentIndex(0)
        self.ui.scale_ch_2_power.repaint()
        self.ui.checkBox_is_use_chan_3.setChecked(False)
        self.ui.checkBox_is_use_chan_3.repaint()
        self.ui.line_chan_3_name.setText("")
        self.ui.line_chan_3_name.repaint()
        self.ui.scale_ch_3.setValue(200)
        self.ui.scale_ch_3.repaint()
        self.ui.scale_ch_3_power.setCurrentIndex(0)
        self.ui.scale_ch_3_power.repaint()
        self.ui.checkBox_is_use_chan_4.setChecked(False)
        self.ui.checkBox_is_use_chan_4.repaint()
        self.ui.line_chan_4_name.setText("")
        self.ui.line_chan_4_name.repaint()
        self.ui.scale_ch_4.setValue(200)
        self.ui.scale_ch_4.repaint()
        self.ui.scale_ch_4_power.setCurrentIndex(0)
        self.ui.scale_ch_4_power.repaint()
        return

    def set_channels_data(self, channels:list[Channel], trig_src, trig_lvl, tim_scale):
        self.set_channels_data_zero()
        if len(channels) == 0:
            return

        self.ui.trigger_src_box.setCurrentIndex(trig_src)
        self.ui.trigger_src_box.repaint()
        trig_lvl_value, trig_lvl_index = self.process_power_to_value(trig_lvl, "V")
        self.ui.trig_lvl_oscilloscope.setValue(trig_lvl_value)
        self.ui.trig_lvl_oscilloscope.repaint()
        self.ui.comboBox_trig_lvl_oscilloscope.setCurrentIndex(trig_lvl_index)
        self.ui.comboBox_trig_lvl_oscilloscope.repaint()

        time_scale_value, time_scale_index = self.process_power_to_value(tim_scale, "s")
        self.ui.scale_time.setValue(time_scale_value)
        self.ui.scale_time.repaint()
        self.ui.comboBox_time_scale.setCurrentIndex(time_scale_index)
        self.ui.comboBox_time_scale.repaint()

        for ch in channels:
            match ch.index:
                case 1:
                    self.ui.checkBox_is_use_chan_1.setChecked(True)
                    self.ui.checkBox_is_use_chan_1.repaint()
                    self.ui.line_chan_1_name.setText(ch.name)
                    self.ui.line_chan_1_name.repaint()
                    ch_1_value, ch_1_index = self.process_power_to_value(ch.scale, "V")
                    self.ui.scale_ch_1.setValue(ch_1_value)
                    self.ui.scale_ch_1.repaint()
                    self.ui.scale_ch_1_power.setCurrentIndex(ch_1_index)
                    self.ui.scale_ch_1_power.repaint()
                case 2:
                    self.ui.checkBox_is_use_chan_2.setChecked(True)
                    self.ui.checkBox_is_use_chan_2.repaint()
                    self.ui.line_chan_2_name.setText(ch.name)
                    self.ui.line_chan_2_name.repaint()
                    ch_2_value, ch_2_index = self.process_power_to_value(ch.scale, "V")
                    self.ui.scale_ch_2.setValue(ch_2_value)
                    self.ui.scale_ch_2.repaint()
                    self.ui.scale_ch_2_power.setCurrentIndex(ch_2_index)
                    self.ui.scale_ch_2_power.repaint()
                case 3:
                    self.ui.checkBox_is_use_chan_3.setChecked(True)
                    self.ui.checkBox_is_use_chan_3.repaint()
                    self.ui.line_chan_3_name.setText(ch.name)
                    self.ui.line_chan_3_name.repaint()
                    ch_3_value, ch_3_index = self.process_power_to_value(ch.scale, "V")
                    self.ui.scale_ch_3.setValue(ch_3_value)
                    self.ui.scale_ch_3.repaint()
                    self.ui.scale_ch_3_power.setCurrentIndex(ch_3_index)
                    self.ui.scale_ch_3_power.repaint()
                case 4:
                    self.ui.checkBox_is_use_chan_4.setChecked(True)
                    self.ui.checkBox_is_use_chan_4.repaint()
                    self.ui.line_chan_4_name.setText(ch.name)
                    self.ui.line_chan_4_name.repaint()
                    ch_4_value, ch_4_index = self.process_power_to_value(ch.scale, "V")
                    self.ui.scale_ch_4.setValue(ch_4_value)
                    self.ui.scale_ch_4.repaint()
                    self.ui.scale_ch_4_power.setCurrentIndex(ch_4_index)
                    self.ui.scale_ch_4_power.repaint()
        return
    
    def set_generator_sample(self, sample:GeneratorSample):
        self.set_generator_data_zero()

        self.ui.signal_type_box.setCurrentIndex(self.process_signal_type_to_ui(sample.signal_type))
        self.ui.signal_type_box.repaint()
        
        offset_value, offset_index = self.process_power_to_value(sample.offset, "V")
        self.ui.offset.setValue(offset_value)
        self.ui.offset.repaint()
        self.ui.comboBox_offset.setCurrentIndex(offset_index)
        self.ui.comboBox_offset.repaint()

        delay_value, delay_index = self.process_power_to_value(sample.delay, "s")
        self.ui.delay.setValue(delay_value)
        self.ui.delay.repaint()
        self.ui.comboBox_delay.setCurrentIndex(delay_index)
        self.ui.comboBox_delay.repaint()

        width_value, width_index = self.process_power_to_value(sample.width, "s")
        self.ui.width.setValue(width_value)
        self.ui.width.repaint()
        self.ui.comboBox_width.setCurrentIndex(width_index)
        self.ui.comboBox_width.repaint()

        lead_value, lead_index = self.process_power_to_value(sample.lead, "s")
        self.ui.lead.setValue(lead_value)
        self.ui.lead.repaint()
        self.ui.comboBox_lead.setCurrentIndex(lead_index)
        self.ui.comboBox_lead.repaint()

        trail_value, trail_index = self.process_power_to_value(sample.trail, "s")
        self.ui.trail.setValue(trail_value)
        self.ui.trail.repaint()
        self.ui.comboBox_trail.setCurrentIndex(trail_index)
        self.ui.comboBox_trail.repaint()

        ampl_value, ampl_index = self.process_power_to_value(sample.ampl, "V")
        self.ui.ampl.setValue(ampl_value)
        self.ui.ampl.repaint()
        self.ui.comboBox_ampl.setCurrentIndex(ampl_index)
        self.ui.comboBox_ampl.repaint()

        freq_value, freq_index = self.process_power_to_value(sample.freq, "Hz")
        self.ui.freq.setValue(freq_value)
        self.ui.freq.repaint()
        self.ui.comboBox_freq.setCurrentIndex(freq_index)
        self.ui.comboBox_freq.repaint()

        self.ui.checkBox_is_triggered.setChecked(sample.is_triggered)
        self.ui.checkBox_is_triggered.repaint()
        trig_value, trig_index = self.process_power_to_value(sample.trig_lvl, "V")
        self.ui.trig_lvl.setValue(trig_value)
        self.ui.trig_lvl.repaint()
        self.ui.comboBox_trig_lvl.setCurrentIndex(trig_index)
        self.ui.comboBox_trig_lvl.repaint()

    
    def get_channels_data(self):
        channels = []
        trig_lvl = self.process_value_power(self.ui.trig_lvl_oscilloscope.value(), self.ui.comboBox_trig_lvl_oscilloscope.currentText())
        tim_scale = self.process_value_power(self.ui.scale_time.value(), self.ui.comboBox_time_scale.currentText())

        if self.ui.checkBox_is_use_chan_1.isChecked():
            name = self.ui.line_chan_1_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #1")
            channels.append(Channel(name, 1, self.process_value_power(self.ui.scale_ch_1.value(), self.ui.scale_ch_1_power.currentText())))
        if self.ui.checkBox_is_use_chan_2.isChecked():
            name = self.ui.line_chan_2_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #2")
            channels.append(Channel(name, 2, self.process_value_power(self.ui.scale_ch_2.value(), self.ui.scale_ch_2_power.currentText())))
        if self.ui.checkBox_is_use_chan_3.isChecked():
            name = self.ui.line_chan_3_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #3")
            channels.append(Channel(name, 3, self.process_value_power(self.ui.scale_ch_3.value(), self.ui.scale_ch_3_power.currentText())))
        if self.ui.checkBox_is_use_chan_4.isChecked():
            name = self.ui.line_chan_4_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #4")
            channels.append(Channel(name, 4, self.process_value_power(self.ui.scale_ch_4.value(), self.ui.scale_ch_4_power.currentText())))

        if len(channels) == 0:
            return [], 0, 0, 0

        if self.ui.trigger_src_box.currentIndex() == 0:
            raise Exception(f"Need to chose channel to trigger source.")

        flag = 0
        for ch in channels:
            if ch.index == self.ui.trigger_src_box.currentIndex():
                flag = 1
                break
        
        if flag == 0:
            raise Exception(f"Trigger source is unused channel.")
        
        return channels, self.ui.trigger_src_box.currentIndex(), trig_lvl, tim_scale
        
    def delete_last_layer(self):
        if self.ui.spinBox_layer_count.value() == 0:
            return
        self.decrease_layer_count()
        history = self.ui.scenario_status_plain_text.toPlainText()
        history_parts = history.split("\n")
        data = ""
        for part in history_parts[:-2]:
            data += part + "\n"
        self.ui.scenario_status_plain_text.setPlainText(data)

    def change_rw_gen(self):
        self.ui.signal_type_box.setEnabled(self.is_gen_readonly)
        self.ui.signal_type_box.repaint()
        self.ui.offset.setEnabled(self.is_gen_readonly)
        self.ui.offset.repaint()
        self.ui.delay.setEnabled(self.is_gen_readonly)
        self.ui.delay.repaint()
        self.ui.comboBox_offset.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_offset.repaint()
        self.ui.comboBox_delay.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_delay.repaint()
        self.ui.width.setEnabled(self.is_gen_readonly)
        self.ui.width.repaint()
        self.ui.width_2.setEnabled(self.is_gen_readonly)
        self.ui.width_2.repaint()
        self.ui.spinBox_width_times.setEnabled(self.is_gen_readonly)
        self.ui.spinBox_width_times.repaint()
        self.ui.comboBox_width.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_width.repaint()
        self.ui.comboBox_width_2.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_width_2.repaint()
        self.ui.comboBox_width_delta.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_width_delta.repaint()
        self.ui.lead.setEnabled(self.is_gen_readonly)
        self.ui.lead.repaint()
        self.ui.lead_2.setEnabled(self.is_gen_readonly)
        self.ui.lead_2.repaint()
        self.ui.spinBox_lead_times.setEnabled(self.is_gen_readonly)
        self.ui.spinBox_lead_times.repaint()
        self.ui.comboBox_lead.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_lead.repaint()
        self.ui.comboBox_lead_2.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_lead_2.repaint()
        self.ui.comboBox_lead_delta.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_lead_delta.repaint()
        self.ui.trail.setEnabled(self.is_gen_readonly)
        self.ui.trail.repaint()
        self.ui.trail_2.setEnabled(self.is_gen_readonly)
        self.ui.trail_2.repaint()
        self.ui.spinBox_trail_times.setEnabled(self.is_gen_readonly)
        self.ui.spinBox_trail_times.repaint()
        self.ui.comboBox_trail.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_trail.repaint()
        self.ui.comboBox_trail_2.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_trail_2.repaint()
        self.ui.comboBox_trail_delta.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_trail_delta.repaint()
        self.ui.ampl.setEnabled(self.is_gen_readonly)
        self.ui.ampl.repaint()
        self.ui.ampl_2.setEnabled(self.is_gen_readonly)
        self.ui.ampl_2.repaint()
        self.ui.spinBox_ampl_times.setEnabled(self.is_gen_readonly)
        self.ui.spinBox_ampl_times.repaint()
        self.ui.comboBox_ampl.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_ampl.repaint()
        self.ui.comboBox_ampl_2.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_ampl_2.repaint()
        self.ui.comboBox_ampl_delta.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_ampl_delta.repaint()
        self.ui.freq.setEnabled(self.is_gen_readonly)
        self.ui.freq.repaint()
        self.ui.freq_2.setEnabled(self.is_gen_readonly)
        self.ui.freq_2.repaint()
        self.ui.spinBox_freq_times.setEnabled(self.is_gen_readonly)
        self.ui.spinBox_freq_times.repaint()
        self.ui.comboBox_freq.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_freq.repaint()
        self.ui.comboBox_freq_2.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_freq_2.repaint()
        self.ui.comboBox_freq_delta.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_freq_delta.repaint()
        self.ui.checkBox_is_triggered.setEnabled(self.is_gen_readonly)
        self.ui.checkBox_is_triggered.repaint()
        self.ui.trig_lvl.setEnabled(self.is_gen_readonly)
        self.ui.trig_lvl.repaint()
        self.ui.comboBox_trig_lvl.setEnabled(self.is_gen_readonly)
        self.ui.comboBox_trig_lvl.repaint()
        self.ui.gen_zero_butt.setEnabled(self.is_gen_readonly)
        self.ui.gen_zero_butt.repaint()
        self.is_gen_readonly = not self.is_gen_readonly

    def set_gen_writeable(self):
        self.ui.signal_type_box.setEnabled(True)
        self.ui.signal_type_box.repaint()
        self.ui.offset.setEnabled(True)
        self.ui.offset.repaint()
        self.ui.delay.setEnabled(True)
        self.ui.delay.repaint()
        self.ui.comboBox_offset.setEnabled(True)
        self.ui.comboBox_offset.repaint()
        self.ui.comboBox_delay.setEnabled(True)
        self.ui.comboBox_delay.repaint()
        self.ui.width.setEnabled(True)
        self.ui.width.repaint()
        self.ui.width_2.setEnabled(True)
        self.ui.width_2.repaint()
        self.ui.spinBox_width_times.setEnabled(True)
        self.ui.spinBox_width_times.repaint()
        self.ui.comboBox_width.setEnabled(True)
        self.ui.comboBox_width.repaint()
        self.ui.comboBox_width_2.setEnabled(True)
        self.ui.comboBox_width_2.repaint()
        self.ui.comboBox_width_delta.setEnabled(True)
        self.ui.comboBox_width_delta.repaint()
        self.ui.lead.setEnabled(True)
        self.ui.lead.repaint()
        self.ui.lead_2.setEnabled(True)
        self.ui.lead_2.repaint()
        self.ui.spinBox_lead_times.setEnabled(True)
        self.ui.spinBox_lead_times.repaint()
        self.ui.comboBox_lead.setEnabled(True)
        self.ui.comboBox_lead.repaint()
        self.ui.comboBox_lead_2.setEnabled(True)
        self.ui.comboBox_lead_2.repaint()
        self.ui.comboBox_lead_delta.setEnabled(True)
        self.ui.comboBox_lead_delta.repaint()
        self.ui.trail.setEnabled(True)
        self.ui.trail.repaint()
        self.ui.trail_2.setEnabled(True)
        self.ui.trail_2.repaint()
        self.ui.spinBox_trail_times.setEnabled(True)
        self.ui.spinBox_trail_times.repaint()
        self.ui.comboBox_trail.setEnabled(True)
        self.ui.comboBox_trail.repaint()
        self.ui.comboBox_trail_2.setEnabled(True)
        self.ui.comboBox_trail_2.repaint()
        self.ui.comboBox_trail_delta.setEnabled(True)
        self.ui.comboBox_trail_delta.repaint()
        self.ui.ampl.setEnabled(True)
        self.ui.ampl.repaint()
        self.ui.ampl_2.setEnabled(True)
        self.ui.ampl_2.repaint()
        self.ui.spinBox_ampl_times.setEnabled(True)
        self.ui.spinBox_ampl_times.repaint()
        self.ui.comboBox_ampl.setEnabled(True)
        self.ui.comboBox_ampl.repaint()
        self.ui.comboBox_ampl_2.setEnabled(True)
        self.ui.comboBox_ampl_2.repaint()
        self.ui.comboBox_ampl_delta.setEnabled(True)
        self.ui.comboBox_ampl_delta.repaint()
        self.ui.freq.setEnabled(True)
        self.ui.freq.repaint()
        self.ui.freq_2.setEnabled(True)
        self.ui.freq_2.repaint()
        self.ui.spinBox_freq_times.setEnabled(True)
        self.ui.spinBox_freq_times.repaint()
        self.ui.comboBox_freq.setEnabled(True)
        self.ui.comboBox_freq.repaint()
        self.ui.comboBox_freq_2.setEnabled(True)
        self.ui.comboBox_freq_2.repaint()
        self.ui.comboBox_freq_delta.setEnabled(True)
        self.ui.comboBox_freq_delta.repaint()
        self.ui.checkBox_is_triggered.setEnabled(True)
        self.ui.checkBox_is_triggered.repaint()
        self.ui.trig_lvl.setEnabled(True)
        self.ui.trig_lvl.repaint()
        self.ui.comboBox_trig_lvl.setEnabled(True)
        self.ui.comboBox_trig_lvl.repaint()
        self.ui.gen_zero_butt.setEnabled(True)
        self.ui.gen_zero_butt.repaint()
        self.is_gen_readonly = False

    def change_rw_channels(self):
        self.ui.scale_time.setEnabled(self.is_channels_readonly)
        self.ui.scale_time.repaint()
        self.ui.comboBox_time_scale.setEnabled(self.is_channels_readonly)
        self.ui.comboBox_time_scale.repaint()
        self.ui.checkBox_is_use_chan_1.setEnabled(self.is_channels_readonly)
        self.ui.checkBox_is_use_chan_1.repaint()
        self.ui.line_chan_1_name.setEnabled(self.is_channels_readonly)
        self.ui.line_chan_1_name.repaint()
        self.ui.scale_ch_1.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_1.repaint()
        self.ui.scale_ch_1_power.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_1_power.repaint()
        self.ui.checkBox_is_use_chan_2.setEnabled(self.is_channels_readonly)
        self.ui.checkBox_is_use_chan_2.repaint()
        self.ui.line_chan_2_name.setEnabled(self.is_channels_readonly)
        self.ui.line_chan_2_name.repaint()
        self.ui.scale_ch_2.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_2.repaint()
        self.ui.scale_ch_2_power.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_2_power.repaint()
        self.ui.checkBox_is_use_chan_3.setEnabled(self.is_channels_readonly)
        self.ui.checkBox_is_use_chan_3.repaint()
        self.ui.line_chan_3_name.setEnabled(self.is_channels_readonly)
        self.ui.line_chan_3_name.repaint()
        self.ui.scale_ch_3.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_3.repaint()
        self.ui.scale_ch_3_power.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_3_power.repaint()
        self.ui.checkBox_is_use_chan_4.setEnabled(self.is_channels_readonly)
        self.ui.checkBox_is_use_chan_4.repaint()
        self.ui.line_chan_4_name.setEnabled(self.is_channels_readonly)
        self.ui.line_chan_4_name.repaint()
        self.ui.scale_ch_4.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_4.repaint()
        self.ui.scale_ch_4_power.setEnabled(self.is_channels_readonly)
        self.ui.scale_ch_4_power.repaint()
        self.ui.trigger_src_box.setEnabled(self.is_channels_readonly)
        self.ui.trigger_src_box.repaint()
        self.ui.trig_lvl_oscilloscope.setEnabled(self.is_channels_readonly)
        self.ui.trig_lvl_oscilloscope.repaint()
        self.ui.comboBox_trig_lvl_oscilloscope.setEnabled(self.is_channels_readonly)
        self.ui.comboBox_trig_lvl_oscilloscope.repaint()
        self.is_channels_readonly = not self.is_channels_readonly

    def set_channels_writeable(self):
        self.ui.scale_time.setEnabled(True)
        self.ui.scale_time.repaint()
        self.ui.comboBox_time_scale.setEnabled(True)
        self.ui.comboBox_time_scale.repaint()
        self.ui.checkBox_is_use_chan_1.setEnabled(True)
        self.ui.checkBox_is_use_chan_1.repaint()
        self.ui.line_chan_1_name.setEnabled(True)
        self.ui.line_chan_1_name.repaint()
        self.ui.scale_ch_1.setEnabled(True)
        self.ui.scale_ch_1.repaint()
        self.ui.scale_ch_1_power.setEnabled(True)
        self.ui.scale_ch_1_power.repaint()
        self.ui.checkBox_is_use_chan_2.setEnabled(True)
        self.ui.checkBox_is_use_chan_2.repaint()
        self.ui.line_chan_2_name.setEnabled(True)
        self.ui.line_chan_2_name.repaint()
        self.ui.scale_ch_2.setEnabled(True)
        self.ui.scale_ch_2.repaint()
        self.ui.scale_ch_2_power.setEnabled(True)
        self.ui.scale_ch_2_power.repaint()
        self.ui.checkBox_is_use_chan_3.setEnabled(True)
        self.ui.checkBox_is_use_chan_3.repaint()
        self.ui.line_chan_3_name.setEnabled(True)
        self.ui.line_chan_3_name.repaint()
        self.ui.scale_ch_3.setEnabled(True)
        self.ui.scale_ch_3.repaint()
        self.ui.scale_ch_3_power.setEnabled(True)
        self.ui.scale_ch_3_power.repaint()
        self.ui.checkBox_is_use_chan_4.setEnabled(True)
        self.ui.checkBox_is_use_chan_4.repaint()
        self.ui.line_chan_4_name.setEnabled(True)
        self.ui.line_chan_4_name.repaint()
        self.ui.scale_ch_4.setEnabled(True)
        self.ui.scale_ch_4.repaint()
        self.ui.scale_ch_4_power.setEnabled(True)
        self.ui.scale_ch_4_power.repaint()
        self.ui.trigger_src_box.setEnabled(True)
        self.ui.trigger_src_box.repaint()
        self.ui.trig_lvl_oscilloscope.setEnabled(True)
        self.ui.trig_lvl_oscilloscope.repaint()
        self.ui.comboBox_trig_lvl_oscilloscope.setEnabled(True)
        self.ui.comboBox_trig_lvl_oscilloscope.repaint()
        self.is_channels_readonly = False

    def change_rw_constants(self):
        self.ui.is_analog_use.setEnabled(self.is_regs_readonly)
        self.ui.is_analog_use.repaint()
        self.ui.is_analog_digit_use.setEnabled(self.is_regs_readonly)
        self.ui.is_analog_digit_use.repaint()
        self.ui.is_digit_use.setEnabled(self.is_regs_readonly)
        self.ui.is_digit_use.repaint()
        self.ui.Is_send_consts.setEnabled(self.is_regs_readonly)
        self.ui.Is_send_consts.repaint()
        self.ui.is_read_consts.setEnabled(self.is_regs_readonly)
        self.ui.is_read_consts.repaint()
        self.ui.is_read_interface_data.setEnabled(self.is_regs_readonly)
        self.ui.is_read_interface_data.repaint()
        self.ui.comboBox_CCAL.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_CCAL.repaint()
        self.ui.comboBox_CCSA.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_CCSA.repaint()
        self.ui.comboBox_GAIN.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_GAIN.repaint()
        self.ui.comboBox_ICSA.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_ICSA.repaint()
        self.ui.comboBox_SHA.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_SHA.repaint()
        self.ui.comboBox_SHTR.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_SHTR.repaint()
        self.ui.comboBox_POL.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_POL.repaint()
        self.ui.comboBox_BIAS_CORE_CUR.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_BIAS_CORE_CUR.repaint()
        self.ui.comboBox_EMUL_ADDR_i.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_EMUL_ADDR_i.repaint()
        self.ui.comboBox_EMUL_EN_L0.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_EMUL_EN_L0.repaint()
        self.ui.comboBox_EMUL_EN_L1.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_EMUL_EN_L1.repaint()
        self.ui.comboBox_EMUL_tau_v.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_EMUL_tau_v.repaint()
        self.ui.comboBox_EMUL_L0_v.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_EMUL_L0_v.repaint()
        self.ui.comboBox_CMP_TH.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_CMP_TH.repaint()
        self.ui.comboBox_CFG_SW_force_EN.setEnabled(self.is_regs_readonly)
        self.ui.comboBox_CFG_SW_force_EN.repaint()
        self.ui.spinBox_DAC_CAL.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_DAC_CAL.repaint()
        self.ui.spinBox_REZ.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_REZ.repaint()
        self.ui.spinBox_CAL_EN_CH.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CAL_EN_CH.repaint()
        self.ui.spinBox_AN_CH_DISABLE.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_AN_CH_DISABLE.repaint()
        self.ui.spinBox_CFG_p1_in_time.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p1_in_time.repaint()
        self.ui.spinBox_CFG_p1_L0_over.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p1_L0_over.repaint()
        self.ui.spinBox_CFG_p2_puls_SOC.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p2_puls_SOC.repaint()
        self.ui.spinBox_CFG_p2_puls_SWM.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p2_puls_SWM.repaint()
        self.ui.spinBox_CFG_p2_puls_EOC.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p2_puls_EOC.repaint()
        self.ui.spinBox_CFG_p3_L1_over.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_p3_L1_over.repaint()
        self.ui.spinBox_CFG_rst_puls_EOC.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_rst_puls_EOC.repaint()
        self.ui.spinBox_CFG_SW_force_num.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_SW_force_num.repaint()
        self.ui.spinBox_CFG_OUT_INT.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_CFG_OUT_INT.repaint()
        self.ui.spinBox_ADC_EMU_CFG.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_ADC_EMU_CFG.repaint()
        self.ui.spinBox_EMUL_DATA_i.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_EMUL_DATA_i.repaint()
        self.ui.spinBox_EMUL_L1_v.setEnabled(self.is_regs_readonly)
        self.ui.spinBox_EMUL_L1_v.repaint()
        self.ui.butt_set_default_regs.setEnabled(self.is_regs_readonly)
        self.ui.butt_set_default_regs.repaint()
        self.is_regs_readonly = not self.is_regs_readonly

    def set_constants_writeable(self):
        self.ui.is_analog_use.setEnabled(True)
        self.ui.is_analog_use.repaint()
        self.ui.is_analog_digit_use.setEnabled(True)
        self.ui.is_analog_digit_use.repaint()
        self.ui.is_digit_use.setEnabled(True)
        self.ui.is_digit_use.repaint()
        self.ui.Is_send_consts.setEnabled(True)
        self.ui.Is_send_consts.repaint()
        self.ui.is_read_consts.setEnabled(True)
        self.ui.is_read_consts.repaint()
        self.ui.is_read_interface_data.setEnabled(True)
        self.ui.is_read_interface_data.repaint()
        self.ui.comboBox_CCAL.setEnabled(True)
        self.ui.comboBox_CCAL.repaint()
        self.ui.comboBox_CCSA.setEnabled(True)
        self.ui.comboBox_CCSA.repaint()
        self.ui.comboBox_GAIN.setEnabled(True)
        self.ui.comboBox_GAIN.repaint()
        self.ui.comboBox_ICSA.setEnabled(True)
        self.ui.comboBox_ICSA.repaint()
        self.ui.comboBox_SHA.setEnabled(True)
        self.ui.comboBox_SHA.repaint()
        self.ui.comboBox_SHTR.setEnabled(True)
        self.ui.comboBox_SHTR.repaint()
        self.ui.comboBox_POL.setEnabled(True)
        self.ui.comboBox_POL.repaint()
        self.ui.comboBox_BIAS_CORE_CUR.setEnabled(True)
        self.ui.comboBox_BIAS_CORE_CUR.repaint()
        self.ui.comboBox_EMUL_ADDR_i.setEnabled(True)
        self.ui.comboBox_EMUL_ADDR_i.repaint()
        self.ui.comboBox_EMUL_EN_L0.setEnabled(True)
        self.ui.comboBox_EMUL_EN_L0.repaint()
        self.ui.comboBox_EMUL_EN_L1.setEnabled(True)
        self.ui.comboBox_EMUL_EN_L1.repaint()
        self.ui.comboBox_EMUL_tau_v.setEnabled(True)
        self.ui.comboBox_EMUL_tau_v.repaint()
        self.ui.comboBox_EMUL_L0_v.setEnabled(True)
        self.ui.comboBox_EMUL_L0_v.repaint()
        self.ui.comboBox_CMP_TH.setEnabled(True)
        self.ui.comboBox_CMP_TH.repaint()
        self.ui.comboBox_CFG_SW_force_EN.setEnabled(True)
        self.ui.comboBox_CFG_SW_force_EN.repaint()
        self.ui.spinBox_DAC_CAL.setEnabled(True)
        self.ui.spinBox_DAC_CAL.repaint()
        self.ui.spinBox_REZ.setEnabled(True)
        self.ui.spinBox_REZ.repaint()
        self.ui.spinBox_CAL_EN_CH.setEnabled(True)
        self.ui.spinBox_CAL_EN_CH.repaint()
        self.ui.spinBox_AN_CH_DISABLE.setEnabled(True)
        self.ui.spinBox_AN_CH_DISABLE.repaint()
        self.ui.spinBox_CFG_p1_in_time.setEnabled(True)
        self.ui.spinBox_CFG_p1_in_time.repaint()
        self.ui.spinBox_CFG_p1_L0_over.setEnabled(True)
        self.ui.spinBox_CFG_p1_L0_over.repaint()
        self.ui.spinBox_CFG_p2_puls_SOC.setEnabled(True)
        self.ui.spinBox_CFG_p2_puls_SOC.repaint()
        self.ui.spinBox_CFG_p2_puls_SWM.setEnabled(True)
        self.ui.spinBox_CFG_p2_puls_SWM.repaint()
        self.ui.spinBox_CFG_p2_puls_EOC.setEnabled(True)
        self.ui.spinBox_CFG_p2_puls_EOC.repaint()
        self.ui.spinBox_CFG_p3_L1_over.setEnabled(True)
        self.ui.spinBox_CFG_p3_L1_over.repaint()
        self.ui.spinBox_CFG_rst_puls_EOC.setEnabled(True)
        self.ui.spinBox_CFG_rst_puls_EOC.repaint()
        self.ui.spinBox_CFG_SW_force_num.setEnabled(True)
        self.ui.spinBox_CFG_SW_force_num.repaint()
        self.ui.spinBox_CFG_OUT_INT.setEnabled(True)
        self.ui.spinBox_CFG_OUT_INT.repaint()
        self.ui.spinBox_ADC_EMU_CFG.setEnabled(True)
        self.ui.spinBox_ADC_EMU_CFG.repaint()
        self.ui.spinBox_EMUL_DATA_i.setEnabled(True)
        self.ui.spinBox_EMUL_DATA_i.repaint()
        self.ui.spinBox_EMUL_L1_v.setEnabled(True)
        self.ui.spinBox_EMUL_L1_v.repaint()
        self.ui.butt_set_default_regs.setEnabled(True)
        self.ui.butt_set_default_regs.repaint()
        self.is_regs_readonly = False

    def set_env_writeable(self):
        self.ui.oscilloscope_conn_butt.setEnabled(True)
        self.ui.oscilloscope_conn_butt.repaint()
        self.ui.reset_osc_butt.setEnabled(True)
        self.ui.reset_osc_butt.repaint()
        self.ui.oscilloscope_addr.setEnabled(True)
        self.ui.oscilloscope_addr.repaint()
        self.ui.generator_addr.setEnabled(True)
        self.ui.generator_addr.repaint()
        self.ui.reset_gen_butt.setEnabled(True)
        self.ui.reset_gen_butt.repaint()
        self.ui.generator_conn_butt.setEnabled(True)
        self.ui.generator_conn_butt.repaint()
        self.ui.comboBox_resources.setEnabled(True)
        self.ui.comboBox_resources.repaint()
        self.ui.command_send_butt.setEnabled(True)
        self.ui.command_send_butt.repaint()
        self.ui.scan_res_butt.setEnabled(True)
        self.ui.scan_res_butt.repaint()
        self.is_env_readonly = False
        pass

    def change_rw_env(self):
        self.ui.oscilloscope_conn_butt.setEnabled(self.is_env_readonly)
        self.ui.oscilloscope_conn_butt.repaint()
        self.ui.reset_osc_butt.setEnabled(self.is_env_readonly)
        self.ui.reset_osc_butt.repaint()
        self.ui.oscilloscope_addr.setEnabled(self.is_env_readonly)
        self.ui.oscilloscope_addr.repaint()
        self.ui.generator_addr.setEnabled(self.is_env_readonly)
        self.ui.generator_addr.repaint()
        self.ui.reset_gen_butt.setEnabled(self.is_env_readonly)
        self.ui.reset_gen_butt.repaint()
        self.ui.generator_conn_butt.setEnabled(self.is_env_readonly)
        self.ui.generator_conn_butt.repaint()
        self.ui.comboBox_resources.setEnabled(self.is_env_readonly)
        self.ui.comboBox_resources.repaint()
        self.ui.command_send_butt.setEnabled(self.is_env_readonly)
        self.ui.command_send_butt.repaint()
        self.ui.scan_res_butt.setEnabled(self.is_env_readonly)
        self.ui.scan_res_butt.repaint()
        self.is_env_readonly = not self.is_env_readonly
        pass

    def set_uart_writeable(self):
        self.ui.com_addr.setEnabled(True)
        self.ui.com_addr.repaint()
        self.ui.com_conn_butt.setEnabled(True)
        self.ui.com_conn_butt.repaint()
        self.ui.com_write_butt.setEnabled(True)
        self.ui.com_write_butt.repaint()
        self.ui.com_read_all_butt.setEnabled(True)
        self.ui.com_read_all_butt.repaint()
        self.ui.com_read_r_butt.setEnabled(True)
        self.ui.com_read_r_butt.repaint()
        self.ui.com_read_rw_butt.setEnabled(True)
        self.ui.com_read_rw_butt.repaint()
        self.is_uart_readonly = False
        pass

    def change_rw_uart(self):
        self.ui.com_addr.setEnabled(self.is_uart_readonly)
        self.ui.com_addr.repaint()
        self.ui.com_conn_butt.setEnabled(self.is_uart_readonly)
        self.ui.com_conn_butt.repaint()
        self.ui.com_write_butt.setEnabled(self.is_uart_readonly)
        self.ui.com_write_butt.repaint()
        self.ui.com_read_all_butt.setEnabled(self.is_uart_readonly)
        self.ui.com_read_all_butt.repaint()
        self.ui.com_read_r_butt.setEnabled(self.is_uart_readonly)
        self.ui.com_read_r_butt.repaint()
        self.ui.com_read_rw_butt.setEnabled(self.is_uart_readonly)
        self.ui.com_read_rw_butt.repaint()
        self.is_uart_readonly = not self.is_uart_readonly
        pass

    def set_testing_writeable(self):
        self.ui.is_EM_ADC_EN.setEnabled(True)
        self.ui.is_EM_ADC_EN.repaint()
        self.ui.is_EM_L0_L1.setEnabled(True)
        self.ui.is_EM_L0_L1.repaint()
        self.ui.toggle_CH_EM_butt.setEnabled(True)
        self.ui.toggle_CH_EM_butt.repaint()
        self.ui.save_trigs_comm.setEnabled(True)
        self.ui.save_trigs_comm.repaint()
        self.ui.send_start_em_comm.setEnabled(True)
        self.ui.send_start_em_comm.repaint()
        self.ui.send_start_comm.setEnabled(True)
        self.ui.send_start_comm.repaint()
        self.ui.command_send_butt_2.setEnabled(True)
        self.ui.command_send_butt_2.repaint()
        self.ui.is_auto_CS.setEnabled(True)
        self.ui.is_auto_CS.repaint()
        self.ui.toggle_CS_butt.setEnabled(True)
        self.ui.toggle_CS_butt.repaint()
        self.ui.command_send_raw_butt.setEnabled(True)
        self.ui.command_send_raw_butt.repaint()
        self.ui.isScreenshotable.setEnabled(True)
        self.ui.isScreenshotable.repaint()
        self.ui.isScreenshotable_scenario.setEnabled(True)
        self.ui.isScreenshotable_scenario.repaint()
        self.ui.comboBox_using_out.setEnabled(True)
        self.ui.comboBox_using_out.repaint()
        self.ui.comboBox_scenario_using_out.setEnabled(True)
        self.ui.comboBox_scenario_using_out.repaint()
        self.ui.start_butt.setEnabled(True)
        self.ui.start_butt.repaint()
        self.ui.start_butt_scenar.setEnabled(True)
        self.ui.start_butt_scenar.repaint()
        self.ui.gen_config_butt.setEnabled(True)
        self.ui.gen_config_butt.repaint()
        self.ui.osc_config_butt.setEnabled(True)
        self.ui.osc_config_butt.repaint()
        self.ui.gen_out_butt.setEnabled(True)
        self.ui.gen_out_butt.repaint()
        self.ui.gen_not_out_butt.setEnabled(True)
        self.ui.gen_not_out_butt.repaint()
        self.ui.osc_run_butt.setEnabled(True)
        self.ui.osc_run_butt.repaint()
        self.ui.measure_butt.setEnabled(True)
        self.ui.measure_butt.repaint()
        self.ui.scan_scen_butt.setEnabled(True)
        self.ui.scan_scen_butt.repaint()
        self.ui.comboBox_scenarios.setEnabled(True)
        self.ui.comboBox_scenarios.repaint()
        self.ui.generate_scen_butt.setEnabled(True)
        self.ui.generate_scen_butt.repaint()
        self.ui.add_layer_scen_butt.setEnabled(True)
        self.ui.add_layer_scen_butt.repaint()
        self.ui.delete_layer_scen_butt.setEnabled(True)
        self.ui.delete_layer_scen_butt.repaint()
        self.ui.reset_scen_butt.setEnabled(True)
        self.ui.reset_scen_butt.repaint()
        self.ui.scenario_desc_plain_text_input.setEnabled(True)
        self.ui.scenario_desc_plain_text_input.repaint()
        self.ui.scenario_name.setEnabled(True)
        self.ui.scenario_name.repaint()
        self.is_testing_readonly = False
        pass

    def change_rw_testing(self):
        self.ui.is_EM_ADC_EN.setEnabled(self.is_testing_readonly)
        self.ui.is_EM_ADC_EN.repaint()
        self.ui.is_EM_L0_L1.setEnabled(self.is_testing_readonly)
        self.ui.is_EM_L0_L1.repaint()
        self.ui.toggle_CH_EM_butt.setEnabled(self.is_testing_readonly)
        self.ui.toggle_CH_EM_butt.repaint()
        self.ui.save_trigs_comm.setEnabled(self.is_testing_readonly)
        self.ui.save_trigs_comm.repaint()
        self.ui.send_start_em_comm.setEnabled(self.is_testing_readonly)
        self.ui.send_start_em_comm.repaint()
        self.ui.send_start_comm.setEnabled(self.is_testing_readonly)
        self.ui.send_start_comm.repaint()
        self.ui.command_send_butt_2.setEnabled(self.is_testing_readonly)
        self.ui.command_send_butt_2.repaint()
        self.ui.is_auto_CS.setEnabled(self.is_testing_readonly)
        self.ui.is_auto_CS.repaint()
        self.ui.toggle_CS_butt.setEnabled(self.is_testing_readonly)
        self.ui.toggle_CS_butt.repaint()
        self.ui.command_send_raw_butt.setEnabled(self.is_testing_readonly)
        self.ui.command_send_raw_butt.repaint()
        self.ui.isScreenshotable.setEnabled(self.is_testing_readonly)
        self.ui.isScreenshotable.repaint()
        self.ui.isScreenshotable_scenario.setEnabled(self.is_testing_readonly)
        self.ui.isScreenshotable_scenario.repaint()
        self.ui.comboBox_using_out.setEnabled(self.is_testing_readonly)
        self.ui.comboBox_using_out.repaint()
        self.ui.comboBox_scenario_using_out.setEnabled(self.is_testing_readonly)
        self.ui.comboBox_scenario_using_out.repaint()
        self.ui.start_butt.setEnabled(self.is_testing_readonly)
        self.ui.start_butt.repaint()
        self.ui.start_butt_scenar.setEnabled(self.is_testing_readonly)
        self.ui.start_butt_scenar.repaint()
        self.ui.gen_config_butt.setEnabled(self.is_testing_readonly)
        self.ui.gen_config_butt.repaint()
        self.ui.osc_config_butt.setEnabled(self.is_testing_readonly)
        self.ui.osc_config_butt.repaint()
        self.ui.gen_out_butt.setEnabled(self.is_testing_readonly)
        self.ui.gen_out_butt.repaint()
        self.ui.gen_not_out_butt.setEnabled(self.is_testing_readonly)
        self.ui.gen_not_out_butt.repaint()
        self.ui.osc_run_butt.setEnabled(self.is_testing_readonly)
        self.ui.osc_run_butt.repaint()
        self.ui.measure_butt.setEnabled(self.is_testing_readonly)
        self.ui.measure_butt.repaint()
        self.ui.scan_scen_butt.setEnabled(self.is_testing_readonly)
        self.ui.scan_scen_butt.repaint()
        self.ui.comboBox_scenarios.setEnabled(self.is_testing_readonly)
        self.ui.comboBox_scenarios.repaint()
        self.ui.generate_scen_butt.setEnabled(self.is_testing_readonly)
        self.ui.generate_scen_butt.repaint()
        self.ui.add_layer_scen_butt.setEnabled(self.is_testing_readonly)
        self.ui.add_layer_scen_butt.repaint()
        self.ui.delete_layer_scen_butt.setEnabled(self.is_testing_readonly)
        self.ui.delete_layer_scen_butt.repaint()
        self.ui.reset_scen_butt.setEnabled(self.is_testing_readonly)
        self.ui.reset_scen_butt.repaint()
        self.ui.scenario_desc_plain_text_input.setEnabled(self.is_testing_readonly)
        self.ui.scenario_desc_plain_text_input.repaint()
        self.ui.scenario_name.setEnabled(self.is_testing_readonly)
        self.ui.scenario_name.repaint()
        self.is_testing_readonly = not self.is_testing_readonly
        pass

    def set_logs_writeable(self):
        self.ui.clean_log_butt.setEnabled(True)
        self.ui.clean_log_butt.repaint()
        self.is_logs_readonly = False
        pass

    def change_rw_logs(self):
        self.ui.clean_log_butt.setEnabled(self.is_logs_readonly)
        self.ui.clean_log_butt.repaint()
        self.is_logs_readonly = not self.is_logs_readonly
        pass

    def set_gui_buttons_writeable(self):
        self.ui.butt_set_default_gui.setEnabled(True)
        self.ui.butt_set_default_gui.repaint()
        self.ui.butt_show_res.setEnabled(True)
        self.ui.butt_show_res.repaint()
        self.is_gui_buttons_readonly = False
        pass

    def change_rw_gui_buttons(self):
        self.ui.butt_set_default_gui.setEnabled(self.is_gui_buttons_readonly)
        self.ui.butt_set_default_gui.repaint()
        self.ui.butt_show_res.setEnabled(self.is_gui_buttons_readonly)
        self.ui.butt_show_res.repaint()
        self.is_gui_buttons_readonly = not self.is_gui_buttons_readonly
        pass

    def change_rw_triggs(self):
        self.ui.delay_trig.setEnabled(self.is_triggs_readonly)
        self.ui.delay_trig.repaint()
        self.ui.comboBox_delay_trig.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_delay_trig.repaint()
        self.ui.L0.setEnabled(self.is_triggs_readonly)
        self.ui.L0.repaint()
        self.ui.spinBox_L0_times.setEnabled(self.is_triggs_readonly)
        self.ui.spinBox_L0_times.repaint()
        self.ui.L0_2.setEnabled(self.is_triggs_readonly)
        self.ui.L0_2.repaint()
        self.ui.comboBox_L0.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L0.repaint()
        self.ui.comboBox_L0_2.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L0_2.repaint()
        self.ui.comboBox_L0_delta.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L0_delta.repaint()
        self.ui.L1.setEnabled(self.is_triggs_readonly)
        self.ui.L1.repaint()
        self.ui.spinBox_L1_times.setEnabled(self.is_triggs_readonly)
        self.ui.spinBox_L1_times.repaint()
        self.ui.L1_2.setEnabled(self.is_triggs_readonly)
        self.ui.L1_2.repaint()
        self.ui.comboBox_L1.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L1.repaint()
        self.ui.comboBox_L1_2.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L1_2.repaint()
        self.ui.comboBox_L1_delta.setEnabled(self.is_triggs_readonly)
        self.ui.comboBox_L1_delta.repaint()
        self.is_triggs_readonly = not self.is_triggs_readonly
        pass

    def set_triggs_writeable(self):
        self.ui.delay_trig.setEnabled(True)
        self.ui.delay_trig.repaint()
        self.ui.comboBox_delay_trig.setEnabled(True)
        self.ui.comboBox_delay_trig.repaint()
        self.ui.L0.setEnabled(True)
        self.ui.L0.repaint()
        self.ui.spinBox_L0_times.setEnabled(True)
        self.ui.spinBox_L0_times.repaint()
        self.ui.L0_2.setEnabled(True)
        self.ui.L0_2.repaint()
        self.ui.comboBox_L0.setEnabled(True)
        self.ui.comboBox_L0.repaint()
        self.ui.comboBox_L0_2.setEnabled(True)
        self.ui.comboBox_L0_2.repaint()
        self.ui.comboBox_L0_delta.setEnabled(True)
        self.ui.comboBox_L0_delta.repaint()
        self.ui.L1.setEnabled(True)
        self.ui.L1.repaint()
        self.ui.spinBox_L1_times.setEnabled(True)
        self.ui.spinBox_L1_times.repaint()
        self.ui.L1_2.setEnabled(True)
        self.ui.L1_2.repaint()
        self.ui.comboBox_L1.setEnabled(True)
        self.ui.comboBox_L1.repaint()
        self.ui.comboBox_L1_2.setEnabled(True)
        self.ui.comboBox_L1_2.repaint()
        self.ui.comboBox_L1_delta.setEnabled(True)
        self.ui.comboBox_L1_delta.repaint()
        self.is_triggs_readonly = False
        pass

    def update_scenario_combo_box(self, scenarios:list[Scenario]):
        self.ui.comboBox_scenarios.clear()
        for scenario in scenarios:
            self.ui.comboBox_scenarios.addItem(scenario.name)

    def update_scenario_description(self, desc):
        self.ui.scenario_desc_plain_text_output.setPlainText(desc)

    def get_current_scenario_box_index(self)->int:
        return self.ui.comboBox_scenarios.currentIndex()
    
    def get_resource_comm_data(self):
        return self.ui.comboBox_resources.currentIndex(), self.ui.resource_command_text.text().strip()
    
    def get_chip_metadata(self):
        name = self.ui.chip_name.text().strip()
        if name == "":
            raise Exception("Empty chip name.")
        return name, self.ui.chip_desc_plain_text_input.toPlainText().strip()
    
    def clear_chip_metadata(self):
        self.ui.chip_name.setText("")
        self.ui.chip_desc_plain_text_input.setPlainText("")
        return
    
    def scenario_comp_out_use_index(self) -> bool:
        return self.ui.comboBox_scenario_using_out.currentIndex()
    
    def manual_comp_out_use_index(self) -> bool:
        return self.ui.comboBox_using_out.currentIndex()
    
    def is_scenario_screenable(self) -> bool:
        return self.ui.isScreenshotable_scenario.isChecked()
    
    def is_manual_screenable(self) -> bool:
        return self.ui.isScreenshotable.isChecked()
    
    def get_logs(self):
        return self.ui.logs_plain_text.toPlainText()
    
    def clean_plots_data(self):
        scene = QGraphicsScene()
        self.ui.graphicsView_plots.setScene(scene)
        self.ui.graphicsView_plots.repaint()

    def set_plots_data(self, file_name):
        scene = QGraphicsScene()
        self.image_qt = QImage(file_name)

        pic = QGraphicsPixmapItem()
        pic.setPixmap(QPixmap.fromImage(self.image_qt))
        # scene.setSceneRect(0, 0, 400, 400)
        scene.addItem(pic)
        self.ui.graphicsView_plots.setScene(scene)
        self.ui.graphicsView_plots.repaint()

# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
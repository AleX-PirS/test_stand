from re import M
from PyQt5 import QtWidgets
import sys
import datetime
import regex
from pytz import timezone
import math
from itertools import product

from ui_gen import Ui_MainWindow
from pkg import Channel, RegData, GeneratorSample


class Ui(object):
    PULSE_SIGNAL_TYPE = "PULS"
    SQUARE_SIGNAL_TYPE = "SQU"
    SINE_SIGNAL_TYPE = "SIN"
    RAMP_SIGNAL_TYPE = "RAMP"
    NOISE_SIGNAL_TYPE = "NOIS"
    ARB_SIGNAL_TYPE = "USER"

    PULSE_BOX_TYPE = "Pulse"
    SQUARE_BOX_TYPE = "Square"
    SINE_BOX_TYPE = "Sine"
    RAMP_BOX_TYPE = "Ramp"
    NOISE_BOX_TYPE = "Noise"
    ARB_BOX_TYPE = "Arb"

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

    def process_value_power(self, value:float, power:str) -> int:
        # one is mV, ns, kHz
        match power:
            case "mV" | "ns" | "kHz":
                return value
            case "V" | "μs" | "MHz":
                return value*10**(3)
            case "ps" | "Hz":
                return value*10**(-3)
            case "ms":
                return value*10**(6)
            case "s":
                return value*10**(9)
            case _:
                raise Exception("Bad dimension.")
            
    def process_signal_type(self, signal:str) -> str:
        match signal:
            case self.PULSE_BOX_TYPE:
                return self.PULSE_SIGNAL_TYPE
            case self.SQUARE_BOX_TYPE:
                return self.SQUARE_SIGNAL_TYPE
            case self.SINE_BOX_TYPE:
                return self.SINE_SIGNAL_TYPE
            case self.RAMP_BOX_TYPE:
                return self.RAMP_SIGNAL_TYPE
            case self.NOISE_BOX_TYPE:
                return self.NOISE_SIGNAL_TYPE
            case self.ARB_BOX_TYPE:
                return self.ARB_SIGNAL_TYPE
            case _:
                raise Exception("Bad signal type.")

    def get_generator_data_manual(self)-> GeneratorSample:
        return GeneratorSample(
            signal_type=self.process_signal_type(self.ui.signal_type_box.currentText()),
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

    def create_sequence_samples(self, start, finish, count, rule) -> list[float]:
        match count:
            case 1:
                return [start]
            case 2:
                return [start, finish]
            
        if finish==start or finish==0.0:
            return [start]
        
        if finish<start:
            raise Exception("Finish value less than start value.")

        result = []
        match rule:
            case "linear":
                step = (finish-start)/(count-1)
                for i in range(count):
                    result.append(round(i*step+start, 3))
                return result
            case "logarithmic":
                if start == 0.0:
                    raise Exception("Forbidden to use zero value with logarithmic scale.")
                step = (finish/start)**(1/(count-1))
                for i in range(count):
                    result.append(round(start*step**i, 3))
                return result
            case _:
                raise Exception("Bad sequence rule.")

    def get_generator_data_scenario(self)-> list[GeneratorSample]:
        sig_type = self.process_signal_type(self.ui.signal_type_box.currentText())
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

    def set_generator_data_zero(self) -> None:
        self.ui.signal_type_box.setCurrentIndex(0)
        self.ui.offset.setValue(0)
        self.ui.delay.setValue(0)
        self.ui.comboBox_offset.setCurrentIndex(0)
        self.ui.comboBox_delay.setCurrentIndex(0)
        self.ui.width.setValue(0)
        self.ui.width_2.setValue(0)
        self.ui.spinBox_width_times.setValue(0)
        self.ui.comboBox_width.setCurrentIndex(0)
        self.ui.comboBox_width_2.setCurrentIndex(0)
        self.ui.comboBox_width_delta.setCurrentIndex(0)
        self.ui.lead.setValue(0)
        self.ui.lead_2.setValue(0)
        self.ui.spinBox_lead_times.setValue(0)
        self.ui.comboBox_lead.setCurrentIndex(0)
        self.ui.comboBox_lead_2.setCurrentIndex(0)
        self.ui.comboBox_lead_delta.setCurrentIndex(0)
        self.ui.trail.setValue(0)
        self.ui.trail_2.setValue(0)
        self.ui.spinBox_trail_times.setValue(0)
        self.ui.comboBox_trail.setCurrentIndex(0)
        self.ui.comboBox_trail_2.setCurrentIndex(0)
        self.ui.comboBox_trail_delta.setCurrentIndex(0)
        self.ui.ampl.setValue(0)
        self.ui.ampl_2.setValue(0)
        self.ui.spinBox_ampl_times.setValue(0)
        self.ui.comboBox_ampl.setCurrentIndex(0)
        self.ui.comboBox_ampl_2.setCurrentIndex(0)
        self.ui.comboBox_ampl_delta.setCurrentIndex(0)
        self.ui.freq.setValue(0)
        self.ui.freq_2.setValue(0)
        self.ui.spinBox_freq_times.setValue(0)
        self.ui.comboBox_freq.setCurrentIndex(0)
        self.ui.comboBox_freq_2.setCurrentIndex(0)
        self.ui.comboBox_freq_delta.setCurrentIndex(0)
        self.ui.checkBox_is_triggered.setChecked(True)
        self.ui.trig_lvl.setValue(0)
        self.ui.comboBox_trig_lvl.setCurrentIndex(0)

    def reset_scenario_data(self)->None:
        self.ui.scenario_name.setText("")
        self.ui.scenario_desc_plain_text_input.setPlainText("")
        self.ui.spinBox_layer_count.setValue(0)
        self.ui.scenario_status_plain_text.setPlainText("")

    def get_scenario_data(self) -> (str, str, int):
        return self.ui.scenario_name.text(), self.ui.scenario_desc_plain_text_input.toPlainText(), self.ui.spinBox_layer_count.value()

    def increase_layer_count(self) -> None:
        self.ui.spinBox_layer_count.setValue(self.ui.spinBox_layer_count.value() + 1)

    def decrease_layer_count(self) -> None:
        self.ui.spinBox_layer_count.setValue(self.ui.spinBox_layer_count.value() - 1)

    def add_log_layer_data(self, layer_count, test_count) -> None:
        history = self.ui.scenario_status_plain_text.toPlainText()
        self.ui.scenario_status_plain_text.setPlainText(history+f"layer:{layer_count}, tests:{test_count};\n")

    def get_channels_data(self):
        # Добавить сюда обработку источника триггера
        channels = []
        if self.ui.checkBox_is_use_chan_1.isChecked():
            name = self.ui.line_chan_1_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #1")
            channels.append(Channel(name, 1))
        if self.ui.checkBox_is_use_chan_2.isChecked():
            name = self.ui.line_chan_2_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #2")
            channels.append(Channel(name, 2))
        if self.ui.checkBox_is_use_chan_3.isChecked():
            name = self.ui.line_chan_3_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #3")
            channels.append(Channel(name, 3))
        if self.ui.checkBox_is_use_chan_4.isChecked():
            name = self.ui.line_chan_4_name.text().strip()
            if name == "":
                raise Exception(f"Empty signal name for channel #4")
            channels.append(Channel(name, 4))
        return channels
        

    # def change_rw_constants(self) -> bool:
        # Сделать сдесь следующее поведение: переключение readOnly у окон.
        # Для выпадающих окон создаю строки ридонли, в которые буду записывать значения и делать их видимыми при тесте
        # выпадающие буду делать невидимыми и тд.
        # self.ui.comboBox_CCAL.
        # self.ui.comboBox_CCSA.
        # self.ui.comboBox_GAIN.
        # self.ui.comboBox_ICSA.
        # self.ui.comboBox_SHA.
        # self.ui.comboBox_SHTR.
        # self.ui.comboBox_POL.
        # self.ui.comboBox_BIAS_CORE_CUR.
        # self.ui.comboBox_EMUL_ADDR_i.
        # self.ui.comboBox_EMUL_EN_L0.
        # self.ui.comboBox_EMUL_EN_L1.
        # self.ui.comboBox_EMUL_tau_v.
        # self.ui.comboBox_EMUL_L0_v.
        # self.ui.comboBox_CMP_TH.
        # self.ui.comboBox_CFG_SW_force_EN.setVisible()

        # self.ui.spinBox_DAC_CAL.isReadOnly()
        # self.ui.spinBox_REZ.
        # self.ui.spinBox_CAL_EN_CH.
        # self.ui.spinBox_AN_CH_DISABLE.
        # self.ui.spinBox_CFG_p1_in_time.
        # self.ui.spinBox_CFG_p1_L0_over.
        # self.ui.spinBox_CFG_p2_puls_SOC.
        # self.ui.spinBox_CFG_p2_puls_SWM.
        # self.ui.spinBox_CFG_p2_puls_EOC.
        # self.ui.spinBox_CFG_p3_L1_over.
        # self.ui.spinBox_CFG_rst_puls_EOC.
        # self.ui.spinBox_CFG_SW_force_num.
        # self.ui.spinBox_CFG_OUT_INT.
        # self.ui.spinBox_ADC_EMU_CFG.
        # self.ui.spinBox_EMUL_DATA_i.
        # self.ui.spinBox_EMUL_L1_v.


# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
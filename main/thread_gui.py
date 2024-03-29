import plistlib
from telnetlib import NOP
from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import OscilloscopeData, RegData, Scenario, ADCSample, ADCResult, ADCFigs, \
Layer, TestSample, ChipData, ResultLayer, Result, Channel, GeneratorSample, CharOscilloscopeData
from pkg import find_scenarios, differenence

import sys
import time
import os
import datetime
from pytz import timezone
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, QThread, pyqtSignal

TESTS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'tests')
MANUAL_TESTS_PATH = os.path.join(TESTS_PATH, r'manual')
SCENARIO_TESTS_PATH = os.path.join(TESTS_PATH, r'scenario')
PICTURES_PLOTS_FOLDER = r'plots'
PICTURES_FOLDER = r'pictures'
PICTURES_SCREENSHOTS_FOLDER = r'screenshots'
RAW_DATA_FOLDER = r'points'
LOGS_FOLDER = r'logs'

class UARTListener(QObject):
    data_logging = pyqtSignal(str)

    def __init__(self, uart:UART) -> None:
        super().__init__()
        self.uart = uart

    def start_listen(self):
        pass

class StatusWidget(QObject):
    THREAD_SLEEP_TIME = 0.001

    MANUAL_TEST = 0
    SCENARIO_TEST = 1

    logging = pyqtSignal(str)
    clear_log = pyqtSignal()
    clean_plots_data = pyqtSignal()
    set_channels_data = pyqtSignal(dict, int, float, float)
    chng_rw_gui = pyqtSignal()
    set_reg_values = pyqtSignal(RegData)
    set_triggers_data = pyqtSignal(int, int)
    set_generator_sample = pyqtSignal(GeneratorSample)
    set_w_gui = pyqtSignal()
    set_plots_data = pyqtSignal(str)
    finished = pyqtSignal(Result)
    finished_ADC = pyqtSignal(ADCResult)
    exception_sig = pyqtSignal()

    scenario_to_start = Scenario([], "", "", [], 0, 0, 0)
    is_screaning = False
    out_index:int
    triggers:list[tuple[int, int]]
    chip_name:str
    chip_desc:str
    current_test_type:int
    current_start_time:str
    is_dont_send_consts:bool
    get_char_status:bool
    is_dont_read_r:bool
    is_dont_send_interface:bool
    STOP_flag = 0
    averaging = 1
    polarity = 1
    scale_factor_adc = 1.0
    test_count = 1

    def __init__(self, visa:Visa, uart:UART) -> None:
        super().__init__()
        self.visa = visa
        self.uart = uart

    def start_adc_test(self):
        try:
            self.start_adc_test_inner()
        except Exception as e:
            self.set_w_gui.emit()
            self.logging.emit(f"QThred ADC TEST ERROR: {e.args[0]}")
            self.exception_sig.emit()

    def start_adc_test_inner(self):
        start_time = str(datetime.datetime.now(tz=timezone('Europe/Moscow'))).replace(":", ".")[:-13].replace(" ", "_")
        self.current_start_time = f"ADC_{start_time}"
        testing_type = self.MANUAL_TEST
        chip_name = self.chip_name
        chip_desc = self.chip_desc
        scenario = self.scenario_to_start
        scale_factor_adc = self.scale_factor_adc
        test_count = self.test_count

        self.clear_log.emit()
        self.clean_plots_data.emit()
        
        self.visa.v2_off_all_out1()

        self.logging.emit(f"Start ADC test for chip:{chip_name}")

        self.visa.v2_configurate_oscilloscope_scenario_ADC(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)
        # self.visa.v2_configurate_oscilloscope_scenario(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)
        dict_data = {}
        for idx, val in enumerate(scenario.channels):
            dict_data[idx] = val
        self.set_channels_data.emit(dict_data, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)

        self.chng_rw_gui.emit()

        samples = []
        plots = ADCFigs()
        idx = 1
        try:
            total_test_count = len(scenario.layers[0].samples) * len(list(scenario.layers[0].samples.values())[0])
        except:
            total_test_count = 0

        for test_number in range(1, test_count+1):
            for offset, gen_samples in list(scenario.layers[0].samples.items()):
                ampls = []
                adc_vals = []
                for sample in gen_samples:
                    self.set_generator_sample.emit(sample)
                    self.visa.v2_configurate_ADC_sample(sample)
                    self.visa.v2_oscilloscope_run()
                    self.visa.v2_on_out1(-1)

                    get_flag = 0
                    while True:
                        if get_flag == 1:
                            break

                        uart_data = self.uart.send_start_adc_test_command()

                        try:
                            adcValue = int(uart_data[0] << 2) + int(uart_data[1] & 0x03)
                            timeout = (uart_data[1] >> 7) & 0x01
                            if uart_data[0] == 0:
                                print("old byte is zero")
                                continue
                            get_flag = 1
                        except:
                            print("empty uart adc data")
                            continue                                            
                    
                    uart_data_message = f"ADC Value: {adcValue} (bin: {format(adcValue, '#012b')}), timeout: {timeout}"

                    self.logging.emit(f"ADC TEST (#{idx} of {total_test_count*test_count}), offset:{offset}V, amplitude:{sample.ampl}V. Get payload:{uart_data}, Message:{uart_data_message}")


                    sample_result = ADCSample(
                        uart_data=uart_data,
                        sample=sample
                    )

                    ampls.append(sample.ampl)
                    adc_vals.append(adcValue)
                    self.save_adc_plot(self.current_start_time, chip_name, scenario.name, testing_type, offset, ampls, adc_vals, plots, scale_factor_adc, test_number, end=False)

                    samples.append(sample_result)
                    idx += 1
                plots.add_plot(offset,  ampls, adc_vals)

            self.save_adc_plot(self.current_start_time, chip_name, scenario.name, testing_type, -1, [], [], plots, scale_factor_adc, test_number, end=True)

        if len(scenario.layers[0].samples) == 0:
            uart_data = self.uart.send_start_adc_test_command()
            self.logging.emit(f"ADC TEST, offset:{offset}V, amplitude:{sample.ampl}V. Get payload:{uart_data}, Message:{uart_data_message}")

        self.logging.emit(f"Finish ADC test.")

        result = ADCResult(chip_name, chip_desc, samples, "")

        self.set_w_gui.emit()
        self.finished_ADC.emit(result)

    def start_test(self):
        try:
            self.start_test_inner()
        except Exception as e:
            self.set_w_gui.emit()
            self.logging.emit(f"QThred TEST ERROR: {e.args[0]}")
            self.exception_sig.emit()

    def start_test_inner(self):
        start_time = str(datetime.datetime.now(tz=timezone('Europe/Moscow'))).replace(":", ".")[:-13].replace(" ", "_")
        self.current_start_time = start_time
        testing_type = self.current_test_type
        scenario = self.scenario_to_start
        is_screening = self.is_screaning
        out_index = self.out_index
        triggers = self.triggers
        chip_name = self.chip_name
        chip_desc = self.chip_desc
        get_char_status = self.get_char_status
        averaging = self.averaging
        polarity = self.polarity
        is_dont_read_r = self.is_dont_read_r
        is_dont_send_interface = self.is_dont_send_interface
        test_count = self.test_count

        if not get_char_status:
            averaging = 1

        self.clear_log.emit()
        self.clean_plots_data.emit()
        self.results_folder = ""

        if scenario.total_test_count != 0:
            self.visa.v2_off_all_out1()
            
        match testing_type:
            case self.MANUAL_TEST:
                self.logging.emit(f"Start manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.logging.emit(f"Start scenario:{scenario.name} test for chip:{chip_name}")

        if scenario.total_test_count != 0:
            self.visa.v2_configurate_oscilloscope_scenario(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale, polarity, averaging)
            dict_data = {}
            for idx, val in enumerate(scenario.channels):
                dict_data[idx] = val
            self.set_channels_data.emit(dict_data, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)

        self.chng_rw_gui.emit()
        averaging = 1
        
        test_idx = 1
        result = Result(
            chip_name=chip_name,
            chip_description=chip_desc,
            test_name=scenario.name,
            test_description=scenario.description,
            channels=scenario.channels,
            trig_src=scenario.trig_src,
            trig_lvl=scenario.trig_lvl,
            tim_scale=scenario.tim_scale,
            logs="",
            layers=[],
            layers_count=0,
            total_test_count=0,
        )

        for idx_layer, test in enumerate(scenario.layers):
            if self.STOP_flag == 1:
                self.STOP_flag = 0
                break
            result_layer = ResultLayer(0, [], test.consts_to_json())

            if not self.is_dont_send_consts:
                self.set_reg_values.emit(RegData(is_zero_init=False, template_list=test.constants))
                self.uart.write_w_regs(RegData(is_zero_init=False, template_list=test.constants), True, (True, True, True))
                
                sended = test.constants
                get = self.uart.read_rw_regs(True)

                if sended != get:
                    diff = differenence(sended, get)
                    # Param was 4
                    for i in range(0):
                        if len(diff) <= 1:
                            break
                        print(f'in diff if: len:{len(diff)}')
                        self.uart.write_w_regs(RegData(is_zero_init=False, template_list=test.constants), True, (True, True, True))
                        get = self.uart.read_rw_regs(True)
                        diff = differenence(sended, get)
                        print(f'diff after resend: len:{len(diff)}')
                    
                
                for k,v in diff.items():
                    match testing_type:
                        case self.MANUAL_TEST:
                            self.logging.emit(f"WARNING! constants mismatch. reg:{k}, mismatch:{v}")
                        case self.SCENARIO_TEST:
                            self.logging.emit(f"WARNING! Layer#{idx_layer+1}. Constants mismatch. reg:{k}, mismatch:{v}")

            char = CharOscilloscopeData(scenario.trig_src, "Amplitude, V")
            for test_number in range(1, test_count+1):
                for sample_index, test_sample in enumerate(test.samples):
                    for l0, l1 in triggers[0]:
                        if self.STOP_flag == 1:
                            break

                        self.set_triggers_data.emit(l0*5, l1*5)

                        match testing_type:
                            case self.MANUAL_TEST:
                                self.logging.emit(f"Start sample#{test_idx} of {test_count*scenario.total_test_count*len(triggers[0])*averaging}")
                            case self.SCENARIO_TEST:
                                self.logging.emit(f"Layer#{idx_layer+1}. Start sample#{sample_index+1} of {test_count*test.test_count*len(triggers[0])*averaging}. Total tests:{scenario.total_test_count*len(triggers[0])*averaging}")
                        
                        self.uart.send_triggers((test_sample.delay*10**9+triggers[1])//5, l0, l1)
                            
                        averaging_results = {1:[], 2:[], 3:[], 4:[]}
                        averaging = 1
                        for av in range(averaging):                        
                            if scenario.total_test_count != 0:
                                self.set_generator_sample.emit(test_sample)
                                self.visa.v2_configurate_generator_sample(test_sample)
                                self.visa.v2_oscilloscope_run()
                                self.visa.v2_on_out1(out_index)

                            self.uart.send_start_command()

                            points_file, plots_file = "", ""
                            if scenario.total_test_count != 0:
                                sample_data = self.visa.v2_get_sample()
                                points_file, plots_file = self.save_points(start_time, chip_name, scenario.name, testing_type, idx_layer, test_idx, sample_data, scenario.channels, l0, l1, test_number, get_char_status)

                            chip_data, RAW_data = {}, ""
                            chip_data_output = ChipData(
                                    V=-1,
                                    R=-1,
                                    ADR=-1,
                                    N0=-1,
                                    A0=-1,
                                    N1=-1,
                                    A1=-1,
                                    N2=-1,
                                    A2=-1,
                                    N3=-1,
                                    A3=-1,
                                    N4=-1,
                                    A4=-1,
                                    O=-1,
                                    TIME=-1,
                                    RAW=-1,
                                )
                            
                            if not is_dont_send_interface:
                                chip_data, RAW_data = self.uart.get_chip_data()
                                chip_data_output = ChipData(
                                    V=chip_data['V'],
                                    R=chip_data['R'],
                                    ADR=chip_data['ADR'],
                                    N0=chip_data['N0'],
                                    A0=chip_data['A0'],
                                    N1=chip_data['N1'],
                                    A1=chip_data['A1'],
                                    N2=chip_data['N2'],
                                    A2=chip_data['A2'],
                                    N3=chip_data['N3'],
                                    A3=chip_data['A3'],
                                    N4=chip_data['N4'],
                                    A4=chip_data['A4'],
                                    O=chip_data['O'],
                                    TIME=chip_data['TIME'],
                                    RAW=RAW_data,
                                )

                                match testing_type:
                                    case self.MANUAL_TEST:
                                        self.logging.emit(f"Get chip data:{chip_data} (Sample#{test_idx} of {test_count*scenario.total_test_count*len(triggers[0])*averaging})")
                                    case self.SCENARIO_TEST:
                                        self.logging.emit(f"Get chip data:{chip_data} (Layer#{idx_layer+1}. Sample#{sample_index+1} of {test_count*test.test_count*len(triggers[0])*averaging}. Total tests:{scenario.total_test_count*len(triggers[0])*averaging})")
                            
                            screen_file = ""
                            if is_screening:
                                self.logging.emit(f"Taking screenshot.")
                                screen_data = self.visa.v2_take_screen()
                                screen_file = self.save_screenshot(start_time, chip_name, scenario.name, screen_data, testing_type, idx_layer, test_idx, test_number)
                                time.sleep(5)
                                self.logging.emit(f"Screenshot saved.")

                            if scenario.total_test_count != 0:
                                self.visa.v2_off_all_out1()
                            
                            for i in range(1, 5):
                                if len(sample_data.data[i][1]) != 0:
                                    averaging_results[i].append(max(sample_data.data[i][1]))

                            match testing_type:
                                case self.MANUAL_TEST:
                                    self.logging.emit(f"Finish sample#{test_idx} of {test_count*scenario.total_test_count*len(triggers[0])*averaging}")
                                case self.SCENARIO_TEST:
                                    self.logging.emit(f"Layer#{idx_layer+1}. Finish sample#{sample_index+1} of {test_count*test.test_count*len(triggers[0])*averaging}. Total tests:{scenario.total_test_count*len(triggers[0])*averaging}")
                            
                            test_result = TestSample(
                                chip_data=chip_data_output,
                                amplitude=test_sample.ampl,
                                delay=test_sample.delay,
                                frequency=test_sample.freq,
                                is_triggered=test_sample.is_triggered,
                                lead=test_sample.lead,
                                offset=test_sample.offset,
                                signal_type=test_sample.signal_type,
                                trail=test_sample.trail,
                                trigger_lvl=test_sample.trig_lvl,
                                width=test_sample.width,
                                screenshot=screen_file,
                                points_data=points_file,
                                plots=plots_file,
                                L0=l0*5,
                                L1=l1*5,
                            )

                            if not is_dont_read_r:
                                result_layer.r_constants = self.uart.read_r_regs(True).consts_to_json_regs()

                            test_idx += 1
                            result_layer.test_count += 1
                            result_layer.samples.append(test_result)
                            time.sleep(self.THREAD_SLEEP_TIME)
                        
                        if get_char_status:
                            char.add_points(averaging_results, test_sample.ampl)
                            self.save_char_plot(start_time, chip_name, scenario.name, testing_type, idx_layer, test_idx, char, scenario.channels, test_number, end=False)
                        # averaging
                if get_char_status:
                    self.save_char_plot(start_time, chip_name, scenario.name, testing_type, idx_layer, test_idx, char, scenario.channels, test_number, end=True)

                result.layers.append(result_layer)
                result.layers_count += 1
                result.total_test_count += result_layer.test_count

                
        match testing_type:
            case self.MANUAL_TEST:
                self.logging.emit(f"Finish manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.logging.emit(f"Finish scenario:{scenario.name} test for chip:{chip_name}")
            
        self.set_w_gui.emit()
        self.finished.emit(result)

    def save_screenshot(self, start_time, chip_name, scenario_name, screenshot_data, testing_type, layer_index, sample_index, test_number):
        file_name = f"screenshot_sample_{sample_index}.png"
        match testing_type:
            case self.MANUAL_TEST:
                path = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, PICTURES_FOLDER, PICTURES_SCREENSHOTS_FOLDER)
            case self.SCENARIO_TEST:
                path = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, test_number, f"layer_{layer_index+1}", PICTURES_FOLDER, PICTURES_SCREENSHOTS_FOLDER)
        
        try:
            os.makedirs(path)
        except:
            pass

        f = open(path+"\\"+file_name, "wb")
        f.write(screenshot_data)
        f.close()

        return path+"\\"+file_name
    
    def save_points(self, start_time, chip_name, scenario_name, testing_type, layer_index, sample_index, data:OscilloscopeData, channels, l0, l1, test_number, is_char=False):
        file_name_points = f"channels_data_{sample_index}.json"
        match testing_type:
            case self.MANUAL_TEST:
                path_points = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, RAW_DATA_FOLDER)
            case self.SCENARIO_TEST:
                path_points = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, test_number, f"layer_{layer_index+1}", RAW_DATA_FOLDER)
        
        try:
            os.makedirs(path_points)
        except:
            pass

        with open(path_points+"\\"+file_name_points, 'w') as file:
            file.write(data.toJSON())
            file.close()

        file_name_plots = f"plots_{sample_index}.pdf"
        match testing_type:
            case self.MANUAL_TEST:
                path_plots = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
            case self.SCENARIO_TEST:
                path_plots = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, test_number, f"layer_{layer_index+1}", PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
        
        try:
            os.makedirs(path_plots)
        except:
            pass

        link_file = "plots.png"
        data.plot_all(channels).savefig(path_plots+"\\"+file_name_plots, format='pdf')
        plt.close('all')
        if is_char:
            data.plot_for_gui(channels, sample_index, l0, l1).savefig(link_file, format='png', dpi=80)
            plt.close('all')

        self.set_plots_data.emit(link_file)

        return path_points+"\\"+file_name_points, path_plots+"\\"+file_name_plots
    
    def save_char_plot(self, start_time, chip_name, scenario_name, testing_type, layer_index, sample_index, data:CharOscilloscopeData, channels, test_number, end=False):
        if end:
            file_name_points = f"channels_char_data.json"
            match testing_type:
                case self.MANUAL_TEST:
                    path_points = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, RAW_DATA_FOLDER)
                case self.SCENARIO_TEST:
                    path_points = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, test_number, f"layer_{layer_index+1}", RAW_DATA_FOLDER)
            
            try:
                os.makedirs(path_points)
            except:
                pass

            with open(path_points+"\\"+file_name_points, 'w') as file:
                file.write(data.toJSON())
                file.close()

            file_name_plots = f"plots_"
            match testing_type:
                case self.MANUAL_TEST:
                    path_plots = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
                case self.SCENARIO_TEST:
                    path_plots = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, test_number, f"layer_{layer_index+1}", PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
            
            try:
                os.makedirs(path_plots)
            except:
                pass

            plots_data = data.save_all_plots(channels)
            for plot in plots_data:
                plot.savefig(path_plots+"\\"+f"{file_name_plots}{plot.axes[0].get_title()}.pdf", format='pdf')
            plt.close('all')
        link_file = "plots.png"
        data.plot_for_gui(channels).savefig(link_file, format='png', dpi=80)
        plt.close('all')

        self.set_plots_data.emit(link_file)
        
        if end:
            return path_points+"\\"+file_name_points, path_plots+"\\"+file_name_plots

    def save_adc_plot(self, start_time, chip_name, scenario_name, testing_type, offset, ampl, adc_vals, data:ADCFigs, scale_factor_adc, test_number, end=False):
        link_file = "plots.png"

        if end:
            print("im plot all")
            file_name_points = f"channels_adc_data.json"
            match testing_type:
                case self.MANUAL_TEST:
                    path_points = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, RAW_DATA_FOLDER)
                case self.SCENARIO_TEST:
                    path_points = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, RAW_DATA_FOLDER)
            
            try:
                os.makedirs(path_points)
            except:
                pass

            with open(path_points+"\\"+file_name_points, 'w') as file:
                file.write(data.toJSON())
                file.close()

            file_name_plots = f"adc_plots_"
            match testing_type:
                case self.MANUAL_TEST:
                    path_plots = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, test_number, PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
                case self.SCENARIO_TEST:
                    path_plots = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
            
            try:
                os.makedirs(path_plots)
            except:
                pass

            plots_data = data.plot_all(scale_factor_adc)
            for plot in plots_data:
                plot.savefig(path_plots+"\\"+f"{file_name_plots}{plot.axes[0].get_title()}.pdf", format='pdf')
            plt.close('all')

            data.plot_final_gui(scale_factor_adc).savefig(link_file, format='png', dpi=80)
            plt.close('all')

            self.set_plots_data.emit(link_file)

        else:            
            data.plot_for_gui(offset, ampl, adc_vals, scale_factor_adc).savefig(link_file, format='png', dpi=80)
            plt.close('all')

            self.set_plots_data.emit(link_file)
        
        if end:
            return path_points+"\\"+file_name_points, path_plots+"\\"+file_name_plots

class UARTListener(QObject):
    logging = pyqtSignal(str)

    def __init__(self, uart:UART) -> None:
        super().__init__()
        self.uart = uart

    
    def listen(self):
        pass
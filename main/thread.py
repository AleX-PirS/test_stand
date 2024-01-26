from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import OscilloscopeData, RegData, Scenario, Layer, TestSample, ChipData, ResultLayer, Result, Channel
from stand_lib import Stand
from pkg import find_scenarios, differenence

import sys
import time
import os
import datetime
from pytz import timezone
import matplotlib.pyplot as plt
from PyQt5.QtCore import QObject, QThread, pyqtSignal

class StatusWidget(Stand):
    logging = pyqtSignal(str)
    clear_log = pyqtSignal()
    clean_plots_data = pyqtSignal()
    set_channels_data = pyqtSignal(list[Channel], int, int, int)
    chng_rw_gui = pyqtSignal()
    set_reg_values = pyqtSignal(RegData)
    set_triggers_data = pyqtSignal(int, int)
    set_generator_sample = pyqtSignal(TestSample)
    set_w_gui = pyqtSignal()
    finished = pyqtSignal(Result)

    scenario_to_start = Scenario([], "", "", [], 0, 0, 0)
    is_screaning = bool
    out_index = int
    triggers = list[tuple[int, int]]
    chip_name = str
    chip_desc = str
    current_test_type = int
    current_start_time = str

    def __init__(self, visa:Visa, uart:UART) -> None:
        super().__init__()
        self.visa = visa
        self.uart = uart
        self.ui = ""

    def start_test(self):
        start_time = str(datetime.datetime.now(tz=timezone('Europe/Moscow'))).replace(":", ".")[:-13].replace(" ", "_")
        self.current_start_time = start_time
        testing_type = self.current_test_type
        scenario = self.scenario_to_start
        is_screening = self.is_screaning
        out_index = self.out_index
        triggers = self.triggers
        chip_name = self.chip_name
        chip_desc = self.chip_desc

        self.check_instruments_connection()
        self.clear_log.emit()
        self.clean_plots_data.emit()
        self.results_folder = ""

        self.visa.v2_off_all_out1()
            
        match testing_type:
            case self.MANUAL_TEST:
                self.logging.emit(f"Start manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.logging.emit(f"Start scenario:{scenario.name} test for chip:{chip_name}")

        if len(scenario.channels) != 0:
            self.visa.v2_configurate_oscilloscope_scenario(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)
            self.set_channels_data.emit(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)

        self.chng_rw_gui.emit()

        
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

            self.set_reg_values.emit(RegData(is_zero_init=False, template_list=test.constants))
            self.uart.write_w_regs(RegData(is_zero_init=False, template_list=test.constants))
            
            sended = test.constants
            get = self.uart.read_rw_regs()

            if sended != get:
                diff = differenence(sended, get)

                for i in range(4):
                    if len(diff) <= 1:
                        break
                    print(f'in diff if: len:{len(diff)}')
                    self.uart.write_w_regs(RegData(is_zero_init=False, template_list=test.constants))
                    get = self.uart.read_rw_regs()
                    diff = differenence(sended, get)
                    print(f'diff after resend: len:{len(diff)}')
                    
                
                for k,v in diff.items():
                    match testing_type:
                        case self.MANUAL_TEST:
                            self.logging.emit(f"WARNING! constants mismatch. reg:{k}, mismatch:{v}")
                        case self.SCENARIO_TEST:
                            self.logging.emit(f"WARNING! Layer#{idx_layer+1}. Constants mismatch. reg:{k}, mismatch:{v}")

            for sample_index, test_sample in enumerate(test.samples):
                for l0, l1 in triggers:
                    if self.STOP_flag == 1:
                        break

                    self.set_triggers_data.emit(l0*5, l1*5)

                    match testing_type:
                        case self.MANUAL_TEST:
                            self.logging.emit(f"Start sample#{test_idx} of {scenario.total_test_count*len(triggers)}")
                        case self.SCENARIO_TEST:
                            self.logging.emit(f"Layer#{idx_layer+1}. Start sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)}")
                    
                    self.uart.send_triggers((test_sample.delay*10**9)//5, l0, l1)

                    self.set_generator_sample.emit(test_sample)
                    self.visa.v2_configurate_generator_sample(test_sample)
                    self.visa.v2_oscilloscope_run()
                    self.visa.v2_on_out1(out_index)

                    self.uart.send_start_command()

                    sample_data = self.visa.v2_get_sample()

                    points_file, plots_file = self.save_points(start_time, chip_name, scenario.name, testing_type, idx_layer, test_idx, sample_data, scenario.channels, l0, l1)

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
                            self.logging.emit(f"Get chip data:{chip_data} (Sample#{test_idx} of {scenario.total_test_count*len(triggers)})")
                        case self.SCENARIO_TEST:
                            self.logging.emit(f"Get chip data:{chip_data} (Layer#{idx_layer+1}. Sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)})")
                    
                    screen_file = ""
                    if is_screening:
                        self.logging.emit(f"Taking screenshot.")
                        screen_data = self.visa.v2_take_screen()
                        screen_file = self.save_screenshot(start_time, chip_name, scenario.name, screen_data, testing_type, idx_layer, test_idx)
                        time.sleep(5)
                        self.logging.emit(f"Screenshot saved.")

                    self.visa.v2_off_all_out1()
                    match testing_type:
                        case self.MANUAL_TEST:
                            self.logging.emit(f"Finish sample#{test_idx} of {scenario.total_test_count*len(triggers)}")
                        case self.SCENARIO_TEST:
                            self.logging.emit(f"Layer#{idx_layer+1}. Finish sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)}")
                    
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

                    test_idx += 1
                    result_layer.test_count += 1
                    result_layer.samples.append(test_result)

            result.layers.append(result_layer)
            result.layers_count += 1
            result.total_test_count += result_layer.test_count

                
        match testing_type:
            case self.MANUAL_TEST:
                self.logging.emit(f"Finish manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.logging.emit(f"Finish scenario:{scenario.name} test for chip:{chip_name}")
            
        # logs = self.ui.get_logs()
        # logs_file = self.save_logs(start_time, chip_name, scenario.name, testing_type, logs)

        # result.logs = logs_file

        # result_file = self.save_results(result, start_time, chip_name, scenario.name, testing_type)
        
        # self.results_folder = result_file

        self.set_w_gui.emit()
        self.finished.emit(result)

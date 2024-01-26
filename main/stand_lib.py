from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import OscilloscopeData, RegData, Scenario, Layer, TestSample, ChipData, ResultLayer, Result, Channel
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

class Stand(QObject):
    MANUAL_TEST = 0
    SCENARIO_TEST = 1

    def __init__(self) -> None:
        super(Stand, self).__init__()
        self.main_scenario = Scenario([], "", "", [], 0, 0, 0)
        self.list_of_scenarios = list[Scenario]
        self.scenario_to_start = Scenario([], "", "", [], 0, 0, 0)
        self.results_folder = ""
        self.STOP_flag = 0

        self.ui = Ui()
        self.uart = UART()
        self.visa = Visa()
        # Main window
        self.ui.ui.butt_set_default_gui.clicked.connect(self.process_default_gui_butt)
        self.ui.ui.butt_show_res.clicked.connect(self.process_show_res_butt)
        self.ui.ui.butt_STOP_test.clicked.connect(self.process_STOP_butt)
        # Registers panel
        self.ui.ui.com_write_butt.clicked.connect(self.process_com_write_butt)
        self.ui.ui.com_read_all_butt.clicked.connect(self.process_com_read_all_butt)
        self.ui.ui.com_read_r_butt.clicked.connect(self.process_com_read_r_butt)
        self.ui.ui.com_read_rw_butt.clicked.connect(self.process_com_read_rw_butt)
        self.ui.ui.com_conn_butt.clicked.connect(self.process_com_conn_butt)
        # Constants panel
        self.ui.ui.butt_set_default_regs.clicked.connect(self.process_set_default_reg_values_butt)
        # Environment panel
        self.ui.ui.oscilloscope_conn_butt.clicked.connect(self.process_oscilloscope_conn_butt)
        self.ui.ui.generator_conn_butt.clicked.connect(self.process_generator_conn_butt)
        self.ui.ui.reset_osc_butt.clicked.connect(self.process_reset_osc_butt)
        self.ui.ui.reset_gen_butt.clicked.connect(self.process_reset_gen_butt)
        self.ui.ui.scan_res_butt.clicked.connect(self.process_scan_res_butt)
        self.ui.ui.command_send_butt.clicked.connect(self.process_send_comm_butt)
        # Generator settings panel
        self.ui.ui.gen_zero_butt.clicked.connect(self.process_set_zeros_generator_butt)
        # Logs panel
        self.ui.ui.clean_log_butt.clicked.connect(self.process_clear_log_butt)
        # Scenario processing panel
        self.ui.ui.reset_scen_butt.clicked.connect(self.process_reset_scenario_butt)
        self.ui.ui.generate_scen_butt.clicked.connect(self.process_generate_scenario_butt)
        self.ui.ui.add_layer_scen_butt.clicked.connect(self.process_add_layer_butt)
        self.ui.ui.delete_layer_scen_butt.clicked.connect(self.process_delete_layer_butt)
        # Start scenario sampling
        self.ui.ui.comboBox_scenarios.currentIndexChanged.connect(self.process_scenario_box)
        self.ui.ui.scan_scen_butt.clicked.connect(self.process_scan_butt)
        self.ui.ui.start_butt_scenar.clicked.connect(self.process_scenar_start_butt)
        # Manual testing
        self.ui.ui.gen_config_butt.clicked.connect(self.process_config_gen_butt)
        self.ui.ui.gen_out_butt.clicked.connect(self.process_out_toggle_butt)
        self.ui.ui.gen_not_out_butt.clicked.connect(self.process_not_out_toggle_butt)
        self.ui.ui.osc_config_butt.clicked.connect(self.process_osc_config_butt)
        self.ui.ui.measure_butt.clicked.connect(self.process_measure_butt)
        self.ui.ui.start_butt.clicked.connect(self.process_start_butt)
        self.ui.ui.osc_run_butt.clicked.connect(self.process_osc_run_butt)
        self.ui.ui.command_send_butt_2.clicked.connect(self.process_send_regs_butt)

        # Threading with testing
        # self.thread = QThread()
        # self.worker = StatusWidget(uart=self.uart, visa=self.visa)
        # self.worker.moveToThread(self.thread)

        # self.thread.started.connect(self.worker.start_test)
        # self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)

        # self.thread.start()

        self.ui.MainWindow.show()
        sys.exit(self.ui.app.exec_())

    def process_send_regs_butt(self):
        try:
            idx, addr, val = self.ui.get_regs_comm_data()
            match idx:
                case 0:
                    self.uart.write_reg(int.to_bytes(addr, 1, 'big'), [int.to_bytes(val, 1, 'big'), int.to_bytes(val, 1, 'big')])
                case 1:
                    data = self.uart.read_reg(int.to_bytes(addr, 1, 'big'), int.to_bytes(1, 1, 'big'))
                    reg_data = RegData(is_zero_init=True)
                    reg_data.reg_data[addr] = data[0]
                    self.ui.log_registers(reg_data.__str__())
        except Exception as e:
            self.ui.logging("ERROR send constant cause: ", e.args[0])

    def process_show_res_butt(self):
        if self.results_folder == "":
            self.ui.logging(f"No test results")
            return
        try:
            os.system(f'explorer.exe "{self.results_folder}"')
        except:
            self.ui.logging("ERROR open result folder.")

    def process_STOP_butt(self):
        self.STOP_flag = 1

    def process_com_write_butt(self):
        try:
            self.uart.write_w_regs(self.ui.get_w_registers_data())
            self.ui.logging("Constants sended succesfully")
        except Exception as e:
            self.ui.logging("ERROR send constants: ", e.args[0])
            return

    def process_com_read_all_butt(self):
        try:
            self.ui.log_registers(self.uart.read_all_regs().__str__())
        except Exception as e:
            self.ui.logging("ERROR read constants: ", e.args[0])
            return
        
    def process_com_read_r_butt(self):
        try:
            self.ui.log_registers(self.uart.read_r_regs().__str__())
        except Exception as e:
            self.ui.logging("ERROR read constants: ", e.args[0])
            return
        
    def process_com_read_rw_butt(self):
        try:
            self.ui.log_registers(self.uart.read_rw_regs().__str__())
        except Exception as e:
            self.ui.logging("ERROR read constants: ", e.args[0])
            return

    def process_com_conn_butt(self):
        try:
            address = self.ui.get_com_port_address()
            self.uart.connect_com(address)
            self.ui.logging(f"Successfull connect to {address}")
            return
        except Exception as e:
            self.ui.logging("ERROR connect using uart: ", e.args[0])
            return

    def process_oscilloscope_conn_butt(self):
        try:
            self.visa.connect_osc(self.ui.ui.oscilloscope_addr.text())
            self.ui.logging("Successfull connect oscilloscope")
        except Exception as e:
            self.ui.logging("ERROR connect oscilloscope: ", e.args[0])
            return

    def process_generator_conn_butt(self):
        try:
            self.visa.connect_gen(self.ui.ui.generator_addr.text())
            self.ui.logging("Successfull connect generator")
        except Exception as e:
            self.ui.logging("ERROR connect generator: ", e.args[0])
            return

    def process_reset_osc_butt(self):
        try:
            self.visa.reset_oscilloscope()
            self.ui.logging("Successfull disconnect oscilloscope")
        except Exception as e:
            self.ui.logging("ERROR disconnect oscilloscope: ", e.args[0])
            return

    def process_reset_gen_butt(self):
        try:
            self.visa.reset_generator()
            self.ui.logging("Successfull disconnect generator")
        except Exception as e:
            self.ui.logging("ERROR disconnect generator: ", e.args[0])
            return

    def process_scan_res_butt(self):
        self.ui.log_resources(self.visa.resource_list())

    def process_set_default_reg_values_butt(self):
        self.ui.set_default_reg_values(RegData(is_zero_init=False))

    def process_set_zeros_generator_butt(self):
        self.ui.set_generator_data_zero()

    def process_clear_log_butt(self):
        self.ui.clear_log()

    def process_reset_scenario_butt(self):
        self.ui.reset_scenario_data()
        self.main_scenario = Scenario([], "", "", [], 0, 0, 0)

    def process_add_layer_butt(self):
        try:
            samples = self.ui.get_generator_data_scenario()
        except Exception as e:
            self.ui.logging("ERROR get generator samples data: ", e.args[0])
            return
        self.ui.increase_layer_count()
        _, _, count = self.ui.get_scenario_data()
        self.ui.add_log_layer_data(count, len(samples))

        self.main_scenario.add_layer(
            Layer(
                self.ui.get_w_registers_data(),
                samples,
            )
        )
        self.ui.logging(f"Successfully added a new scenario layer #{count}")

    def process_generate_scenario_butt(self):
        if self.main_scenario.layers_count == 0:
            self.ui.logging("ERROR generate a new scenario. Zero layers count")
            return
        name, desc, _ = self.ui.get_scenario_data()
        if name.strip() == "":
            self.ui.logging("Please, write the scenario name!")
            return
        try:
            channels, trig_src, trig_lvl, tim_scale = self.ui.get_channels_data()
        except Exception as e:
            self.ui.logging("ERROR get data about signals: ", e.args[0])
            return
        self.main_scenario.name = name
        self.main_scenario.description = desc
        self.main_scenario.channels = channels
        self.main_scenario.trig_src = trig_src
        self.main_scenario.trig_lvl = trig_lvl
        self.main_scenario.tim_scale = tim_scale
        try:
            self.main_scenario.save_scenario()
        except Exception as e:
            self.ui.logging("ERROR create a new scenario: ", e.args[0])
            return
        self.ui.logging(f"Successfull creation of a new scenario '{self.main_scenario.name}'. Layers: {self.main_scenario.layers_count}, total tests:{self.main_scenario.total_test_count}")
        self.process_reset_scenario_butt()

    def process_delete_layer_butt(self):
        self.main_scenario.delete_last_layer()
        self.ui.delete_last_layer()

    def process_scenario_box(self):
        index = self.ui.get_current_scenario_box_index()
        if index == -1:
            return
        self.ui.update_scenario_description(self.list_of_scenarios[index].description+f'Totat test count:{self.list_of_scenarios[index].total_test_count}')
        self.ui.set_reg_values(RegData(is_zero_init=False, template_list=self.list_of_scenarios[index].layers[0].constants))
        self.ui.set_channels_data(self.list_of_scenarios[index].channels, self.list_of_scenarios[index].trig_src, self.list_of_scenarios[index].trig_lvl, self.list_of_scenarios[index].tim_scale)
        self.scenario_to_start = Scenario([], "", "", [], 0, 0, 0)
        self.scenario_to_start = self.list_of_scenarios[index]

    def process_scan_butt(self):
        try:
            self.list_of_scenarios = find_scenarios()
        except Exception as e:
            self.ui.logging("ERROR scan scenario files: ", e.args[0])
            return
        self.ui.update_scenario_combo_box(self.list_of_scenarios)
        self.process_scenario_box()

    def process_config_gen_butt(self):
        try:
            self.visa.v2_configurate_generator_sample(self.ui.get_generator_data_manual())
        except Exception as e:
            self.ui.logging("ERROR configurate generator: ", e.args[0])
            return
        self.ui.logging("Successfull configurate generator")

    def process_out_toggle_butt(self):
        try:
            self.visa.v2_toggle_out1()
        except Exception as e:
            self.ui.logging("ERROR toggle generator out1: ", e.args[0])
            return
        self.ui.logging("Generator out1 has been toggled")

    def process_not_out_toggle_butt(self):
        try:
            self.visa.v2_toggle_not_out1()
        except Exception as e:
            self.ui.logging("ERROR toggle generator !out1: ", e.args[0])
            return
        self.ui.logging("Generator !out1 has been toggled")

    def process_send_comm_butt(self):
        try:
            res_index, comm = self.ui.get_resource_comm_data()
            if comm == "":
                return
            match res_index:
                case 0:
                    res = self.visa.oscilloscope
                    self.visa.v2_oscilloscope_ping()
                case 1:
                    res = self.visa.generator
                    self.visa.v2_generator_ping()
                    
            if comm[-1] == "?":
                query = self.visa.query(res, comm)
                self.ui.logging(f"'{comm}', QUERY:{query}")
                self.visa.detect_errors(res)
                return
            self.visa.send_command(res, comm)
            self.visa.detect_errors(res)
        except Exception as e:
            self.ui.logging("ERROR send command to resource: ", e.args[0])
            return

    def process_osc_run_butt(self):
        try:
            self.visa.v2_oscilloscope_run()
        except Exception as e:
            self.ui.logging("ERROR RUN oscilloscope: ", e.args[0])
            return

    def process_measure_butt(self):
        try:
            channels, _, _, _ = self.ui.get_channels_data()
            sample = self.visa.v2_get_sample()
            sample.show_all(channels)
        except Exception as e:
            self.ui.logging("ERROR measure results oscilloscope: ", e.args[0])
            return

    def process_default_gui_butt(self):
        try:
            self.ui.set_default_reg_values(RegData(is_zero_init=False))
            self.ui.set_channels_data_zero()
            self.ui.set_generator_data_zero()
            self.ui.set_triggers_data_zero()
            self.ui.clear_chip_metadata()
            self.ui.clean_plots_data()
            self.process_reset_scenario_butt()
        except Exception as e:
            self.ui.logging("ERROR set default gui status: ", e.args[0])
            return

    def process_scenar_start_butt(self):
        try:
            if self.scenario_to_start.name == '':
                self.ui.logging("ERROR start scenario testing. No scenario to start.")
                return
            file = self.start_test(self.scenario_to_start, self.ui.is_scenario_screenable(), self.ui.scenario_comp_out_use_index(), self.SCENARIO_TEST)
        except Exception as e:
            self.set_writeable_gui()
            self.ui.logging("ERROR start scenario testing: ", e.args[0])
            return

    def create_manual_scenario(self):
        manual_scenar = Scenario([], "", "", [], 0, 0, 0)
        generator_samples = self.ui.get_generator_data_scenario()
        manual_scenar.add_layer(
            Layer(
                self.ui.get_w_registers_data(),
                generator_samples,
            )
        )
        channels, trig_src, trig_lvl, tim_scale = self.ui.get_channels_data()

        manual_scenar.name = str(datetime.datetime.now(tz=timezone('Europe/Moscow')))
        manual_scenar.description = "manual test"
        manual_scenar.channels = channels
        manual_scenar.trig_src = trig_src
        manual_scenar.trig_lvl = trig_lvl
        manual_scenar.tim_scale = tim_scale
        return manual_scenar

    def process_start_butt(self):
        try:
            manual_scenar = self.create_manual_scenario()
            file = self.start_test(manual_scenar, self.ui.is_manual_screenable(), self.ui.manual_comp_out_use_index(), self.MANUAL_TEST)
        except Exception as e:
            self.set_writeable_gui()
            self.ui.logging("ERROR start manual testing: ", e.args[0])
            return

    def process_osc_config_butt(self):
        try:
            channels, trig_src, trig_lvl, tim_scale = self.ui.get_channels_data()
            self.visa.v2_configurate_oscilloscope_scenario(channels, trig_src, trig_lvl, tim_scale)
        except Exception as e:
            self.ui.logging("ERROR configurate oscilloscope:", e.args[0])
        return

    def check_instruments_connection(self):
        try:
            self.visa.v2_generator_ping()
            self.visa.v2_oscilloscope_ping()
            self.uart.is_connection_open()
        except:
            raise Exception("Need to connect other instruments.")

    def change_rw_gui(self):
        self.ui.change_rw_constants()
        self.ui.change_rw_channels()
        self.ui.change_rw_gen()
        self.ui.change_rw_env()
        self.ui.change_rw_gui_buttons()
        self.ui.change_rw_logs()
        self.ui.change_rw_uart()
        self.ui.change_rw_testing()
        self.ui.change_rw_triggs()

    def set_writeable_gui(self): 
        self.ui.set_constants_writeable()
        self.ui.set_channels_writeable()
        self.ui.set_gen_writeable()
        self.ui.set_env_writeable()
        self.ui.set_gui_buttons_writeable()
        self.ui.set_logs_writeable()
        self.ui.set_uart_writeable()
        self.ui.set_testing_writeable()
        self.ui.set_triggs_writeable()

    def start_test(self, scenario:Scenario, is_screening:bool, out_index:int, testing_type:int):
        start_time = str(datetime.datetime.now(tz=timezone('Europe/Moscow'))).replace(":", ".")[:-13].replace(" ", "_")

        self.check_instruments_connection()
        self.ui.clear_log()
        self.ui.clean_plots_data()
        self.results_folder = ""

        triggers = self.ui.get_triggers_data()

        chip_name, chip_desc = self.ui.get_chip_metadata()

        self.visa.v2_off_all_out1()
            
        match testing_type:
            case self.MANUAL_TEST:
                self.ui.logging(f"Start manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.ui.logging(f"Start scenario:{scenario.name} test for chip:{chip_name}")

        if len(scenario.channels) != 0:
            self.visa.v2_configurate_oscilloscope_scenario(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)
            self.ui.set_channels_data(scenario.channels, scenario.trig_src, scenario.trig_lvl, scenario.tim_scale)

        self.change_rw_gui()    

        
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

            self.ui.set_reg_values(RegData(is_zero_init=False, template_list=test.constants))
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
                            self.ui.logging(f"WARNING! constants mismatch. reg:{k}, mismatch:{v}")
                        case self.SCENARIO_TEST:
                            self.ui.logging(f"WARNING! Layer#{idx_layer+1}. Constants mismatch. reg:{k}, mismatch:{v}")

            for sample_index, test_sample in enumerate(test.samples):
                for l0, l1 in triggers:
                    if self.STOP_flag == 1:
                        break

                    self.ui.set_triggers_data(l0*5, l1*5)

                    match testing_type:
                        case self.MANUAL_TEST:
                            self.ui.logging(f"Start sample#{test_idx} of {scenario.total_test_count*len(triggers)}")
                        case self.SCENARIO_TEST:
                            self.ui.logging(f"Layer#{idx_layer+1}. Start sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)}")
                    
                    self.uart.send_triggers((test_sample.delay*10**9)//5, l0, l1)

                    self.ui.set_generator_sample(test_sample)
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
                            self.ui.logging(f"Get chip data:{chip_data} (Sample#{test_idx} of {scenario.total_test_count*len(triggers)})")
                        case self.SCENARIO_TEST:
                            self.ui.logging(f"Get chip data:{chip_data} (Layer#{idx_layer+1}. Sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)})")
                    
                    screen_file = ""
                    if is_screening:
                        self.ui.logging(f"Taking screenshot.")
                        screen_data = self.visa.v2_take_screen()
                        screen_file = self.save_screenshot(start_time, chip_name, scenario.name, screen_data, testing_type, idx_layer, test_idx)
                        time.sleep(5)
                        self.ui.logging(f"Screenshot saved.")

                    self.visa.v2_off_all_out1()
                    match testing_type:
                        case self.MANUAL_TEST:
                            self.ui.logging(f"Finish sample#{test_idx} of {scenario.total_test_count*len(triggers)}")
                        case self.SCENARIO_TEST:
                            self.ui.logging(f"Layer#{idx_layer+1}. Finish sample#{sample_index+1} of {test.test_count*len(triggers)}. Total tests:{scenario.total_test_count*len(triggers)}")
                    
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
                self.ui.logging(f"Finish manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.ui.logging(f"Finish scenario:{scenario.name} test for chip:{chip_name}")
            
        logs = self.ui.get_logs()
        logs_file = self.save_logs(start_time, chip_name, scenario.name, testing_type, logs)

        result.logs = logs_file

        result_file = self.save_results(result, start_time, chip_name, scenario.name, testing_type)
        
        self.results_folder = result_file

        self.set_writeable_gui()
        return result_file

    def save_results(self, data:Result, start_time, chip_name, scenario_name, testing_type):
        file_name = f"result.json"
        match testing_type:
            case self.MANUAL_TEST:
                path = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time)
            case self.SCENARIO_TEST:
                path = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time)
        
        try:
            os.makedirs(path)
        except:
            pass

        with open(path+"\\"+file_name, 'w') as file:
            file.write(data.toJSON())
            file.close()

        return path

    def save_screenshot(self, start_time, chip_name, scenario_name, screenshot_data, testing_type, layer_index, sample_index):
        file_name = f"screenshot_sample_{sample_index}.png"
        match testing_type:
            case self.MANUAL_TEST:
                path = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, PICTURES_FOLDER, PICTURES_SCREENSHOTS_FOLDER)
            case self.SCENARIO_TEST:
                path = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, f"layer_{layer_index+1}", PICTURES_FOLDER, PICTURES_SCREENSHOTS_FOLDER)
        
        try:
            os.makedirs(path)
        except:
            pass

        f = open(path+"\\"+file_name, "wb")
        f.write(screenshot_data)
        f.close()

        return path+"\\"+file_name
    
    def save_points(self, start_time, chip_name, scenario_name, testing_type, layer_index, sample_index, data:OscilloscopeData, channels, l0, l1):
        file_name_points = f"channels_data_{sample_index}.json"
        match testing_type:
            case self.MANUAL_TEST:
                path_points = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, RAW_DATA_FOLDER)
            case self.SCENARIO_TEST:
                path_points = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, f"layer_{layer_index+1}", RAW_DATA_FOLDER)
        
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
                path_plots = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
            case self.SCENARIO_TEST:
                path_plots = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, f"layer_{layer_index+1}", PICTURES_FOLDER, PICTURES_PLOTS_FOLDER)
        
        try:
            os.makedirs(path_plots)
        except:
            pass

        link_file = "plots.png"
        data.plot_all(channels).savefig(path_plots+"\\"+file_name_plots, format='pdf')
        plt.close('all')
        data.plot_for_gui(channels, sample_index, l0, l1).savefig(link_file, format='png', dpi=80)
        plt.close('all')

        self.ui.set_plots_data(link_file)

        return path_points+"\\"+file_name_points, path_plots+"\\"+file_name_plots
    
    def save_logs(self, start_time, chip_name, scenario_name, testing_type, logs:str):
        file_name = f"logs.txt"
        match testing_type:
            case self.MANUAL_TEST:
                path = os.path.join(MANUAL_TESTS_PATH, chip_name, start_time, LOGS_FOLDER)
            case self.SCENARIO_TEST:
                path = os.path.join(SCENARIO_TESTS_PATH, chip_name, f"scenario_{scenario_name}", start_time, LOGS_FOLDER)
        
        try:
            os.makedirs(path)
        except:
            pass

        f = open(path+"\\"+file_name, "w")
        f.write(logs)
        f.close()

        return path+"\\"+file_name

if __name__ == "__main__":
    stand = Stand()

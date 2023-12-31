from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import RegData, Scenario, TestSample, find_scenarios, differenence

import sys
import time
import os
import datetime
from pytz import timezone

tests_path = os.path.dirname(os.path.abspath(__file__)) + r'\tests\\'

class Stand(object):
    MANUAL_TEST = 0
    SCENARIO_TEST = 0

    def __init__(self) -> None:
        self.main_scenario = Scenario([], "", "", [], 0, 0, 0)
        self.list_of_scenarios = list[Scenario]
        self.scenario_to_start = Scenario([], "", "", [], 0, 0, 0)

        self.ui = Ui()
        self.uart = UART()
        self.visa = Visa()
        # Main window
        self.ui.ui.butt_set_default_gui.clicked.connect(self.process_default_gui_butt)
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
            TestSample(
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
        self.ui.update_scenario_description(self.list_of_scenarios[index].description)
        self.ui.set_reg_values(RegData(is_zero_init=False, template_list=self.list_of_scenarios[index].tests[0].constants))
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
            sample.plot_all(channels)
        except Exception as e:
            self.ui.logging("ERROR measure results oscilloscope: ", e.args[0])
            return

    def process_default_gui_butt(self):
        try:
            self.ui.set_default_reg_values(RegData(is_zero_init=False))
            self.ui.set_channels_data_zero()
            self.ui.set_generator_data_zero()
            self.ui.clear_chip_metadata()
            self.process_reset_scenario_butt()
        except Exception as e:
            self.ui.logging("ERROR set default gui status: ", e.args[0])
            return

    def process_scenar_start_butt(self):
        try:
            self.start_test(self.scenario_to_start, self.ui.is_scenario_screenable(), self.ui.scenario_comp_out_use_index(), self.SCENARIO_TEST)
        except Exception as e:
            self.ui.logging("ERROR start scenario testing: ", e.args[0])
            return

    def create_manual_scenario(self):
        manual_scenar = Scenario([], "", "", [], 0, 0, 0)
        generator_samples = self.ui.get_generator_data_scenario()
        manual_scenar.add_layer(
            TestSample(
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
        # try:
        manual_scenar = self.create_manual_scenario()
        # for s in manual_scenar.tests[0].samples:
        #     print(s.toJSON())
        #     pass
        self.start_test(manual_scenar, self.ui.is_manual_screenable(), self.ui.manual_comp_out_use_index(), self.MANUAL_TEST)
        # except Exception as e:
        #     self.ui.logging("ERROR start manual testing: ", e.args[0])
        #     return

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

    def set_writeable_gui(self): 
        self.ui.set_constants_writeable()
        self.ui.set_channels_writeable()
        self.ui.set_gen_writeable()

    def start_test(self, scenario:Scenario, is_screening:bool, out_index:int, testing_type:int):
        self.check_instruments_connection()
        self.ui.clear_log()

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

        self.ui.set_reg_values(RegData(is_zero_init=False, template_list=scenario.tests[0].constants))
        self.uart.write_w_regs(RegData(is_zero_init=False, template_list=scenario.tests[0].constants))
        
        test_idx = 1
        for idx_layer, test in enumerate(scenario.tests):
            sended = test.constants
            get = self.uart.read_rw_regs()
            if sended != get:
                diff = differenence(sended, get)
                for k,v in diff.items():
                    match testing_type:
                        case self.MANUAL_TEST:
                            self.ui.logging(f"WARNING! constants mismatch. reg:{k}, mismatch:{v}")
                        case self.SCENARIO_TEST:
                            self.ui.logging(f"WARNING! Layer#{idx_layer+1}. Constants mismatch. reg:{k}, mismatch:{v}")

            for _, test_sample in enumerate(test.samples):
                match testing_type:
                    case self.MANUAL_TEST:
                        self.ui.logging(f"Start sample #{test_idx} of {scenario.total_test_count}")
                    case self.SCENARIO_TEST:
                        self.ui.logging(f"Layer#{idx_layer+1}. Start sample#{test_idx} of {test.test_count}. Total tests:{scenario.total_test_count}")
                
                self.ui.set_generator_sample(test_sample)
                self.visa.v2_configurate_generator_sample(test_sample)
                self.visa.v2_oscilloscope_run()
                self.visa.v2_on_out1(out_index)

                self.uart.send_start_command()

                sample_data = self.visa.v2_get_sample()
                chip_data = self.uart.get_chip_data()
                match testing_type:
                    case self.MANUAL_TEST:
                        self.ui.logging(f"Get chip data:{chip_data} (Sample#{test_idx} of {scenario.total_test_count})")
                    case self.SCENARIO_TEST:
                        self.ui.logging(f"Get chip data:{chip_data} (Layer#{idx_layer+1}. Sample#{test_idx} of {test.test_count}. Total tests:{scenario.total_test_count})")
                
                if is_screening:
                    screen_data = self.visa.v2_take_screen()
                    time.sleep(5)

                self.visa.v2_off_all_out1()
                match testing_type:
                    case self.MANUAL_TEST:
                        self.ui.logging(f"Finish sample #{test_idx} of {scenario.total_test_count}")
                    case self.SCENARIO_TEST:
                        self.ui.logging(f"Layer#{idx_layer+1}. Finish sample#{test_idx} of {test.test_count}. Total tests:{scenario.total_test_count}")
                
                test_idx += 1
                
        match testing_type:
            case self.MANUAL_TEST:
                self.ui.logging(f"Finish manual test for chip:{chip_name}")
            case self.SCENARIO_TEST:
                self.ui.logging(f"Finish scenario:{scenario.name} test for chip:{chip_name}")
            
        logs = self.ui.get_logs()

        self.set_writeable_gui()

    def save_manual_data(self, chip_name, chip_data, plots, dots, screen_bytes):
        pass

    def save_scenario_data(self, chip_name, chip_data, plots, dots, screen_bytes):
        pass

if __name__ == "__main__":
    stand = Stand()
    stand.ui.MainWindow.show()
    sys.exit(stand.ui.app.exec_())

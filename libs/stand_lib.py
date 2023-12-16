from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import RegData, Scenario, TestSample

import sys


class Stand(object):
    ui: Ui
    uart: UART
    visa: Visa

    def __init__(self) -> None:
        self.main_scenario = Scenario()

        self.ui = Ui()
        self.uart = UART()
        self.visa = Visa()
        # Registers panel
        self.ui.ui.com_write_butt.clicked.connect(self.process_com_write_butt)
        self.ui.ui.com_read_all_butt.clicked.connect(self.process_com_read_all_butt)
        self.ui.ui.com_read_r_butt.clicked.connect(self.process_com_read_r_butt)
        self.ui.ui.com_read_rw_butt.clicked.connect(self.process_com_read_rw_butt)
        self.ui.ui.com_conn_butt.clicked.connect(self.process_com_conn_butt)
        # Constants panel
        self.ui.ui.butt_set_default_regs.clicked.connect(self.process_set_default_reg_values_butt)
        # Environment panel
        self.ui.ui.oscilloscope_conn_butt.clicked.connect(
            self.process_oscilloscope_conn_butt)
        self.ui.ui.generator_conn_butt.clicked.connect(
            self.process_generator_conn_butt)
        self.ui.ui.reset_osc_butt.clicked.connect(self.process_reset_osc_butt)
        self.ui.ui.reset_gen_butt.clicked.connect(self.process_reset_gen_butt)
        self.ui.ui.scan_res_butt.clicked.connect(self.process_scan_res_butt)
        # Generator settings panel
        self.ui.ui.gen_zero_butt.clicked.connect(self.process_set_zeros_generator_butt)
        # Logs panel
        self.ui.ui.clean_log_butt.clicked.connect(self.process_clear_log_butt)
        # Scenario processing panel
        self.ui.ui.reset_scen_butt.clicked.connect(self.process_reset_scenario_butt)
        self.ui.ui.generate_scen_butt.clicked.connect(self.process_generate_scenario_butt)
        self.ui.ui.add_layer_scen_butt.clicked.connect(self.process_add_layer_butt)
        # self.ui.ui.delete
        
        # TEST BUTT
        self.ui.ui.start_butt.clicked.connect(self.process_TEST_BUTT)

    def process_com_write_butt(self):
        try:
            self.uart.write_w_regs(self.ui.get_w_registers_data())
            self.ui.logging("Constants sended succesfully")
        except Exception as e:
            self.ui.logging("ERROR send constants: ", e.args[0])
            return
        # Send custom data
        # try:
        #     self.uart.write_reg(int.to_bytes(65, 1, 'big'), [int.to_bytes(255, 1, 'big') for i in range(70)])
        #     self.ui.logging("Constants sended succesfully")
        # except Exception as e:
        #     self.ui.logging("ERROR send constants: ", e.args[0])
        #     return


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
        self.ui.log_resources(self.visa.res_list())

    def process_set_default_reg_values_butt(self):
        self.ui.set_reg_values(RegData())

    def process_set_zeros_generator_butt(self):
        self.ui.set_generator_data_zero()

    def process_clear_log_butt(self):
        self.ui.clear_log()

    def process_reset_scenario_butt(self):
        self.ui.reset_scenario_data()
        self.main_scenario = Scenario()
        self.ui.logging("Successfully reset scenario")

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
        name, desc, _ = self.ui.get_scenario_data()
        if name.strip() == "":
            self.ui.logging("Please, write the scenario name!")
            return
        try:
            channels = self.ui.get_channels_data()
        except Exception as e:
            self.ui.logging("ERROR get data about signals: ", e.args[0])
            return
        self.main_scenario.name = name
        self.main_scenario.description = desc
        self.main_scenario.channels = channels
        try:
            self.main_scenario.save_scenario()
        except Exception as e:
            self.ui.logging("ERROR create a new scenario: ", e.args[0])
            return
        self.ui.logging(f"Successfull creation of a new scenario '{self.main_scenario.name}'. Layers: {self.main_scenario.layers_count}, total tests:{self.main_scenario.total_test_count}")
        self.process_reset_scenario_butt()

    def process_TEST_BUTT(self):
        data = self.ui.get_generator_data_scenario()
        for sample in data:
            print(sample.toJSON())
        self.ui.log_registers(f"len: {len(data)}")


if __name__ == "__main__":
    stand = Stand()
    stand.ui.MainWindow.show()
    sys.exit(stand.ui.app.exec_())

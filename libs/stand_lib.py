from ui_lib import Ui
from uart_lib import UART
from visa_lib import Visa
from pkg import RegData

import sys

class Stand(object):
    ui:Ui
    uart:UART
    visa:Visa

    def __init__(self) -> None:
        self.ui = Ui()
        self.uart = UART()
        self.visa = Visa()

        self.ui.ui.com_write_butt.clicked.connect(self.process_com_write_butt)
        self.ui.ui.com_read_butt.clicked.connect(self.process_com_read_butt)
        self.ui.ui.com_conn_butt.clicked.connect(self.process_com_conn_butt)

        self.ui.ui.oscilloscope_conn_butt.clicked.connect(self.process_oscilloscope_conn_butt)
        self.ui.ui.generator_conn_butt.clicked.connect(self.process_generator_conn_butt)
        self.ui.ui.reset_osc_butt.clicked.connect(self.process_reset_osc_butt)
        self.ui.ui.reset_gen_butt.clicked.connect(self.process_reset_gen_butt)

        self.ui.ui.start_butt.clicked.connect(self.process_start_butt)

    def process_com_write_butt(self):
        try:
            self.uart.write_w_regs(self.ui.get_w_registers_data())
        except Exception as e:
            self.ui.logging("ERROR send constants: ", e.args)
            return

    def process_com_read_butt(self):
        try:
            self.ui.log_registers(self.uart.read_all_regs().__str__())
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

    def process_oscilloscope_conn_butt (self):
        pass

    def process_generator_conn_butt (self):
        pass

    def process_reset_osc_butt (self):
        pass

    def process_reset_gen_butt (self):
        pass

    def process_start_butt (self):
        pass

if __name__ == "__main__":
    stand = Stand()
    stand.ui.MainWindow.show()
    sys.exit(stand.ui.app.exec_())
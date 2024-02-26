import serial
import time
import builtins

from pkg import RegData, rw_regs_start_addr_count, r_regs_start_addr_count, rw_regs_start_addr_count_analog, rw_regs_start_addr_count_analog_digit, rw_regs_start_addr_count_digit


class UART(object):
    TIME_TO_SLEEP = 0.6

    def __init__(self) -> None:
        self.ser = serial.Serial()
        self.BAUDRATE = 115200
        self.BYTESIZE = 8
        self.PARITY = serial.PARITY_NONE
        self.STOPBITS = 1
        self.TIMEOUT = 0.1

        self.WRITE_WORD =         int.to_bytes(0b0111_0111, 1, 'big')
        self.READ_WORD =          int.to_bytes(0b0111_0010, 1, 'big')
        self.START_WORD =         int.to_bytes(0b0111_0011, 1, 'big')
        self.CHIP_DATA_WORD =     int.to_bytes(0b0110_0100, 1, 'big')
        self.ERR_CHIP_WORD =      int.to_bytes(0b0110_0101, 1, 'big')
        self.SEND_TRIGGERS_WORD = int.to_bytes(0b0111_0100, 1, 'big')
        self.SEND_SETTINGS_WORD = int.to_bytes(0b0110_0111, 1, 'big')
        self.EMULATION_WORD =     int.to_bytes(0b0110_0101, 1, 'big')
        self.CS_UP_WORD =         int.to_bytes(0b1110_0011, 1, 'big')
        self.CS_DOWN_WORD =       int.to_bytes(0b0110_0011, 1, 'big')
        self.AUTO_CS_WORD =       int.to_bytes(0b0111_1010, 1, 'big')
        self.NOT_AUTO_CS_WORD =   int.to_bytes(0b1111_1010, 1, 'big')
        self.DAC_START_WORD =     int.to_bytes(0b1010_1010, 1, 'big')

    def send_start_adc_test_command(self):
        self.ser.reset_input_buffer()
        self.ser.write(self.DAC_START_WORD)
        data = []
        while True:
            raw_data = self.ser.read(1)
            if raw_data == b"":
                break
            data.append(int.from_bytes(raw_data, 'big'))

        return data

    def send_sc_raw_data(self, data, type_mess):
        byte_data = [int.to_bytes(i, 1, 'big') for i in data]
        message = [type_mess, int.to_bytes(len(data)-1, 1, 'big')]

        self.ser.reset_input_buffer()

        for mes in message:
            self.ser.write(mes)

        for mes in byte_data:
            self.ser.write(mes)

    def send_auto_cs_raw_data(self, data):
        self.send_sc_raw_data(data, self.AUTO_CS_WORD)

    def send_not_auto_cs_raw_data(self, data):
        self.send_sc_raw_data(data, self.NOT_AUTO_CS_WORD)

    def connect_com(self, com: str):
        try:
            self.ser.close()
        except:
            pass

        self.ser = serial.Serial(
            com,
            baudrate=self.BAUDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT,
        )

    def send_stand_settings(self, em_adc, em_trigs):
        settings = 0

        settings += em_adc
        settings += em_trigs*2

        message = [self.SEND_SETTINGS_WORD, int.to_bytes(settings, 1, 'big')]
        for m in message:
            self.ser.write(m)

    def send_emulation_state(self, state, start_status):
        settings = 0

        settings += state
        settings += start_status*2

        message = [self.EMULATION_WORD, int.to_bytes(settings, 1, 'big')]
        for m in message:
            self.ser.write(m)

    def send_CS_state(self, state):
        match state:
            case False:
                self.ser.write(self.CS_DOWN_WORD)
            case True:
                self.ser.write(self.CS_UP_WORD)

    def read_i_regs(self, settings: tuple, is_auto) -> RegData:
        reg_data = RegData(is_zero_init=True)

        packages = self.spi_read_data_former(settings)

        for pk in packages:
            data = self.read_reg(pk, is_auto)

            for byte_idx in range(len(data)):
                reg_data.reg_data[byte_idx+pk[0]] = data[byte_idx]
            time.sleep(self.TIME_TO_SLEEP)
            
        return reg_data

    def read_all_regs(self, is_auto) -> RegData:
        # return self.read_i_regs((r_regs_start_addr_count + rw_regs_start_addr_count))
        return self.read_i_regs((r_regs_start_addr_count + rw_regs_start_addr_count_analog + rw_regs_start_addr_count_analog_digit + rw_regs_start_addr_count_digit), is_auto)

    def read_r_regs(self, is_auto) -> RegData:
        return self.read_i_regs(r_regs_start_addr_count, is_auto)

    def read_rw_regs(self, is_auto) -> RegData:
        # return self.read_i_regs(rw_regs_start_addr_count)
        return self.read_i_regs((rw_regs_start_addr_count_analog + rw_regs_start_addr_count_analog_digit + rw_regs_start_addr_count_digit), is_auto)

    def write_one_reg(self, data, addr, is_auto):
        payload = [0b1000_0000+addr, data]
        print(f"to SPI data: {payload}")
        match is_auto:
            case True:
                self.send_sc_raw_data(payload, self.AUTO_CS_WORD)
            case False:
                self.send_sc_raw_data(payload, self.NOT_AUTO_CS_WORD)

        time.sleep(self.TIME_TO_SLEEP)

    def write_w_regs(self, data: RegData, is_auto, settings):
        regs = []

        if settings[0]:
            regs += rw_regs_start_addr_count_analog
        if settings[1]:
            regs += rw_regs_start_addr_count_analog_digit
        if settings[2]:
            regs += rw_regs_start_addr_count_digit
        
        packages = self.spi_write_data_former(regs, data)
        
        for pk in packages:
            match is_auto:
                case True:
                    self.send_sc_raw_data(pk, self.AUTO_CS_WORD)
                case False:
                    self.send_sc_raw_data(pk, self.NOT_AUTO_CS_WORD)

            time.sleep(self.TIME_TO_SLEEP)

        # for tupl in rw_regs_start_addr_count:

        #     start_addr = tupl[0]
        #     count = tupl[1]
        #     self.write_reg(
        #         int.to_bytes(start_addr, 1, "big"),
        #         data.reg_data[start_addr:start_addr+count],
        #     )
        #     time.sleep(self.TIME_TO_SLEEP)

    def spi_read_data_former(self, data_settings):
        to_spi_package = []

        for setting in data_settings:
            start_addr = setting[0]
            count = setting[1]

            read_package = []

            for reg_idx in range(start_addr, start_addr+count):
                read_package.append(reg_idx)
            read_package.append(0b0000_0000)

            to_spi_package.append(read_package)           

        print(f"to SPI data: {to_spi_package}")
        return to_spi_package

    def spi_write_data_former(self, data_settings, data: RegData):
        to_spi_package = []

        for setting in data_settings:
            start_addr = setting[0]
            count = setting[1]

            write_package = []

            for reg_idx in range(start_addr, start_addr+count):
                write_package.append(0b1000_0000+reg_idx)
                match type(data.reg_data[reg_idx]):
                    case builtins.int:
                        write_package.append(data.reg_data[reg_idx])
                    case builtins.bytes:
                        write_package.append(int.from_bytes(data.reg_data[reg_idx], 'big'))

            to_spi_package.append(write_package)           

        print(f"to SPI data: {to_spi_package}")
        return to_spi_package


    def send_start_command(self):
        self.is_connection_open()
        self.ser.write(self.START_WORD)

    def write_reg(self, start_addr: bytes, data: list[bytes]):
        self.is_connection_open()
        package = [self.WRITE_WORD, start_addr,
                   int.to_bytes(len(data), 1, "big")]
        
        for byte in package:
            self.ser.write(byte)

        for byte in data:
            self.ser.write(byte)

    def send_triggers(self, delay:int, l0:int, l1:int):
        package = [
            self.SEND_TRIGGERS_WORD,
            int.to_bytes(int(delay), 1, 'big'),
            int.to_bytes(int(l0), 1, 'big'),
            int.to_bytes(int(l1), 2, 'big'),
        ]

        for byte in package:
            self.ser.write(byte)

    def read_reg(self, package:list[int], is_auto) -> list[bytes]:
        self.is_connection_open()
        corrupt_count = 0
        read_data = []

        while True:
            if corrupt_count == 10:
                raise Exception("Restart. Detected corrupted data!")      
            match is_auto:
                case True:
                    self.send_sc_raw_data(package, self.AUTO_CS_WORD)
                case False:
                    self.send_sc_raw_data(package, self.NOT_AUTO_CS_WORD)

            read_data = []
            while True:
                data = self.ser.read(1)

                if data == b'':
                    break

                read_data.append(data)

                if len(read_data) == len(package):
                    break
            
            if len(package) != len(read_data):
                print(f"Packet corrupted. Try again!")
                corrupt_count+=1
                if corrupt_count == 1:
                    raise Exception("Restart. Detected corrupted data!")
                break
            break

        return read_data[1:]

    # def read_reg(self, package:list[int], is_auto) -> list[bytes]:
    #     self.is_connection_open()
    #     corrupt_count = 0
    #     while True:
    #         # package = [self.READ_WORD, start_addr, count]

    #         # for byte in package:
    #         #     self.ser.write(byte)

    #         match is_auto:
    #             case True:
    #                 self.send_sc_raw_data(package, self.AUTO_CS_WORD)
    #             case False:
    #                 self.send_sc_raw_data(package, self.NOT_AUTO_CS_WORD)

    #         get_flag = 0
    #         read_data = []
    #         while True:
    #             if corrupt_count == 100:
    #                 raise Exception("Check FPGA, detected read loop")
    #             if get_flag == 0:
    #                 data = self.ser.read(1)
    #                 if data != self.READ_WORD:
    #                     if data == b'':
    #                         break
    #                     continue
    #                 get_flag = 1

    #             data = self.ser.read(1)

    #             if data == b'':
    #                 break

    #             read_data.append(data)
    #             if len(read_data) == int.from_bytes(count, "big"):
    #                 break
            
    #         if int.from_bytes(count, "big") != len(read_data):
    #             print(f"Packet corrupted. Try again with: start_addr:{int.from_bytes(start_addr, 'big')}, count:{int.from_bytes(count, 'big')}")
    #             corrupt_count+=1
    #             continue
    #         break

    #     return read_data

    def is_connection_open(self):
        if not self.ser.is_open:
            raise Exception("No connection to COM PORT.")
        return

    def force_get_chip_data(self):
        self.is_connection_open()
        self.ser.write(self.CHIP_DATA_WORD)

    def get_chip_data(self) -> dict:
        self.is_connection_open()
        err_count = 0
        while True:
            try:
                data, str_res = self.read_chip_data()
                return data, str_res
            except:
                err_count += 1
                if err_count == 3:
                    raise Exception("Cat't get data from chip.")
                self.force_get_chip_data()

    def read_chip_data(self)-> dict:
        state = 0
        empty_count = 0
        data_list = []
        while True:
            data = self.ser.read(1)
            if data == self.ERR_CHIP_WORD:
                return {}, ""
            if state == 0 and data == b'':
                empty_count += 1
                if empty_count == 3:
                    raise Exception("Read timeout reached.")
                continue
            if state == 1 and data == b'':
                break
            state = 1
            data_list.append(data)
            if len(data_list) == 12:
                break

        if len(data_list) != 12:
            raise Exception("Data is corrupted")
        
        str_res = ""
        for i in data_list:
            str_res += f"{int.from_bytes(i, 'big'):08b}"

        data_in = dict()

        data_in['V'] = int(f'0b'+str_res[0], base=0)
        data_in['R'] = int(f'0b'+str_res[1:6], base=0)
        data_in['ADR'] = int(f'0b'+str_res[6:9], base=0)
        data_in['N0'] = int(f'0b'+str_res[9:13], base=0)
        data_in['A0'] = int(f'0b'+str_res[13:23], base=0)
        data_in['N1'] = int(f'0b'+str_res[23:27], base=0)
        data_in['A1'] = int(f'0b'+str_res[27:37], base=0)
        data_in['N2'] = int(f'0b'+str_res[37:41], base=0)
        data_in['A2'] = int(f'0b'+str_res[41:51], base=0)
        data_in['N3'] = int(f'0b'+str_res[51:55], base=0)
        data_in['A3'] = int(f'0b'+str_res[55:65], base=0)
        data_in['N4'] = int(f'0b'+str_res[65:69], base=0)
        data_in['A4'] = int(f'0b'+str_res[69:79], base=0)
        data_in['O'] = int(f'0b'+str_res[79], base=0)
        data_in['TIME'] = int(f'0b'+str_res[80:], base=0)

        return data_in, str_res
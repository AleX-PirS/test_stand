import serial

from pkg import RegData, rw_regs_start_addr_count, r_regs_start_addr_count


class UART(object):
    def __init__(self) -> None:
        self.ser = serial.Serial()
        self.BAUDRATE = 115200
        self.BYTESIZE = 8
        self.PARITY = serial.PARITY_NONE
        self.STOPBITS = 1
        self.TIMEOUT = 1

        self.WRITE_WORD = int.to_bytes(0b01110111, 1, 'big')
        self.READ_WORD = int.to_bytes(0b01110010, 1, 'big')
        self.START_WORD = int.to_bytes(0b01110011, 1, "big")

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

    def read_i_regs(self, settings: tuple) -> RegData:
        reg_data = RegData(is_zero_init=True)
        for tupl in settings:
            data = self.read_reg(
                int.to_bytes(tupl[0], 1, "big"),
                int.to_bytes(tupl[1], 1, "big"),
            )

            for byte_idx in range(len(data)):
                reg_data.reg_data[byte_idx+tupl[0]] = data[byte_idx]

        return reg_data

    def read_all_regs(self) -> RegData:
        return self.read_i_regs((r_regs_start_addr_count + rw_regs_start_addr_count))

    def read_r_regs(self) -> RegData:
        return self.read_i_regs(r_regs_start_addr_count)

    def read_rw_regs(self) -> RegData:
        return self.read_i_regs(rw_regs_start_addr_count)

    def write_w_regs(self, data: RegData):
        for tupl in rw_regs_start_addr_count:
            start_addr = tupl[0]
            count = tupl[1]
            self.write_reg(
                int.to_bytes(start_addr, 1, "big"),
                data.reg_data[start_addr:start_addr+count],
            )

    def send_start_command(self):
        self.ser.write(self.START_WORD)

    def write_reg(self, start_addr: bytes, data: list[bytes]):
        self.is_connection_open()
        package = [self.WRITE_WORD, start_addr,
                   int.to_bytes(len(data), 1, "big")]
        # Actual version
        for byte in package:
            self.ser.write(byte)

        for byte in data:
            self.ser.write(byte)
        # Test version
        # for byte in package+data:
        #     self.ser.write(byte)

    def read_reg(self, start_addr: bytes, count: bytes) -> list[bytes]:
        self.is_connection_open()
        corrupt_count = 0
        while True:
            package = [self.READ_WORD, start_addr, count]

            for byte in package:
                self.ser.write(byte)

            get_flag = 0
            read_data = []
            while True:
                if get_flag == 0:
                    data = self.ser.read(1)
                    if data != self.READ_WORD:
                        if data == b'':
                            break
                        continue
                    get_flag = 1

                data = self.ser.read(1)
                print(f'Get payload from uart:"{int.from_bytes(data, "big"):08b}"')

                if data == b'':
                    break

                read_data.append(data)
                if len(read_data) == int.from_bytes(count, "big"):
                    break
            
            print(f'Asked len={int.from_bytes(count, "big")}, get len={len(read_data)}')
            if int.from_bytes(count, "big") != len(read_data):
                print(f"Packet corrupted. Try again with: start_addr:{int.from_bytes(start_addr, 'big')}, count:{int.from_bytes(count, 'big')}")
                corrupt_count+=1
                continue
            if corrupt_count == 5:
                print("Critical error with FPGA")
                raise Exception("Check FPGA, detected read loop")
            break

        return read_data

    def is_connection_open(self):
        if not self.ser.is_open:
            raise Exception("No connection to COM PORT.")
        return

    # def listen_uart(self):
    #     while True:
    #         data = self.ser.read()
    #         match data:
    #             case self.WRITE_WORD:
    #                 print("GET WRITE WORD FROM FPGA")
    #                 pass
    #             case self.READ_WORD:
    #                 print("GET READ WORD FROM FPGA")
    #                 pass
    #             case _:
    #                 print("GET UNSIGNED DATA FROM FPGA:", data)
    #                 pass

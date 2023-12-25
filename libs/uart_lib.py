import serial

from pkg import RegData, rw_regs_start_addr_count, r_regs_start_addr_count


class UART(object):
    def __init__(self) -> None:
        self.ser = serial.Serial()
        self.BAUDRATE = 115200
        self.BYTESIZE = 8
        self.PARITY = serial.PARITY_NONE
        self.STOPBITS = 1
        self.TIMEOUT = 0.5

        self.WRITE_WORD =     int.to_bytes(0b0111_0111, 1, 'big')
        self.READ_WORD =      int.to_bytes(0b0111_0010, 1, 'big')
        self.START_WORD =     int.to_bytes(0b0111_0011, 1, 'big')
        self.CHIP_DATA_WORD = int.to_bytes(0b0000_0000, 1, 'big')
        self.ERR_CHIP_WORD =  int.to_bytes(0b0110_0101, 1, 'big')

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
        self.is_connection_open()
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
                if corrupt_count == 5:
                    raise Exception("Check FPGA, detected read loop")
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
            break

        return read_data

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
                data = self.read_chip_data()
                return data
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
                return {}
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
        data = dict()
        data['V'] = int.from_bytes((data_list[0]&0b1000_0000)>>7, "big")
        data['R'] = int.from_bytes((data_list[0]&0b0111_1100)>>2, "big")
        data['ADR'] = int.from_bytes(((data_list[0]&0b0000_0011)<<1)+((data_list[1]&0b1000_0000)>>7), "big")
        data['N0'] = int.from_bytes((data_list[1]&0b0111_1000)>>3, "big")
        data['A0'] = int.from_bytes(((data_list[1]&0b0000_0111)<<7)+((data_list[2]&0b1111_1110)>>1), "big")
        data['N1'] = int.from_bytes(((data_list[2]&0b0000_0001)<<3)+((data_list[3]&0b1110_0000)>>5), "big")
        data['A1'] = int.from_bytes(((data_list[3]&0b0001_1111)<<5)+((data_list[4]&0b1111_1000)>>3), "big")
        data['N2'] = int.from_bytes(((data_list[4]&0b0000_0111)<<1)+((data_list[5]&0b1000_0000)>>7), "big")
        data['A2'] = int.from_bytes(((data_list[5]&0b0111_1111)<<5)+((data_list[6]&0b1110_0000)>>5), "big")
        data['N3'] = int.from_bytes((data_list[6]&0b0001_1110)>>1, "big")
        data['A3'] = int.from_bytes(((data_list[6]&0b0000_0001)<<9)+(data_list[7]<<1)+((data_list[8]&0b1000_0000)>>7), "big")
        data['N4'] = int.from_bytes((data_list[8]&0b0111_1000)>>3, "big")
        data['A4'] = int.from_bytes(((data_list[8]&0b0000_0111)<<5)+((data_list[9]&0b1111_1110)>>1), "big")
        data['O'] = int.from_bytes(data_list[9]&0b0000_0001, "big")
        data['TIME'] = int.from_bytes((data_list[10]<<8)+data_list[11], "big")

        return data
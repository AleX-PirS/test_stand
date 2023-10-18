import serial

class UART(object):
    BAUDRATE = 115200
    BYTESIZE = 8
    PARITY = serial.PARITY_NONE
    STOPBITS = 1
    TIMEOUT = 2

    WRITE_WORD = 0b10101010
    READ_WORD  = 0b01010101

    ser:serial.Serial
        
    def connect_com(self, com:str):
        self.ser = serial.Serial(
            com, 
            baudrate=self.BAUDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT,
        )

    def write_reg(self, start_addr:int, count:int, data:[int]):
        if len(data)!=count:
            raise Exception("count and len data isn't same")

        package = [self.WRITE_WORD, start_addr, count]
        
        # 1-st realisation
        for i in data:
            package.append(i)

        self.ser.write(package)

        # 2-nd realisation
        for i in package:
            self.ser.write(i)

        for i in data:
            self.ser.write(i)
    # я думаю надо отдельно сделать комманду отправить read и функцию считывания данных
    # те будут функции чтения от FPGF и записи в FPGA
    # и вот как раз в функции read_reg надо убрать часть со считыванием в обработчик в бесконечном лупе
    def read_reg(self, start_addr:int, count:int):
        package = [self.READ_WORD, start_addr, count]
         # 1-st realisation
        self.ser.write(package)

        # 2-nd realisation
        for i in package:
            self.ser.write(i)

        get_flag = 0
        read_data = []
        while True:
            if get_flag == 0:
                data = self.ser.read()
                if data != self.READ_WORD:
                    continue
                get_flag = 1
                
            if len(read_data) == count:
                break
            
            # work if we send from FPGA in a loop like in python
            data = self.ser.read()
            if data == b'':
                continue

            read_data.append(data)
            
    def listen_uart(self):
        while True:
            data = self.ser.read()
            match data:
                case self.WRITE_WORD:
                    print("GET WRITE WORD FROM FPGA")
                    pass
                case self.READ_WORD:
                    print("GET READ WORD FROM FPGA")
                    pass
                case _:
                    print("GET UNSIGNED DATA FROM FPGA:", data)
                    pass



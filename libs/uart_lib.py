import serial

class UART(object):
    BAUDRATE = 115200
    BYTESIZE = 8
    PARITY = serial.PARITY_NONE
    STOPBITS = 1
    TIMEOUT = 2

    ser:serial.Serial
    
    def __init__(self, com) -> None:
        ser = serial.Serial(
            com, 
            baudrate=self.BAUDRATE,
            bytesize=self.BYTESIZE,
            parity=self.PARITY,
            stopbits=self.STOPBITS,
            timeout=self.TIMEOUT,
            )
        
    def connect_com(self, com:str)->str:
        try:
            self.ser = serial.Serial(
                com, 
                baudrate=self.BAUDRATE,
                bytesize=self.BYTESIZE,
                parity=self.PARITY,
                stopbits=self.STOPBITS,
                timeout=self.TIMEOUT,
            )
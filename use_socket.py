# if we need to send command we use session.write("")
# if we need to send command and get response we use session.query("")
import pyvisa as visa
import socket

import time

try:
    rm = visa.ResourceManager()
    print(rm.list_resources())

    devByHTML = "TCPIP0::10.3.69.145::inst0::INSTR"
    devListGen = "TCPIP::10.3.69.145::INSTR"
    devListOsc = "TCPIP::10.3.69.144::INSTR"
    devListOscNew = "TCPIP::10.3.69.144::hislip0,4880::INSTR"

    generator = rm.open_resource(devListGen)
    generator.timeout = 30000
    generator.chunk_size = 128
    generator.read_termination = '\n'
    generator.write_termination = '\n'

    osciloscope = rm.open_resource(devListOsc)
    osciloscope.timeout = 30000
    osciloscope.chunk_size = 128
    osciloscope.read_termination = '\n'
    osciloscope.write_termination = '\n'

    # print("IDN:"+str(generator.query('*IDN?')))
    print(generator.write('*RST'))
    time.sleep(2)
    print(generator.write(':OUTP1 ON'))
    time.sleep(2)
    print(generator.write(':VOLT:HIGH 3mV'))
    # print(generator.read_bytes(1))
    # generator.query(':OUTP1 OFF')
    # time.sleep(5)
    # generator.query(':OUTP1 OFF')

    print(osciloscope.query('*IDN?'))

    # print("IDN:"+str(session.query('*RST')))
    # print("output"+str(session.query(':OUTP1 ON?')))
    # print("res comm:" + str(session.query(":VOLT:HIGH 3V")))

except Exception as e:
    print('[!] Exception:' + str(e))
    
import pyvisa as visa

class Visa(object):
    PULSE_SIGNAL_TYPE = "PULS"
    SQUARE_SIGNAL_TYPE = "SQU"
    SINE_SIGNAL_TYPE = "SIN"
    RAMP_SIGNAL_TYPE = "RAMP"
    NOISE_SIGNAL_TYPE = "NOIS"
    ARB_SIGNAL_TYPE = "USER"

    PULSE_BOX_TYPE = "PULSE"
    SQUARE_BOX_TYPE = "SQUARE"
    SINE_BOX_TYPE = "SINE"
    RAMP_BOX_TYPE = "RAMP"
    NOISE_BOX_TYPE = "NOISE"
    ARB_BOX_TYPE = "ARB"
    
    oscilloscope:visa.Resource
    generator:visa.Resource
    rm:visa.ResourceManager

    def __init__(self) -> None:
        rm = visa.ResourceManager("@py")

"""
Тут надо сделать класс для стенда с функциями только для UI
Чтобы сгенерированный UI просто подбрасывался этим классом
"""
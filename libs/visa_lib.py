import pyvisa as visa

class Visa(object):
    oscilloscope:visa.Resource
    generator:visa.Resource
    rm:visa.ResourceManager

    def __init__(self) -> None:
        rm = visa.ResourceManager("@py")

"""
Тут надо сделать класс для стенда с функциями только для UI
Чтобы сгенерированный UI просто подбрасывался этим классом
"""
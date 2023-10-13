from PyQt5 import QtWidgets
import sys

from ui_gen import Ui_MainWindow

class Ui(object):
    app:QtWidgets.QApplication
    MainWindow:QtWidgets.QMainWindow
    ui:Ui_MainWindow

    def __init__(self) -> None:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()

"""
Тут надо сделать класс для стенда с функциями только для UI
Чтобы сгенерированный UI просто подбрасывался этим классом
"""
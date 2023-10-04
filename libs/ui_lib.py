from PyQt5 import QtWidgets

import sys

class Ui(object):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

"""
Тут надо сделать класс для стенда с функциями только для UI
Чтобы сгенерированный UI просто подбрасывался этим классом
"""
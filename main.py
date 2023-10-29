from PyQt5 import uic
from PyQt5.QtWidgets import *


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("GUI.ui", self)


if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec()

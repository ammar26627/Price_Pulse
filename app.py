from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Price Pulse")
        self.initUi()

    def initUi(self) -> None:
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Price Pulse")
        self.label.move(50, 80)

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText("Start")
        self.button1.clicked.connect(self.clicked)
    
    def clicked(self) -> None:
        self.label.setText("Started")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
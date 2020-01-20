import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5 import QtWidgets, uic


class Ui(QtWidgets.QMainWindow):
    def _init_(self):
        super(Ui, self)._init_()
        uic.loadUi('SepsisDetection.ui', self)

        self.show()



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

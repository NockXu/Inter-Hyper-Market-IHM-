import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox, QScrollArea, QSpacerItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Classes import *


class VuePlan(QWidget):
    def __init__(self):
        super().__init__()
        
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel('Plan du magasin')
        self.layout.addWidget(self.label)




if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VuePlan()
    fenetre.show()
    sys.exit(app.exec())

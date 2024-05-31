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

        # QLabel pour afficher l'image
        self.plan_label = QLabel()
        self.layout.addWidget(self.plan_label)

        pixmap = QPixmap('app2/image/plan1.jpg').scaled(700, 700, Qt.AspectRatioMode.KeepAspectRatio)
        self.plan_label.setPixmap(pixmap)
        

                    
        self.setWindowTitle('Application client')
        self.showMaximized() 




if __name__ == "__main__":
    print(f' --- main --- ')
    app = QApplication(sys.argv)
    fenetre = VuePlan()
    fenetre.show()
    sys.exit(app.exec())

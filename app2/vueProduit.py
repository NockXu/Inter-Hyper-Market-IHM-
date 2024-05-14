import sys
from vueApplication import *
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMainWindow, QToolBar, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction, QPixmap, QGuiApplication, QFont

##########################################################
#                                                        #
#                    Classe vueProduit                   #
#                                                        #
##########################################################
class VueProduit():
    def __init__(self):
        self.filtre_label = QLabel("Filtre")
        self.filtre1 = QComboBox()
        self.filtre1.addItem("Type de produit")
        self.filtre1.addItem("Option 2")
        self.filtre2 = QComboBox()
        self.filtre2.addItem("Rayon")
        self.filtre2.addItem("Option B")

def vue_produit(layout_principal):
    vue_produit = VueProduit()
    filtre1_layout = QVBoxLayout()
    layout_principal.addLayout(filtre1_layout)
    filtre2_layout = QHBoxLayout()
    layout_principal.addLayout(filtre2_layout)

    filtre1_layout.addWidget(vue_produit.filtre_label)
    filtre1_layout.addWidget(vue_produit.filtre1)
    filtre1_layout.addWidget(vue_produit.filtre2)
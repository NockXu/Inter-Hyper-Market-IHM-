from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class VueDockMenuCarre(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_dock = QVBoxLayout()

        self.carre_button : QPushButton = QPushButton('Carre')
        
        self.layout_dock.addWidget(self.carre_button)

        self.layout_dock.addStretch(1)
        self.setLayout(self.layout_dock)
        
    def get_load_plan_button(self):
        return self.load_plan_button
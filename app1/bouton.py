from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFormLayout, QApplication, QColorDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

class Bouton(QPushButton):

    # Signaux
    couleurChangee = pyqtSignal(QColor)
    
    def __init__(self, color : str):
            super().__init__()
            self.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
            self.clicked.connect(self.change_color)
            self.couleur = QColor(color)
        
    def change_color(self):
        color : QColor = QColorDialog.getColor()
        if color.isValid():
            self.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
            self.couleur = QColor(color)
            self.couleurChangee.emit(color)
            
    def get_color(self):
        return self.couleur
            
# Exemple d'utilisation
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = Bouton("red")
    print(widget.get_color())
    widget.show()
    sys.exit(app.exec())

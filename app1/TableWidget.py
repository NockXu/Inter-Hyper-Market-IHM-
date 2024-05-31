from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QColorDialog, QLineEdit, QPushButton
)
from PyQt6.QtGui import QColor, QIcon, QPalette
from PyQt6.QtCore import Qt, pyqtSignal
import sys

class TableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Signaux
    rayonAjoute = pyqtSignal(str, QColor)
    nomRayonChangee = pyqtSignal(str)
    rayonRetire = pyqtSignal()
    couleurRayonChangee = pyqtSignal(QColor)
    rayonSelectionee = pyqtSignal(QColor)
    
    def initUI(self):
        self.layout = QVBoxLayout()

        # Création du layout pour l'entrée de texte et le bouton
        self.top_layout = QHBoxLayout()
        
        # Création du QLineEdit pour entrer le nom du rayon
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("Entrez le nom du rayon")
        
        # Création du QPushButton pour ajouter le rayon
        self.add_button = QPushButton("Ajouter Rayon", self)
        self.add_button.clicked.connect(self.add_row_from_input)

        # Ajout des widgets au layout supérieur
        self.top_layout.addWidget(self.name_edit)
        self.top_layout.addWidget(self.add_button)
        
        # Ajout du layout supérieur au layout principal
        self.layout.addLayout(self.top_layout)

        # Créer le tableau
        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Nom", "Couleur", ""])
        self.table.itemClicked.connect(self.change_color)

        # Définir la largeur de la troisième colonne
        self.table.setColumnWidth(2, 39)

        # Ajouter le tableau au layout principal
        self.layout.addWidget(self.table)
        
        self.setLayout(self.layout)
        self.setWindowTitle('Tableau avec Actions')
        
        self.table.cellClicked.connect(self.get_color)

    def add_row_from_input(self):
        name = self.name_edit.text()
        if name:
            self.add_row(name)
            self.nomRayonChangee.emit(name)
            self.name_edit.clear()
        

    def add_row(self, name):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        # Nom
        name_item = QTableWidgetItem(name)
        self.table.setItem(row_position, 0, name_item)

        # Couleur
        color_item = QTableWidgetItem()
        color_item.setBackground(QColorDialog.getColor())
        color_item.setFlags(color_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Rendre la cellule non éditable
        self.table.setItem(row_position, 1, color_item)

        # Action - Supprimer
        remove_icon = QIcon("app1/images/sup.svg")
        remove_label = QLabel()
        remove_label.setPixmap(remove_icon.pixmap(16, 16))
        remove_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        remove_label.mousePressEvent = lambda event, row=row_position: self.remove_row(row)
        remove_label.enterEvent = lambda event: self.hover_enter(remove_label)
        remove_label.leaveEvent = lambda event: self.hover_leave(remove_label)
        self.table.setCellWidget(row_position, 2, remove_label)
        
        # Envoie du signal
        self.rayonAjoute.emit(name, self.table.item(row_position, 1).background().color())



    def remove_row(self, row):
        self.table.removeRow(row)
        
        # Réaffecter les indices des lignes dans la première colonne
        for i in range(self.table.rowCount()):
            remove_label = self.table.cellWidget(i, 2)
            remove_label.mousePressEvent = lambda event, row=i: self.remove_row(row)
        
        self.rayonRetire.emit()


    def change_color(self, item):
        column = item.column()
        if column == 1:  # Vérifier si la colonne est la colonne de couleur
            color_item = self.table.item(item.row(), column)
            color = QColorDialog.getColor(color_item.background().color())
            if color.isValid():
                color_item.setBackground(color)
        
                self.couleurRayonChangee.emit(color_item.background().color())

    def hover_enter(self, label):
        label.setStyleSheet("background-color: green;")

    def hover_leave(self, label):
        label.setStyleSheet("")


    def get_data(self):
        data = []
        for row in range(self.table.rowCount()):
            name = self.table.item(row, 0).text()
            color = self.table.item(row, 1).background().color().name()
            data.append((name, color))
        return data
    
    def get_color(self, row : int, column : int) -> QColor:
        print(self.table.item(row, 1).background().color())
        return self.table.item(row, 1).background().color()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = TableWidget()
    
    # Ajouter des lignes de démonstration
    widget.add_row('Alice')
    widget.add_row('Bob')
    widget.add_row('Charlie')
    
    widget.show()
    print(widget.get_data())
    sys.exit(app.exec())

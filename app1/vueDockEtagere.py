import sys
from PyQt6.QtWidgets import QGridLayout, QWidget, QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal
import imageDeplacement

class VueEtagere(QWidget):
    # Define a signal that will carry the shelf name
    etagereSelectionnee = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        
        # Tableau des étagères à gauche
        self.table_etageres = QTableWidget(0, 1)  # 0 lignes et 1 colonne
        self.table_etageres.setHorizontalHeaderLabels(["Nom"])
        self.table_etageres.cellClicked.connect(self.afficher_produits_etagere)
        self.layout.addWidget(self.table_etageres, 0, 0)
        
        # Tableau des produits de l'étagère sélectionnée à droite
        self.table_produits = QTableWidget(0, 1)  # 0 lignes et 1 colonne
        self.table_produits.setHorizontalHeaderLabels(["Produit"])
        self.layout.addWidget(self.table_produits, 0, 1)
        
        self.setLayout(self.layout)

        self.etageres = {}
        
    def afficher_etageres(self, etageres: list[dict]):
        self.table_etageres.setRowCount(0)  
        for etagere in etageres:
            row_position = self.table_etageres.rowCount()
            self.table_etageres.insertRow(row_position)
            item_nom = QTableWidgetItem(etagere['nom'])
            self.table_etageres.setItem(row_position, 0, item_nom)
        
    def ajouterEtagere(self, etagere_info: tuple):
        position = (etagere_info[0], etagere_info[1])
        nom_etagere = f"{etagere_info[0]}_{etagere_info[1]}"
        
        if position in self.etageres:
            self.retirerEtagere(position)
        else:
            row_position = self.table_etageres.rowCount()
            self.table_etageres.insertRow(row_position)
            item_nom = QTableWidgetItem(nom_etagere)
            self.table_etageres.setItem(row_position, 0, item_nom)
            self.etageres[position] = row_position
        
    def retirerEtagere(self, position: tuple):
        if position in self.etageres:
            row_position = self.etageres.pop(position)
            self.table_etageres.removeRow(row_position)
    
    def afficher_produits_etagere(self, row, column):
        if column != 0:
            return
        self.table_produits.setRowCount(0)  # Clear the table
        nom_etagere = self.table_etageres.item(row, 0).text()
        produits = self.get_produits_etagere(nom_etagere)
        for produit in produits:
            row_position = self.table_produits.rowCount()
            self.table_produits.insertRow(row_position)
            item = QTableWidgetItem(produit['nom'])
            self.table_produits.setItem(row_position, 0, item)
            
    def get_produits_etagere(self, nom_etagere: str) -> list:
        # Exemple de données pour l'étagère
        if nom_etagere == 'Etagere_1_0':
            return [{'nom': 'Produit A'}, {'nom': 'Produit B'}]
        elif nom_etagere == 'Etagere_2_1':
            return [{'nom': 'Produit C'}, {'nom': 'Produit D'}]
        return []

# Exemple d'utilisation
if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue = VueEtagere()
    etageres = [{'nom': 'Etagere_1_0'}, {'nom': 'Etagere_2_1'}]
    vue.afficher_etageres(etageres)
    
    # Connecter le signal etagereAjoutee à la méthode ajouterEtagere
    image_label = imageDeplacement.ImageDeplacement()
    image_label.etagereAjoutee.connect(vue.ajouterEtagere)
    
    vue.show()
    sys.exit(app.exec())

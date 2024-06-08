import sys
from PyQt6.QtWidgets import QGridLayout, QWidget, QApplication, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import pyqtSignal

class VueEtagere(QWidget):
    # Définir un signal qui portera le nom de l'étagère
    etagereSelectionnee = pyqtSignal(str)
    etagereAjoutee = pyqtSignal(str)
    etagereSupprimee = pyqtSignal(str)
    produitAjouteAvecEtagere = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        
        self.table_etageres = QTableWidget(0, 1)
        self.table_etageres.setHorizontalHeaderLabels(["Nom"])
        self.table_etageres.cellClicked.connect(self.afficher_produits_etagere)
        self.layout.addWidget(self.table_etageres, 0, 0)
        
        self.table_produits = QTableWidget(0, 1)
        self.table_produits.setHorizontalHeaderLabels(["Produit"])
        self.layout.addWidget(self.table_produits, 0, 1)
        
        self.setLayout(self.layout)

        self.etageres = {}
        
    def afficher_etageres(self, etageres):
        self.table_etageres.setRowCount(0)
        for etagere in etageres:
            row_position = self.table_etageres.rowCount()
            self.table_etageres.insertRow(row_position)
            item_nom = QTableWidgetItem(etagere)
            self.table_etageres.setItem(row_position, 0, item_nom)

    def ajouterEtagere(self, etagere_info):
        nom_etagere = f"Etagere_{etagere_info[0]}_{etagere_info[1]}"
        if nom_etagere not in self.etageres:
            row_position = self.table_etageres.rowCount()
            self.table_etageres.insertRow(row_position)
            item_nom = QTableWidgetItem(nom_etagere)
            self.table_etageres.setItem(row_position, 0, item_nom)
            self.etageres[nom_etagere] = []
            self.etagereAjoutee.emit(nom_etagere)
        else:
            self.supprimerEtagere(etagere_info)

    def supprimerEtagere(self, etagere_info):
        nom_etagere = f"Etagere_{etagere_info[0]}_{etagere_info[1]}"
        for i in range(self.table_etageres.rowCount()):
            item = self.table_etageres.item(i, 0)
            if item.text() == nom_etagere:
                self.table_etageres.removeRow(i)
                break
        if nom_etagere in self.etageres:
            del self.etageres[nom_etagere]
            self.etagereSupprimee.emit(nom_etagere)

    def ajouterProduitAEtagere(self, produit, etagere):
        if self.table_etageres.currentRow() >= 0:
            if etagere in self.etageres:
                self.etageres[etagere].append(produit)
                self.afficher_produits_etagere(self.table_etageres.currentRow(), 0)
                # Émettre le signal pour ajouter le produit à l'étagère
                self.produitAjouteAvecEtagere.emit(produit, etagere)


    def afficher_produits_etagere(self, row, column):
        if row >= 0:  # Vérifier si la rangée est valide
            etagere_nom = self.table_etageres.item(row, 0).text()
            produits = self.etageres.get(etagere_nom, [])

            self.table_produits.setRowCount(0)
            for produit in produits:
                row_position = self.table_produits.rowCount()
                self.table_produits.insertRow(row_position)
                item_produit = QTableWidgetItem(produit)
                self.table_produits.setItem(row_position, 0, item_produit)


    def get_produits_etagere(self, nom_etagere: str) -> list:
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
    import imageDeplacement  # Importation ajoutée pour l'exemple
    image_label = imageDeplacement.ImageDeplacement()
    image_label.etagereAjoutee.connect(vue.ajouterEtagere)
    
    vue.show()
    sys.exit(app.exec())
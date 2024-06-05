import sys
from PyQt6.QtWidgets import QGridLayout, QHBoxLayout, QWidget, QApplication, QListWidgetItem, QListWidget
from PyQt6.QtGui import QColor

class VueEtagere(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        
        # Liste des étagères à gauche
        self.liste_etageres = QListWidget()
        self.liste_etageres.itemClicked.connect(self.afficher_produits_etagere)
        self.layout.addWidget(self.liste_etageres, 0, 0)
        
        # Liste des produits de l'étagère sélectionnée à droite
        self.liste_produits = QListWidget()
        self.layout.addWidget(self.liste_produits, 0, 1)
        
        self.setLayout(self.layout)
        
    def afficher_etageres(self, etageres: list[dict]):
        self.liste_etageres.clear()
        for etagere in etageres:
            item = QListWidgetItem(etagere['nom'])
            item.setBackground(etagere['couleur'])
            self.liste_etageres.addItem(item)
        
    def afficher_produits_etagere(self, item):
        self.liste_produits.clear()
        # Récupérer les produits de l'étagère associée à l'élément sélectionné
        produits = self.get_produits_etagere(item.text())
        for produit in produits:
            item = QListWidgetItem(produit['nom'])
            self.liste_produits.addItem(item)
            
    def get_produits_etagere(self, nom_etagere: str) -> list:
        return []
        
# Exemple d'utilisation
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    vue = VueEtagere()
    etageres = [{'nom': 'Etagere 1', 'couleur': QColor('red')}, {'nom': 'Etagere 2', 'couleur': QColor('blue')}]
    vue.afficher_etageres(etageres)
    vue.show()
    sys.exit(app.exec())
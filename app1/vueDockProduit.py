from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import sys

class VueDockProduit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Charger les produits depuis un fichier texte
        self.categories = self.charger_produits("app1/produits.txt")

        # Configuration de la mise en page
        self.layout = QVBoxLayout()
        
        # Création des widgets
        self.category_combo_box = QComboBox()
        self.product_list_widget = QListWidget()

        # Ajouter les catégories à la liste déroulante
        self.category_combo_box.addItems(self.categories.keys())
        
        # Ajouter les widgets à la mise en page
        self.layout.addWidget(QLabel("Catégories"))
        self.layout.addWidget(self.category_combo_box)
        self.layout.addWidget(QLabel("Produits"))
        self.layout.addWidget(self.product_list_widget)
        
        self.setLayout(self.layout)
        
        # Connecter les signaux
        self.category_combo_box.currentIndexChanged.connect(self.afficher_produits)
        self.product_list_widget.itemDoubleClicked.connect(self.ajouter_produit_au_rayon)
        
        # Afficher les produits de la première catégorie par défaut
        self.afficher_produits()

    def charger_produits(self, file_path):
        """
        Charge les produits depuis un fichier texte et les organise par catégories.
        """
        categories = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                category, product = line.split(";")
                if category not in categories:
                    categories[category] = []
                categories[category].append(product)
        return categories

    def afficher_produits(self):
        """
        Affiche les produits de la catégorie sélectionnée.
        """
        self.product_list_widget.clear()
        category = self.category_combo_box.currentText()
        products = self.categories.get(category, [])
        self.product_list_widget.addItems(products)

    def ajouter_produit_au_rayon(self, item):
        """
        Propose d'ajouter le produit sélectionné à un rayon.
        """
        product = item.text()
        category = self.category_combo_box.currentText()
        response = QMessageBox.question(self, "Ajouter produit", 
                                        f"Voulez-vous ajouter le produit '{product}' au rayon '{category}'?", 
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if response == QMessageBox.StandardButton.Yes:
            # Logique pour ajouter le produit au rayon
            print(f"Produit '{product}' ajouté au rayon '{category}'")
            # Vous pouvez implémenter ici la logique pour ajouter le produit au rayon


if __name__ == "__main__":
    app = QApplication(sys.argv)
    vue_produit = VueDockProduit()
    vue_produit.setWindowTitle("Gestion des Produits")
    vue_produit.resize(300, 400)
    vue_produit.show()
    sys.exit(app.exec())

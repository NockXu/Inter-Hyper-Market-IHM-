from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *
import sys

from TableWidget import TableWidget

class VueDockProduit(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.categories = self.charger_produits("app1/produits.txt")

        self.layout = QVBoxLayout()

        self.category_combo_box = QComboBox()
        self.product_list_widget = QListWidget()
        self.etagere_combo_box = QComboBox()
        self.search_line_edit = QLineEdit()

        self.etagere_label = QLabel("Etageres")
        
        

        self.category_combo_box.addItems(self.categories.keys())

        self.layout.addWidget(QLabel("Catégories"))
        self.layout.addWidget(self.category_combo_box)
        self.layout.addWidget(QLabel("Recherche de Produit"))
        self.layout.addWidget(self.search_line_edit)
        self.layout.addWidget(QLabel("Produits"))
        self.layout.addWidget(self.product_list_widget)
        self.layout.addWidget(self.etagere_label)
        self.layout.addWidget(self.etagere_combo_box)
        self.etagere_label.hide()
        self.etagere_combo_box.hide()

        self.setLayout(self.layout)

        self.category_combo_box.currentIndexChanged.connect(self.afficher_produits)
        self.search_line_edit.textChanged.connect(self.rechercher_produit)
        self.product_list_widget.itemDoubleClicked.connect(self.ajouter_produit_au_etagere)

        self.afficher_produits()
    
    produitAjoute = pyqtSignal(str, str)

    def charger_produits(self, file_path):
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
        self.product_list_widget.clear()
        category = self.category_combo_box.currentText()
        products = self.categories.get(category, [])
        self.product_list_widget.addItems(products)

    def ajouter_produit_au_etagere(self, item):
        product = item.text()
        if self.etagere_combo_box.count() == 0:
            QMessageBox.warning(self, "Aucune étagère trouvée", "Aucune étagère trouvée. Veuillez créer une nouvelle étagère d'abord.")
        else:
            etageres = [self.etagere_combo_box.itemText(i) for i in range(self.etagere_combo_box.count())]
            etagere, ok = QInputDialog.getItem(self, "Choisir une étagère", "Sélectionnez l'étagère pour ajouter le produit :", etageres, 0, False)
            if ok:
                self.produitAjoute.emit(product, etagere)

    def mettre_a_jour_liste_rayons(self, nom_etagere: tuple):
        if isinstance(nom_etagere, tuple):
            nom_etagere = " ".join(map(str, nom_etagere))  # Concatène les éléments du tuple en une seule chaîne
        if nom_etagere not in [self.etagere_combo_box.itemText(i) for i in range(self.etagere_combo_box.count())]:
            self.etagere_combo_box.addItem(nom_etagere)

    def supprimer_etagere_selectionnee(self, index):
        if index != -1:
            self.etagere_combo_box.removeItem(index)

    def retirer_etagere(self, nom_etagere):
        # Supprimer l'étagère du QComboBox
        index = self.etagere_combo_box.findText(nom_etagere)
        if index != -1:
            self.etagere_combo_box.removeItem(index)

    def rechercher_produit(self):
        self.product_list_widget.clear()
        category = self.category_combo_box.currentText()
        products = self.categories.get(category, [])
        search_text = self.search_line_edit.text().lower()
        filtered_products = [product for product in products if search_text in product.lower()]
        self.product_list_widget.addItems(filtered_products)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer le TableWidget et VueDockProduit
    table_widget = TableWidget()
    vue_produit = VueDockProduit(table_widget)

    main_window = QMainWindow()
    main_window.setWindowTitle("Gestion des Produits")

    # Ajouter le vue_produit à la fenêtre principale
    main_window.setCentralWidget(vue_produit)
    main_window.resize(300, 400)
    main_window.show()

    sys.exit(app.exec())
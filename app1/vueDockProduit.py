from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import *
import sys

from TableWidget import TableWidget

class VueDockProduit(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        
        # Enregistrer la référence au TableWidget
        self.table_widget = table_widget
        
        # Charger les produits depuis un fichier texte
        self.categories = self.charger_produits("app1/produits.txt")

        # Configuration de la mise en page
        self.layout = QVBoxLayout()
        
        # Création des widgets
        self.category_combo_box = QComboBox()
        self.product_list_widget = QListWidget()
        self.rayon_combo_box = QComboBox()
        self.search_line_edit = QLineEdit()

        # Ajouter les catégories à la liste déroulante
        self.category_combo_box.addItems(self.categories.keys())
        
        # Ajouter les widgets à la mise en page
        self.layout.addWidget(QLabel("Catégories"))
        self.layout.addWidget(self.category_combo_box)
        self.layout.addWidget(QLabel("Recherche de Produit"))
        self.layout.addWidget(self.search_line_edit)
        self.layout.addWidget(QLabel("Produits"))
        self.layout.addWidget(self.product_list_widget)
        self.layout.addWidget(QLabel("Rayons"))
        self.layout.addWidget(self.rayon_combo_box)
        
        self.setLayout(self.layout)
        
        # Connecter les signaux
        self.category_combo_box.currentIndexChanged.connect(self.afficher_produits)
        self.search_line_edit.textChanged.connect(self.rechercher_produit)
        self.product_list_widget.itemDoubleClicked.connect(self.ajouter_produit_au_rayon)
        
        # Connecter les signaux de table_widget pour mettre à jour les rayons
        self.table_widget.rayonAjoute.connect(self.mettre_a_jour_liste_rayons)
        self.table_widget.rayonRetire.connect(self.enlever_rayon)
        
        # Afficher les produits de la première catégorie par défaut
        self.afficher_produits()
        
        # Initialiser la liste des rayons
        self.mettre_a_jour_tous_les_rayons()

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

        # Vérifier si des rayons existent déjà
        if self.rayon_combo_box.count() == 0:
            response = QMessageBox.question(self, "Aucun rayon trouvé", 
                                            "Aucun rayon trouvé. Voulez-vous créer un nouveau rayon ?", 
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if response == QMessageBox.StandardButton.Yes:
                self.table_widget.add_row_from_dialog()
        else:
            # Ajouter une option pour créer un nouveau rayon
            rayons = [self.rayon_combo_box.itemText(i) for i in range(self.rayon_combo_box.count())]
            rayons.append("Créer un nouveau rayon")

            rayon, ok = QInputDialog.getItem(self, "Choisir un rayon", 
                                             "Sélectionnez le rayon pour ajouter le produit :", rayons, 0, False)
            if ok:
                if rayon == "Créer un nouveau rayon":
                    self.table_widget.add_row_from_dialog()
                else:
                    print(f"Produit '{product}' ajouté au rayon '{rayon}'")

    def mettre_a_jour_liste_rayons(self, nom_rayon, couleur_rayon):
        """
        Met à jour la liste des rayons dans le QComboBox.
        """
        self.rayon_combo_box.addItem(nom_rayon)

    def enlever_rayon(self, nom_rayon, couleur_rayon):
        """
        Retire un rayon de la liste des rayons dans le QComboBox.
        """
        index = self.rayon_combo_box.findText(nom_rayon)
        if index != -1:
            self.rayon_combo_box.removeItem(index)
    
    def mettre_a_jour_tous_les_rayons(self):
        """
        Met à jour la liste des rayons en utilisant les données actuelles de table_widget.
        """
        self.rayon_combo_box.clear()
        rayons = self.table_widget.get_data()
        for rayon in rayons:
            self.rayon_combo_box.addItem(rayon[0])

    def rechercher_produit(self):
        """
        Filtre et affiche les produits qui correspondent au texte de recherche saisi.
        """
        # Efface la liste actuelle des produits affichés
        self.product_list_widget.clear()

        category = self.category_combo_box.currentText()
        products = self.categories.get(category, [])

        # Récupère le texte de recherche et le convertit en minuscules pour une comparaison insensible à la casse
        search_text = self.search_line_edit.text().lower()
        
        # Initialise une liste pour stocker les produits filtrés
        filtered_products = []
        
        # Parcourt tous les produits et ajoute ceux qui contiennent le texte de recherche à la liste filtrée
        for product in products:
            if search_text in product.lower():
                filtered_products.append(product)
        
        # Affiche les produits filtrés dans le widget de la liste des produits
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
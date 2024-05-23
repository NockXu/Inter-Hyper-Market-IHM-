import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.produit import Produit
from Classes.fonction import Fonction

class Etagere(Fonction):
    def __init__(self, liste_produit : list[Produit] = []) -> None:
        super().__init__("étagère")
        self._produits: list[Produit] = liste_produit
    
    def vider(self) -> None:
        """Vide l'étagère en supprimant tous les produits."""
        self._produits = []
    
    def ajouter(self, ajout: Produit) -> None:
        """Ajoute un produit à l'étagère."""
        self._produits.append(ajout)
    
    def retirer(self, suppression: Produit) -> None:
        """Retire un produit de l'étagère."""
        if suppression in self._produits:
            self._produits.remove(suppression)
    
    def get_produits(self) -> list[Produit]:
        """Retourne la liste des produits sur l'étagère."""
        return self._produits
    
    def set_produits(self, produits: list[Produit]) -> None:
        """Définit la liste des produits sur l'étagère."""
        self._produits = produits
    
    # Méthode spéciale __str__()
    def __str__(self) -> str:
        """Retourne une représentation sous forme de chaîne de l'étagère avec les noms des produits."""
        produits_str = ""
        for produit in self._produits:
            produits_str += "{"+str(produit)+"}, "
        
        # Enlever la dernière virgule et l'espace
        if produits_str.endswith(", "):
            produits_str = produits_str[:-2]
        
        if produits_str == "":
            produits_str = "vide"

        return f"[Etagere : [Produits: {produits_str}, Accessibilité : {self._acces}]"
    
    # Méthode spéciale __eq__()
    def __eq__(self, other : object) -> bool:
        """Vérifie l'égalité de deux étagères en comparant les listes de produits."""
        if isinstance(other, Etagere):
            return self._produits == other._produits
        return False

if __name__ == "__main__":
        # Création de quelques produits
    produit1 = Produit("Livre", 15.99, "Un livre intéressant", "livre.png", "livre")
    produit2 = Produit("Ordinateur portable", 999.99, "Puissant et léger", "ordi.png", "électronique")
    produit3 = Produit("Montre", 79.99, "Montre élégante", "montre.png", "élecrtonique")
    
    # Création d'une étagère
    etagere = Etagere()
    
    # Ajout des produits à l'étagère
    etagere.ajouter(produit1)
    etagere.ajouter(produit2)
    etagere.ajouter(produit3)
    
    # Affichage des produits sur l'étagère
    print("Produits sur l'étagère:")
    print(etagere)
    
    # Comparaison d'étagères
    etagere2 = Etagere()
    etagere2.ajouter(produit1)
    etagere2.ajouter(produit2)
    etagere2.ajouter(produit3)
    
    print("\nComparaison d'étagères:")
    print("Etagere == Etagere2 ?", etagere == etagere2)
    
    # Retrait d'un produit
    print("\nRetrait du produit 'Montre'...")
    montre = Produit("Montre", 79.99, "Montre élégante", "montre.png", "électronique")  # Nouvelle instance pour comparer
    etagere.retirer(montre)
    
    # Affichage mis à jour des produits sur l'étagère
    print("\nProduits sur l'étagère après retrait:")
    print(etagere)
    
    # Vidage de l'étagère
    etagere.vider()
    print("\nEtagère vidée. Produits restants:")
    print(etagere)
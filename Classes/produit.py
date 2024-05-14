class Produit:
    def __init__(self, nom: str, prix: float, description: str, icone: str, type: str) -> None:
        self._nom = nom
        self._prix = prix
        self._description = description
        self._icone = icone
        self._type = type

    # Méthodes getters
    def get_nom(self) -> str:
        return self._nom
    
    def get_prix(self) -> float:
        return self._prix
    
    def get_description(self) -> str:
        return self._description
    
    def get_icone(self) -> str:
        return self._icone

    def get_type(self) -> str:
        return self._type
    
    # Méthodes setters
    def set_nom(self, nom: str) -> None:
        self._nom = nom
    
    def set_prix(self, prix: float) -> None:
        self._prix = prix
    
    def set_description(self, description: str) -> None:
        self._description = description
    
    def set_icone(self, icone: str) -> None:
        self._icone = icone
    
    def set_type(self, type : str) -> None:
        self._type = type

    # Méthode spéciale __str__()
    def __str__(self) -> str:
        return f"Produit : {self._nom}\nPrix : {self._prix} €\nDescription : {self._description}\nIcône : {self._icone}"

    # Méthode spéciale __eq__()
    def __eq__(self, other) -> bool:
        if isinstance(other, Produit):
            return (self._nom == other._nom) and (self._prix == other._prix) and \
                   (self._description == other._description) and (self._icone == other._icone) and \
                   (self._type == other._type)
        return False
    
if __name__ == "__main__":
    # Tester la classe Produit
    produit1 = Produit("Ordinateur Portable", 1200.0, "Ordinateur portable puissant et léger.", "icone_ordinateur.png", "électronique")
    produit2 = Produit("Souris sans Fil", 29.99, "Souris ergonomique avec connectivité sans fil.", "icone_souris.png", "électronique")

    print("Produit 1:")
    print(produit1)
    print("\nProduit 2:")
    print(produit2)

    print("\nComparaison des produits:")
    print("produit1 == produit2 :", produit1 == produit2)
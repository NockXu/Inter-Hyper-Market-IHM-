import sys, os

class Produit:
    def __init__(self, nom: str, prix: float, description: str, icone: str, nomType: str) -> None:
        self._nom = nom
        self._prix = prix
        self._description = description
        self._icone = icone
        self._type = nomType

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
    
    def set_type(self, nomType : str) -> None:
        self._type = nomType

    # Méthode spéciale __str__()
    def __str__(self) -> str:
        return f"Nom : '{self._nom}', Prix : '{self._prix}€', Description : '{self._description}', Icône : '{self._icone}'"

    # Méthode spéciale __eq__()
    def __eq__(self, other) -> bool:
        if isinstance(other, Produit):
            return (self._nom == other._nom) and (self._prix == other._prix) and \
                   (self._description == other._description) and (self._icone == other._icone) and \
                   (self._type == other._type)
        return False

def liste_produit(chemin : str) -> dict:
    produits : dict = {}
    est_type : bool = False
    texte : str = ""
    type_actuel : str = ""
    
    ##################################################################
    # Ouverture du fichier                                           #
    ##################################################################
    # Récupérer le chemin du répertoire parent
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    
    try:
        # Ouvre le fichier en mode lecture
        with open(os.path.join(parent_dir, chemin), 'r') as fichier:
            # Lit tout le contenu du fichier
            contenu = fichier.read()

    except FileNotFoundError:
        print(f"Erreur : le fichier '{chemin}' n'a pas été trouvé.")

    except Exception as e:
        print(f"Erreur lors de la lecture du fichier : {e}")
    ##################################################################
    
    for caractere in contenu:
        if caractere == "[":
            est_type = True
            type_actuel = ""
        elif caractere == "]":
            est_type = False
            if type_actuel:
                if type_actuel not in produits:
                    produits[type_actuel] = []
        else:
            if est_type:
                type_actuel += caractere
            else:
                if caractere != "\n":
                    texte += caractere
                else:
                    if type_actuel and texte != "":
                        produits[type_actuel].append(texte.strip())
                    texte = ""

                
    return produits

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
    
    print(liste_produit("liste_produits.txt"))
    
    
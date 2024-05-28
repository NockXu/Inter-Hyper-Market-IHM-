import os, sys
from PyQt6.QtGui import QColor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class Rayon:
    """_summary_ 
    Cette classe permet de créer un rayon et permet d'attribuer la couleur et le nom d'un rayon sur un point.
    """
    def __init__(self, nom: str = None, couleur: QColor = None) -> None:
        """
        Initialise une nouvelle instance de la classe Rayon.
        
        :param nom: Le nom du rayon, par défaut None.
        :param couleur: La couleur associée au rayon, par défaut None.
        """
        self._nom = nom
        self._couleur = couleur
    
    def getNom(self) -> str:
        """
        Retourne le nom du rayon.
        
        :return: Le nom du rayon.
        """
        return self._nom
    
    def getCouleur(self) -> QColor:
        """
        Retourne la couleur du rayon.
        
        :return: La couleur du rayon.
        """
        return self._couleur
    
    def setNom(self, nom: str) -> None:
        """
        Définit le nom du rayon.
        
        :param nom: Le nouveau nom du rayon.
        """
        self._nom = nom
    
    def setCouleur(self, couleur: QColor) -> None:
        """
        Définit la couleur du rayon.
        
        :param couleur: La nouvelle couleur du rayon.
        """
        self._couleur = couleur

    def __str__(self) -> str:
        """
        Retourne une représentation sous forme de chaîne de caractères de l'objet Rayon.
        
        :return: Une chaîne de caractères représentant l'objet Rayon.
        """
        couleur_name = self._couleur.name() if self._couleur else "None"
        return f"nom : {self._nom}, couleur : {couleur_name}"
    
    def __eq__(self, other: object) -> bool:
        """
        Compare deux objets Rayon pour vérifier leur égalité.
        
        :param other: L'autre objet à comparer.
        :return: True si les deux objets sont égaux, sinon False.
        """
        if not isinstance(other, Rayon):
            return False
        return self._nom == other._nom and self._couleur == other._couleur

if __name__ == "__main__":
    # Création de quelques instances de Rayon
    rayon1 = Rayon("Fruits", QColor("red"))
    rayon2 = Rayon("Légumes", QColor("green"))
    rayon3 = Rayon("Fruits", QColor("red"))
    rayon4 = Rayon("Produits Laitiers", QColor("blue"))
    rayon5 = Rayon("Légumes", QColor("green"))
    
    # Affichage des rayons
    print(rayon1)
    print(rayon2)
    print(rayon3)
    print(rayon4)
    print(rayon5)
    
    # Comparaison des rayons
    print("rayon1 est égal à rayon2:", rayon1 == rayon2)
    print("rayon1 est égal à rayon3:", rayon1 == rayon3)
    print("rayon2 est égal à rayon5:", rayon2 == rayon5)
    print("rayon3 est égal à rayon4:", rayon3 == rayon4)
    
    # Modification d'un rayon
    rayon4.setNom("Produits Laitiers Bio")
    rayon4.setCouleur(QColor("cyan"))
    print("rayon4 modifié:", rayon4)

# Classe qui permet de créer des objet Point qui possède deux attributs x et y
# Cette classe contient aussi des méthodes qui permette de simplifier son interaction avec les autres points du plan
class Point:
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
    
    # méthode qui renvoie une liste de tout les voisin d'un point à partir d'une liste
    def voisin(self, liste : dict) -> list:
        liste_voisin : list = []
        
        # pour chaque point de la liste 
        for point in liste:
            
            # on récupère les coordonnées
            coordonnee : Point = point["coordonnees"]
            
            # Si les coordonnée récupérer sont voisine avec la coordonnée de base
            if coordonnee.x == self.x - 1 or coordonnee.x == self.x + 1 :
                if coordonnee.y == self.y - 1 or coordonnee.y == self.y - 1 :
                    
                    # on l'ajoute à la liste de voisin
                    liste_voisin.append(coordonnee)
        
        return liste_voisin
    
    def __str__(self) -> str:
        return ("(",self.x,',',self.y,")")
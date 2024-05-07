from point import Point
# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self.points : list = []
        
        for x in range(h):
            for y in range(l):
                # Création d'un dictionnaire 'neighbors' pour stocker les coordonnées des voisins de chaque point
                neighbors = {
                    Point(x - 1, y) if x > 0 else None,        # Voisin à gauche (dans l'axe x), si x > 0
                    Point(x + 1, y) if x < h - 1 else None,    # Voisin à droite (dans l'axe x), si x < h - 1
                    Point(x, y - 1) if y > 0 else None,        # Voisin en haut  (dans l'axe y), si y > 0
                    Point(x, y + 1) if y < l - 1 else None     # Voisin en bas   (dans l'axe y), si y < l - 1
                }

                # Création d'un dictionnaire 'point_info' pour représenter les informations d'un point
                point_info = {
                    "coordonnees": Point(x, y),
                    "produit": None,
                    "voisins": neighbors
                }

                # Ajout du dictionnaire 'point_info' à la liste 'self.points' de la classe Plan
                self.points.append(point_info)
    
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x : int, y : int) -> None:
        # on crée le point
        point_info = {
                    "coordonnees": Point(x, y),
                    "produit": None,
                    "voisins": Point(x, y).voisin(self.points)
                }
        
        # on ajoute ses voisins
        self.points.append(point_info)

                
                

if __name__ == "__main__" :
    test : Plan = Plan(2,2)
    for point in test.points:
        print(point)
    
    test.ajoutPoint(2, 3)
    for point in test.points:
        print(point)
    
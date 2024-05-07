# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self.points : list = []
        
        for x in range(h):
            for y in range(l):
                # Création d'un dictionnaire 'neighbors' pour stocker les coordonnées des voisins de chaque point
                neighbors = {
                    (x - 1, y) if x > 0 else None,        # Voisin à gauche (dans l'axe x), si x > 0
                    (x + 1, y) if x < h - 1 else None,    # Voisin à droite (dans l'axe x), si x < h - 1
                    (x, y - 1) if y > 0 else None,        # Voisin en haut  (dans l'axe y), si y > 0
                    (x, y + 1) if y < l - 1 else None     # Voisin en bas   (dans l'axe y), si y < l - 1
                }

                # Création d'un dictionnaire 'point_info' pour représenter les informations d'un point
                point_info = {
                    "coordonnees": (x, y),
                    "fonction": None,
                    "voisins": neighbors
                }

                # Ajout du dictionnaire 'point_info' à la liste 'self.points' de la classe Plan
                self.points.append(point_info)

                
                

if __name__ == "__main__" :
    test : Plan = Plan(1,1)
    for point in test.points:
        print(point)
    
from point import Point
from fonction import Fonction
from etagere import Etagere
from chemin import Chemin
from entree import Entree
import json
import os

# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self.plan : list[Point] = []
        
        # ajout des points dans la liste des points
        for x in range(h):
            for y in range(l):
                self.plan.append(Point(x, y))
        
        # Après la création des point on reparcour la liste pour ajouter les voisins de chaque point et inversement ajouter chaque point à ses voisins
        for i in range(len(self.plan)):
            self.plan[i].set_voisins(self.plan)
            
    # méthode mettant à jour la totalitée des voisins pour tout les points      
    def set_voisinage(self) -> None:
        for point in self.plan:
            point.set_voisins(self.plan)
            
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x : int, y : int) -> None:
        # on crée le point
        nouveauPoint : Point = Point(x, y)
        
        # on l'ajoute dans le plan
        self.plan.append(nouveauPoint)
        
        # on ajoute ses voisins et inversement on l'ajoute à ses voisins
        self.plan[-1].set_voisins(self.plan)
    
    # méthode qui permet d'ajouter un plan dans un autre  
    def ajoutPlan(self, plan : list) -> None :
        
        # pour chaque point dans plan
        for point in plan:
            
            # on ajoute le point dans le plan
            self.plan.append(point)
            
            # on met à jour les voisins
            self.plan[-1].set_voisins(self.plan)
    
    # méthode qui permet de supprimer un point du plan si il existe
    def suppPoint(self, suppression : Point) -> None :
        # Parcourir la liste de point pour supprimer le point correspondant à suppression
        for point in self.plan:
            if point == suppression:
                self.plan.remove(point)
    
    # méthode qui permet de supprimer les point d'un plan à partir d'une liste de point        
    def suppPlan(self, suppression : list) -> None :
        for point in suppression:
            self.suppPoint(point)
                
    def __str__(self) -> str:
        texte = "{\n"
        for point in self.plan:
            texte += str(point) + "\n"  # Concaténer chaque point converti en chaîne à texte
        
        return texte + "}"

    def __eq__(self, other):
        if isinstance(other, Plan):  # Vérifie si 'other' est une instance de la classe Plan
            # Comparaison des listes de points
            return self.plan == other.points
        return False

def ecrire_JSON(plan : Plan, nomFichier : str) -> None:
    data : dict = []
    voisins : list = []
    foction : dict = {}
    points : list = []

    # Création/Ouverture du fichier JSON
    file = open(nomFichier, 'w')
    
    # pour chaque point du plan
    for point in plan.plan:
        
        # on récupere son/ses voisin(s) sous la forme d'une liste de dictionnaire de deux coordonnées
        # si il est pas vide
        if point.get_voisins() != None:
            for voisin in point.get_voisins():
                voisins.append(
                    {
                        "x" : voisin[0],
                        "y" : voisin[1]
                    }
                            )
            
        # on fait un définision générale de sa fonction
        fonction : dict = {
                           "spécialitée" : point.get_fonction().getNom(),
                           "acces" : [
                                      point.getHaut(), 
                                      point.getBas(), 
                                      point.getGauche(), 
                                      point.getDroite()
                                     ]
                          }
        # on ajoute à la fonction ses infos spécialisées
        
        if fonction["spécialitée"] == "étagère":
            # on crée la noyuvelle clé
            fonction["produits"] = []
            
            # on récupere les info de l'etagere
            etagere : Etagere = point.get_fonction()
            
             # pour chaque produit dans la liste de produits de l'étagère
            for produit in etagere.get_produits():
                
                # on ajoute le produit dans la liste de produits
                fonction["produits"].append(
                    {
                    "nom" : produit.get_nom,
                    "prix" : produit.get_prix,
                    "description" : produit.get_description,
                    "icone" : produit.get_icone
                    }
                                           )
            
        elif fonction["spécialitée"] == "entrée":
            # on récupere les info de l'entree
            entree : Entree = point.get_fonction()
            
            # on l'ajoute
            fonction["nomEntree"] = entree.getNomEntree()
            
        # on met le tout dans un dictionnaire qui regroupe toute les infos du point
        data = {
                    "x" : point.get_x(), 
                    "y" : point.get_y(),
                    "voisins" : voisins,
                    "fonction" : fonction
               }
        
        # Ajout du point à la liste des points
        points.append(data)
        
    # Récupérer le chemin du répertoire contenant votre script Python
    chemin = os.path.dirname(__file__)

    # Remonter d'un dossier pour obtenir le chemin du dossier parent
    chemin = os.path.dirname(chemin)
    
    # Aller dans le dossier Magasin
    chemin = os.path.join(chemin,"Magasin")
    
    # Ajouter le nom du fichier
    chemin = os.path.join(chemin, nomFichier)

    # Écriture des données dans le fichier JSON
    with open(chemin, 'w', encoding='utf-8') as file:
        json.dump(points, file, indent=4, ensure_ascii=False)
        
        

if __name__ == "__main__":
    test = Plan(10, 10)

    print(test)  # Affichage des points initiaux

    test.ajoutPoint(11, 10)

    print("\n",test)  # Affichage après ajout du nouveau point
    
    # création d'un fichier json
    ecrire_JSON(test, "test1.json")
    
    # Vérifier si le fichier a été créé
    if os.path.exists("test1.json"):
        print("Le fichier a été créé avec succès.")
    else:
        print("Le fichier n'a pas été créé.")
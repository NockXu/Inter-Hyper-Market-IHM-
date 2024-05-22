from PyQt6.QtCore import QPointF
import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes import *


# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self._plan : list[Point] = []
        self._fichier : str = "MonPlan"
        
        # ajout des points dans la liste des points
        for x in range(h):
            for y in range(l):
                self._plan.append(Point(x, y))
        
        # Après la création des point on reparcour la liste pour ajouter les voisins de chaque point et inversement ajouter chaque point à ses voisins
        for i in range(len(self._plan)):
            self._plan[i].set_voisins(self._plan)
            
    # méthode mettant à jour la totalitée des voisins pour tout les points      
    def set_voisinage(self) -> None:
        for point in self._plan:
            point.set_voisins(self._plan)
    
    # Méthodes setters
    def set_plan(self, plan : list) -> None:
        self._plan = plan
        
    def set_fichier(self, fichier : str) -> None:
        self._fichier = fichier
    
    # Méthodes getters    
    def get_plan(self) -> list:
        return self._plan
    
    def get_fichier(self) -> str:
        return self._fichier
            
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x : int, y : int) -> None:
        # on crée le point
        nouveauPoint : Point = Point(x, y)
        
        # on l'ajoute dans le plan
        self._plan.append(nouveauPoint)
        
        # on ajoute ses voisins et inversement on l'ajoute à ses voisins
        self._plan[-1].set_voisins(self._plan)
    
    # méthode qui permet d'ajouter un plan dans un autre  
    def ajoutPlan(self, plan : list) -> None :
        
        # pour chaque point dans plan
        for point in plan:
            
            # on ajoute le point dans le plan
            self._plan.append(point)
            
            # on met à jour les voisins
            self._plan[-1].set_voisins(self._plan)
    
    # méthode qui permet de supprimer un point du plan si il existe
    def suppPoint(self, x : int, y : int) -> None :
        # Parcourir la liste de point pour supprimer le point correspondant à suppression
        for point in self._plan:
            if point.get_x() == x and point.get_y() == y:
                self._plan.remove(point)
    
    # méthode qui permet de supprimer les point d'un plan à partir d'une liste de point        
    def suppPlan(self, suppression : list) -> None :
        for point in suppression:
            self.suppPoint(point)
            
    def lienQPlan(self, qPlan : list[QPointF]) -> None:
        for i in range(len(qPlan)):
            self._plan[i].setQPointF(qPlan[i])
                
    def __str__(self) -> str:
        texte = "{\n"
        for point in self._plan:
            texte += str(point) + "\n"  # Concaténer chaque point converti en chaîne à texte
        
        return texte + "}"

    def __eq__(self, other):
        if isinstance(other, Plan):  # Vérifie si 'other' est une instance de la classe Plan
            # Comparaison des listes de points
            return self._plan == other.get_plan() and self._fichier == other.get_fichier()
        return False

    def ecrire_JSON(self, nomFichier : str) -> None:
        data : dict = []
        voisins : list = []
        foction : dict = {}
        points : list = []

        # Création/Ouverture du fichier JSON
        file = open(nomFichier, 'w')
        
        # pour chaque point du plan
        for point in self._plan:
            
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
                        "nom" : produit.get_nom(),
                        "prix" : produit.get_prix(),
                        "description" : produit.get_description(),
                        "icone" : produit.get_icone(),
                        "type" : produit.get_type()
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
            data = []
            voisins = []
            fonction = []
            
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
            
    def lire_JSON(self, nomFichier: str) -> None:
        # Récupérer le chemin du répertoire contenant votre script Python
        chemin = os.path.dirname(__file__)

        # Remonter d'un dossier pour obtenir le chemin du dossier parent
        chemin = os.path.dirname(chemin)

        # Aller dans le dossier Magasin
        chemin = os.path.join(chemin, "Magasin")

        # Ajouter le nom du fichier
        chemin = os.path.join(chemin, nomFichier)

        # Lecture des données à partir du fichier JSON
        with open(chemin, 'r', encoding='utf-8') as file:
            points_data = json.load(file)

        # Liste pour stocker les nouveaux points
        self._plan = []

        # Dictionnaire pour stocker les points créés afin de référencer les voisins correctement
        points_dict = {}

        # Création de tous les points sans les voisins
        for point_data in points_data:
            x = point_data['x']
            y = point_data['y']
            fonction_data = point_data['fonction']
            specialite = fonction_data['spécialitée']

            # Création de la fonction du point
            if specialite == "étagère":
                produits = [
                    Produit(
                        p['nom'],
                        p['prix'],
                        p['description'],
                        p['icone'],
                        p['type']
                    ) for p in fonction_data['produits']
                ]
                fonction = Etagere(produits)
            elif specialite == "entrée":
                fonction = Entree(fonction_data['nomEntree'])
            else:
                fonction = Chemin()

            # Création du point sans les voisins pour l'instant
            point = Point(x, y, fonction=fonction)
            points_dict[(x, y)] = point
            self._plan.append(point)

        # Ajout des voisins pour chaque point
        for point_data in points_data:
            x = point_data['x']
            y = point_data['y']
            point = points_dict[(x, y)]
            voisins_data = point_data['voisins']
            voisins = []
            for voisin_data in voisins_data:
                voisin = points_dict.get((voisin_data['x'], voisin_data['y']))
                if voisin:
                    voisins.append(voisin)
            point.set_voisins(voisins)
        
        
        

if __name__ == "__main__":
    test = Plan(3, 3)

    print(test)  # Affichage des points initiaux

    test.ajoutPoint(3, 2)
    
    produitTest : Produit = Produit("truc",100,"un truc","le/chemin/vers/l'icone.png", "objet")
    test.get_plan()[0].set_fonction(Etagere([produitTest]))

    print("\n",test)  # Affichage après ajout du nouveau point
    
    test.suppPoint(3, 2)
    
    print("\n",test)  # Affichage après suppression
    
    # création d'un fichier json
    print("\n... écriture de test en fichier json ...")
    test.ecrire_JSON("test1.json")
    
    # Vérifier si le fichier a été créé
    if os.path.exists("test1.json"):
        print("Le fichier a été créé avec succès.")
    else:
        print("Le fichier n'a pas été créé.")
        
    test2 = Plan()
    test2.lire_JSON("test1.json")
    print("\nlecture de test1.json sur test2:\n",test2)
    print("test == test2 ?", test == test2)
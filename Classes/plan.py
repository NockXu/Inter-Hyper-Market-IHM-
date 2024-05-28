from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRectF

import json
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Classes.point import Point
from Classes.entree import Entree
from Classes.etagere import Etagere
from Classes.chemin import Chemin
from Classes.produit import Produit
from Classes.rayon import Rayon

# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9, nom  : str = "MonMagasin", auteur : str = "", date : str = "17/11/2005", adresse : str = "None of your business") -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self._plan : list[Point] = []
        self._fichier : str = nom + "_Info"
        self._nom : str = nom
        self._auteur : str = auteur
        self._date : str = date
        self._adresse : str = adresse
        
        # ajout des points dans la liste des points
        for x in range(h):
            for y in range(l):
                self._plan.append(Point(x, y))
        
        # Après la création des point on reparcour la liste pour ajouter les voisins de chaque point et inversement ajouter chaque point à ses voisins
        for i in range(len(self._plan)):
            self._plan[i].set_voisins(self._plan)
            
    # Méthodes setters
            
    # méthode mettant à jour la totalitée des voisins pour tout les points      
    def set_voisinage(self) -> None:
        for point in self._plan:
            point.set_voisins(self._plan)
    
    def set_plan(self, plan : list) -> None:
        self._plan = plan
        
    def set_fichier(self, fichier: str) -> None:
        self._fichier = fichier
    
    def set_nom(self, nom : str) -> None:
        self._nom = nom
        self._fichier = nom + "_Info"
    
    def set_auteur(self, auteur : str) -> None:
        self._auteur = auteur
    
    def set_date(self, date : str) -> None:
        self._date = date
    
    def set_adresse(self, adresse : str) -> None:
        self._adresse = adresse
    
    # Méthodes getters    
    def get_plan(self) -> list:
        return self._plan
    
    def get_fichier(self) -> str:
        return self._fichier
    
    def get_nom(self) -> str:
        return self._nom

    def get_auteur(self) -> str:
        return self._auteur
    
    def get_date(self) -> str:
        return self._date
    
    def get_adresse(self) -> str:
        return self._adresse
            
    # méthode qui permet d'ajouter un point dans le plan
    def ajoutPoint(self, x: int, y: int) -> None:
        # on crée le point
        nouveauPoint: Point = Point(x, y)
        
        # on l'ajoute dans le plan
        self._plan.append(nouveauPoint)
        
        # on ajoute ses voisins et inversement on l'ajoute à ses voisins
        self._plan[-1].set_voisins(self._plan)
    
    # méthode qui permet d'ajouter un plan dans un autre  
    def ajoutPlan(self, plan: list) -> None:
        
        # pour chaque point dans plan
        for point in plan:
            
            # on ajoute le point dans le plan
            self._plan.append(point)
            
            # on met à jour les voisins
            self._plan[-1].set_voisins(self._plan)
    
    # méthode qui permet de supprimer un point du plan si il existe
    def suppPoint(self, x: int, y: int) -> None:
        # Parcourir la liste de point pour supprimer le point correspondant à suppression
        for point in self._plan:
            if point.get_x() == x and point.get_y() == y:
                self._plan.remove(point)
    
    # méthode qui permet de supprimer les point d'un plan à partir d'une liste de point        
    def suppPlan(self, suppression: list) -> None:
        for point in suppression:
            self.suppPoint(point)
            
    def lienQPlan(self, qPlan : list[QRectF]) -> None:
        for i in range(len(qPlan)):
            self._plan[i].setQRectF(qPlan[i])
                
    def __str__(self) -> str:
        texte = "{\n"
        texte += self._nom + ",\n" + self._fichier + ",\n" + self._auteur + ",\n" + self._adresse + ",\n" + self._date + ",\n"
        
        for point in self._plan:
            texte += str(point) + "\n"  # Concaténer chaque point converti en chaîne à texte
        
        return texte + "}"

    def __eq__(self, other):
        if isinstance(other, Plan):  # Vérifie si 'other' est une instance de la classe Plan
            # Comparaison des listes de points
            return self._plan == other.get_plan() and self._fichier == other.get_fichier()
        return False

    def ecrire_JSON(self, nomFichier: str) -> None:
        data: dict = []
        voisins: list = []
        fonction: dict = {}
        points: list = []

        # Création/Ouverture du fichier JSON
        file = open(nomFichier, 'w')
        
        info_plan = {"info_plan" : {
            "nom" : self._nom,
            "auteur" : self._auteur,
            "adresse" : self._adresse,
            "date" : self._date
        }}
        points.append(info_plan)
        
        # pour chaque point du plan
        for point in self._plan:
            
            # on récupere son/ses voisin(s) sous la forme d'une liste de dictionnaire de deux coordonnées
            # si il est pas vide
            if point.get_voisins() is not None:
                for voisin in point.get_voisins():
                    voisins.append(
                        {
                            "x": voisin[0],
                            "y": voisin[1]
                        }
                    )
                
            # on fait une définition générale de sa fonction
            fonction: dict = {
                "spécialitée": point.get_fonction().getNom(),
                "acces": [
                    point.getHaut(), 
                    point.getBas(), 
                    point.getGauche(), 
                    point.getDroite()
                ]
            }
            # on ajoute à la fonction ses infos spécialisées
            
            if fonction["spécialitée"] == "étagère":
                # on crée la nouvelle clé
                fonction["produits"] = []
                
                # on récupere les info de l'etagere
                etagere: Etagere = point.get_fonction()
                
                # pour chaque produit dans la liste de produits de l'étagère
                for produit in etagere.get_produits():
                    
                    # on ajoute le produit dans la liste de produits
                    fonction["produits"].append(
                        {
                            "nom": produit.get_nom(),
                            "prix": produit.get_prix(),
                            "description": produit.get_description(),
                            "icone": produit.get_icone(),
                            "type": produit.get_type()
                        }
                    )
                
            elif fonction["spécialitée"] == "entrée":
                # on récupere les info de l'entree
                entree: Entree = point.get_fonction()
                
                # on l'ajoute
                fonction["nomEntree"] = entree.getNomEntree()
            
            # on récupère les données du rectangle
            rect = point.getQRectF()
            if rect is not None:
                width = rect.width()
                height = rect.height()
                left = rect.left()
                top = rect.top()
                
                rectangle = {
                            "top" : top,
                            "left" : left,
                            "width" : width,
                            "height" : height
                            }
            else:
                rectangle = "None"
                
            # on récupere le rayon
            ray = point.getRayon()
            
            # si il y a un rayon
            if ray is not None:
                rayon = {
                    "nom" : ray.getNom()
                }
                
                # on récupere la couleur (pas besoin de vérifier car lors de la création d'un rayon on sera obligé d'en mettre une)
                coul = ray.getCouleur()
                
                if coul is not None:
                    couleur = {
                        "rouge": coul.redF(),
                        "vert": coul.greenF(),
                        "bleu": coul.blueF(),
                        "alpha": coul.alphaF()
                    }
                    rayon["couleur"] = couleur      
                
            # on met le tout dans un dictionnaire qui regroupe toutes les infos du point
            data = {
                        "x" : point.get_x(), 
                        "y" : point.get_y(),
                        "voisins" : voisins,
                        "fonction" : fonction,
                        "rectangle" : rectangle,
                        "rayon" : rayon
                }
            
            # Ajout du point à la liste des points
            points.append(data)
            
            data = {}
            voisins = []
            fonction = {}
            rectangle = {}
            rayon = {}
            
        # Récupérer le chemin du répertoire contenant votre script Python
        chemin = os.path.dirname(__file__)

        # Remonter d'un dossier pour obtenir le chemin du dossier parent
        chemin = os.path.dirname(chemin)
        
        # Aller dans le dossier Magasin
        chemin = os.path.join(chemin, "Magasin")
        
        # Ajouter le nom du fichier au chemin
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
            info = json.load(file)
            
        # On supprime le plan
        self._plan = []

        # Dictionnaire pour stocker les points créés afin de référencer les voisins correctement
        points_dict = {}

        # Création de tous les points sans les voisins
        for point_data in info:
            if 'info_plan' in point_data:
                self.set_nom(point_data['info_plan']['nom'])
                self._auteur = point_data['info_plan']['auteur']
                self._adresse = point_data['info_plan']['adresse']
                self._date = point_data['info_plan']['date']
            
            else:
                x = point_data['x']
                y = point_data['y']
                
                # Création du rectangle du point
                rectangle = point_data['rectangle']
                if rectangle != "None":
                    left = rectangle['left']
                    top = rectangle['right']
                    width = rectangle['width']
                    height = rectangle['height']
                    rectangle = QRectF(left, top, width, height)
                    
                # Création du rayon du point
                if 'rayon' in point_data:
                    
                    rayon = point_data['rayon']
                    nom_rayon = rayon['nom']
                    
                    if 'couleur' in rayon:
                        
                        couleur_rayon = QColor(rayon['couleur']['rouge'],rayon['couleur']['vert'],rayon['couleur']['bleu'],rayon['couleur']['alpha'])
                        rayon = Rayon(nom_rayon, couleur_rayon)
                        
                    rayon = Rayon(nom_rayon)
                
                # Création de la fonction du point
                fonction_data = point_data['fonction']
                specialite = fonction_data['spécialitée']

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
                point = Point(x, y, fonction=fonction, qRectF=rectangle, rayon=rayon)
                points_dict[(x, y)] = point
                self._plan.append(point)

        # Ajout des voisins pour chaque point
        for point_data in info:
            if 'info_plan' not in point_data:
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
    
    produitTest: Produit = Produit("truc", 100, "un truc", "le/chemin/vers/l'icone.png", "objet")
    test.get_plan()[0].set_fonction(Etagere([produitTest]))

    print("\n", test)  # Affichage après ajout du nouveau point
    
    test.suppPoint(3, 2)
    
    print("\n", test)  # Affichage après suppression
    
    # création d'un fichier json
    print("\n... écriture de test en fichier json ...")
    test.ecrire_JSON("test1.json")
    
    # Vérifier si le fichier a été créé
    if os.path.exists("test1.json"):
        print("Le fichier a été créé avec succès.")
    else:
        print("Le fichier n'a pas été créé.")
        
    test2 = Plan(3, 3)
    test2.lire_JSON("test1.json")
    print("\nlecture de test1.json sur test2:\n", test2)
    print("test == test2 ?", test == test2)
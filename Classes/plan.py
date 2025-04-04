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
from Classes.dijkstra import dijkstra
from Classes.fonction import Fonction

# Cette classe servirat de base à la création du plan des magasins
class Plan :
    def __init__(self, h : int = 9, l : int = 9, nom  : str = "MonMagasin", auteur : str = "", date : str = "17/11/2005", adresse : str = "None of your business", image : str = None) -> None:
        # on définit un liste contenant un dictionnaire contenant toutes les coordonnées des point du plan ses voisins et sa fonction dans le magasin (None par défaut)
        self._plan : list[Point] = []
        self._fichier : str = nom
        self._nom : str = nom
        self._auteur : str = auteur
        self._date : str = date
        self._adresse : str = adresse
        self._h : int = h
        self._l : int = l
        self._image : str = image
        
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
            
    def set_image(self, image : str) -> None:
        self._image = image
    
    def set_plan(self, plan : list) -> None:
        self._plan = plan
        
    def set_fichier(self, fichier: str) -> None:
        self._fichier = fichier
    
    def set_nom(self, nom : str) -> None:
        self._nom = nom
    
    def set_auteur(self, auteur : str) -> None:
        self._auteur = auteur
    
    def set_date(self, date : str) -> None:
        self._date = date
    
    def set_adresse(self, adresse : str) -> None:
        self._adresse = adresse
        
    def set_h(self, h : int) -> None:
        self._h = h
        
    def set_l(self, l : int) -> None:
        self._l = l
    
    # Méthodes getters    
    def get_plan(self) -> list:
        return self._plan
    
    def get_l(self) -> int:
        return self._l
    
    def get_h(self) -> int:
        return self._h
    
    def get_image(self) -> None:
        return self._image
    
    def get_planSimple(self) -> dict:
        dico : dict = {}
        
        for point in self._plan:
            dico[point.get_coordonnee()] = point.get_voisins()
            
        return dico
    
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
    
    def getInfos(self) -> dict:
        dico = {}
        for point in self._plan:
            x = point.get_x()
            y = point.get_y()
            rayon = point.getRayon()
            fonc = point.get_fonction()
            
            # Initialiser l'entrée si elle n'existe pas encore
            if (x, y) not in dico:
                dico[(x, y)] = {}
            
            # Ajouter les informations sur le rayon
            if rayon.getNom():
                dico[(x, y)].update({"color": rayon.getCouleur(), "name": rayon.getNom()})
            else:
                dico[(x, y)].update({"color": None, "name": None})
            
            # Ajouter les informations sur la fonction
            if fonc.getNom():
                dico[(x, y)].update({"fonction": fonc.getNom()})
            else:
                dico[(x, y)].update({"fonction": None})
        return dico
    
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
            
    def dijkstra(self, depart : Point, arrivee : Point) -> list[Point]:
        chemin : list[tuple] = []
        
        # on récupère le plan sous la forme d'un dictionnaire de coordonnées et de leurs voisins
        dico = self.get_planSimple()
        
        # on récupère les coordonnées du départ et de l'arrivée
        depart = depart.get_coordonnee()
        arrivee = arrivee.get_coordonnee()
        
        chemins : dict = {}
        chemins = dijkstra(dico, depart)
        
        # pour chaque point dans chemins
        for point in chemins.keys():
            # si le point correspond à l'arriver
            if point == arrivee:
                # alors on définit le point de retour depuis le point en liaison avec ce point
                # le programe vat donc faire le chemin inverse pour arriver au départ depuis l'arrivée
                pointRetour : tuple = chemins[point][1]
                
                # tant que le cout du chemin est supérieur à zéro
                while chemins[pointRetour][0] > 0:
                    # on ajoute le point de retour au chemin finale
                    chemin.append(pointRetour)
                    # on prend un nouveau point de retour à partir de l'ancien
                    pointRetour = chemins[pointRetour][1]

        # inversement de la liste
        chemin.reverse()
        # ajout du départ et de l'arriver
        chemin.insert(0, depart)          
        chemin.append(arrivee)
        
        # on renvoie la liste de coordonner
        return chemin

    def chemin_rapide(self, depart: Point, points_articles: list[Point]) -> list[list[Point]]:
        chemins= []  # Liste du chemins entre deux articles
        point_courant = depart
        points = points_articles.copy()

        while points:
            plus_proche = None
            distance_min = 1000000000000 # Initialisation d'une valeur très élever pour être modifier à la première iteration de la boucle

            for point in points: 
                # Appel de dijkstra pour connaitre la distance entre le point actuel et tous les autres
                chemin_temp = self.dijkstra(point_courant, point) 
                distance_temp = len(chemin_temp)
                if distance_temp < distance_min:
                    plus_proche = point
                    distance_min = distance_temp
                    
            if plus_proche:
                chemin = self.dijkstra(point_courant, plus_proche)
                chemins.append(chemin)  # Ajouter le chemin partiel à la liste
                point_courant = plus_proche
                points.remove(plus_proche)

        return chemins
    
    
    def del_rayon(self, nom : str, couleur : QColor):
        for point in self._plan:
            if point.getRayon() == Rayon(nom, couleur):
                point.setRayon(Rayon())
                
    def set_rayon(self, nom : str, couleur : QColor, new_couleur : QColor):
        for i in range(len(self._plan)):
            point : Point = self.get_plan()[i]
            print(point.getRayon().getNom(), nom, point.getRayon().getCouleur() , couleur)
            if point.getRayon().getNom() == nom and point.getRayon().getCouleur() == couleur:
                
                self.get_plan()[i].setRayon(Rayon(nom, new_couleur))
                
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
        file = open(nomFichier + '.json', 'w')
        
        info_plan = {"info_plan" : {
            "nom" : self._nom,
            "auteur" : self._auteur,
            "adresse" : self._adresse,
            "date" : self._date,
            "h" : self._h,
            "l" : self._l,
            "image" : self._image
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
            
            if fonction["spécialitée"] == "etagere":
                # on crée la nouvelle clé
                fonction["produits"] = []
                
                # on récupere les info de l'etagere
                etagere : Etagere = point.get_fonction()
                
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
                        "rouge": coul.red(),
                        "vert": coul.green(),
                        "bleu": coul.blue(),
                        "alpha": coul.alpha()
                    }
                    rayon["couleur"] = couleur
            else: 
                rayon = None   
                
            # on met le tout dans un dictionnaire qui regroupe toutes les infos du point
            data = {
                        "x" : point.get_x(), 
                        "y" : point.get_y(),
                        "voisins" : voisins,
                        "fonction" : fonction,
                        "rayon" : rayon
                }
            
            # Ajout du point à la liste des points
            points.append(data)
            
            data = {}
            voisins = []
            fonction = {}
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
        with open(chemin + '.json', 'w', encoding='utf-8') as file:
            json.dump(points, file, indent=4, ensure_ascii=False)
            
    def lire_JSON(self, nomFichier: str) -> None:
        # Chemin du répertoire actuel (où se trouve ce script)
        chemin = os.path.dirname(__file__)

        # Remonter d'un dossier pour obtenir le chemin du dossier parent
        chemin = os.path.dirname(chemin)

        # Aller dans le dossier Magasin
        chemin = os.path.join(chemin, "Magasin")

        # Ajouter le nom du fichier
        chemin_fichier = os.path.join(chemin, nomFichier)

        # Lecture des données à partir du fichier JSON
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as file:
                info = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la lecture du fichier JSON: {e}")
            return
        except FileNotFoundError:
            print("Le fichier n'a pas été trouvé.")
            return
        except Exception as e:
            print(f"Une erreur s'est produite: {e}")
            return

        # On supprime le plan
        self._plan = []

        # Dictionnaire pour stocker les points créés afin de référencer les voisins correctement
        points_dict = {}

        # Création de tous les points sans les voisins
        for point_data in info:
            if 'info_plan' in point_data:
                self.set_nom(point_data['info_plan']['nom'])
                self.set_auteur(point_data['info_plan']['auteur'])
                self.set_adresse(point_data['info_plan']['adresse'])
                self.set_date(point_data['info_plan']['date'])
                self.set_h(point_data['info_plan']['h'])
                self.set_l(point_data['info_plan']['l'])
                self.set_image(point_data['info_plan']['image'])
            else:
                x = point_data['x']
                y = point_data['y']
                rayon = None

                # Création du rayon du point
                if 'rayon' in point_data and point_data['rayon'] is not None:
                    rayon_data = point_data['rayon']
                    nom_rayon = rayon_data['nom'] if 'nom' in rayon_data else None

                    couleur_rayon = None
                    if 'couleur' in rayon_data:
                        couleur = rayon_data['couleur']
                        couleur_rayon = QColor(
                            int(couleur['rouge']),
                            int(couleur['vert']),
                            int(couleur['bleu']),
                            int(couleur['alpha'])
                        )

                    rayon = Rayon(nom_rayon, couleur_rayon)
                
                # Création de la fonction du point
                fonction_data = point_data['fonction']
                specialite = fonction_data['spécialitée']

                if specialite == "etagere":
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
                elif specialite == "entree":
                    fonction = Entree()
                elif specialite == "chemin":
                    fonction = Chemin()
                else:
                    fonction = Fonction()

                # Création du point sans les voisins pour l'instant
                point = Point(x, y, fonction=fonction, rayon=rayon)
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
    
    print("chemin : ",test2.get_plan()[0].get_coordonnee()," -> ",test2.get_plan()[5].get_coordonnee()," :", test2.dijkstra(test2.get_plan()[0], test2.get_plan()[5]))
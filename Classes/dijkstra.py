from Classes.filepile import *

def dijkstra(graphe: dict, depart: tuple) -> dict:
    '''La fonction renvoie un dictionnaire dont les clés sont les sommets que l'on peut atteindre
à partir du sommet_depart.
A chaque clé est associée la distance qui sépare ce sommet du sommet_depart.

:param: graphe, objet Plan
:param: depart, type str, sommet à partir duquel sont calculées les distances
:param: bk_liste, liste de sommets à éviter
:return: la liste du chemin à suivre
:CU: Respect des types
:bord_effect: None
'''
    # On crée une file
    file = File()
    
    # On enfile le sommet de départ (chemin initial)   
    file.enfiler(depart)
    
    # On crée un dictionnaire {sommet : (distance, chemin)} avec le sommet de départ
    dico = {depart : (0, [])}
    
    # Tant que la file n’est pas vide :
    while not file.est_vide():
        
        # – on défile un chemin
        chemin_actuel : tuple = file.defiler()
        
        #– on extrait le dernier sommet
        dernier_sommet = dico[chemin_actuel]
        
        # – on consulte ses voisins
        voisins = graphe[chemin_actuel]
        
        # – Pour chaque voisin :
        for voisin in voisins:
                
            # on calcule la distance du voisin au sommet de départ
            distance = dernier_sommet[0] + 1
            
            # si le voisin n’est pas dans le dictionnaire :
            if voisin not in dico.keys():
                
                # on l’ajoute avec sa distance et son chemin depuis le sommet de départ
                dico[voisin] = (distance, chemin_actuel)
                
                # on enfile le chemin
                file.enfiler(voisin)
            
            # sinon si la distance calculée est plus petite que celle indiquée dans le dictionnaire   
            elif distance < dico[voisin][0]:
                
                # on met à jour la distance et le chemin dans le dictionnaire
                dico[voisin] = (distance, chemin_actuel)
                
                # on enfile le chemin
                file.enfiler(voisin)
                    
    #  On renvoie le dictionnaire
    return dico
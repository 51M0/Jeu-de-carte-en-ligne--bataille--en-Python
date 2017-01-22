import random
from modele.Carte import Carte
class Deck:
    def __init__(self):
        self.cartes = []
        self.melanger()
        
    def get_cartes(self):
        return self._cartes
    
    def set_cartes(self, cartes):
        self.cartes = cartes
        
    def add_carte(self, carte):
        self.cartes.append(carte)
        
    def remove_carte(self, carte):
        self.cartes.remove(carte)
        
    def get_nombreCartes(self):
        return self.cartes.__len__()
    
    def melanger(self):
        liste = []
        
        for i in range(0,52):
            liste.append(i)
        
        random.shuffle(liste)
        
        for i in range(0,52):
            self.cartes.append(Carte(liste[i]))
            
    def distribuer(self, joueurs):
        for i in range(0, joueurs.__len__()):
            for j in range(i*(52/joueurs.__len__()), (i+1)*(52/joueurs.__len__())):
                joueurs[i].add_carte(self.cartes[j])
        
        self.cartes = []
            
    cartes  = property (get_cartes, set_cartes, add_carte, remove_carte)
    
    
    
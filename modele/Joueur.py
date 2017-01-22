class Joueur:
    def __init__(self, num):
        self.num    = num
        self.cartes = []
        self.score  = 0
    
    def get_cartes(self):
        return self.cartes
    
    def set_cartes(self, cartes):
        self.cartes = cartes
    
    def add_carte(self, carte):
        self.cartes.append(carte)
        
    def getNombreCartes(self):
        return self.cartes.__len__()
        
    def get_num(self):
        return self.num
        
    def set_num(self, num):
        self.num = num
        
    def get_score(self):
        return self.score
        
    def set_score(self, score):
        self.score = score
        
    def retirerCarte(self):
        carte = self.cartes[0]
        self.cartes.remove(carte)
        return carte
        
    def afficher(self):
        print "Joueur ", self.num, " avec ", self.cartes.__len__() , " Cartes :"
        for i in range(0, self.cartes.__len__()):
            print self.cartes[i].afficher()
    
    cartes  = property (get_cartes, set_cartes, getNombreCartes)
    num     = property (get_num, set_num)
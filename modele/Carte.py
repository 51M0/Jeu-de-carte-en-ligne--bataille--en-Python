class Carte:
    def __init__(self, num):
        self.rang   =   num % 13
        self.forme  =   num / 13
        self.num    =   num
    
    def get_rang(self):
        return self.rang
    
    def set_rang(self, rang):
        self.rang = rang
        
    def get_forme(self):
        return self.forme
    
    def set_forme(self, forme):
        self.forme = forme
        
    def get_num(self):
        return self.num
    
    def set_num(self, num):
        self.num = num
        
    def compare(self, carte):
        if self.get_rang() < carte.get_rang():
            return 0
        if self.get_rang() > carte.get_rang():
            return 1
        if self.get_rang() == carte.get_rang():
            return 2
        
    def afficher(self):
        print "Carte " ,str(self.num) ," Forme : ", self.forme, " Rang : ", self.rang

        
    rang    =   property (get_rang, set_rang)
    forme   =   property (get_forme, set_forme)
    num     =   property (get_num, set_num)
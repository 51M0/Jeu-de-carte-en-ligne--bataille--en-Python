import Tkinter as Tk
import time
import tkFont
from Tkinter import StringVar
from modele.Joueur import Joueur
from modele.Deck import Deck
from tkFont import BOLD
from modele.Carte import Carte


class Application(Tk.Canvas):
    def __init__(self,master = None):
        Tk.Canvas.__init__(self, master, width=1200, height=650)
        self.initialiser()
        
        
    def initialiser(self):
        #Options pour le nombre de joueurs
        self.options = self.top =  Tk.Toplevel(self)
        self.options.title("Options")
                
        self.label1 = Tk.Label(self.options, text="Nombre de Joueurs : ", fg="black" , font=('Times', 12))
        self.label1.grid(row=0, column=0)
        
        self.label2 = Tk.Label(self.options, text="Type : ", fg="black" , font=('Times', 12))
        self.label2.grid(row=1, column=0)
                
        OPTIONS = [
        "2",
        "3",
        "4"
        ]
        
        self.variable = StringVar(self.options)
        self.variable.set(OPTIONS[0]) # default value
    
        self.joueurs = apply(Tk.OptionMenu, (self.options, self.variable) + tuple(OPTIONS))
        self.joueurs.grid(row=0, column=1)
        
        #Options pour le type de Jeu de carte (Actuelle ou Courte)
        OPTIONS2 = [
        "Actuelle",
        "Courte"
        ]
        
        self.variable2 = StringVar(self.options)
        self.variable2.set(OPTIONS2[0]) # default value
    
        self.types = apply(Tk.OptionMenu, (self.options, self.variable2) + tuple(OPTIONS2))
        self.types.grid(row=1, column=1)

        #Bouton pour valider les choix
        self.validerOptions = Tk.Button(self.options, text="OK", command=self.ok)
        self.validerOptions.grid(row=2, column=0)


    def createWidget(self):        
        #On definit la largeur de notre fenetre en dependant du nombre de joueurs choisis
        self.config(width=self.nombreJoueurs*300)
        
        #Les elements du Jeu
            #Les Joueurs
        self.joueurs = []
        for i in range (0,self.nombreJoueurs):
            self.joueurs.append(Joueur(i))

            #Le Deck
        self.deckJeu = Deck()
        self.deckJeu.distribuer(self.joueurs)
        
            #Carte pour les joueurs elimines
        self.carteElimine = Carte(-1)
        self.carteElimine.set_rang(-1)
            
            #Nombre de cartes gagnees (pour la version courte) 
        self.cartesGagnees = []
        for i in range (0,self.nombreJoueurs):
            self.cartesGagnees.append(0)
        
        #Canvas principal
        self.configure(background = "WHITE") 
        self.grid(row=0, column=0, rowspan=2, columnspan=self.nombreJoueurs)
        
        # Table du Jeu
        self.terrains = []
        self.fond = Tk.PhotoImage(file="gazon.gif")
        for i in range (0,self.nombreJoueurs):
            self.terrains.append(Tk.Canvas(self.master, width = 1/self.nombreJoueurs, height=0.5))
            self.terrains[i].create_image(0, 0, image=self.fond)
            self.terrains[i].grid(row=0, column=i, sticky="NESW")
            self.terrains[i].create_rectangle(60, 60, 235, 300 , fill="WHITE")

        
        #Les decks des joueurs
        self.deck = Tk.PhotoImage(file="deck.gif")
        self.font1 = tkFont.Font(family="Times", size=14, weight=tkFont.BOLD)
        
        self.cadres         =   []
        self.fonds          =   []
        self.labelJoueurs   =   []
        self.decks          =   []
        
        self.fonds.append(Tk.PhotoImage(file="bg/rouge.gif"))
        self.fonds.append(Tk.PhotoImage(file="bg/orange.gif"))
        self.fonds.append(Tk.PhotoImage(file="bg/noir.gif"))
        self.fonds.append(Tk.PhotoImage(file="bg/bleu.gif"))
        
        for i in range (0,self.nombreJoueurs):
            self.cadres.append(Tk.Canvas(self.master, width=1/self.nombreJoueurs, height = 0.5))
            self.cadres[i].create_image(0, 0, image=self.fonds[i])
            self.labelJoueurs.append(Tk.Label(self.master, text="JOUEUR " + str(i+1), font=self.font1))
            self.labelJoueurs[i].grid(row=1, column=i, sticky="N")
            self.cadres[i].create_rectangle(60, 60, 235, 300 , fill="WHITE")
            self.decks.append(self.cadres[i].create_image(150, 180, image=self.deck, tag='toggle_cursor'))
            self.cadres[i].grid(row=1, column=i, columnspan=1, sticky="NESW")
        

        self.font2 = tkFont.Font(family="Times", size=12, weight=tkFont.BOLD)
        
        self.texteScores    =   []
        self.labelScores    =   []
        for i in range (0,self.nombreJoueurs):
            self.texteScores.append(StringVar())
            self.texteScores[i].set("Cartes : " + str(self.joueurs[0].getNombreCartes()))
            self.labelScores.append(Tk.Label(self.master, textvariable=self.texteScores[i], bg="WHITE", font=self.font2))
            self.labelScores[i].grid(row=1, column=i, sticky="S")
        
        # Signaux & Curseurs
        for i in range (0,self.nombreJoueurs):
            self.cadres[i].tag_bind(self.decks[i], "<Button-1>", lambda event,arg1=i : self.cliquerDeck(event,arg1))
            self.cadres[i].tag_bind('toggle_cursor', '<Enter>', lambda e: self.cadres[i].configure(cursor = 'hand1'))

 
        # Ce qui a relation avec l'affichage de la carte de chacun
        self.choix      = []
        self.cartes     = []
        self.cartesJeu  = []
        for i in range (0,self.joueurs.__len__()):
            self.choix.append(self.terrains[i].create_image(0, 0))
            self.cartes.append(Tk.PhotoImage())
            self.cartesJeu.append(Carte(0))
            

        # Bataille !
        self.labelBataille          = []
        self.cartesBataille         = []
        self.bataille               = False


        # On remet a zero le tour de chacun pour demarrer la partie
        self.tourAZero()


    # Action pour valider le nombre des joueurs et le type de Bataille
    def ok(self):
        self.nombreJoueurs = int(self.variable.get())
        self.version = self.variable2.get()
        self.options.destroy()
        self.createWidget()
        
        
    # Remet le tour de chaque joueur a zero
    def tourAZero(self):
        if self.bataille == True:
            for i in range(0, self.batailles.__len__()):
                self.b[self.batailles[i].get_num()] = False
        else:
            self.b = []
            for i in range (0,self.joueurs.__len__()):
                if (self.cartesJeu[i] == self.carteElimine):
                    self.b.append(True)
                else:
                    self.b.append(False)
    
    # Responsable sur les signaux lors du clic sur un deck
    def cliquerDeck(self, event, arg1):
        if self.b[arg1] == False:
            if self.joueurs[arg1].cartes.__len__() > 0:
                carteRetire          =   self.joueurs[arg1].retirerCarte()
                self.cartes[arg1]    =   Tk.PhotoImage(file="cartes/" + str(carteRetire.get_num()) + ".gif")
                self.cartesJeu[arg1] =   carteRetire
                self.choix[arg1]     =   self.terrains[arg1].create_image(150, 180, image=self.cartes[arg1])
                self.b[arg1]         =   True
                self.verifier()

    
    # MAJ des scores
    def majScores(self):
        if self.bataille == True:
            indexMax = self.batailles[0].get_num()
            for i in range (1, self.batailles.__len__()):
                if self.cartesJeu[indexMax].get_rang() < self.cartesJeu[self.batailles[i].get_num()].get_rang():
                    indexMax = self.batailles[i].get_num()
        else:
            indexMax = 0
            for i in range (1,self.cartesJeu.__len__()):
                if self.cartesJeu[indexMax].get_rang() < self.cartesJeu[i].get_rang():
                    indexMax = i
            
        
        self.verifierBataille(indexMax)
        if self.bataille == True:
            self.ecrireBataille()
            self.lancerBataille()
        else:
            self.prendreCartes(indexMax)
            self.majLabelScores()
            self.clignoter(indexMax)

    
    def lancerBataille(self):
        for i in range(0, self.batailles.__len__()):
            self.b[self.batailles[i].get_num()] = False
            
        """
        self.cartesJeu[0].rang = -1
        self.cartesJeu[1].rang = -2
        """
        

    def ecrireBataille(self):
        for i in range(0, self.labelBataille.__len__()):
            self.labelBataille[i].destroy()
                    
        self.labelBataille = []
        
        for i in range(0, self.joueurs.__len__()):
            self.labelBataille.append(Tk.Label(self.master, text="Bataille !", fg="RED" , font=('Times', 20, tkFont.BOLD)))
        for i in range(0, self.batailles.__len__()):
            self.labelBataille[i].grid(row=1, column=self.batailles[i].get_num())
            
    
    def majLabelScores(self):
        if (self.version == "Actuelle"):
            for i in range(0,self.joueurs.__len__()):
                self.texteScores[i].set("Cartes : " + str(self.joueurs[i].getNombreCartes()))
                
        if (self.version == "Courte"):
            for i in range(0,self.joueurs.__len__()):
                self.texteScores[i].set("Cartes : " + str(self.cartesGagnees[i]))
    
    def clignoter(self, num):
        for i in range(0,self.joueurs.__len__()):
            if i==num:
                self.labelScores[i].config(fg='red', font=('Times', 16, BOLD))
            else:
                self.labelScores[i].config(fg='black', font=('Times', 12, BOLD))
        
    # Verifie si tous les joueurs ont fait leur choix 
    def verifier(self):
        reset=True
        for i in range(0,self.b.__len__()):
            if self.b[i] == False:
                reset=False
        
        if reset==True:
            self.update()
            self.majScores()
            self.verifierDecksVides()
            self.pause()
            self.tourAZero()
            self.viderTerrains()
            self.verifierFinPartie()
            
    
    def verifierDecksVides(self):
        for i in range(0,self.joueurs.__len__()):
            if self.joueurs[i].getNombreCartes() == 0:
                self.cadres[i].delete(root, self.decks[i])
                self.cartesJeu[i] = self.carteElimine
                self.b[i] = True


    def verifierBataille(self, indexMax):
        if self.bataille == True:
            self.bataille  = False
            temp = self.batailles
            self.batailles = []
            self.batailles.append(self.joueurs[indexMax])
            
            for i in range(0, temp.__len__()):
                if (self.cartesJeu[indexMax].get_rang() == self.cartesJeu[temp[i].get_num()].get_rang() and (indexMax != temp[i].get_num())):
                    self.bataille = True
                    self.batailles.append(self.joueurs[temp[i].get_num()])
                    self.cartesBataille.append(self.cartesJeu[temp[i].get_num()])
                
            if self.bataille == True:
                self.cartesBataille.append(self.cartesJeu[indexMax])
        else:
            self.bataille  = False
            self.batailles = []
            self.batailles.append(self.joueurs[indexMax])
            
            for i in range(0, self.joueurs.__len__()):
                if (self.cartesJeu[indexMax].get_rang() == self.cartesJeu[i].get_rang()) and (indexMax != i):
                    self.bataille = True
                    self.batailles.append(self.joueurs[i])
                    self.cartesBataille.append(self.cartesJeu[i])
                
            if self.bataille == True:
                self.cartesBataille.append(self.cartesJeu[indexMax])
        
     
    def prendreCartes(self, num):
        if (self.version == "Actuelle"):
            for i in range(0,self.cartesBataille.__len__()):
                self.joueurs[num].add_carte(self.cartesBataille[i])
                
        if (self.version == "Courte"):
            self.cartesGagnees[num] += self.cartesBataille.__len__()
            
        self.retirerBataille()
        
        if (self.version == "Actuelle"):
            for i in range(0,self.cartesJeu.__len__()):
                if self.cartesJeu[i] != self.carteElimine:
                    self.joueurs[num].add_carte(self.cartesJeu[i])
        
        if (self.version == "Courte"):
            self.cartesGagnees[num] += self.cartesJeu.__len__()
    
    #Sort le jeu de l'etat bataille  
    def retirerBataille(self):
        self.bataille = False
        self.cartesBataille = []
        
        for i in range(0, self.labelBataille.__len__()):
            self.labelBataille[i].destroy()

    
    # Verifie si la partie est finie
    def verifierFinPartie(self):
        # cpt correspond au nombre de joueurs qui n'ont plus de cartes
        cpt = 0
                
        for i in range(0,self.joueurs.__len__()):
            if self.joueurs[i].getNombreCartes() == 10:
                cpt += 1
                
        if (self.version == "Actuelle"):
            if cpt == self.nombreJoueurs - 1:
                self.finPartie()
                
        if (self.version == "Courte"):
            if cpt == self.nombreJoueurs:
                self.finPartie()
    
       
    # Met fin a la partie de jeu        
    def finPartie(self):
        for i in range(0,self.joueurs.__len__()):
            self.terrains[i].destroy()
            #self.cadres[i].tag_bind(self.decks[i], "<Button-1>", self.interdire)
            
            
        font = tkFont.Font(family="Times", size=30, weight=tkFont.BOLD)
        gagnant = self.gagnant()
        self.labelGagnant  = Tk.Label(self.master, text="Le Gagnant est le joueur : " + str(gagnant+1), fg="RED" , bg="WHITE", font=font)
        self.labelGagnant.grid(row=0, column=0, columnspan=self.nombreJoueurs, sticky="NESW")


    # Retourne le joueur gagnant
    def gagnant(self):
        gagnant = 0
        if (self.version == "Actuelle"):
            for i in range(1,self.joueurs.__len__()):
                if self.joueurs[gagnant].getNombreCartes() < self.joueurs[i].getNombreCartes():
                    gagnant = i
                    
        if (self.version == "Courte"):
            for i in range(1,self.cartesGagnees.__len__()):
                if self.cartesGagnees[gagnant] < self.cartesGagnees[i]:
                    gagnant = i

            
        return gagnant

    def interdire(self, event):
        print "Partie Finie"
            
    # Vide la table de toutes les cartes affiches (pour recommencer le tour)
    def viderTerrains(self):
        for i in range(0,self.joueurs.__len__()):
            self.terrains[i].delete(root, self.choix[i])
            
        
    def pause(self):
        time.sleep(1)
            
root = Tk.Tk()

root.title("Jeu de Carte Bataille !")
root.resizable(width=False,height=False)

app = Application(master=root)
app.mainloop()
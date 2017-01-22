from modele.Deck import Deck


class Table:
    def __init__(self):
        self._joueurs   = []
        self._deck      = Deck
        
    def _get_deck(self):
        return self._deck
    
    def _set_deck(self, deck):
        self._deck = deck
        
    def _get_joueurs(self):
        return self._jouers
    
    def _get_joueur(self, numero):
        return self._joueurs[numero]
    
    def _set_joueurs(self, joueurs):
        self._joueurs = joueurs
        
    def _add_joueur(self, joueur):
        self._joueurs.append(joueur)
        
    deck    = property (_get_deck, _set_deck)
    joueurs = property (_get_joueurs, _set_joueurs)
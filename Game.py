from Human import Human
from Deck import Deck
from Computer import Computer

class Game:

    def __init__(self):
        self.deck = self.__get_deck(shuffled = True)
        self.humans = []
        self.computer = Computer()
        self.mode = "EU"
        self.ranking = []
        self.coop = False

    def __generate_humans(self, count): 
        humans = []
        for i in range(count):
            name = str(input("Quel est votre pseudo, joueur {} ?".format(i+1)))
            while len(name) < 2:
                print("2 caractères minimum s'il vous plaît!")
                name = str(input("Quel est votre pseudo, joueur {} ?".format(i+1)))
            humans.append(Human(name))
        return humans

    def __get_deck(self, shuffled):
        deck = Deck()
        if shuffled:
            deck.shuffle()
        return deck

    def distribution(self):
        for human in self.humans:
            self.distribute_to(human, 1)
        self.distribute_to(self.computer, 1)
        for human in self.humans:
            self.distribute_to(human, 1)
        if self.mode == "US":
            self.distribute_to(self.computer, 1, hide = True)

    def distribute_to(self, player, count, hide = False):
        for i in range(count):
            card = self.deck.draw()
            if hide:
                card.hide()
            player.hand.add_card(card)

    def status(self):
        self.computer.show_hand()
        for human in self.humans:
            human.show_hand()

    def __set_ranking(self):
        tmp = {
            "name": self.computer.name,
            "score": self.computer.hand.score() if self.computer.hand.score() <= 21 else 0,
            "blackjack": self.computer.hand.is_blackjack()
        }
        self.ranking.append(tmp)
        for human in self.humans:
            rank = {
                "name" : human.name,
                "score" : human.hand.score() if human.hand.score() <= 21 else 0,
                "blackjack": human.hand.is_blackjack()
            }
            if rank['score'] >= tmp['score'] and not tmp['blackjack']:
                self.ranking.insert(0, rank)
                tmp = rank
            else:
                self.ranking.insert(self.ranking.index(tmp) + 1, rank)            

    def reset(self):
        self.__init__(self.mode, len(self.humans))

    def ask_action(self):
        action = input("Tapez 'Carte !' pour piocher, ou 'Je reste' pour passer.")
        while action not in ['Carte !', 'Je reste']:
            action = input("Tapez 'Carte !' pour piocher, ou 'Je reste' pour passer.")
        return action

    def play(self):

        # Message de bienvenue
        print("================================================== \n")
        print('              Bienvenue au Black jack!             \n')    
        print("================================================== \n")

        # Paramétrage du mode
        mode = input("À quel mode de jeu souhaitez-vous jouer? (EU/US) \n")
        while mode not in ['EU', 'US']:
            mode = input("À quel mode de jeu souhaitez-vous jouer? (EU/US) \n")
        self.mode = mode

        # Génération des joueurs "humains"
        players_count = int(input("Combien de joueurs vont participer à cette partie? \n"))
        while(players_count<1):
            print('Il faut au moins un joueur pour jouer!')
            players_count = int(input("Combien de joueurs vont participer à cette partie? \n"))
        self.humans = self.__generate_humans(players_count)

        # Paramétrage du style de jeu
        if players_count > 1:
            coop = input("Voulez vous jouer en coop contre l'ordinateur? (y/n) \n")
            while coop not in ['y', 'n']:
                coop = input("Voulez vous jouer en coop contre l'ordinateur? (y/n) \n")
            self.coop = True if coop == 'y' else False

        # distribution des cartes
        print('             Distribution des cartes...            \n')
        self.distribution()
     
        # Affichage du status
        print('===================== STATUT ===================== \n')
        self.status()

        # Tour des humains
        for human in self.humans:
            print("================================================== \n")
            print("C'est au tour de {}".format(human.name))
            human.show_hand()
            if self.ask_action() == 'Carte !':
                card = self.deck.draw()
                print("Pioche d'un {}".format(card.value))
                human.hand.add_card(card)
                human.show_hand()
                while human.hand.score() < 21 and self.ask_action() == 'Carte !':
                    human.hand.add_card(self.deck.draw())
                    human.show_hand()
                    
        # Tour de l'ordinateur / la banque tire à 16, reste à 17
        print("================================================== \n")
        print("C'est au tour de l'ordinateur")
        if self.mode == 'EU':
            self.distribute_to(self.computer, 1)
        elif self.mode == 'US':
            self.computer.hand.unhide()
        self.computer.show_hand()
        while self.computer.hand.score() < 17:
            card = self.deck.draw()
            print("Pioche d'un {}".format(card.value))
            self.computer.hand.add_card(card)
            self.computer.show_hand()

        # Génération du classement
        self.__set_ranking()

        print("================================================== \n")
        print("         THE WINNER IS {} ! CONGRATS !             \n".format(self.ranking[0]["name"]))
        print("================================================== \n")

        # Affichage du classement
        print("================================================== \n")
        print("                     CLASSEMENT                    \n")
        print("================================================== \n")
        for i, rank in enumerate(self.ranking):
            if not rank['blackjack']:
                end_sentence = str(rank['score']) + " points."  
            else:
                end_sentence = "un BLACK JACK!"
            print("{} termine cette partie en position {}, avec {} \n".format(
                rank['name'], 
                i+1, 
                end_sentence
            ))
            print("-------------------------------------------------- \n")
        
        


       



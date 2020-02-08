from Human import Human
from Deck import Deck
from Computer import Computer

class Game:

    def __init__(self):
        self.deck = self.get_deck(shuffled = True)
        self.humans = []
        self.computer = Computer()
        self.mode = "EU"
        self.ranking = []
        self.coop = False

    def generate_humans(self, count): 
        humans = []
        for i in range(count):
            msg = "Quel est votre pseudo, joueur {} ?\n".format(i+1)
            name = str(input(msg))
            while len(name) < 2:
                print("2 caractères minimum s'il vous plaît!")
                name = str(input(msg))
            humans.append(Human(name))
        return humans

    def get_deck(self, shuffled):
        deck = Deck()
        if shuffled:
            deck.shuffle()
        return deck

    def distribution(self):
        print('             Distribution des cartes...            \n')
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
        print('===================== STATUT ===================== \n')
        self.computer.show_hand()
        for human in self.humans:
            human.show_hand()

    def set_ranking(self):
        self.ranking.append({
            "name": self.computer.name,
            "score": self.computer.hand.score() if self.computer.hand.score() <= 21 else 0,
            "blackjack": self.computer.hand.is_blackjack()
        })
        for human in self.humans:
            rank = {
                "name" : human.name,
                "score" : human.hand.score() if human.hand.score() <= 21 else 0,
                "blackjack": human.hand.is_blackjack()
            }
            i = 0
            while (i < len(self.ranking)-1) and (rank['score'] < self.ranking[i]['score']) or self.ranking[i]['blackjack']:
                print(" I = ",i)
                i += 1
            self.ranking.insert(i, rank)

    def reset(self):
        self.__init__(self.mode, len(self.humans))

    def ask_action(self):
        msg = "Tapez 'Carte !' pour piocher, ou 'Je reste' pour passer.\n"
        action = input(msg)
        while action not in ['Carte !', 'Je reste']:
            action = input(msg)
        return action

    def welcome_msg(self):
        print("================================================== \n")
        print('              Bienvenue au Black jack!             \n')    
        print("================================================== \n")
    
    def set_mode(self):
        msg = "À quel mode de jeu souhaitez-vous jouer? (EU/US) \n"
        mode = input(msg)
        while mode not in ['EU', 'US']:
            mode = input(msg)
        self.mode = mode

    def set_humans(self):
        msg = "Combien de joueurs vont participer à cette partie? \n"
        players_count = input(msg)
        while(not players_count.isdigit() or int(players_count)<1):
            if not players_count.isdigit():
                print('{} n\'est pas un nombre valide!'.format(players_count))
            else:
                print('Il faut au moins un joueur pour jouer!')
            players_count = input(msg)
        players_count = int(players_count)
        self.humans = self.generate_humans(players_count)
    
    def set_coop_mode(self):
        msg = "Voulez vous jouer en coopération contre l'ordinateur? (y/n) \n"
        if len(self.humans) > 1:
            coop = input(msg)
            while coop not in ['y', 'n']:
                coop = input(msg)
            self.coop = True if coop == 'y' else False

    def humans_turn(self):
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

    def computer_turn(self):
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

    def show_winner(self):
        if not self.coop:
            sentence = "THE WINNER IS" + self.ranking[0]["name"] + "! CONGRATS !" 
        elif self.ranking[0]["name"] is not self.computer.name:
            sentence = "PLAYERS DEFEATED THE COMPUTER ! CONGRATS !" 
        else:
            sentence = "COMPUTER WON THIS TIME !"
        print("================================================== \n")
        print("    {}    \n".format(sentence))
        print("================================================== \n")

    def show_ranking(self):
        print("================================================== \n")
        print("                    RANKINGS                       \n")
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

    def run(self):

        # Message de bienvenue
        self.welcome_msg()

        # Paramétrage du mode
        self.set_mode()

        # Génération des joueurs "humains"
        self.set_humans()

        # Paramétrage du style de jeu
        self.set_coop_mode()

        # distribution des cartes
        self.distribution()
     
        # Affichage du status
        self.status()

        # Tour des humains
        self.humans_turn()
                    
        # Tour de l'ordinateur / la banque tire à 16, reste à 17
        self.computer_turn()

        # Génération du classement
        self.set_ranking()

        # Affichage du gagnant
        self.show_winner()

        # Affichage du classement
        self.show_ranking()
        
        


       



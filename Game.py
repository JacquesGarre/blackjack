from Human import Human
from Player import Player
from Deck import Deck
from Computer import Computer
import os


class Game:

    def __init__(self):
        self.deck = self.get_deck(shuffled = True)
        self.humans = []
        self.computer = Computer()
        self.mode = "EU"
        self.ranking = []
        self.coop = False
        self.bet = 0

    def clear(self):
        return lambda: os.system('cls')

    def generate_humans(self, count, stack): 
        humans = []
        for i in range(count):
            msg = "Quel est votre pseudo, joueur {} ?\n".format(i+1)
            name = str(input(msg))
            while len(name) < 2:
                print("2 caractères minimum s'il vous plaît!")
                name = str(input(msg))
            humans.append(Human(name, int(stack)))
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
        print('\n')
        for human in self.humans:
            human.show_hand()
            human.show_stack()
    
    def set_ranking(self):
        players = self.humans + [self.computer]
        sorted(players, key=lambda player: (player.hand.score(), player.hand.is_blackjack()))
        ranked_players = [player for player in players if player.hand.score() <= 21]
        unranked_players  = [player for player in players if player.hand.score() > 21]
        self.ranking = ranked_players + unranked_players
    
    def get_winners(self):
        ranked_players = [player for player in self.ranking if player.hand.score() <= 21]
        one_of_the_best = max(ranked_players, key=lambda player: (player.hand.score(), player.hand.is_blackjack()))
        winners = []
        for player in ranked_players:
            if player.hand.score() == one_of_the_best.hand.score() and player.hand.is_blackjack() == one_of_the_best.hand.is_blackjack():
                winners.append(player)
        return winners

    def reset(self):
        self.ranking = []
        self.deck = self.get_deck(shuffled = True)
        self.computer.hand.reset()
        for human in self.humans:
            human.hand.reset()

    def ask_action(self):
        msg = "Tapez 'Carte !' pour piocher, ou 'Je reste' pour passer.\n"
        action = input(msg)
        while action not in ['Carte !', 'Je reste']:
            action = input(msg)
        return action

    def welcome_msg(self):
        self.clear()
        print("================================================== \n")
        print('              Bienvenue au Black jack!             \n')    
        print("================================================== \n")
    
    def set_mode(self):
        msg = "À quel mode de jeu souhaitez-vous jouer? (EU/US) \n"
        mode = input(msg)
        while mode not in ['EU', 'US']:
            mode = input(msg)
        self.mode = mode
    
    def set_players_count(self):
        msg = "Combien de joueurs vont participer à cette partie? (1-7)\n"
        players_count = input(msg)
        while not players_count.isdigit() or int(players_count)<1 or int(players_count)>7:
            if not players_count.isdigit():
                print('{} n\'est pas un nombre valide!'.format(players_count))
            elif int(players_count)<1:
                print('Il faut au moins un joueur pour jouer!')
            else:
                print('7 joueurs maximum autorisés!')
            players_count = input(msg)
        return int(players_count)
    
    def set_players_stack(self):
        msg = "Combien de jetons auront les joueurs? \n"
        stack = input(msg)
        while not stack.isnumeric() or int(stack)<1:
            if not stack.isnumeric():
                print('{} n\'est pas un nombre valide!'.format(stack))
            elif int(stack)<1:
                print('Il faut au moins un jeton par joueur pour parier!')
            stack = input(msg)
        return int(stack)

    def set_players_bet(self, stack):
        msg = "Quelle sera la mise des joueurs? ({} jeton(s) maximum!) \n".format(stack)
        bet = input(msg)
        while not bet.isnumeric() or int(bet)<1 or int(bet)>stack:
            if not bet.isnumeric():
                print('{} n\'est pas un nombre valide!'.format(bet))
            elif int(bet)<1:
                print('La mise doit être au minimum de 1 jeton!')
            bet = input(msg)
        return int(bet)

    def set_humans(self):
        players_count = self.set_players_count()
        stack = self.set_players_stack()
        self.bet = self.set_players_bet(stack)
        self.humans = self.generate_humans(players_count, stack)
    
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
            if human.hand.score() != 21:
              if self.ask_action() == 'Carte !':
                  card = self.deck.draw()
                  print("Pioche d'un {}".format(card.value))
                  human.hand.add_card(card)
                  human.show_hand()
                  while human.hand.score() < 21 and self.ask_action() == 'Carte !':
                      human.hand.add_card(self.deck.draw())
                      human.show_hand()

    def computer_turn(self):
        is_playing = False
        for human in self.humans:
            if 0 < human.hand.score() <= 21:
                is_playing = True
        if is_playing:
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
        winners = self.get_winners()
        if len(winners) == 1:
            print("================================================== \n")
            print("         LE GAGNANT DE CE TOUR EST {} !            \n".format(winners[0].name))
            print("================================================== \n")
        else:
            draw = self.computer in winners
            if draw :
                winners.remove(self.computer)
            joueurs = ''
            for player in winners:
                joueurs += player.name + '\n'
            if draw:
                print("================================================== \n")
                print("                Les joueurs :\n{}                  \n".format(joueurs))
                print("              sont à égalité avec                  \n")
                print("                        {} !                       \n".format(self.computer.name))
                print("================================================== \n")
            else:
                print("================================================== \n")
                print("                LES GAGNANTS SONT :\n{}                  \n".format(joueurs))
                print("================================================== \n")

    def humans_bet(self):
        print("================= MISE DES JOUEURS =============== \n")
        for human in self.humans:
            if human.stack - self.bet < 0: 
                print("{} ne peut pas miser, il ne lui reste plus que {} jeton(s), la mise est de {}!\n".format(human.name, human.stack, self.bet))
                print("{} est éliminé!\n".format(human.name))
                self.humans.remove(human)
            else:
                human.stack -= self.bet
                print("{} place sa mise de {} jeton(s) sur le tapis. ({} jeton(s) restant)".format(human.name, self.bet, human.stack))
        print("\n================================================== \n")
    
    def set_gains(self):
        winners = self.get_winners()
        print("====================== GAINS ===================== \n")
        if len(winners) == 1 and winners[0] == self.computer:
            print("     {} a remporté toutes les mises!           \n".format(self.computer.name))
            print("================================================== \n")
            return
        elif self.computer in winners:
            gains = self.bet * 1.5
            winners.remove(self.computer)
        else:
            gains = self.bet * 2
        if self.coop:
            for human in self.humans:
                human.stack += gains
            players_getting_gains = [player.name for player in self.humans]
        else:
            for winner in winners:
                winner.stack += gains
            players_getting_gains = [player.name for player in winners]
        print("{}".format("\n".join(players_getting_gains)))
        print("{} remporté {} jeton(s) {}! \n".format("a" if len(players_getting_gains) == 1 else "ont", gains, "chacun" if len(players_getting_gains) > 1 else ""))
        print("================================================== \n")
        
    def game_over(self):
        if self.coop:
            for human in self.humans:
                if human.stack <= 0:
                    print("==================== GAME OVER ==================== \n")
                    print("L'ordinateur a remporté tous les jetons de chacun des joueurs! La partie est finie!")
                    return True
        else:
            for human in self.humans:
                if human.is_out():
                    self.humans.remove(human)
            if len(self.humans) == 0:
                print("==================== GAME OVER ==================== \n")
                print("L'ordinateur a remporté tous les jetons de chacun des joueurs! La partie est finie!")
                return True        
        return False

    def initialisation(self):
        self.welcome_msg() # Message de bienvenue
        self.set_mode() # Paramétrage du mode
        self.set_humans() # Génération des joueurs "humains"
        self.set_coop_mode() # Paramétrage du style de jeu

    def turn(self):
        self.humans_bet() # Mise
        self.distribution() # distribution des cartes
        self.status() # Affichage du status
        self.humans_turn() # Tour des humains
        self.computer_turn() # Tour de l'ordinateur
        self.set_ranking() # Génération du classement
        self.show_winner() # Affichage du gagnant
        self.set_gains() # Répartition des gains
        self.reset() # Reset des mains et du jeu

    def run(self):
        self.initialisation()
        while not self.game_over():
            self.turn()
        
        


       



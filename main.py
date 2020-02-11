from Game import Game
from SettingsPage import SettingsPage
from PlayersPage import PlayersPage
import pygame as pg

def die():
    import sys
    sys.exit()

def main():
  
    # game = Game()
    # game.run()

    game_title = 'Blackjack by Jaks'
    resolution = (800, 600)
    
    pg.init()
    screen = pg.display.set_mode(resolution)
    pg.display.set_caption(game_title)
    clock = pg.time.Clock()

    settings_page = SettingsPage('C:/Users/Utilisateur/Desktop/FORMATION/S5_1002-1602_/1102_mardi/blackjack/json/settings.json')


    done_settings = False
    done_generating_players = False
    running = True
    while running:

        # Tant que les paramètres n'ont pas été renseignés
        while done_settings == False:
            running, done_settings, game, players_count, stack = settings_page.settings_page(screen, clock)

        # Reset page
        screen.fill([30, 30, 30])
        pg.display.flip()
        players_page = PlayersPage('C:/Users/Utilisateur/Desktop/FORMATION/S5_1002-1602_/1102_mardi/blackjack/json/players.json', players_count)

        # Création des joueurs
        while done_generating_players == False:
            running, done_generating_players, players_name = players_page.players_page(screen, clock, players_count)

        # Génération des joueurs
        for name in players_name:
            
        
        # Reset page
        screen.fill([30, 30, 30])
        pg.display.flip()




        # Pour quitter le jeu    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

if __name__ == "__main__":
    main()
from Game import Game
from Settings import Settings
import pygame as pg

def die():
    import sys
    sys.exit()

def main():
  
    game = Game()
    game.run()

    # game_title = 'Blackjack by Jaks'
    # resolution = (800, 600)
    
    # pg.init()
    # screen = pg.display.set_mode(resolution)
    # pg.display.set_caption(game_title)
    # clock = pg.time.Clock()

    # settings = Settings('C:/Users/Utilisateur/Desktop/FORMATION/S5_1002-1602_/1102_mardi/blackjack/json/settings.json')

    # game = None
    # running = True
    # while running:
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             running = False
    #         if event.type == pg.MOUSEBUTTONDOWN:
    #             mouse = pg.mouse.get_pos()
    #             if settings.button.rect.collidepoint(mouse):
    #                 print("clicked")

    #                 mode = settings.fields[0]['input']['text']
    #                 players_count = settings.fields[1]['input']['text']
    #                 stack = settings.fields[2]['input']['text']
    #                 bet = settings.fields[3]['input']['text']
    #                 coop = settings.fields[4]['input']['text']

    #                 print(mode, players_count, stack, bet, coop)

    #             else:
    #                 for field in settings.fields:
    #                     field['input'] = settings.active(field['input'], event.pos)    
    #         if event.type == pg.KEYDOWN:
    #             for field in settings.fields:
    #                 if field['input']['active']:
    #                     if event.key == pg.K_BACKSPACE:
    #                         field['input']['text'] = field['input']['text'][:-1]
    #                     else:
    #                         field['input']['text'] += event.unicode

    #     settings.display(screen)
    #     pg.display.flip()
    #     clock.tick(30)
      

if __name__ == "__main__":
    main()
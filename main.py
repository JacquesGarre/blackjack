from Game import Game
from Settings import Settings
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

    settings = Settings('json/settings.json')

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if settings.button.rect.collidepoint(mouse):
                    print("clicked")
                else:
                    for field in settings.fields:
                        field['input'] = settings.active(field['input'], event.pos)    
            if event.type == pg.KEYDOWN:
                for field in settings.fields:
                    if field['input']['active']:
                        if event.key == pg.K_BACKSPACE:
                            field['input']['text'] = field['input']['text'][:-1]
                        else:
                            field['input']['text'] += event.unicode

        settings.display(screen)
        pg.display.flip()
        clock.tick(30)
      

if __name__ == "__main__":
    main()
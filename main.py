from Game import Game
import pygame as pg

def main():
    # game = Game()
    # game.run()

    game_title = 'Blackjack by Jaks'
    resolution = (800, 600)
    
    pg.init()
    screen = pg.display.set_mode(resolution)
    pg.display.set_caption(game_title)
    clock = pg.time.Clock()


    background_color = (30, 30, 30)
    
    title = {
        'x': 400,
        'y': 50,
        'bg_color': pg.Color('lightskyblue3'),
        'font_size': 32,
        'font_color': (30, 30, 30),
        'content': 'Paramètres'
    }

    fields = [{
        'label': {
            'x': 400,
            'y': 100,
            'bg_color': pg.Color('lightskyblue3'),
            'font_size': 25,
            'font_color': (30, 30, 30),
            'content': "Mode de jeu (EU / US)"
        },
        'input': {
            'rect': pg.Rect(300, 120, 140, 32),
            'color': pg.Color('lightskyblue3'),
            'active': False,
            'text': ''
        }
    },{
        'label': {
            'x': 400,
            'y': 200,
            'bg_color': pg.Color('lightskyblue3'),
            'font_size': 25,
            'font_color': (30, 30, 30),
            'content': "Nombre de joueurs (1 - 6)"
        },
        'input': {
            'rect': pg.Rect(300, 220, 140, 32),
            'color': pg.Color('lightskyblue3'),
            'active': False,
            'text': ''
        }
    },{     
        'label': {
            'x': 400,
            'y': 300,
            'bg_color': pg.Color('lightskyblue3'),
            'font_size': 25,
            'font_color': (30, 30, 30),
            'content': "Coopération (y / n)"
        },
        'input': {
            'rect': pg.Rect(300, 320, 140, 32),
            'color': pg.Color('lightskyblue3'),
            'active': False,
            'text': ''
        }
    }]




    def display_text(screen, text):
        font = pg.font.Font(None, text['font_size'])
        font_render = font.render(text['content'], True, text['bg_color'], text['font_color']) 
        text_rect = font_render.get_rect()
        text_rect.center = (text['x'], text['y']) 
        screen.blit(font_render, text_rect) 

    def active(field, pos):

        print(field)
        pass
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        active = False
        if field['rect'].collidepoint(pos):
            active = not active
        else:
            active = False
        return {
            'rect': field['rect'],
            'color': color_active if active else color_inactive,
            'active': active,
            'text': field['text']
        }

    def display_text_field(screen, field):
        text_field = field['rect']
        text_field_txt_surface = pg.font.Font(None, 32).render(field['text'], True, field['color'])
        text_field.w = max(200, text_field_txt_surface.get_width()+10)
        screen.blit(text_field_txt_surface, (text_field.x+5, text_field.y+5))
        pg.draw.rect(screen, field['color'], text_field, 2)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                for field in fields:
                    field['input'] = active(field['input'], event.pos)    
            if event.type == pg.KEYDOWN:
                for field in fields:
                    if field['input']['active']:
                        if event.key == pg.K_BACKSPACE:
                            field['input']['text'] = field['input']['text'][:-1]
                        else:
                            field['input']['text'] += event.unicode


        screen.fill(background_color)
        display_text(screen, title)
        for field in fields:
            display_text(screen, field['label'])
            display_text_field(screen, field['input'])

        pg.display.flip()
        clock.tick(30)
      

if __name__ == "__main__":
    main()
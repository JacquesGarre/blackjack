import pygame as pg
from Button import Button
from Game import Game
import json

class PlayersPage:

    def __init__(self, jsonfile, players_count):
        with open(jsonfile, encoding='utf-8') as json_file:
            data = json.load(json_file)        
        self.title = data['title']
        self.fields = self.generate_fields(players_count)
        self.bg_color = data['bg_color']
        self.btn_data = data['button']
        self.button = None
        self.players_count = players_count
    
    def generate_fields(self, count):
        fields_generated = []
        for i in range(count):
            field = {
                'label': 
                    {
                        'x': 400, 
                        'y': 80 + i * 70, 
                        'bg_color': [173, 216, 230], 
                        'font_size': 25, 
                        'font_color': [30, 30, 30], 
                        'content': 'Joueur ' + str(i + 1)
                    }, 
                'input': 
                    {
                        'rect': [300, 90 + i * 70, 140, 32],
                        'color': [173, 216, 230],
                        'active': 'False',
                        'text': ''
                    }
            }
            fields_generated.append(field)
        return fields_generated


    def display_text(self, screen, text):
        font = pg.font.Font(None, text['font_size'])
        font_render = font.render(text['content'], True, text['bg_color'], text['font_color']) 
        text_rect = font_render.get_rect()
        text_rect.center = (text['x'], text['y']) 
        screen.blit(font_render, text_rect) 

    def active(self, field, pos):
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        active = False
        if pg.Rect(field['rect']).collidepoint(pos):
            active = not active
        else:
            active = False
        return {
            'rect': field['rect'],
            'color': color_active if active else color_inactive,
            'active': active,
            'text': field['text']
        }

    def display_text_field(self, screen, field):
        text_field = pg.Rect(field['rect'])
        text_field_txt_surface = pg.font.Font(None, 32).render(field['text'], True, field['color'])
        text_field.w = max(200, text_field_txt_surface.get_width()+10)
        screen.blit(text_field_txt_surface, (text_field.x+5, text_field.y+5))
        pg.draw.rect(screen, field['color'], text_field, 2)

    def generate_button(self):
        data = self.btn_data
        button = Button(
            (data['x'], data['y']), 
            (data['w'], data['h']), 
            data['font_color'], 
            data['text'], 
            data['bg_color'], 
            data['font_size']
        ) 
        return button

    def display(self, screen):
        self.display_text(screen, self.title)
        for field in self.fields:
            self.display_text(screen, field['label'])
            self.display_text_field(screen, field['input'])
        self.button = self.generate_button()
        self.button.draw(screen)
    
    def validate_values(self):
        for field in self.fields:
            if len(field['input']['text']) < 2 and len(field['input']['text']) > 8:
                return False
        return True

    def players_page(self, screen, clock, players_count):
        running = True
        done_generating_players = False
        players_name = []
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done_generating_players = True
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                if self.button.rect.collidepoint(mouse):
                    print("clicked!")
                    if self.validate_values():
                        print('Entrées valides!')
                        done_generating_players = True
                        players_name = [field['input']['text'] for field in self.fields]
                    else:
                        print('Entrées invalides!')                
                else:
                    for field in self.fields:
                        field['input'] = self.active(field['input'], event.pos)    
            if event.type == pg.KEYDOWN:
                for field in self.fields:
                    if field['input']['active']:
                        if event.key == pg.K_BACKSPACE:
                            field['input']['text'] = field['input']['text'][:-1]
                        else:
                            field['input']['text'] += event.unicode
        self.display(screen)
        pg.display.flip()
        clock.tick(30)

        return running, done_generating_players, players_name
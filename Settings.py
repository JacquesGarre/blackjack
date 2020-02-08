import pygame as pg
from Button import Button
import json

class Settings:

    def __init__(self, jsonfile):
        with open(jsonfile, encoding='utf-8') as json_file:
            data = json.load(json_file)        
        self.title = data['title']
        self.fields = data['fields']
        self.bg_color = data['bg_color']
        self.btn_data = data['button']
        self.button = None

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

    def display(self, screen):
        screen.fill(self.bg_color)
        self.display_text(screen, self.title)
        for field in self.fields:
            self.display_text(screen, field['label'])
            self.display_text_field(screen, field['input'])
        data = self.btn_data
        button = Button(
            (data['x'], data['y']), 
            (data['w'], data['h']), 
            data['font_color'], 
            data['text'], 
            data['bg_color'], 
            data['font_size']
        )
        self.button = button
        button.draw(screen)

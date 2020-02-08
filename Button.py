import pygame as pg

class Button:

    def __init__(self, position, size, color, text, font_color, font_size):

        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = pg.Rect((0,0), size)
        font = pg.font.Font(None, font_size)
        text = font.render(text, True, font_color)
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.image.blit(text, text_rect)
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

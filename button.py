import pygame as pg

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, _image, _single_click, _id=None):
        pg.sprite.Sprite.__init__(self)
        self.image = _image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
        self.single_click = _single_click
        self.id = _id

    def draw(self, surface):
        position = pg.mouse.get_pos()
        action = False
        if self.rect.collidepoint(position):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                if self.single_click:
                    self.clicked = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surface.blit(self.image, self.rect)
        return action
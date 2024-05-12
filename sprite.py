import math
import os
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('sprites', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image.set_colorkey(image.get_at((49, 0)))
    else:
        image = image.convert_alpha()
    return image


class CustomSprite(pygame.sprite.Sprite):
    def __init__(self, image, groups, x, y, parent=None):
        super().__init__(*groups)
        self.original_image = self.image = image
        self.rect = self.image.get_rect().move(x, y)
        self.parent = parent

    def turn_right(self):
        self.image = pygame.transform.flip(self.original_image, True, False)

    def turn_left(self):
        self.image = pygame.transform.flip(self.original_image, False, False)

    def get_event(self, event):
        pass


class DamagableSprite(CustomSprite):
    def __init__(self, image, groups, x, y, hp=10, parent=None):
        super().__init__(image, groups, x, y, parent)
        self.original_image = image
        self.hp = self.max_hp = hp
        self.mixer = pygame.mixer
        self.mixer.init()
        self.am_sound = self.mixer.Sound("sounds/attack.mp3")

    def take_damage(self):
        damage = 0.1
        self.hp -= damage
        if self.hp % 1.5 < 0.01:
            self.am_sound.play()
        if self.hp <= 0:
            self.kill()
        else:
            self.image = pygame.transform.scale(self.original_image,
                                                (self.original_image.get_width() * self.hp / self.max_hp,
                                                 self.original_image.get_height() * self.hp / self.max_hp))
            self.rect = self.image.get_rect().move(self.rect.x, self.rect.y)

import pygame as pg
from pygame.math import Vector2
import math
import random
import time

import constants as c
from enemy_data import ENEMY_DATA

class Projectile(pg.sprite.Sprite):
    def __init__(self, _firing_turret, _target_enemy, _distance):
        pg.sprite.Sprite.__init__(self)
        self.firing_turret = _firing_turret
        self.original_image = self.firing_turret.projectile_image
        self.angle = self.firing_turret.angle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.target_enemy = _target_enemy
        self.rect = self.image.get_rect()
        self.target = Vector2(self.target_enemy.rect.center)
        self.distance = _distance
        self.position = Vector2(_firing_turret.rect.center)
        self.rect.center = self.position
        self.speed = self.firing_turret.projectile_speed
        self.damage = self.firing_turret.damage
        self.damage_type = self.firing_turret.damage_type
        self.effect = self.firing_turret.effect
        self.level = self.firing_turret.upgrade_level

    def update(self, world):
        self.move(world)

    def move(self, world):
        self.target = Vector2(self.target_enemy.rect.center)
        self.movement = self.target - self.position
        self.distance = self.movement.length()
        if self.distance >= self.speed * world.game_speed:
            if self.movement.length() != 0:
                self.position += self.movement.normalize() * self.speed * world.game_speed
        else:
            if self.distance != 0:
                if self.movement.length() != 0:
                    self.position += self.movement.normalize() * self.distance
                # self.target_enemy.hp -= self.damage
                self.apply_hit()
                self.kill()
        self.rect.center = self.position
        self.angle = math.degrees(math.atan2(self.position[1] - self.target_enemy.position[1], self.target_enemy.position[0] - self.position[0]))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        
    def apply_hit(self):
        if self.damage_type in self.target_enemy.resistance:
            self.damage = self.damage*c.RESISTANCE_MULT
        elif self.damage_type in self.target_enemy.vulnerability:
            self.damage = self.damage*c.VULNERABILITY_MULT
        self.target_enemy.hp -= (self.damage-(self.target_enemy.armor*self.damage))
        for effect in self.effect:
            if effect not in self.target_enemy.effect:
                self.target_enemy.effect.append(effect)
                self.target_enemy.effect_data.append((effect, pg.time.get_ticks(), self))

    # def apply_hit(self):
    #     if self.target_enemy.resistance == self.damage_type:
    #         self.damage = self.damage*c.RESISTANCE_MULT
    #     elif self.target_enemy.vulnerability == self.damage_type:
    #         self.damage = self.damage*c.VULNERABILITY_MULT
    #     self.target_enemy.hp -= (self.damage-(self.target_enemy.armor*self.damage))
    #     for effect in self.effect:
    #         if effect not in self.target_enemy.effect:
    #             self.target_enemy.effect.append(effect)
    #             self.target_enemy.effect_data.append((effect, pg.time.get_ticks(), self))

    # def move(self, world):
    #     self.target = Vector2(self.target_enemy.rect.center)
    #     self.movement = self.target - self.position
    #     self.distance = self.movement.length()
    #     if self.distance >= self.speed * world.game_speed:
    #         self.position += self.movement.normalize() * self.speed * world.game_speed
    #     else:
    #         if self.distance != 0:
    #             self.position += self.movement.normalize() * self.distance
    #             # self.target_enemy.hp -= self.damage
    #             self.apply_hit()
    #             self.kill()
    #     self.rect.center = self.position
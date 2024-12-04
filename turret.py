import pygame as pg
import math
from functools import partial

import constants as c
from turret_data import TURRET_DATA
from projectile import Projectile

class Turret(pg.sprite.Sprite):
    def __init__(self, _type, _tile_x, _tile_y, _projectile_group, _turret_group):
        pg.sprite.Sprite.__init__(self)
        self.type = _type
        print(self.type)
        self.type_data = TURRET_DATA[_type]
        self.name = _type.title()
        self.upgrade_level = 0
        self.upgrade_limit = len(self.type_data) - 1
        self.turret_group = _turret_group

        # self.sprite_sheets = _sprite_sheets
        self.original_image = pg.image.load(self.type_data[self.upgrade_level]["image"]).convert_alpha()
        self.projectile_image = pg.image.load(self.type_data[self.upgrade_level]["projectile_image"]).convert_alpha()

        self.projectile_group = _projectile_group

        self.angle = 0#90
        self.image = pg.transform.rotate(self.original_image, self.angle)

        self.rect = self.image.get_rect()
        self.tile_x = _tile_x
        self.tile_y = _tile_y
        self.x = (self.tile_x + .5) * c.TILE_SIZE
        self.y = (self.tile_y + .5) * c.TILE_SIZE
        self.rect.center = (self.x, self.y)

        self.selected = False
        self.range = self.type_data[self.upgrade_level]["range"]
        self.cooldown = self.type_data[self.upgrade_level]["cooldown"]
        self.damage = self.type_data[self.upgrade_level]["damage"]
        self.damage_type = self.type_data[self.upgrade_level]["damage_type"]
        self.effect = self.type_data[self.upgrade_level]["effect"]
        self.num_targets = self.type_data[self.upgrade_level]["num_of_targets_hit"]
        self.upgrade_cost = self.type_data[self.upgrade_level]["upgrade_cost"]
        self.cost = self.type_data[self.upgrade_level]["cost"]
        self.total_cost = self.cost
        self.projectile_speed = self.type_data[self.upgrade_level]["projectile_speed"]
        self.sfx = pg.mixer.Sound(self.type_data[self.upgrade_level]["projectile_sfx"])
        self.sfx_cooldown = 1000
        self.sfx_last_played = pg.time.get_ticks() - self.sfx_cooldown
        self.sfx.set_volume(.25)
        self.update_time = pg.time.get_ticks()
        self.last_shot = pg.time.get_ticks()-self.cooldown
        self.target = None

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0,0,0))
        self.range_image.set_colorkey((0,0,0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemy_group, _world):
        # if not self.target:
        if pg.time.get_ticks() - self.last_shot > self.cooldown / _world.game_speed:
            self.targeting(enemy_group, _world)
            # self.last_shot = pg.time.get_ticks()

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)  
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
        surface.blit(self.image, self.rect)

    def targeting(self, enemy_group, _world):
        x_dist = 0
        y_dist = 0
        targets = []
        target_ids = []
        for enemy in enemy_group:
            if len(targets) == self.num_targets:
                break
            if enemy.hp > 0 and enemy.id not in target_ids:
                x_dist = enemy.position[0] - self.x
                y_dist = enemy.position[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    targets.append(enemy)
                    target_ids.append(enemy.id)
        self.angle = math.degrees(math.atan2(-y_dist, x_dist))
        for enemy in targets:
            self.target = enemy
            projectile = Projectile(self, self.target, dist)
            self.projectile_group.add(projectile)
            self.last_shot = pg.time.get_ticks()
            if projectile and _world.sfx_data[self.type][1]:# and pg.time.get_ticks() - self.sfx_last_played > self.sfx_cooldown / _world.game_speed:
                self.sfx.play()
                self.sfx_last_played = pg.time.get_ticks()
                _world.sfx_data[self.type][0] += 1
                # print("inc")
        _world.sfx_manager()
        # print("ran manager")

    def sell(self, world):
        world.money += int((self.total_cost * c.TURRET_SELL_VALUE)//1)
        self.kill()

    def upgrade(self, world):
        if self.upgrade_level < self.upgrade_limit:
            world.money -= self.upgrade_cost
            self.upgrade_level += 1
            self.original_image = pg.image.load(self.type_data[self.upgrade_level]["image"]).convert_alpha()
            self.range = self.type_data[self.upgrade_level]["range"]
            self.cooldown = self.type_data[self.upgrade_level]["cooldown"]
            self.damage = self.type_data[self.upgrade_level]["damage"]
            self.damage_type = self.type_data[self.upgrade_level]["damage_type"]
            self.effect = self.type_data[self.upgrade_level]["effect"]
            self.num_targets = self.type_data[self.upgrade_level]["num_of_targets_hit"]
            self.total_cost += self.upgrade_cost
            self.upgrade_cost = self.type_data[self.upgrade_level]["upgrade_cost"]
            self.projectile_image = pg.image.load(self.type_data[self.upgrade_level]["projectile_image"]).convert_alpha()
            self.projectile_speed = self.type_data[self.upgrade_level]["projectile_speed"]
            # self.sfx = self.type_data[self.upgrade_level]["projectile_sfx"]
            self.range_image = pg.Surface((self.range * 2, self.range * 2))
            self.range_image.fill((0,0,0))
            self.range_image.set_colorkey((0,0,0))
            pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
            self.range_image.set_alpha(100)
            self.range_rect = self.range_image.get_rect()
            self.range_rect.center = self.rect.center
            world.undo_deck.append(partial(self.undo, world))

    def undo(self, world):
        if self in self.turret_group:
            if self.upgrade_level > 0:
                self.upgrade_level -= 1
                self.original_image = pg.image.load(self.type_data[self.upgrade_level]["image"]).convert_alpha()
                self.range = self.type_data[self.upgrade_level]["range"]
                self.cooldown = self.type_data[self.upgrade_level]["cooldown"]
                self.damage = self.type_data[self.upgrade_level]["damage"]            
                self.upgrade_cost = self.type_data[self.upgrade_level]["upgrade_cost"]
                self.total_cost -= self.upgrade_cost
                world.money += self.upgrade_cost

                self.range_image = pg.Surface((self.range * 2, self.range * 2))
                self.range_image.fill((0,0,0))
                self.range_image.set_colorkey((0,0,0))
                pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
                self.range_image.set_alpha(100)
                self.range_rect = self.range_image.get_rect()
                self.range_rect.center = self.rect.center
            else:
                world.money += self.cost
                self.kill()
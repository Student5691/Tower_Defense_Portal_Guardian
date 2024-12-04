import pygame as pg
from pygame.math import Vector2
import math
import random
import time

import constants as c
from enemy_data import ENEMY_DATA

class Enemy(pg.sprite.Sprite):
    def __init__(self, _enemy_type, _waypoints, _world):
        pg.sprite.Sprite.__init__(self)
        self.id = random.randint(0,65535)
        self.world = _world
        self.type = _enemy_type
        self.name = ENEMY_DATA[self.type[0]][self.type[1]]["name"]
        self.waypoints = _waypoints
        self.position = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.base_hp = ENEMY_DATA[self.type[0]][self.type[1]]["hp"]**c.DIFFICULTY_HP_POWER(self.world.level)
        self.hp = self.base_hp
        if ENEMY_DATA[self.type[0]][self.type[1]]["speed"] + c.DIFFICULTY_SPEED_ADD(self.world.level) < c.ENEMY_SPEED_CAP:
            self.base_speed = ENEMY_DATA[self.type[0]][self.type[1]]["speed"] + c.DIFFICULTY_SPEED_ADD(self.world.level)
        else:
            self.base_speed = c.ENEMY_SPEED_CAP
        self.speed = self.base_speed
        self.value = int(ENEMY_DATA[self.type[0]][self.type[1]]["value"]*c.DIFFICULTY_VALUE_MULT(self.world.level))
        if ENEMY_DATA[self.type[0]][self.type[1]]["armor"]*c.DIFFICULTY_ARMOR_MULT(self.world.level) < c.ENEMY_ARMOR_CAP:
            self.armor = ENEMY_DATA[self.type[0]][self.type[1]]["armor"]*c.DIFFICULTY_ARMOR_MULT(self.world.level)
        else:
            self.armor = c.ENEMY_ARMOR_CAP
        self.resistance = ENEMY_DATA[self.type[0]][self.type[1]]["dmg_resist"]
        self.vulnerability = ENEMY_DATA[self.type[0]][self.type[1]]["dmg_vulnerability"]
        self.effect = []
        self.effect_data = []
        self.dmg_over_time_counter = 0
        self.angle = 0
        self.original_image = pg.image.load(ENEMY_DATA[self.type[0]][self.type[1]]["image"]).convert_alpha()
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.spawn_time = time.time()
        self.selected = False

    def update(self, world):
        self.move(world)
        self.rotate()
        self.check_alive(world)
        self.implement_effect()

    def move(self, world):
        #define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.position
        else:
            #enemy has reach the final waypoint
            self.kill()
            world.missed_enemies += 1
            world.hp -= 1

        #calc distance to target
        distance = self.movement.length()
        if distance >= self.speed * world.game_speed:
            self.position += self.movement.normalize() * self.speed * world.game_speed
        else:
            if distance != 0:
                self.position += self.movement.normalize() * distance
            self.target_waypoint += 1

    def rotate(self):
        #calc distance to next waypoint
        distance = self.target - self.position
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def draw_hp(self, _surface):
        hp_ratio = (self.hp/self.base_hp)*self.rect.width
        x = self.position[0]-self.rect.width/2
        y = self.position[1]-self.rect.height/2-3
        pg.draw.rect(_surface, "black", (x, y, self.rect.width, 5))
        pg.draw.rect(_surface, "green", (x, y, hp_ratio, 5))
        if self.selected:
            pg.draw.rect(_surface, "orange", (self.position[0]-self.rect.width*1.3//2, self.position[1]-self.rect.height*1.3//2, self.rect.width*1.3, self.rect.height*1.3), 3)

    def check_alive(self, world):
        if self.hp <= 0:
            self.kill()
            world.killed_enemies += 1
            world.money += int(self.value)
            world.score += int(self.value)
    
    def implement_effect(self):
        if len(self.effect_data) == 0:
            return
        for effect in self.effect_data:
            if effect[0] == "dmg_over_time":
                if pg.time.get_ticks() > effect[1] + c.EFFECTS["dmg_over_time"]["interval_time"]*self.dmg_over_time_counter:
                    # self.hp -= c.EFFECTS["dmg_over_time"]["dmg_mult"]*effect[2].damage
                    self.hp -= c.EFFECTS["dmg_over_time"]["dmg_mult"]*(effect[2].level+1)*effect[2].damage
                    self.dmg_over_time_counter += 1
                if pg.time.get_ticks() > effect[1] + c.EFFECTS["dmg_over_time"]["duration"]:
                    self.effect.remove(effect[0])
                    self.effect_data.remove(effect)
                    self.dmg_over_time_counter = 0
            elif effect[0] == "slow":
                if pg.time.get_ticks() > effect[1] + c.EFFECTS["slow"]["duration"]:
                    self.effect.remove(effect[0])
                    self.effect_data.remove(effect)
                    self.speed = self.base_speed
                else:
                    self.speed = self.base_speed * (c.EFFECTS["slow"]["speed_mult"]/(effect[2].firing_turret.upgrade_level+1))
            elif effect[0] == "stun":
                if pg.time.get_ticks() > effect[1] + c.EFFECTS["stun"]["duration"]:
                    self.speed = self.base_speed
                else:
                    self.speed = 0
                if pg.time.get_ticks() > effect[1] + c.EFFECTS["stun"]["cooldown"]:
                    self.effect.remove(effect[0])
                    self.effect_data.remove(effect)
            elif effect[0] == "armor_pen":
                self.hp -= self.armor*effect[2].damage*c.ARMOR_PEN_EFFECTIVENESS
                self.effect.remove(effect[0])
                self.effect_data.remove(effect)
            else:
                print("error in implement_effect() of Enemy class from tower: ", effect[2].firing_turret.sfx, effect[0])


class Wandering_Enemy(Enemy):
    def __init__(self, _enemy_type, _waypoints, _world):
        super().__init__( _enemy_type, _waypoints, _world)
        self.create_waypoint_graph()
        self.position = Vector2(self.waypoints[random.randint(0, len(self.waypoints)-1)])
        self.position_key = self.waypoints[0]
        self.select_new_waypoint = True
        # self.base_hp = 20 * (_world.level+1)
        # self.hp = self.base_hp

    def update(self, world):
        super().update(world)
        self.self_destruct()

    def move(self, world):
        #define a target waypoint
        if self.select_new_waypoint:
            target_options = self.adj_list[self.position_key]
            n = len(target_options)
            target = random.randint(0, n//2)
            self.target_key = target_options[target]
            self.select_new_waypoint = False
            self.target = Vector2(target_options[target])
        
        self.movement = self.target - self.position

        #calc distance to target
        distance = self.movement.length()
        if distance >= self.speed * world.game_speed:
            self.position += self.movement.normalize() * self.speed * world.game_speed
        else:
            if distance != 0:
                self.position += self.movement.normalize() * distance
            self.select_new_waypoint = True
            self.position_key = self.target_key

    def create_waypoint_graph(self):
        random.shuffle(self.waypoints)
        self.adj_list = {}
        for i in self.waypoints:
            self.adj_list[i] = []
        n = len(self.waypoints)
        max_connections = n//2
        for j in self.waypoints:
            num_of_connections = random.randint(3, max_connections)
            connections = random.sample([x for x in self.waypoints if x != j], num_of_connections)
            self.adj_list[j] = connections

    def check_alive(self, world):
        if self.hp <= 0:
            self.kill()
            world.money += int(self.value * (1+(world.level/c.TOTAL_LEVELS)*2))
            world.score += int(self.value * (1+(world.level/c.TOTAL_LEVELS)*2))
    
    def self_destruct(self):
        if self.spawn_time < time.time() - 30:
            self.kill()
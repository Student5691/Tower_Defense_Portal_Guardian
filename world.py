import pygame as pg
import random
from collections import deque
from binarytree import Node

import constants as c
from enemy_data import ENEMY_SPAWN_DATA, ENEMY_DATA

class World():
    def __init__(self, data, map_image):
        self.tree = self.generate_tree(0, 7, [])
        # print(self.tree)
        self.tree_level = 0
        self.currentNode = self.tree
        self.leftNode = self.tree.left
        self.rightNode = self.tree.right
        
        self.level = 0
        self.level_group = self.currentNode.value
        self.enemy_category = c.ENEMY_CATEGORIES[self.level_group]
        self.spawn_data = ENEMY_SPAWN_DATA
        self.level_group_length = len(self.spawn_data[self.level_group])
        self.level_group_wave = 0
        self.game_speed = 1
        self.enemy_list = []
        self.hp = c.PLAYER_HP
        self.money = c.PLAYER_MONEY

        self.way_points = []
        self.level_data = data
        self.image = map_image

        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.score = 0

        self.sfx_data = {
            #[number of proj sfx activations, allowed to play sfx?, tick delay before allowing more sfx, num of ticks when sfx play authorization revoked]
            "archer": [0, True, 10000, 0],
            "crossbowman": [0, True, 1000, 0],
            "melee": [0, True, 1000, 0],
            "siege": [0, True, 1000, 0],
            "sniper": [0, True, 1000, 0],
            "fire": [0, True, 1000, 0],
            "frost": [0, True, 1000, 0],
            "poison": [0, True, 1000, 0],
            "electric": [0, True, 1000, 0]
        }
        # self.sfx_status = {
        #     "archer": True,
        #     "crossbowman": True,
        #     "melee": True,
        #     "siege": True,
        #     "sniper": True,
        #     "fire": True,
        #     "frost": True,
        #     "poison": True,
        #     "electric": True
        # }

        self.undo_deck = deque(maxlen=c.UNDO_MAX)

    def sfx_manager(self):
        for unit_type in self.sfx_data:
            data = self.sfx_data[unit_type]
            if data[0] > 2:
                if data[1] is True:
                    data[3] = pg.time.get_ticks()
                data[1] = False
            # print(pg.time.get_ticks() - data[3], " > ", data[2])
            if pg.time.get_ticks() - data[3] > data[2]:
                data[0] = 0
                data[1] = True
                print("TRUE")
        print(self.sfx_data["archer"], pg.time.get_ticks() - data[2])

    def process_data(self):
        x_offset = self.level_data["layers"][1]["objects"][0]["x"]
        y_offset = self.level_data["layers"][1]["objects"][0]["y"]
        coordinates = self.level_data["layers"][1]["objects"][0]["polyline"]
        for coord in coordinates:
            x = coord.get("x") + x_offset
            y = coord.get("y") + y_offset
            self.way_points.append((x, y))
        self.tile_map = self.level_data["layers"][0]["data"]

    def process_enemies(self):
        self.enemy_list = []
        self.enemy_category = c.ENEMY_CATEGORIES[self.level_group]
        enemies = ENEMY_SPAWN_DATA[self.level_group][self.level_group_wave]
        for i in range(len(enemies)):
            for specific_enemy in range(enemies[i]):
                self.enemy_list.append((self.enemy_category, i))
        random.shuffle(self.enemy_list)

    def check_level_complete(self):
        if self.killed_enemies + self.missed_enemies == len(self.enemy_list):
            return True

    def reset_level(self):
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.level_group = self.currentNode.value

    def draw(self, surface):
        surface.blit(self.image, (0,0))
    
    def generate_tree(self, current_level, max_level, used_values):
        if current_level == max_level:
            return None
        remaining_values = [i for i in range(max_level) if i not in used_values]
        value = remaining_values.pop(random.randint(0, len(remaining_values)-1))
        node = Node(value)
        node.left = self.generate_tree(current_level + 1, max_level, used_values + [value])
        node.right = self.generate_tree(current_level + 1, max_level, used_values + [value])
        return node

    def traverse_tree(self, choice):
        if self.tree_level < c.TOTAL_GROUPS-1:
            # self.tree_level += 1
            if choice == 0:
                self.currentNode = self.leftNode
                self.leftNode = self.currentNode.left
                self.rightNode = self.currentNode.right
            else:
                self.currentNode = self.rightNode
                self.leftNode = self.currentNode.left
                self.rightNode = self.currentNode.right
        else:
            if choice == 0:
                self.currentNode = self.leftNode
            else:
                self.currentNode = self.rightNode
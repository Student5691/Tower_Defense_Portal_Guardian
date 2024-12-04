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

        self.undo_deck = deque(maxlen=c.UNDO_MAX)

    def process_data(self):
        x_offset = self.level_data["layers"][1]["objects"][0]["x"]
        y_offset = self.level_data["layers"][1]["objects"][0]["y"]
        coordinates = self.level_data["layers"][1]["objects"][0]["polyline"]
        for coord in coordinates:
            x = coord.get("x") + x_offset
            y = coord.get("y") + y_offset
            self.way_points.append((x, y))
        self.tile_map = self.level_data["layers"][0]["data"]

    # def process_enemies(self):
    #     self.enemy_list = []
    #     enemies = ENEMY_SPAWN_DATA[self.level_group][self.level_group_wave]
    #     for enemy_type in enemies:
    #         for specific_enemy in range(len(enemies[enemy_type])):
    #             enemies_to_spawn = enemies[enemy_type][specific_enemy]
    #             for enemy in range(enemies_to_spawn):
    #                 self.enemy_list.append((enemy_type, specific_enemy))
    #     random.shuffle(self.enemy_list)

    def process_enemies(self):
        self.enemy_list = []
        self.enemy_category = c.ENEMY_CATEGORIES[self.level_group]
        enemies = ENEMY_SPAWN_DATA[self.level_group][self.level_group_wave]
        for i in range(len(enemies)):
            for specific_enemy in range(enemies[i]):
                self.enemy_list.append((self.enemy_category, i))
        random.shuffle(self.enemy_list)


        # for enemy_type in enemies:
        #     for specific_enemy in range(len(enemies[enemy_type])):
        #         enemies_to_spawn = enemies[enemy_type][specific_enemy]
        #         for enemy in range(enemies_to_spawn):
        #             self.enemy_list.append((enemy_type, specific_enemy))

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

    # def generate_tree(self, current_level, max_level, used_values):
    #     if current_level == max_level:
    #         return None
    #     remaining_values = [i for i in range(max_level) if i not in used_values]
    #     value = remaining_values.pop(random.randint(0, len(remaining_values)-1))
    #     node = Node(value)

    #     if remaining_values:  # Ensure there are values left to assign
    #         left_value = remaining_values.pop(random.randint(0, len(remaining_values) - 1))
    #         node.left = self.generate_tree(current_level + 1, max_level, used_values + [value, left_value])
    #     else:
    #         node.left = None

    #     if remaining_values:  # Ensure there are values left to assign
    #         right_value = remaining_values.pop(random.randint(0, len(remaining_values) - 1))
    #         node.right = self.generate_tree(current_level + 1, max_level, used_values + [value, right_value])
    #     else:
    #         node.right = None
        
    #     return node

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
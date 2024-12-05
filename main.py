import pygame as pg
import json
import random
import time
from functools import partial

import constants as c
from enemy import Enemy, Wandering_Enemy
from world import World
from turret import Turret
from button import Button
from turret_data import TURRET_DATA
from enemy_data import ENEMY_DATA

pg.init() # start the game
pg.mixer.init()

clock = pg.time.Clock() # define the clock

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT)) # create game window
pg.display.set_caption("Tower Defense")

#load JSON data for level
with open('levels\\level0.tmj') as file:
    world_data = json.load(file)

#load hiscores (list)
with open('data\\scores.txt', "r") as file:
    hiscores = []
    for line in file:
        score, name = line.strip().split(", ")
        hiscores.append((int(score), name))

#game variables
game_over = False
game_outcome = 0 # -1 is a loss and 1 is a win
level_started = False
volume = 1
spawn_cooldown = 800
placing_turrets = [[False, "archer"], [False, "crossbowman"], [False, "melee"], [False, "siege"], [False, "sniper"], [False, "fire"], [False, "frost"], [False, "poison"], [False, "electric"]] #list
selected_turret = None
selected_enemy = None
last_enemy_spawn = pg.time.get_ticks()
choice = None # tree path choice/enemy select
enemy_categories = ['Animals', 'Constructs', 'Draconic', 'Goblins', 'Humanoid', 'Monsters', 'Undead'] #list
user_name = "Anonymous"
temp_user_name = ''
typing = False

archer_sfx = pg.mixer.Sound(TURRET_DATA["archer"][0]["projectile_sfx"])
archer_sfx.set_volume(.2*volume)
crossbowman_sfx = pg.mixer.Sound(TURRET_DATA["crossbowman"][0]["projectile_sfx"])
crossbowman_sfx.set_volume(.2*volume)
melee_sfx = pg.mixer.Sound(TURRET_DATA["melee"][0]["projectile_sfx"])
melee_sfx.set_volume(.175*volume)
siege_sfx = pg.mixer.Sound(TURRET_DATA["siege"][0]["projectile_sfx"])
siege_sfx.set_volume(.2*volume)
sniper_sfx = pg.mixer.Sound(TURRET_DATA["sniper"][0]["projectile_sfx"])
sniper_sfx.set_volume(.1*volume)
fire_sfx = pg.mixer.Sound(TURRET_DATA["fire"][0]["projectile_sfx"])
fire_sfx.set_volume(.15*volume)
frost_sfx = pg.mixer.Sound(TURRET_DATA["frost"][0]["projectile_sfx"])
frost_sfx.set_volume(.2*volume)
poison_sfx = pg.mixer.Sound(TURRET_DATA["poison"][0]["projectile_sfx"])
poison_sfx.set_volume(.3*volume)
electric_sfx = pg.mixer.Sound(TURRET_DATA["electric"][0]["projectile_sfx"])
electric_sfx.set_volume(.175*volume)

sfx_data = { #hash and list
    #[specific sfx, play sound this tick?, seconds till next sfx iteration may be played, time when sfx was played for calculating next available sfx, is the sfx on cooldown?]
    "archer": [archer_sfx, False, TURRET_DATA["archer"][0]["cooldown"]/2000, 0, False],
    "crossbowman": [crossbowman_sfx, False, TURRET_DATA["crossbowman"][0]["cooldown"]/2000, 0, False],
    "melee": [melee_sfx, False, TURRET_DATA["melee"][0]["cooldown"]/2000, 0, False],
    "siege": [siege_sfx, False, TURRET_DATA["siege"][0]["cooldown"]/2000, 0, False],
    "sniper": [sniper_sfx, False, TURRET_DATA["sniper"][0]["cooldown"]/1500, 0, False],
    "fire": [fire_sfx, False, TURRET_DATA["fire"][0]["cooldown"]/2000, 0, False],
    "frost": [frost_sfx, False, TURRET_DATA["frost"][0]["cooldown"]/2000, 0, False],
    "poison": [poison_sfx, False, TURRET_DATA["poison"][0]["cooldown"]/2000, 0, False],
    "electric": [electric_sfx, False, TURRET_DATA["electric"][0]["cooldown"]/1000, 0, False]
}

#map
map_image = pg.image.load('levels\\level0.png').convert_alpha()
#buildable spaces
buildable_space = pg.image.load('assets\\buildable_space.png').convert_alpha()

#world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

#create groups to hold instances of classes
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
projectile_group = pg.sprite.Group()
button_turret_group = pg.sprite.Group()

#individual turret images for mouse cursor when placing turrets
cursor_turrets = [] #list
for i in range(9):
    if i == 0:
        name = "archer"
    elif i == 1:
        name = "crossbowman"
    elif i == 2:
        name = "melee"
    elif i == 3:
        name = "siege"
    elif i == 4:
        name = "sniper"
    elif i == 5:
        name = "fire"
    elif i == 6:
        name = "frost"
    elif i == 7:
        name = "poison"
    elif i == 8:
        name = "electric"
    turret_range = TURRET_DATA[name][0]["range"]
    turret_image = pg.image.load(TURRET_DATA[name][0]["image"]).convert_alpha()
    turret_rect = turret_image.get_rect()
    range_ring = pg.Surface((turret_range * 2, turret_range * 2))
    range_ring.fill((0,0,0))
    range_ring.set_colorkey((0,0,0))
    pg.draw.circle(range_ring, "grey100", (turret_range, turret_range), turret_range)
    range_ring.set_alpha(100)
    cursor_turrets.append([turret_image, range_ring, turret_range])

#UI details
coin_image = pg.image.load('assets\\coin.png').convert_alpha()
heart_image = pg.image.load('assets\\heart.png').convert_alpha()

tiny_font = pg.font.SysFont("Consolas", 14, bold = True)
small_font = pg.font.SysFont("Consolas", 16, bold = True)
med_font = pg.font.SysFont("Consolas", 22, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

#button images
buy_turret_images = [] #list
for i in range(9):
    buy_turret_images.append((pg.image.load(f'assets\\buttons\\towers\\button{i}.png').convert_alpha(), placing_turrets[i][1]))
cancel_image = pg.image.load('assets\\buttons\\cancel.png').convert_alpha()
upgrade_turret_image = pg.image.load('assets\\buttons\\upgrade_turret.png').convert_alpha()
sell_turret_image = pg.image.load('assets\\buttons\\sell.png').convert_alpha()
begin_image = pg.image.load('assets\\buttons\\begin.png').convert_alpha()
restart_image = pg.image.load('assets\\buttons\\restart.png').convert_alpha()
fast_forward_image = pg.image.load('assets\\buttons\\fast_forward.png').convert_alpha()
left_choice_image = pg.image.load('assets\\buttons\\left.png').convert_alpha()
right_choice_image = pg.image.load('assets\\buttons\\right.png').convert_alpha()
vol_up_image = pg.image.load('assets\\buttons\\vol_up.png').convert_alpha()
vol_down_image = pg.image.load('assets\\buttons\\vol_down.png').convert_alpha()
vol_icon_image = pg.image.load('assets\\buttons\\vol_icon.png').convert_alpha()
hiscores_image = pg.image.load('assets\\buttons\\hiscores.png').convert_alpha()

#create groups
enemy_group = pg.sprite.Group()
turret_group = pg.sprite.Group()
projectile_group = pg.sprite.Group()
button_turret_group = pg.sprite.Group()

#create buttons
buy_turret_buttons = [] #list
for i in range(len(buy_turret_images)):
    row = i % 4
    col = i // 4
    buy_turret_buttons.append(Button(c.SCREEN_WIDTH + 2 + (2+c.TILE_SIZE)*row, 550 + 2 + (2+c.TILE_SIZE)*col, buy_turret_images[i][0], True, buy_turret_images[i][1]))
    button_turret_group.add(buy_turret_buttons[i])
cancel_button = Button(c.SCREEN_WIDTH + 203, 686, cancel_image, True)
upgrade_turret_button = Button(c.SCREEN_WIDTH + 215, 330, upgrade_turret_image, True)
sell_turret_button = Button(c.SCREEN_WIDTH + 212, 215, sell_turret_image, True)
begin_button = Button(c.SCREEN_WIDTH + 179, 2, begin_image, True)
restart_button = Button(300, 300, restart_image, True)
fast_forward_button = Button(c.SCREEN_WIDTH + 179, 79, fast_forward_image, False)
left_button = Button(c.SCREEN_WIDTH + 5, 145, left_choice_image, True)
right_button = Button(c.SCREEN_WIDTH + 145, 145, right_choice_image, True)
vol_up_button = Button(c.SCREEN_WIDTH + 225, 870, vol_up_image, True)
vol_down_button = Button(c.SCREEN_WIDTH + 225, 930, vol_down_image, True)
hiscores_button = Button(c.SCREEN_WIDTH + 5, 920, hiscores_image, False) 

def draw_text(text, font, text_color, x, y):
    image = font.render(text, True, text_color)
    screen.blit(image, (x, y))

def display_data():
    pg.draw.rect(screen, "grey50", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 0, c.SIDE_PANEL, 206), 2)
    pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH, 173, c.SIDE_PANEL, 325), 2)
    draw_text("LEVEL: " + str(world.level+1),med_font, "grey100", c.SCREEN_WIDTH + 10, 10)
    screen.blit(heart_image, (c.SCREEN_WIDTH + 10, 35))
    draw_text(str(world.hp),med_font, "grey100", c.SCREEN_WIDTH + 40, 35)
    screen.blit(coin_image, (c.SCREEN_WIDTH + 10, 65))
    draw_text(str(world.money),med_font, "grey100", c.SCREEN_WIDTH + 40, 65)
    draw_text("SCORE: " + str(world.score), med_font, "grey100", c.SCREEN_WIDTH + 10, 95)
    draw_text("Adversary: " + enemy_categories[world.currentNode.value], small_font, "grey100", c.SCREEN_WIDTH+10, 120) 
    for i in range(len(buy_turret_images)):
        row = i % 4
        col = i // 4
        pg.draw.rect(screen, "grey0", (c.SCREEN_WIDTH + 2 + (2 + c.TILE_SIZE)*row, 550 + 2 + (2 + c.TILE_SIZE)*col, 65, 65), 2)
    screen.blit(vol_icon_image, (c.SCREEN_WIDTH + 165, 895))
    draw_text(str(int(volume*50)), tiny_font, "grey100", c.SCREEN_WIDTH + 234, 910)
    draw_text("Player:", small_font, "grey100", c.SCREEN_WIDTH + 5, 182)
    if typing:
        pg.draw.rect(screen, "black", (c.SCREEN_WIDTH+73, 173, 195, 33))
        draw_text(temp_user_name, med_font, "white", c.SCREEN_WIDTH + 75, 180)
    else:
        draw_text(user_name, med_font, "black", c.SCREEN_WIDTH + 75, 180)

def update_info_panel(item):
    if item is None:
        return
    img_size = (75, 75)
    if isinstance(item, Turret):
        data = item.type_data[item.upgrade_level]
        name = item.name
        image = pg.transform.scale(pg.image.load(data["image"]).convert_alpha(), img_size)
        damage = str(data["damage"])
        max_range = str(data["range"])
        time_between_shoots = str(data["cooldown"])
        damage_type = str(data["damage_type"])
        effect = '' 
        for i in range(len(data["effect"])):
            if len(data["effect"]) - i == 1:
                effect += c.EFFECTS[data["effect"][i]]['text']
            else:
                effect += c.EFFECTS[data["effect"][i]]['text'] + ', '
        if effect == '':
            effect = 'None'
        if data["num_of_targets_hit"] > 1:
            targets = str(data["num_of_targets_hit"])
        else:
            targets = '1'
        projectile_speed = str(data["projectile_speed"])
        if data["upgrade_cost"] == 0:
            upgrade_cost = 'MAX LEVEL'
        else:
            upgrade_cost = str(data["upgrade_cost"])
        screen.blit(image, (c.SCREEN_WIDTH + 2+image.get_width()//2, 212+image.get_height()//2))
        draw_text(name, med_font, "grey100", c.SCREEN_WIDTH + 7, 212)
        draw_text("Upgrade Cost: " + upgrade_cost, small_font, (255, 197, 7), c.SCREEN_WIDTH + 7, 340)
        draw_text("Damage: " + damage, small_font, "green", c.SCREEN_WIDTH + 7, 360)
        draw_text("Damage type: " + damage_type, small_font, "grey100", c.SCREEN_WIDTH + 7, 380)
        draw_text("Cooldown: " + time_between_shoots, small_font, "grey100", c.SCREEN_WIDTH + 7, 400)
        draw_text("Range: " + max_range, small_font, "grey100", c.SCREEN_WIDTH + 7, 420)
        draw_text("Multi Target: " + targets, small_font, "grey100", c.SCREEN_WIDTH + 7, 440)
        draw_text("Projectile Speed: " + projectile_speed, small_font, "grey100", c.SCREEN_WIDTH + 7, 460)
        draw_text("Effect: " + effect, small_font, "grey100", c.SCREEN_WIDTH + 7, 480)

    elif isinstance(item, Enemy):
        data = ENEMY_DATA[item.type[0]][item.type[1]]
        name = item.name
        image = pg.transform.scale(pg.image.load(data["image"]).convert_alpha(), img_size)
        hp = str(int(item.base_hp))
        speed = str(int(item.base_speed))
        armor = str(int(item.armor))
        resistances = ''
        for i in range(len(data["dmg_resist"])):
            if len(data["dmg_resist"]) - i == 1:
                resistances += c.DMG_TYPES[data["dmg_resist"][i]]
            else:
                resistances += c.DMG_TYPES[data["dmg_resist"][i]] + ', '
        if resistances == '':
            resistances = 'None'
        vulnerabilities = ''
        for i in range(len(data["dmg_vulnerability"])):
            if len(data["dmg_vulnerability"]) - i == 1:
                vulnerabilities += c.DMG_TYPES[data["dmg_vulnerability"][i]]
            else:
                vulnerabilities += c.DMG_TYPES[data["dmg_vulnerability"][i]] + ', '
        if vulnerabilities == '':
            vulnerabilities = 'None'
        value = str(int(item.value))
        screen.blit(image, (c.SCREEN_WIDTH + 2+image.get_width()//2, 212+image.get_height()//2))
        draw_text(name, med_font, "grey100", c.SCREEN_WIDTH + 7, 212)
        draw_text("Health: " + hp, small_font, "green", c.SCREEN_WIDTH + 7, 340)
        draw_text("Speed: " + speed, small_font, "grey100", c.SCREEN_WIDTH + 7, 360)
        draw_text("Armor: " + armor, small_font, "grey100", c.SCREEN_WIDTH + 7, 380)
        draw_text("Resistances:", small_font, "grey100", c.SCREEN_WIDTH + 7, 400)
        draw_text("  " + resistances, small_font, "grey100", c.SCREEN_WIDTH + 7, 420)
        draw_text("Vulnerabilities:", small_font, "grey100", c.SCREEN_WIDTH + 7, 440)
        draw_text("  " + vulnerabilities, small_font, "grey100", c.SCREEN_WIDTH + 7, 460)
        draw_text("Value: " + value, small_font, "grey100", c.SCREEN_WIDTH + 7, 480)

    elif isinstance(item, Button):
        data = TURRET_DATA[item.id][0]
        name = item.id.title()
        image = pg.transform.scale(pg.image.load(data["image"]).convert_alpha(), img_size)
        damage = str(data["damage"])
        max_range = str(data["range"])
        time_between_shoots = str(data["cooldown"])
        damage_type = str(data["damage_type"])
        effect = '' 
        for i in range(len(data["effect"])):
            if len(data["effect"]) - i == 1:
                effect += c.EFFECTS[data["effect"][i]]['text']
            else:
                effect += c.EFFECTS[data["effect"][i]]['text'] + ', '
        if effect == '':
            effect = 'None'
        if data["num_of_targets_hit"] > 1:
            targets = str(data["num_of_targets_hit"])
        else:
            targets = '1'
        projectile_speed = str(data["projectile_speed"])
        upgrade_cost = str(data["upgrade_cost"])
        cost = str(data["cost"])
        screen.blit(image, (c.SCREEN_WIDTH + 2+image.get_width()//2, 212+image.get_height()//2))
        draw_text(name, med_font, "grey100", c.SCREEN_WIDTH + 7, 212)
        draw_text("Cost: " + cost, small_font, (255, 197, 7), c.SCREEN_WIDTH + 7, 340)
        draw_text("Damage: " + damage, small_font, "green", c.SCREEN_WIDTH + 7, 360)
        draw_text("Damage type: " + damage_type, small_font, "grey100", c.SCREEN_WIDTH + 7, 380)
        draw_text("Cooldown: " + time_between_shoots, small_font, "grey100", c.SCREEN_WIDTH + 7, 400)
        draw_text("Range: " + max_range, small_font, "grey100", c.SCREEN_WIDTH + 7, 420)
        draw_text("Multi Target: " + targets, small_font, "grey100", c.SCREEN_WIDTH + 7, 440)
        draw_text("Projectile Speed: " + projectile_speed, small_font, "grey100", c.SCREEN_WIDTH + 7, 460)
        draw_text("Effect: " + effect, small_font, "grey100", c.SCREEN_WIDTH + 7, 480)

    elif type(item) is str:
        data = TURRET_DATA[item][0]
        name = item.title()
        image = pg.transform.scale(pg.image.load(data["image"]).convert_alpha(), img_size)
        damage = str(data["damage"])
        max_range = str(data["range"])
        time_between_shoots = str(data["cooldown"])
        damage_type = str(data["damage_type"])
        effect = '' 
        for i in range(len(data["effect"])):
            if len(data["effect"]) - i == 1:
                effect += c.EFFECTS[data["effect"][i]]['text']
            else:
                effect += c.EFFECTS[data["effect"][i]]['text'] + ', '
        if effect == '':
            effect = 'None'
        if data["num_of_targets_hit"] > 1:
            targets = str(data["num_of_targets_hit"])
        else:
            targets = '1'
        projectile_speed = str(data["projectile_speed"])
        cost = str(data["cost"])
        screen.blit(image, (c.SCREEN_WIDTH + 2+image.get_width()//2, 212+image.get_height()//2))
        draw_text(name, med_font, "grey100", c.SCREEN_WIDTH + 7, 212)
        draw_text("Cost: " + cost, small_font, (255, 197, 7), c.SCREEN_WIDTH + 7, 340)
        draw_text("Damage: " + damage, small_font, "green", c.SCREEN_WIDTH + 7, 360)
        draw_text("Damage type: " + damage_type, small_font, "grey100", c.SCREEN_WIDTH + 7, 380)
        draw_text("Cooldown: " + time_between_shoots, small_font, "grey100", c.SCREEN_WIDTH + 7, 400)
        draw_text("Range: " + max_range, small_font, "grey100", c.SCREEN_WIDTH + 7, 420)
        draw_text("Multi Target: " + targets, small_font, "grey100", c.SCREEN_WIDTH + 7, 440)
        draw_text("Projectile Speed: " + projectile_speed, small_font, "grey100", c.SCREEN_WIDTH + 7, 460)
        draw_text("Effect: " + effect, small_font, "grey100", c.SCREEN_WIDTH + 7, 480)
    else:
        print('display_details() function error')

def mouseover_details():
    mouseover_position = pg.mouse.get_pos()
    item_to_display = None
    if selected_turret:
        item_to_display = selected_turret
    elif selected_enemy:
        item_to_display = selected_enemy
    elif any(i[0] for i in placing_turrets): #search
        for i in range(len(placing_turrets)):
            if placing_turrets[i][0]:
                item_to_display = placing_turrets[i][1]
    for turret in turret_group:
        if turret.rect.collidepoint(mouseover_position):
            item_to_display = turret
    for enemy in enemy_group:
        if enemy.rect.collidepoint(mouseover_position):
            item_to_display = enemy
    for button in button_turret_group:
        if button.rect.collidepoint(mouseover_position):
            item_to_display = button
    update_info_panel(item_to_display)

def create_turret(mouse_position, _turret_group):
    mouse_tile_x = mouse_position[0] // c.TILE_SIZE
    mouse_tile_y = mouse_position[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 25: #search
        space_is_free = True
        for turret in turret_group:
            if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
                space_is_free = False
        if space_is_free == True:
            for i in placing_turrets:
                if i[0] == True:
                    turret = Turret(i[1], mouse_tile_x, mouse_tile_y, projectile_group, _turret_group, sfx_data)
                    if turret.cost <= world.money:
                        turret_group.add(turret)
                        world.money -= turret.cost
                        world.undo_deck.append(partial(turret.undo, world)) #append to deque
                    else:
                        turret.kill()

def select_turret(mouse_position):
    mouse_tile_x = mouse_position[0] // c.TILE_SIZE
    mouse_tile_y = mouse_position[1] // c.TILE_SIZE
    for turret in turret_group: #search
        if (mouse_tile_x, mouse_tile_y) == (turret.tile_x, turret.tile_y):
            clear_enemy_selection()
            return turret
        
def select_enemy(mouse_position):
    for enemy in enemy_group: #search
        if enemy.rect.collidepoint(mouse_position):
            clear_turret_selection()
            enemy.selected = True
            return enemy
        
def clear_turret_selection():
    for turret in turret_group:
        turret.selected = False
    return None

def clear_enemy_selection():
    for enemy in enemy_group:
        enemy.selected = False
    return None

def process_wandering_waypoints():
        x_offset = wandering_waypoints_data["x"]
        y_offset = wandering_waypoints_data["y"]
        coordinates = wandering_waypoints_data["polyline"]
        for coord in coordinates:
            x = coord.get("x") + x_offset
            y = coord.get("y") + y_offset
            wandering_waypoints.append((x, y))

def next_track(index):
    if index < len(background_audio_playlist):
        pg.mixer.music.load(background_audio_playlist[index])
        pg.mixer.music.play()
        return index + 1
    return 0

def update_volume():
    archer_sfx.set_volume(.2*volume)
    crossbowman_sfx.set_volume(.2*volume)
    melee_sfx.set_volume(.175*volume)
    siege_sfx.set_volume(.2*volume)
    sniper_sfx.set_volume(.15*volume)
    fire_sfx.set_volume(.15*volume)
    frost_sfx.set_volume(.2*volume)
    poison_sfx.set_volume(.2*volume)
    electric_sfx.set_volume(.25*volume)
    pg.mixer.music.set_volume(0.2*volume)

def save_hiscore():
    with open('data\\scores.txt', "r") as file:
        scores = []
        for line in file:
            score, name = line.strip().split(", ")
            scores.append((int(score), name))
    scores.append((world.score, user_name))
    scores.sort(key=lambda x:x[0], reverse=True)
    scores = scores[:10]
    with open('data\\scores.txt', "w") as file:
        for score, name in scores:
            file.write(f"{score}, {name}\n")

def display_hiscores():
    dimension_x = 295
    dimension_y = 305
    top_left_corner_x = c.SCREEN_WIDTH-dimension_x
    top_left_corner_y = c.SCREEN_HEIGHT-dimension_y
    pg.draw.rect(screen, "black", (top_left_corner_x, top_left_corner_y, dimension_x, dimension_y), border_radius = 30)
    draw_text("Leader Board", large_font, "grey100", top_left_corner_x+15, top_left_corner_y+15)
    for i in range(len(hiscores)):
        if i == 0:
            color = (255, 197, 7) # gold
        elif i == 1:
            color = (208, 211, 226) # silver
        elif i == 2:
            color = (197, 90, 0) # bronze
        else:
            color = "grey40"
        draw_text(str(hiscores[i][0]), med_font, color, top_left_corner_x + 15, top_left_corner_y+60+i*23)
        draw_text(hiscores[i][1], med_font, color, top_left_corner_x + 120, top_left_corner_y+60+i*23)

#background music, multiple tracks
audio_path = r"assets\\audio\\bgMusic\\"
background_audio_playlist = [] #list
for i in range(10):
    background_audio_playlist.append(audio_path + str(i) + ".mp3")
random.shuffle(background_audio_playlist)
AUDIO_TRACK_END = pg.USEREVENT + 1
pg.mixer.music.set_endevent(AUDIO_TRACK_END)
pg.mixer.music.set_volume(0.2*volume)
current_track_index = next_track(0) #begin first track

wandering_waypoints_data = world_data["layers"][2]["objects"][0]
wandering_waypoints = [] #list
process_wandering_waypoints()
spawn_wandering_enemy_timer = time.time()

#world
world = World(world_data, map_image)
world.process_data()
world.process_enemies()

run = True # should the game continue running?
while run: #main game loop
    clock.tick(c.FPS) # set framerate cap

    if game_over == False:
        if world.hp <= 0:
            game_over = True
            game_outcome = -1
        
        if world.level > c.TOTAL_LEVELS-1:
            world.level -= 1 # keeps level display text accurate
            game_over = True
            game_outcome = 1
        
        #update groups
        enemy_group.update(world)
        turret_group.update(enemy_group, world)
        projectile_group.update(world)

        #turret/enemy selection if a turret is selected, update teh turret's "selected" member to True
        if selected_turret:
            selected_turret.selected = True
        if selected_enemy:
            selected_enemy.selected = True

    #draw map
    world.draw(screen)

    #draw groups
    enemy_group.draw(screen)
    for enemy in enemy_group:
        enemy.draw_hp(screen)

    projectile_group.draw(screen)

    for turret in turret_group:
        turret.draw(screen)

    display_data()
    mouseover_details()

    if game_over == False:
        if level_started == False:
            world.game_speed = 1 #avoids fast-forward getting stuck upon level completion by resetting world speed
            #player choice using binary tree
            if choice is None and world.tree_level > 0 and enemy_categories[world.leftNode.value] != enemy_categories[world.rightNode.value]:
                curText0 = enemy_categories[world.leftNode.value]
                curText1 = enemy_categories[world.rightNode.value]
                if left_button.draw(screen):
                    choice = 0
                    world.traverse_tree(choice)
                    world.level_group = world.currentNode.value
                    world.level_group_length = len(world.spawn_data[world.level_group])
                    world.process_enemies()
                if right_button.draw(screen):
                    choice = 1
                    world.traverse_tree(choice)
                    world.level_group = world.currentNode.value
                    world.level_group_length = len(world.spawn_data[world.level_group])
                    world.process_enemies()
                draw_text(curText0, small_font, "grey100", c.SCREEN_WIDTH + 15, 150)
                draw_text(curText1, small_font, "grey100", c.SCREEN_WIDTH + 160, 150)
            elif choice is None and world.tree_level > 0 and enemy_categories[world.leftNode.value] == enemy_categories[world.rightNode.value]:
                curText0 = enemy_categories[world.leftNode.value]
                if left_button.draw(screen):
                    choice = 0
                    world.traverse_tree(choice)
                    world.level_group = world.currentNode.value
                    world.level_group_length = len(world.spawn_data[world.level_group])
                    world.process_enemies()
                draw_text(curText0, small_font, "grey100", c.SCREEN_WIDTH + 15, 150)
            if choice is not None or world.tree_level == 0:
                if begin_button.draw(screen):
                    level_started = True
        else:
            if fast_forward_button.draw(screen):
                world.game_speed = c.FAST_FORWARD_SPEED
            else:
                world.game_speed = 1
            #spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > spawn_cooldown / world.game_speed:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.way_points, world)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()
        #sfx manager to prevent annoying spamming sfx
        for unit_type in sfx_data:
            data = sfx_data[unit_type]
            if data[1] is True:
                data[0].play()
                data[1] = False
                data[3] = time.time()
                data[4] = True
            if time.time() > data[3] + data[2] and data[1] is False:
                # data[1] = True
                data[3] = 0
                data[4] = False

        if world.check_level_complete() == True:
            world.money += c.LEVEL_COMPLETE_REWARD*(world.level+1)
            world.level += 1
            world.level_group_wave += 1
            if world.level_group_wave > world.level_group_length-1:
                world.level_group_wave = 0
                world.tree_level += 1
                choice = None
            else:
                world.process_enemies()
            if world.level > c.TOTAL_LEVELS-1: #final level complete, "continue" applies to the main game while loop to move to end-game screen
                continue
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            level_started = False

        for i in range(9):
            if buy_turret_buttons[i].draw(screen):
                placing_turrets[i][0] = True
                for k in range(9):
                    if k != i:
                        placing_turrets[k][0] = False

        for j in range(9): #turret placing UI
            if placing_turrets[j][0] == True:
                for i in range(len(world.tile_map)): #linear search to draw highlight boxes
                    if world.tile_map[i] == 25:
                        x = ((i%c.COLS)+.5) * c.TILE_SIZE
                        y = ((i//c.COLS)+.5) * c.TILE_SIZE
                        buildable_space_rect = buildable_space.get_rect()
                        buildable_space_rect.center = (x,y)
                        screen.blit(buildable_space, buildable_space_rect)
                cursor_rect = cursor_turrets[j][0].get_rect()
                cursor_position = pg.mouse.get_pos()
                cursor_rect.center = ((cursor_position[0]//c.TILE_SIZE + .5) * c.TILE_SIZE, (cursor_position[1]//c.TILE_SIZE + .5) * c.TILE_SIZE) #snap to grid
                if cursor_position[0] < c.SCREEN_WIDTH:
                    screen.blit(cursor_turrets[j][1], (cursor_rect[0]-cursor_turrets[j][2]+cursor_rect[2]/2, cursor_rect[1]-cursor_turrets[j][2]+cursor_rect[2]/2))
                    screen.blit(cursor_turrets[j][0], cursor_rect)
                if cancel_button.draw(screen):
                    placing_turrets[j][0] = False
        #upgrading and selling turrets
        if selected_turret:
            if selected_turret.upgrade_level < selected_turret.upgrade_limit:
                if upgrade_turret_button.draw(screen):
                    print("button Pressed")
                    if world.money >= selected_turret.upgrade_cost:
                        print("eneough money!")
                        selected_turret.upgrade(world)
            if sell_turret_button.draw(screen):
                selected_turret.sell(world)
                selected_turret = None
        #volume control
        if vol_up_button.draw(screen):
            if volume < 2:
                volume *= 100
                volume += 10
                volume /= 100
                update_volume()
        if vol_down_button.draw(screen):
            if volume > 0:
                volume *= 100
                volume -= 10
                volume /= 100
                update_volume()
        #hiscores UI
        if hiscores_button.draw(screen):
            display_hiscores()
    #game over
    else:
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("You WIN", large_font, "grey0", 310, 230)
        if restart_button.draw(screen): # rests level is restart button pressed
            save_hiscore()
            with open('data\\scores.txt', "r") as file: #update hiscores UI, players score will appear if it achieved top 10
                hiscores = []
                for line in file:
                    score, name = line.strip().split(", ")
                    hiscores.append((int(score), name))
            world.score = 0
            game_over = False
            level_started = False
            for i in range(9):
                placing_turrets[i][0] = False
            clear_turret_selection()
            clear_enemy_selection()
            last_enemy_spawn = pg.time.get_ticks()
            world = World(world_data, map_image)
            world.process_data()
            world.process_enemies()
            enemy_group.empty()
            turret_group.empty()
            projectile_group.empty()

    if 1 == random.randint(0,40000): #user of graph
        reaper = Wandering_Enemy(("reaper", 0), wandering_waypoints, world)
        enemy_group.add(reaper)
        spawn_wandering_enemy_timer = time.time()

    # event handlers
    for event in pg.event.get():
        #quit program
        if event.type == pg.QUIT:
            run = False
        #mouse click (left)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_position = pg.mouse.get_pos()
            if mouse_position[0] < c.SCREEN_WIDTH and mouse_position[1] < c.SCREEN_HEIGHT:
                #clear selected turrets
                selected_turret = clear_turret_selection()
                selected_enemy = clear_enemy_selection()
                if any(i[0] for i in placing_turrets):
                    create_turret(mouse_position, turret_group)
                else:
                    selected_turret = select_turret(mouse_position)
                    selected_enemy = select_enemy(mouse_position)
        #mouse click (right)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3: # clear turret placement bools, turret selection, or enemy selection
            selected_turret = clear_turret_selection()
            selected_enemy = clear_enemy_selection()
            for i in range(9):
                placing_turrets[i][0] = False
        #background music check
        if event.type == AUDIO_TRACK_END:
            current_track_index = next_track(current_track_index)
        keys = pg.key.get_pressed()
        if event.type == pg.KEYDOWN and not typing:
            if event.key == pg.K_m:
                world.money += 1000 #cheat
            if event.key == pg.K_h:
                world.hp += 10 #cheat
            if keys[pg.K_z] and keys[pg.K_LCTRL]: #control-z / undo a number of tower builds and/or upgrades equal to the corresponding value in constants.py - deque implementation
                try:
                    func = world.undo_deck.pop()
                    func()
                    selected_turret = clear_turret_selection()
                except:
                    pass
            if event.key == pg.K_RETURN:
                typing = True
        elif event.type == pg.KEYDOWN and typing: # username update
            if event.unicode.isalnum():
                temp_user_name += event.unicode
            elif event.key == pg.K_BACKSPACE:
                temp_user_name = temp_user_name[:-1]
            elif event.key == pg.K_RETURN:
                user_name = temp_user_name
                temp_user_name = ''
                typing = False
    #update display
    pg.display.flip()
#save highscore upon close
save_hiscore()
pg.quit()
from enemy_data import ENEMY_SPAWN_DATA

ROWS = 15
COLS = 24
TILE_SIZE = 65
SIDE_PANEL = 270
SCREEN_WIDTH = COLS * TILE_SIZE
SCREEN_HEIGHT = ROWS * TILE_SIZE
FPS = 60

#SPAWN_COOLDOWN = 800 ### not properly affected by game speed up

PLAYER_HP = 100
PLAYER_MONEY = 100

# BUY_COST = 200
# UPGRADE_COST = 100

TURRET_DMG = 2

KILL_REWARD = 1
LEVEL_COMPLETE_REWARD = 20

level_count = 0
level_group_count = 0
for i in range(len(ENEMY_SPAWN_DATA)):
    level_group_count += 1
    level_count += len(ENEMY_SPAWN_DATA[i])

TOTAL_LEVELS = level_count
TOTAL_GROUPS = level_group_count

FAST_FORWARD_SPEED = 10

WANDERING_SPAWN_RATE = 5

UNDO_MAX = 10

TURRET_SELL_VALUE = 0.75

VULNERABILITY_MULT = 1.2
RESISTANCE_MULT = 0.8
ENEMY_SPEED_CAP = 6
ENEMY_ARMOR_CAP = 0.8

EFFECTS = {
    "dmg_over_time": {"dmg_mult": .05, "duration": 2000, "interval_time": 100, 'text': 'DoT'}, # higher mg_mult, higer damage done
    "slow": {"speed_mult": .0, "duration": 10000, 'text': "Slow"}, # the lower speed_mult, the slower the enemies go
    "stun": {"cooldown": 8000,"duration": 2000, 'text': "Stun"},
    "armor_pen": {"armor_mult": 1.2, "duration": 0, 'text': "Armor Pen"}, # the higher armor_mult, more dmg
}
ARMOR_PEN_EFFECTIVENESS = .5 #high numbers are more effective, 1 for no change, 0 to nullify the effect, negative values heal the target, values between 0 and 1 (exclusive) to dampen the effect

ENEMY_CATEGORIES = ['animal', 'construct', 'dragon', 'goblin', 'humanoid', 'monstrous', 'undead']

DMG_TYPES = {"electric": "Electric", "fire": "Fire", "frost": "Cold", "heavy": "Heavy", "pierce": "Piercing", "poison": "Poison", "ranged": "Ranged", "slash": "Slashing"}

TURRET_LIST = ["archer", "crossbowman", "melee", "siege", "sniper", "fire", "frost", "poison", "electric"]

def DIFFICULTY_HP_POWER(level):
    return (1 + level/TOTAL_LEVELS)

def DIFFICULTY_SPEED_ADD(level):
    return ((level/TOTAL_LEVELS)*2)

def DIFFICULTY_ARMOR_MULT(level):
    return (1 + (level/TOTAL_LEVELS)*3)

def DIFFICULTY_VALUE_MULT(level):
    return (1 + (level/TOTAL_LEVELS))
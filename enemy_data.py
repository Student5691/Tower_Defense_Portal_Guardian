#Index of the outer list corresponds to a specific enemy category as laid out in constants.py.
#Index of the inner lists is the wave, and index of the innermost list corresponds to the specific enemy variant.
ENEMY_SPAWN_DATA = [
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ],
    [
        [20], [20, 5], [15, 10, 5], [15, 10, 10, 5]
    ]
]

ENEMY_DATA = {
    "animal": [
        {
            "name": "Large Snake",
            "hp": 100,
            "speed": 2.5,
            "armor": 0.05,
            "dmg_resist": ["poison"],
            "dmg_vulnerability": ["slash"],
            "image": 'assets\\enemy\\animal\\animal0.png',
            "value": 2
        },
        {
            "name": "Enraged Croc",
            "hp": 150,
            "speed": 2,
            "armor": .3,
            "dmg_resist": ["slash"],
            "dmg_vulnerability": ["pierce"],
            "image": 'assets\\enemy\\animal\\animal1.png',
            "value": 2
        },
        {
            "name": "Great Ape",
            "hp": 200,
            "speed": 2,
            "armor": .1,
            "dmg_resist": [],
            "dmg_vulnerability": ["poison"],
            "image": 'assets\\enemy\\animal\\animal2.png',
            "value": 2
        },
        {
            "name": "Grizzly",
            "hp": 250,
            "speed": 3,
            "armor": .2,
            "dmg_resist": [],
            "dmg_vulnerability": ["poison"],
            "image": 'assets\\enemy\\animal\\animal3.png',
            "value": 2
        },
    ],
    "construct": [
        {
            "name": "Gargoyle",
            "hp": 75,
            "speed": 3,
            "armor": .1,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": ["heavy", "fire", "electric"],
            "image": 'assets\\enemy\\construct\\construct0.png',
            "value": 2
        },
        {
            "name": "Living Armor",
            "hp": 100,
            "speed": 2,
            "armor": .2,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": ["heavy", "fire", "electric"],
            "image": 'assets\\enemy\\construct\\construct1.png',
            "value": 2
        },
        {
            "name": "Dwarven Automaton",
            "hp": 150,
            "speed": 2.5,
            "armor": .3,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": ["heavy", "fire", "electric"],
            "image": 'assets\\enemy\\construct\\construct2.png',
            "value": 2
        },
        {
            "name": "Steel Prowler",
            "hp": 200,
            "speed": 3,
            "armor": .4,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": ["heavy", "fire", "electric"],
            "image": 'assets\\enemy\\construct\\construct3.png',
            "value": 2
        },
    ],
    "dragon": [
        {
            "name": "Kobold",
            "hp": 100,
            "speed": 2,
            "armor": .05,
            "dmg_resist": [],
            "dmg_vulnerability": ["pierce", "frost", "heavy"],
            "image": 'assets\\enemy\\dragon\\dragon0.png',
            "value": 2
        },
        {
            "name": "Dragonborn",
            "hp": 150,
            "speed": 1.75,
            "armor": .25,
            "dmg_resist": ["fire", "poison"],
            "dmg_vulnerability": ["pierce", "frost", "heavy"],
            "image": 'assets\\enemy\\dragon\\dragon1.png',
            "value": 2
        },
        {
            "name": "Dragon Scout",
            "hp": 225,
            "speed": 3,
            "armor": .2,
            "dmg_resist": ["fire", "poison"],
            "dmg_vulnerability": ["pierce", "frost", "heavy", "electric"],
            "image": 'assets\\enemy\\dragon\\dragon2.png',
            "value": 2
        },
        {
            "name": "Green Dragon",
            "hp": 275,
            "speed": 2,
            "armor": .3,
            "dmg_resist": ["fire", "poison"],
            "dmg_vulnerability": ["pierce", "frost", "heavy"],
            "image": 'assets\\enemy\\dragon\\dragon3.png',
            "value": 2
        },
    ],
    "goblin": [
        {
            "name": "Goblin",
            "hp": 100,
            "speed": 2,
            "armor": 0.05,
            "dmg_resist": ["frost"],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\goblin\\goblin0.png',
            "value": 2
        },
        {
            "name": "Saboteur",
            "hp": 75,
            "speed": 4,
            "armor": 0.01,
            "dmg_resist": ["poison"],
            "dmg_vulnerability": ["slash"],
            "image": 'assets\\enemy\\goblin\\goblin1.png',
            "value": 2
        },
        {
            "name": "Berserker",
            "hp": 195,
            "speed": 2.5,
            "armor": .2,
            "dmg_resist": ["ranged", "pierce", "slash", "frost"],
            "dmg_vulnerability": ["fire"],
            "image": 'assets\\enemy\\goblin\\goblin2.png',
            "value": 2
        },
        {
            "name": "Shaman",
            "hp": 155,
            "speed": 2,
            "armor": .1,
            "dmg_resist": ["fire", "frost", "poison", "electric"],
            "dmg_vulnerability": ["slash"],
            "image": 'assets\\enemy\\goblin\\goblin3.png',
            "value": 2
        },
    ],
    "humanoid": [
        {
            "name": "Gnoll Warrior",
            "hp": 120,
            "speed": 2,
            "armor": 0.05,
            "dmg_resist": ["slash"],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\humanoid\\humanoid0.png',
            "value": 2
        },
        {
            "name": "Bugbear Bruiser",
            "hp": 175,
            "speed": 1.8,
            "armor": .1,
            "dmg_resist": [],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\humanoid\\humanoid1.png',
            "value": 2
        },
        {
            "name": "Werebear",
            "hp": 225,
            "speed": 1.9,
            "armor": .1,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\humanoid\\humanoid2.png',
            "value": 2
        },
        {
            "name": "Werewolf",
            "hp": 200,
            "speed": 3.5,
            "armor": 0.05,
            "dmg_resist": ["ranged", "pierce", "slash", "poison"],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\humanoid\\humanoid3.png',
            "value": 2
        },
    ],
    "monstrous": [
        {
            "name": "Winged Horror",
            "hp": 75,
            "speed": 3,
            "armor": .05,
            "dmg_resist": ["ranged", "pierce"],
            "dmg_vulnerability": ["electric"],
            "image": 'assets\\enemy\\monstrous\\monstrous0.png',
            "value": 2
        },
        {
            "name": "Hellhound",
            "hp": 125,
            "speed": 2.5,
            "armor": .1,
            "dmg_resist": ["fire", "poison"],
            "dmg_vulnerability": ["frost", "heavy"],
            "image": 'assets\\enemy\\monstrous\\monstrous1.png',
            "value": 2
        },
        {
            "name": "Slug Thing",
            "hp": 175,
            "speed": 1.75,
            "armor": .2,
            "dmg_resist": ["poison", "ranged"],
            "dmg_vulnerability": ["slash", "heavy"],
            "image": 'assets\\enemy\\monstrous\\monstrous2.png',
            "value": 2
        },
        {
            "name": "Demon Lord",
            "hp": 200,
            "speed": 2,
            "armor": .15,
            "dmg_resist": ["ranged", "slash", "fire", "poison"],
            "dmg_vulnerability": ["electric", "heavy"],
            "image": 'assets\\enemy\\monstrous\\monstrous3.png',
            "value": 2
        },
    ],
    "undead": [
        {
            "name": "Bone Soldier",
            "hp": 100,
            "speed": 2,
            "armor": .2,
            "dmg_resist": ["ranged", "pierce", "poison"],
            "dmg_vulnerability": ["fire", "heavy"],
            "image": 'assets\\enemy\\undead\\undead0.png',
            "value": 1
        },
        {
            "name": "Burning Skull",
            "hp": 125,
            "speed": 3.2,
            "armor": .35,
            "dmg_resist": ["ranged", "pierce", "slash", "poison", "heavy"],
            "dmg_vulnerability": ["fire", "electric", "frost"],
            "image": 'assets\\enemy\\undead\\undead1.png',
            "value": 2
        },
        {
            "name": "Wraith",
            "hp": 160,
            "speed": 3,
            "armor": .3,
            "dmg_resist": ["ranged", "pierce", "slash", "poison", "frost", "heavy"],
            "dmg_vulnerability": ["fire", "electric"],
            "image": 'assets\\enemy\\undead\\undead2.png',
            "value": 2
        },
        {
            "name": "Ghoul",
            "hp": 230,
            "speed": 2.5,
            "armor": .3,
            "dmg_resist": ["poison"],
            "dmg_vulnerability": ["fire", "heavy", "electric"],
            "image": 'assets\\enemy\\undead\\undead3.png',
            "value": 2
        },
    ],
    "reaper": [
        {
            "name": "Reaper",
            "hp": 10000,
            "speed": 2,
            "armor": .5,
            "dmg_resist": [],
            "dmg_vulnerability": [],
            "image": 'assets\\enemy\\reaper\\reaper0.png',
            "value": 1000
        },
    ]
}

values = []

def calculate_value(ENEMY_DATA, enemy_counts): # values can be hard coded or this function can calculate values based on hp, speed and armor
    total = 0
    count0 = 0
    for enemy_category, list_of_enemies in ENEMY_DATA.items():
        count=0
        for enemy in list_of_enemies:
            print(enemy_category, count%4, "\t\t", enemy["value"], end='\t')
            enemy["value"] = int(1 + (enemy["hp"]/10 * enemy["speed"]/2 * (1 + enemy["armor"]) + enemy["hp"] * (1 + len(enemy["dmg_resist"])-len(enemy["dmg_vulnerability"])/2)/40)/5)
            values.append(enemy["value"])
            try:
                print(enemy["value"], "\t", enemy["value"]*enemy_counts[count0])
                total += enemy["value"]*enemy_counts[count0]
            except:
                print(enemy["value"])
                # pass
            count += 1
            count0 += 1
    return total

def consolidate_enemy_totals():
    enemies = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    for i in range(len(ENEMY_SPAWN_DATA)):
        for j in range(len(ENEMY_SPAWN_DATA[i])):
            for k in range(len(ENEMY_SPAWN_DATA[i][j])):
                enemies[i][k] += ENEMY_SPAWN_DATA[i][j][k]
    # print(enemies)

    enemy_counts = []
    for i in range(len(enemies)):
        for j in range(len(enemies[i])):
            enemy_counts.append(enemies[i][j])
    # print(enemy_counts)
    return enemy_counts

total = calculate_value(ENEMY_DATA, consolidate_enemy_totals())
# print(total)
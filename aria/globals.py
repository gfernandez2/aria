# globals.py
# read-only global settings for game

# Level xp thresholds
LEVEL_THRESHOLDS = {
    1 : 50,
    2 : 100,
    3 : 160,
    4 : 230,
    5 : 310,
    6 : 400,
    7 : 500,
    8 : 610,
    9 : 730,
    10 : 860,
    11 : 1000,
    12 : 1160,
    13 : 1340,
    14 : 1540,
    15 : 1790,
    16 : 2090,
    17 : 2440,
    18 : 2840,
    19 : 3290,
    20 : 3790,
    21 : 4390,
    22 : 5090,
    23 : 5890,
    24 : 6790,
    25 : 7790,
    26 : 8890,
    27 : 10390,
    28 : 11990,
    29 : 13790,
    30 : 15790,
    31 : 17790,
    32 : 20390,
    33 : 22990,
    34 : 25790,
    35 : 28790,
    36 : 32000,
    37 : 35400,
    38 : 39000,
    39 : 42800,
    40 : 46800,
    41 : 51300,
    42 : 56300,
    43 : 61800,
    44 : 67800,
    45 : 74300,
    46 : 81300,
    47 : 88800,
    48 : 96800,
    49 : 105300,
    50 : 114300
}

# Stat layout : [HP, ATK, DEF, MAG, RES, LCK]
#
# HP - health points
# ATK - base inflicted damage for physical-type moves
# DEF - subtracted from incomiong physical-type damage
# MAG - base inflicted damage for magic-type moves
# RES - subtracted from incoming magic-type damage
# LCK - decreases success-rate of incoming attacks, increases potential xp gains
#
# Maps index to specified stat
STATS = {
    0 : 'HP',
    1 : 'ATK',
    2 : 'DEF',
    3 : 'MAG',
    4 : 'RES',
    5 : 'LCK'
}

# Class specializations
# Base stats are guaranteed starting stats
# Stat spread are probability of increasing stat (by 1)
CLASSES = {
    'knight' : {
        'base'   : [25, 12, 8, 5, 8, 5],
        'spread' : [65, 75, 60, 20, 20, 8],
        'moves'  : ['strike', 'guard', 'multislash'],
    },
    'mage' : {
        'base'   : [20, 5, 8, 13, 12, 5],
        'spread' : [60, 20, 25, 90, 75, 10],
        'moves'  : ['blast', 'miasma', 'manastorm'],
    },
    'healer' : {
        'base'   : [25, 3, 12, 3, 12, 8],
        'spread' : [90, 25, 25, 90, 95, 20],
        'moves'  : ['heal', 'enhance', 'refresh'],
    },
    'tank' : {
        'base'   : [30, 8, 12, 3, 8, 2],
        'spread' : [95, 40, 100, 10, 90, 5],
        'moves'  : ['bash', 'shield', 'bastion'],
    }
}

# Enemy descriptions
# Similar structure to classes
# When enemy is generated, random name + title (for higher level enemies) is chosen from list
# Yes, I used online generators for most of the names
# rate isn't the percent chance of spawning but contributing weight when enemies are 
# selected randomly from a pool - and this pool changes depending on the room difficulty
ENEMIES = {
    'goblin' : {
        'name' : ['Glilx', 'Clokx', 'Vriosb', 'Vrylx', 'Xos', 'Tonrolx', 'Slialkits', 'Haastuizz',
                  'Dubbakt', 'Krukkis', 'Srig', 'Krield', 'Ukx', 'Treang', 'Briz', 'Pryvigz',
                  'Plolkirm', 'Blegtecs', 'Zrysdoirk', 'Tebalb', 'Aags', 'Glaz', 'Beesz', 'Krir',
                  'Bruing', 'Voidfez', 'Agmets', 'Praazuts', 'Strozgix', 'Ioggox', 'Clet', 'Chakt',
                  'Ealk', 'Ezz', 'Clird', 'Edruik', 'Groiszaard', 'Vriliokt', 'Wrudark'
                 ],
        'difficulty' : 1,
        'base'   : [60, 8, 10, 8, 10, 6],
        'spread' : [90, 30, 10, 20, 25, 7],
        'moves'  : ['jab', 'claw'],
        'rate'   : 35
    },
    'slime' : {
        'name' : ['Niall', 'Ralph', 'Frederick', 'Fraser', 'Troy', 'Zakariya', 'Fred', 'Herman',
                  'Wayne', 'Douglas', 'Tony', 'Declan', 'Mason', 'Hector', 'Robbie', 'Adam',
                  'Vincent', 'Zack', 'Damian', 'Faith', 'Kira', 'Cain', 'Kane', 'Zachary', 'David',
                  'Nicholas', 'Jacob', 'Patrick', 'Tobias', 'Andre', 'Scott', 'Josh', 'Curtis',
                  'Thomas', 'Harry', 'Ben'
                 ],
        'difficulty' : 1,
        'base'   : [90, 5, 5, 5, 5, 2],
        'spread' : [85, 10, 10, 10, 10, 5],
        'moves'  : ['bounce'],
        'rate'   : 60
    },
    'troll' : {
        'name' : ['Ttarmek', 'Tedar', 'Jaafan', 'Venjo', 'Mohanlal', 'Maalik', 'Javyn', 'Haijen',
                  'Kazko', 'Yavo', 'Makas', 'Kuroji', 'Seshi', 'Kazko', 'Zulkis', 'Sligo', 'Rashi'
                  'Hakalai', 'Nuenvan', 'Erasto', 'Trolgar', 'Makas', 'Alzim', 'Kiya', 'Vanjin',
                  'Zulmara', 'Zeti', 'Esha', 'Shubre', 'Jiranty'
                 ],
        'difficulty' : 2,
        'base'   : [120, 20, 18, 15, 10, 2],
        'spread' : [90, 50, 50, 35, 35, 5],
        'moves'  : ['club', 'stomp'],
        'rate'   : 140
    },
    'golem' : {
        'name' : ['Ghuhk', 'Rhahm', 'Grad', 'Groc', 'Dhaud', 'Abradan', 'Evnan', 'Giyim', 'Letai',
                  'Ellam', 'Draukkohm', 'Rhom', 'Rangoc', 'Dramm', 'Grular', 'Avnen', 'Gezer',
                  'Naron', 'Yohem', 'Garik', 'Vazlad', 'Dadduhn', 'Ghuhm', 'Rhek', 'Bhollehm',
                  'Azashai', 'Yeniv', 'Atan', 'Avdia', 'Umar', 'Brudra', 'Khuk', 'Rhogmak',
                  'Gher', 'Rukku', 'Dolel', 'Shazar', 'Gelev', 'Chaham', 'Ralachi'
                 ],
        'difficulty' : 2,
        'base'   : [150, 20, 30, 15, 10, 2],
        'spread' : [40, 50, 100, 35, 35, 5],
        'moves'  : ['crush', 'growl'],
        'rate'   : 100
    },
    'orc' : {
        'name' : ['Ughat', 'Yambagorn', 'Clog', 'Omogulg', 'Orpigig', 'Gomoku', 'Supgugh', 'Kugbu',
                  'Wakgut', 'Routhu', 'Krouthu', 'Jogug', 'Vakmu', 'Waggugat', 'Zargulg', 'Ulam',
                  'Yokgagu', 'Tuggug', 'Yokgagu', 'Zargulg', 'Nargol', 'Borgakh', 'Glasha', 'Burub',
                  'Dura', 'Murob', 'Uloth', 'Mogak', 'Loagakh', 'Rogbut', 'Pergu', 'Durbul', 'Azuk',
                  'Drutha', 'Naguk', 'Teldgulg', 'Vregu', 'Wumkbanok', 'Hokulk'
                 ],
        'difficulty' : 2,
        'base'   : [130, 20, 30, 15, 10, 2],
        'spread' : [40, 50, 50, 20, 20, 5],
        'moves'  : ['club', 'growl'],
        'rate'   : 140
    },
    'ghoul' : {
        'name' : ['Tharrius', 'Hinarus', 'Neuldeas', 'Rosaumas', 'Vinion', 'Rivonos', 'Chrones',
                  'Hasnates', 'Vudeidon', 'Chydarderus', 'Nesys', 'Ryambros', 'Vudrotos', 'Vorreas',
                  'Zusaios', 'Cheraios', 'Zedarus', 'Rodnotus', 'Dispaon', 'Diavarus', 'Mavytion'
                  'Chredneus', 'Chindrion', 'Thosaon', 'Xordaon', 'Zavoeus', 'Xixaestus',
                  'Sthescaon', 'Phirdetus', 'Xuktates'
                 ],
        'difficulty' : 3,
        'base'   : [200, 30, 30, 50, 50, 20],
        'spread' : [90, 45, 45, 50, 50, 15],
        'moves'  : ['phase', 'strangle', 'spook'],
        'rate'   : 350
    },
    'lich' : {
        'name' : ['Nourra', 'Zhok\'vux', 'Sakduag', 'Skolidh', 'Psam\'zokar', 'Qukdeghux', 'Auskaen',
                  'Ok\'mighauk', 'Strutoghes', 'Prikrig', 'Naikkel', 'Tyzco', 'Sratrik', 'Thaumducag',
                  'Tsigvyc', 'Nhozun', 'Crouz\'qar', 'Strakdia', 'Han\'qos', 'Qhundoqal', 'Tregiraec',
                  'Tsocdul', 'Urdados', 'Xhomdikus'
                 ],
        'difficulty' : 3,
        'base'   : [200, 20, 30, 15, 10, 2],
        'spread' : [90, 50, 50, 20, 20, 5],
        'moves'  : ['darkblast', 'corrupt', 'maelstrom'],
        'rate'   : 350
    },
    'demon_king' : {
        'name' : ['Bozzamach', 'Toth\'toch', 'Oth\'tenor', 'Brulgromud', 'Ustren', 'Dozgarech',
                  'Balvanach', 'Garzonoth', 'Bonnuman', 'Orroken', 'Kogdral', 'Xuzruth', 'Dullmoz',
                  'Zennoth', 'El\'goroth', 'Erroron', 'Agthakon'
                 ],
        'difficulty' : 4,
        'base'   : [500, 50, 50, 50, 50, 10],
        'spread' : [50, 50, 50, 50, 50, 50],
        'moves'  : ['Nirvana', 'Vairocana'],
        'rate'   : 5000
    }
}

# Move information
#
# cooldown - time (s) before move can be used again
# chance - % chance of move success
# type - physical uses (atk, def) for calculation, magic uses (mag, res), status buff/debuffs stats
# target - how many targets are affected by move
# side - whether player or enemy side is affected
# scale - % damage scaling with atk/mag for phys/magic moves, or % incr/decr of stat for status moves, or % heal for heal moves
#
# for status moves:
# duration - how long buff/debuff lasts
# mod - list which stores what stats are affected (1 or -1 for incr or decr)
#
# chance field shouldn't really be needed for heal-type moves, those should always land
#
# Vairocana is a unique move used by the final boss - this randomly evokes any possible move

# Includes player and enemy moves
MOVES = {
    'strike'    : {'cooldown' : 3,  'chance' : 95, 'type' : 'physical', 'target' : 'single', 'side' : 'enemy', 'scale' : 100},
    'guard'     : {'cooldown' : 15, 'chance' : 45, 'type' : 'status',   'target' : 'self',   'side' : 'player','scale' : 30, 'duration' : 10, 'mod' : [0, 0, 1, 0, 0, 0]},
    'multislash': {'cooldown' : 180,'chance' : 85, 'type' : 'physical', 'target' : 'all',    'side' : 'enemy', 'scale' : 150},
    'blast'     : {'cooldown' : 3,  'chance' : 95, 'type' : 'magic',    'target' : 'single', 'side' : 'enemy', 'scale' : 120},
    'miasma'    : {'cooldown' : 60, 'chance' : 45, 'type' : 'status',   'target' : 'all',    'side' : 'enemy', 'scale' : 20, 'duration' : 40, 'mod' : [0, 0, -1, 0, -1, 0]},
    'manastorm' : {'cooldown' : 150,'chance' : 80, 'type' : 'magic',    'target' : 'all',    'side' : 'enemy', 'scale' : 180},
    'heal'      : {'cooldown' : 8,  'chance' : 100,'type' : 'heal',     'target' : 'single', 'side' : 'player','scale' : 25},
    'enhance'   : {'cooldown' : 60, 'chance' : 45, 'type' : 'status',   'target' : 'single', 'side' : 'player','scale' : 30, 'duration' : 50, 'mod' : [0, 1, 0, 1, 0, 0]},
    'refresh'   : {'cooldown' : 150,'chance' : 100,'type' : 'heal',     'target' : 'all',    'side' : 'player','scale' : 50},
    'bash'      : {'cooldown' : 10, 'chance' : 80, 'type' : 'physical', 'target' : 'single', 'side' : 'enemy', 'scale' : 60},
    'shield'    : {'cooldown' : 75, 'chance' : 65, 'type' : 'status',   'target' : 'self',   'side' : 'player','scale' : 50, 'duration' : 60, 'mod' : [0, 0, 1, 0, 1, 0]},
    'bastion'   : {'cooldown' : 200,'chance' : 95, 'type' : 'physical', 'target' : 'all',    'side' : 'enemy', 'scale' : 80},

    'jab'       : {'cooldown' : 15, 'chance' : 60, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 60},
    'claw'      : {'cooldown' : 20, 'chance' : 80, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 80},
    'bounce'    : {'cooldown' : 18, 'chance' : 65, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 50},
    'club'      : {'cooldown' : 15, 'chance' : 40, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 120},
    'crush'     : {'cooldown' : 18, 'chance' : 50, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 150},
    'stomp'     : {'cooldown' : 25, 'chance' : 70, 'type' : 'physical', 'target' : 'all',    'side' : 'player','scale' : 150},
    'growl'     : {'cooldown' : 30, 'chance' : 95, 'type' : 'status',   'target' : 'all',    'side' : 'player','scale' : 30, 'duration' : 30, 'mod' : [0, -1, -1, 0, 0, 0]},
    'phase'     : {'cooldown' : 20, 'chance' : 65, 'type' : 'magic',    'target' : 'single', 'side' : 'player','scale' : 110},
    'strangle'  : {'cooldown' : 25, 'chance' : 80, 'type' : 'physical', 'target' : 'single', 'side' : 'player','scale' : 100},
    'spook'     : {'cooldown' : 40, 'chance' : 95, 'type' : 'status',   'target' : 'all',    'side' : 'player','scale' : 40, 'duration' : 30, 'mod' : [0, 0, -1, 0, 0, 0]},
    'darkblast' : {'cooldown' : 15, 'chance' : 65, 'type' : 'magic',    'target' : 'single', 'side' : 'player','scale' : 150},
    'corrupt'   : {'cooldown' : 50, 'chance' : 80, 'type' : 'status',   'target' : 'all',    'side' : 'player','scale' : 50, 'duration' : 40, 'mod' : [0, 0, 0, -1, -1, 0]},
    'maelstrom' : {'cooldown' : 200,'chance' : 55, 'type' : 'magic',    'target' : 'all',    'side' : 'player','scale' : 180},

    'Nirvana'   : {'cooldown' : 60, 'chance' : 90, 'type' : 'status',   'target' : 'self',   'side' : 'enemy', 'scale' : 50, 'duration' : 50, 'mod' : [1, 1, 1, 1, 1, 1]},
    'Vairocana' : {'cooldown' : 30, 'chance' : 75, 'type' : 'magic',    'target' : 'all',    'side' : 'player'}
}

# Equipment characteristics goes here

# Game globals
DUNGEON_SIZE = 11
KEYS_REQUIRED = 3
KEY_DROP_RATE = 25
SPAWN_RATE = 45

# globals.py
# read-only global settings for game

# Level xp thresholds
LEVEL_THRESHOLDS = {
    1  : 150,
    2  : 300,
    3  : 500,
    4  : 800,
    5  : 1300,
    6  : 2000,
    7  : 3100,
    8  : 5000,
    9  : 7000,
    10 : 9500,
    11 : 13000,
    12 : 18000,
    13 : 24000,
    14 : 30000,
    15 : 38000
}

# Class specializations
# Stat layout : [HP, ATK, DEF, MAG, RES, SPD]
#
# HP - health points
# ATK - base inflicted damage for physical-type moves
# DEF - subtracted from incomiong physical-type damage
# MAG - base inflicted damage for magic-type moves
# RES - subtracted from incoming magic-type damage
# SPD - decreases success-rate of incoming attacks
#
# Base stats are guaranteed starting stats
# Stat spread are probability of increasing stat (by 1), 
CLASSES = {
    'knight' : {
        'base'   : [25, 12, 8, 5, 8, 5],
        'spread' : [65, 75, 60, 20, 20, 8],
        'moves'  : ['strike', 'guard', 'trislash'],
    },
    'mage' : {
        'base'   : [20, 5, 8, 13, 12, 5],
        'spread' : [60, 20, 25, 90, 75, 10],
        'moves'  : ['blast', 'miasma', 'manastorm'],
    },
    'healer' : {
        'base'   : [25, 3, 12, 3, 12, 8],
        'spread' : [90, 25, 25, 90, 95, 20],
        'moves'  : ['heal' 'enhance', 'refresh'],
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
        'name' : ['Glilx', 'Clokx', 'Vriosb', 'Vrylx', 'Xos', 'Tonrolx', 'Slialkits', 'Haastuizz'
                  'Dubbakt', 'Krukkis', 'Srig', 'Krield', 'Ukx', 'Treang', 'Briz', 'Pryvigz',
                  'Plolkirm', 'Blegtecs', 'Zrysdoirk', 'Tebalb', 'Aags', 'Glaz', 'Beesz', 'Krir',
                  'Bruing', 'Voidfez', 'Agmets', 'Praazuts', 'Strozgix', 'Ioggox', 'Clet', 'Chakt',
                  'Ealk', 'Ezz', 'Clird', 'Edruik', 'Groiszaard', 'Vriliokt', 'Wrudark'
                 ],
        'difficulty' : 1,
        'base'   : [60, 8, 10, 8, 10, 6],
        'spread' : [90, 30, 10, 20, 25, 7],
        'moves'  : ['jab', 'claw']
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
        'moves'  : ['bounce']
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
        'moves'  : ['club', 'stomp']
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
        'moves'  : ['crush', 'growl']
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
        'moves'  : ['club', 'growl']
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
        'moves'  : ['phase', 'strangle', 'spook']
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
        'moves'  : ['darkblast', 'corrupt', 'maelstrom']
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
        'moves'  : ['Vairocana']
        'rate'   : 5000
    }
}

# Move information
# Includes player and enemy moves
# Cooldown (s) and % chance of success
MOVES = {
    'strike'    : {'cooldown' : 3,  'chance' : 95, 'type' : 'physical', 'target' : 'single'},
    'guard'     : {'cooldown' : 15, 'chance' : 45, 'type' : 'status',   'target' : 'single'},
    'multislash': {'cooldown' : 180,'chance' : 85, 'type' : 'physical', 'target' : 'all'},
    'blast'     : {'cooldown' : 3,  'chance' : 95, 'type' : 'magic',    'target' : 'single'},
    'miasma'    : {'cooldown' : 60, 'chance' : 45, 'type' : 'status',   'target' : 'all'},
    'manastorm' : {'cooldown' : 150,'chance' : 80, 'type' : 'magic',    'target' : 'all'},
    'heal'      : {'cooldown' : 8,  'chance' : 95, 'type' : 'status',   'target' : 'single'},
    'enhance'   : {'cooldown' : 60, 'chance' : 45, 'type' : 'status',   'target' : 'single'},
    'refresh'   : {'cooldown' : 120,'chance' : 100,'type' : 'status',   'target' : 'all'},
    'bash'      : {'cooldown' : 5,  'chance' : 80, 'type' : 'physical', 'target' : 'single'},
    'shield'    : {'cooldown' : 45, 'chance' : 65, 'type' : 'status',   'target' : 'single'},
    'bastion'   : {'cooldown' : 200,'chance' : 95, 'type' : 'physical', 'target' : 'all'},

    'jab'       : {'cooldown' : 15, 'chance' : 60, 'type' : 'physical', 'target' : 'single'},
    'claw'      : {'cooldown' : 20, 'chance' : 80, 'type' : 'physical', 'target' : 'single'},
    'bounce'    : {'cooldown' : 18, 'chance' : 65, 'type' : 'physical', 'target' : 'single'},
    'club'      : {'cooldown' : 15, 'chance' : 40, 'type' : 'physical', 'target' : 'single'},
    'crush'     : {'cooldown' : 18, 'chance' : 50, 'type' : 'physical', 'target' : 'single'},
    'stomp'     : {'cooldown' : 25, 'chance' : 70, 'type' : 'physical', 'target' : 'all'},
    'growl'     : {'cooldown' : 30, 'chance' : 95, 'type' : 'status',   'target' : 'all'},
    'phase'     : {'cooldown' : 20, 'chance' : 65, 'type' : 'magic',    'target' : 'single'},
    'strangle'  : {'cooldown' : 25, 'chance' : 80, 'type' : 'physical', 'target' : 'single'},
    'spook'     : {'cooldown' : 40, 'chance' : 95, 'type' : 'status',   'target' : 'all'},
    'darkblast' : {'cooldown' : 15, 'chance' : 65, 'type' : 'magic',    'target' : 'single'},
    'corrupt'   : {'cooldown' : 30, 'chance' : 80, 'type' : 'status',   'target' : 'all'},
    'maelstrom' : {'cooldown' : 200,'chance' : 55, 'type' : 'magic',    'target' : 'all'},

    'Vairocana' : {'cooldown' : 30, 'chance' : 75, 'type' : 'magic',    'target' : 'all'}
}

# Equipment characteristics goes here

# Game globals
DUNGEON_SIZE = 11

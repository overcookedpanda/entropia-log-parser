#!/usr/bin/env python3
import re
import sys
import os


def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    with open(filepath) as fp:
        counter = 0
        for line in fp:
            attributeGains = get_attribute_gains(line)
            skillGains = get_skill_gains(line)
            tierIncreases = get_tier_increases(line)
            selfHeals = get_self_heals(line)
            dmgInflicted = get_dmg_inflicted(line)
            dmgTaken = get_dmg_taken(line)
            playerGlobals = get_player_globals(player, line)
            if skillGains != (None, None, None):
                f = open("./parsed_logs/skill_gains.csv", "a+")
                f.write(skillGains[0] + "," + skillGains[1] + "," + skillGains[2] + '\n')
                f.close()
            if attributeGains != (None, None, None):
                f = open("./parsed_logs/skill_gains.csv", "a+")
                f.write(attributeGains[0] + ',' + attributeGains[1] + ',' + attributeGains[2] + '\n')
                f.close()
            if tierIncreases != (None, None, None):
                #  Do not track tier increases on (L) items.
                if not re.search(r'\(M,L\)|\(L\)', tierIncreases[1]):
                    f = open("./parsed_logs/tier_increases.csv", "a+")
                    f.write(tierIncreases[0] + "," + tierIncreases[1] + ',' + tierIncreases[2] + "\n")
                    f.close()
            if selfHeals != (None, None, None):
                f = open("./parsed_logs/self_heals.csv", "a+")
                f.write(selfHeals[0] + "," + selfHeals[1] + ',' + selfHeals[2] + "\n")
                f.close()
            if dmgInflicted != (None, None, None):
                f = open("./parsed_logs/damage_inflicted.csv", "a+")
                f.write(dmgInflicted[0] + ',' + dmgInflicted[1] + ',' + dmgInflicted[2] + "\n")
                f.close()
            if dmgTaken != (None, None, None):
                f = open("./parsed_logs/damage_taken.csv", "a+")
                f.write(dmgTaken[0] + ',' + dmgTaken[1] + ',' + dmgTaken[2] + "\n")
                f.close()
            if playerGlobals != (None, None, None):
                f = open("./parsed_logs/globals.csv", "a+")
                f.write(playerGlobals[0] + ',' + playerGlobals[1] + ',' + playerGlobals[2] + "\n")
                f.close()
            counter += 1
        print("Processed " + str(counter) + " lines...")


# Attributes:
def get_attribute_gains(data):
    date = None
    attribute = None
    points = None
    attribute_gains = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):['
                                 r'0-5][0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*gained )(\d.*.\d\d\d\d)\s(\w+)$',
                                 data)

    for attribute_gain in attribute_gains:
        date = attribute_gain[0]
        attribute = attribute_gain[2]
        points = attribute_gain[1]

    return date, attribute, points


# Skill Gains:
def get_skill_gains(data):
    date = None
    skill = None
    points = None
    skill_gains = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-6][0-9])(?: \['
        r'System\] \[\] )(?:.*gained )(\d.*.\d\d\d\d)(?: .*your )(.*)(?: skill)',
        data)

    for skill_gain in skill_gains:
        date = skill_gain[0]
        skill = skill_gain[2]
        points = skill_gain[1]

    return date, skill, points


# Item Tier Increases:
def get_tier_increases(data):
    date = None
    item = None
    tier = None
    tier_increases = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-6][0-9])(?: \['
        r'System\] \[\] )(?:.*Your )(.*)(?: has reached tier )(\d+.\d+)',
        data)

    for tier_increase in tier_increases:
        date = tier_increase[0]
        item = tier_increase[1]
        tier = tier_increase[2]

    return date, item, tier


# Self Heals:
def get_self_heals(data):
    date = None
    points = None
    text = None
    heal_points = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:['
        r'0-6][0-9])(?: \[System\] \[\] )(?:.*You healed yourself )(\d+.\d+)(?: points)', data)

    for heal_point in heal_points:
        date = heal_point[0]
        text = 'Healed'
        points = heal_point[1]

    return date, text, points


# Damage Inflicted
def get_dmg_inflicted(data):
    date = None
    points = None
    text = None
    dmg_inflicted = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5]['
                               r'0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:You inflicted )(\d+.\d+)(?: points of '
                               r'damage)', data)

    for dmg in dmg_inflicted:
        date = dmg[0]
        text = 'Damage Inflicted'
        points = dmg[1]

    return date, text, points


# Damage taken:
def get_dmg_taken(data):
    date = None
    points = None
    text = None
    dmg_taken = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:['
                           r'0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:You took )(\d+.\d+)(?: points of damage)', data)

    for dmg in dmg_taken:
        date = dmg[0]
        text = 'Damage Taken'
        points = dmg[1]

    return date, text, points


# Globals:
def get_player_globals(player, data):
    date = None
    creature = None
    amount = None
    player_globals = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):['
                                r'0-5][0-9]:[0-6][0-9])(?: \[Globals\] \[\] )(?:' + player + ' )(?:killed a creature '
                                                                                             r')\((.*?)\)(?:.* with a value of )(\d+)(?: PED!)',
                                data)
    for my_global in player_globals:
        date = my_global[0]
        creature = my_global[1]
        amount = my_global[2]

    return date, creature, amount


# Define Player Name
player = "Overcooked OC Panda"

# Attribute Gain function parse
# log = '2019-12-23 02:04:59 [System] [] You have gained 0.0134 experience in your Anatomy skill' \
#       '2019-12-23 02:05:04 [System] [] You have gained 0.2376 Alertness'
# attributeGains = get_attribute_gains(log)
# print(attributeGains[0] + ',' + attributeGains[1] + ',' + attributeGains[2])

# Skill Gain function parse
# log = '2019-06-08 22:38:31 [System] [] You have gained 1.1731 experience in your Scourging skill'
# skillGains = get_skill_gains(log)
# print(skillGains[0] + "," + skillGains[1] + "," + skillGains[2])

# Tier Increase function parse
# log = '2019-12-18 04:23:19 [System] [] Your MarCorp Kallous-7 has reached tier 9.60'
# tierIncreases = get_tier_increases(log)
# print(tierIncreases[0] + "," + tierIncreases[1] + "," + tierIncreases[2])

# Self Heals function parse
# log = '2019-06-08 22:38:23 [System] [] You healed yourself 30.0 points'
# selfHeals = get_self_heals(log)
# print(selfHeals[0] + "," + selfHeals[1])

# Damage inflicted:
# log = '2019-06-08 22:38:56 [System] [] Critical hit - Additional damage! You inflicted 235.1 points of damage'
# dmgInflicted = get_dmg_inflicted(log)
# print(dmgInflicted[0] + "," + dmgInflicted[1])

# Damage taken:
# log = '2019-06-08 22:39:04 [System] [] You took 40.5 points of damage'
# dmgTaken = get_dmg_taken(log)
# print(dmgTaken[0] + "," + dmgTaken[1])

# Globals:
# log = '2019-12-08 03:20:33 [Globals] [] Overcooked OC Panda killed a creature (Calamusoid Hunter) with a value ' \
#       'of 515 PED! A record has been added to the Hall of Fame! '

# Define Player Name
# my_globals = get_player_globals(avatar, log)
# print(my_globals[0] + "," + my_globals[1] + "," + my_globals[2])

if __name__ == '__main__':
    main()

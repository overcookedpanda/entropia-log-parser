#!/usr/bin/env python3
import re
import sys
import os


def main():
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()

    with open(filepath, encoding="utf-8") as fp:
        counter = 0
        shots = 0
        hits = 0
        totalDmgTaken = 0
        totalDmgInflicted = 0
        totalSkills = 0
        totalHeals = 0
        totalGlobals = 0
        totalBrokenEnhancers = 0
        totalTierIncreases = []
        for line in fp:
            attributeGains = get_attribute_gains(line)
            skillGains = get_skill_gains(line)
            tierIncreases = get_tier_increases(line)
            selfHeals = get_self_heals(line)
            dmgInflicted = get_dmg_inflicted(line)
            dmgTaken = get_dmg_taken(line)
            playerGlobals = get_player_globals(player, line)
            brokenEnhancers = get_broken_enhancers(line)
            if skillGains != (None, None, None):
                #f = open("./parsed_logs/skill_gains.csv", "a+")
                #f.write(skillGains[0] + "," + skillGains[1] + "," + skillGains[2] + '\n')
                #f.close()
                totalSkills += float(skillGains[2])
            if attributeGains != (None, None, None):
                #f = open("./parsed_logs/skill_gains.csv", "a+")
                #f.write(attributeGains[0] + ',' + attributeGains[1] + ',' + attributeGains[2] + '\n')
                #f.close()
                totalSkills += float(attributeGains[2])
            if tierIncreases != (None, None, None):
                #  Do not track tier increases on (L) items.
                if not re.search(r'\(M,L\)|\(L\)', tierIncreases[1]):
                    #f = open("./parsed_logs/tier_increases.csv", "a+")
                    #f.write(tierIncreases[0] + "," + tierIncreases[1] + ',' + tierIncreases[2] + "\n")
                    #f.close()
                    totalTierIncreases.append(tierIncreases)
            if selfHeals != (None, None, None):
                #f = open("./parsed_logs/self_heals.csv", "a+")
                #f.write(selfHeals[0] + "," + selfHeals[1] + ',' + selfHeals[2] + "\n")
                #f.close()
                totalHeals += float(selfHeals[2])
            if dmgInflicted != (None, None, None):
                shots += 1
                if not re.search(r'The target Dodged your attack', dmgInflicted[1]):
                    #f = open("./parsed_logs/damage_inflicted.csv", "a+")
                    #f.write(dmgInflicted[0] + ',' + dmgInflicted[1] + ',' + dmgInflicted[2] + "\n")
                    #f.close()
                    if dmgInflicted[2] != "":
                        totalDmgInflicted += float(dmgInflicted[2])
            if dmgTaken != (None, None, None):
                #f = open("./parsed_logs/damage_taken.csv", "a+")
                #f.write(dmgTaken[0] + ',' + dmgTaken[1] + ',' + dmgTaken[2] + "\n")
                #f.close()
                hits += hits
                totalDmgTaken += float(dmgTaken[2])
            if playerGlobals != (None, None, None):
                #f = open("./parsed_logs/globals.csv", "a+")
                #f.write(playerGlobals[0] + ',' + playerGlobals[1] + ',' + playerGlobals[2] + "\n")
                #f.close()
                totalGlobals += float(playerGlobals[2])
            if brokenEnhancers != (None, None, None, 0):
                totalBrokenEnhancers += brokenEnhancers[3]
            counter += 1
    print("Processed " + str(counter) + " lines...")
    print("Total Damage Taken: " + format(totalDmgTaken, '.2f') + " Armor Hit Points")
    totalDmgCost = float((totalDmgTaken / (armorCost * (armorMarkUp - 2) * -1) * 0.01))
    print("Total Damage Cost: " + format(totalDmgCost, '.2f') + " PED")
    print("---")
    print("Total Heals: " + format(totalHeals, '.2f') + " Health Points")
    print("Total Heal Cost: " + format((totalHeals / healCost) * 0.01, '.2f') + " PED")
    totalHealCost = float((totalHeals / healCost) * 0.01)
    print("---")
    print("Total Broken Enhancers: " + str(totalBrokenEnhancers))
    totalEnhancerCost = float(totalBrokenEnhancers * ((enhancerCost * enhancerMarkUp) - enhancerCost))
    print("Total Broken Enhancer NET Cost: " + format(totalEnhancerCost, '.2f') + " PED")
    totalWeaponCost = float((shots * weaponCost) + (shots * (weaponDecay * weaponMarkUp)) + totalEnhancerCost)
    print("---")
    print("Total Shots taken: " + str(shots))
    print("Total Damage Inflicted: " + format(totalDmgInflicted, '.2f') + " Mob Hit Points")
    print("Total Weapon Cost: " + format(totalWeaponCost, '.2f') + " PED")
    print("Other User Specified Costs: " + str(otherCosts) + " PED")
    totalPedCycled = float(totalDmgCost + totalHealCost + totalWeaponCost + otherCosts)
    print("---")
    print("Total Cycled: " + format(totalPedCycled, '.2f') + " PED")
    print("Average Eco: " + format(totalDmgInflicted / (totalPedCycled * 100), '.2f') + " DPP")
    print("---")
    print("UL Tier Increases During Run:")
    for tier in totalTierIncreases:
        print(tier[0] + " :: " + tier[1] + " - " + tier[2])
    print("---")
    print("Total Global Loot: " + str(totalGlobals) + " PED")
    print("Total Skills Gained: " + format(totalSkills, '.2f'))

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
                               r'0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*?)(The target Dodged your attack)|([0-9]{'
                               r'4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][ '
                               r'0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:You inflicted )(\d+.\d+)(?: points of '
                               r'damage)', data)

    for dmg in dmg_inflicted:
        date = dmg[0]
        text = 'Damage Inflicted'
        points = dmg[3]

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
                                r')\((.*?)\)(?:.* with a value of )(\d+)(?: PED)', data)
    for my_global in player_globals:
        date = my_global[0]
        creature = my_global[1]
        amount = my_global[2]

    return date, creature, amount


def get_broken_enhancers(data):
    date = None
    enhancer_type = None
    weapon = None
    broken = 0
    broken_enhancers = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):['
                                  r'0-5][0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:Your enhancer )('
                                  r'\S+\s\S+\s\S+\s\d)(?: on your )(.*)(broke)', data)
    for enhancer in broken_enhancers:
        date = enhancer[0]
        enhancer_type = enhancer[1]
        weapon = enhancer[2]
        if enhancer[3] == "broke":
            broken = 1
    return date, enhancer_type, weapon, broken


# Define Player Variables
player = "Overcooked OC Panda"
# MarCorp Kallous 7 + Omegaton A105 Improved
weaponCost = 0.24
weaponDecay = 0.0466
# Mark Up in percentage points, ie) 115% = 1.15
weaponMarkUp = 1
# Weapon Damage Enhancers 1-9
enhancerCost = 0.8
# Average Mark Up in percentage points, ie) 310% = 3.1
enhancerMarkUp = 3.1
# Polaris (L) + Armor Plating Mk. 5B dmg/pec
armorCost = 22.27
# Average Mark Up in percentage points, ie) 110% = 1.1
armorMarkUp = 1.1
# Adjusted Restoration Chip heal/pec
healCost = 159.22
healDecay = 0
# Other Costs, pills, etc, user specified in PED, for items used during hunt.
otherCosts = 0

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

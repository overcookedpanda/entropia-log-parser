#!/usr/bin/env python3
import re


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
    heal_points = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:['
        r'0-6][0-9])(?: \[System\] \[\] )(?:.*You healed yourself )(\d+.\d+)(?: points)', data)

    for heal_point in heal_points:
        date = heal_point[0]
        points = heal_point[1]

    return date, points


# Skill Gain function parse
log = '2019-06-08 22:38:31 [System] [] You have gained 1.1731 experience in your Scourging skill'
skillGains = get_skill_gains(log)
print(skillGains[0] + "," + skillGains[1] + "," + skillGains[2])

# Tier Increase function parse
log = '2019-12-18 04:23:19 [System] [] Your MarCorp Kallous-7 has reached tier 9.60'
tierIncreases = get_tier_increases(log)
print(tierIncreases[0] + "," + tierIncreases[1] + "," + tierIncreases[2])

# Self Heals function parse
log = '2019-06-08 22:38:23 [System] [] You healed yourself 30.0 points'
selfHeals = get_self_heals(log)
print(selfHeals[0] + "," + selfHeals[1])

# Damage inflicted:
sampleData = '2019-06-08 22:38:56 [System] [] Critical hit - Additional damage! You inflicted 235.1 points of damage'
dmgInflicted = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5]['
                          r'0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:You inflicted )(\d+.\d+)(?: points of '
                          r'damage)', sampleData)

for dmg in dmgInflicted:
    print(dmg)

# Damage taken:
sampleData = '2019-06-08 22:39:04 [System] [] You took 40.5 points of damage'
dmgTaken = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:['
                      r'0-6][0-9])(?: \[System\] \[\] )(?:.*?)(?:You took )(\d+.\d+)(?: points of damage)', sampleData)

for dmg in dmgTaken:
    print(dmg)

# Globals:
sampleData = '2019-12-08 03:20:33 [Globals] [] Overcooked OC Panda killed a creature (Calamusoid Hunter) with a value '\
             'of 515 PED! A record has been added to the Hall of Fame! '
playerGlobals = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5]['
                           r'0-9]:[0-6][0-9])(?: \[Globals\] \[\] )(?:Overcooked OC Panda )(?:killed a creature )\(('
                           r'.*?)\)(?:.* with a value of )(\d+)(?: PED!)', sampleData)

for myGlobal in playerGlobals:
    print(myGlobal)

sampleData = '2019-12-18 04:46:30 [System] [] Your MarCorp Kallous-7 is close to reaching minimum condition, ' \
             'consider repairing it as soon as possible '
repairNeeded = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5]['
                          r'0-9]:[0-6][0-9])(?: \[System\] \[\] )(?:.*Your )(.*)(?: is close to reaching minimum '
                          r'condition, consider repairing it as soon as possible)', sampleData)

for repair in repairNeeded:
    print(repair)

#!/usr/bin/env python3
import re

# Skill Gains:
def getSkillGains(data):
    skillGains = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-6][0-9])(?: \['
        r'System\] \[\] )(?:.*gained )(\d.*.\d\d\d\d)(?: .*your )(.*)(?: skill)',
        data)

    for skillGain in skillGains:
        date = skillGain[0]
        skill = skillGain[2]
        points = skillGain[1]

    return date, skill, points

# Item Tier Increases:
def getTierIncreases(data):
    tierIncreases = re.findall(
        r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:[0-6][0-9])(?: \['
        r'System\] \[\] )(?:.*Your )(.*)(?: has reached tier )(\d+.\d+)',
        data)

    for tierIncrease in tierIncreases:
        date = tierIncrease[0]
        item = tierIncrease[1]
        tier = tierIncrease[2]

    return date, item, tier

# Skill Gain function parse
data = '2019-06-08 22:38:31 [System] [] You have gained 1.1731 experience in your Scourging skill'
skillGains = getSkillGains(data)
print(skillGains[0] + "," + skillGains[1] + "," + skillGains[2])

# Tier Increase function parse
data = '2019-12-18 04:23:19 [System] [] Your MarCorp Kallous-7 has reached tier 9.60'
tierIncreases = getTierIncreases(data)
print(tierIncreases[0] + "," + tierIncreases[1] + "," + tierIncreases[2])

# Heal:
sampleData = '2019-06-08 22:38:23 [System] [] You healed yourself 30.0 points'
healPoints = re.findall(r'([0-9]{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[1-2][0-9]|3[0-1]) (?:2[0-3]|[01][0-9]):[0-5][0-9]:['
                        r'0-6][0-9])(?: \[System\] \[\] )(?:.*You healed yourself )(\d+.\d+)(?: points)', sampleData)

for healPoint in healPoints:
    print(healPoint)

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

#!/usr/bin/env python3
import re
import sys
import os
from flask import Flask, request, render_template, Markup, redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSIONS = {'log'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# limit upload size to 8MB
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            player = request.form.get('player', '')
            weaponCost = float(request.form.get('weaponCost', '0'))
            weaponDecay = float(request.form.get('weaponDecay', '0'))
            weaponMarkUp = float(request.form.get('weaponMarkUp', '0'))
            enhancerCost = float(request.form.get('enhancerCost', '0'))
            enhancerMarkUp = float(request.form.get('enhancerMarkUp', '0'))
            armorCost = float(request.form.get('armorCost', '0'))
            armorMarkUp = float(request.form.get('armorMarkUp', '0'))
            healCost = float(request.form.get('healCost', '0'))
            healDecay = int(request.form.get('healDecay', '0'))
            otherCosts = int(request.form.get('otherCosts', '0'))
            text = Markup("Player Defined Parameters:<br> Player Name: {}<br>Weapon Cost: {}<br>Weapon Decay: {}<br>Weapon MarkUp: {}<br>Enhancer Cost: {}<br> \
                 Enhancer MarkUp: {}<br>Armor Cost: {}<br>Armor MarkUp: {}<br>Heal Cost: {}<br>Heal Decay: {}<br> \
                 Other Costs: {}".format(player, weaponCost, weaponDecay, weaponMarkUp, enhancerCost, enhancerMarkUp, armorCost, \
                 armorMarkUp, healCost, healDecay, otherCosts))
            stats = process_stats(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return '{} {}'.format(text, stats)
    return render_template('index.html')


#def process_file(path, filename):

def process_stats(path):
    player = request.form.get('player', '')
    weaponCost = float(request.form.get('weaponCost', '0'))
    weaponDecay = float(request.form.get('weaponDecay', '0'))
    weaponMarkUp = float(request.form.get('weaponMarkUp', '0'))
    enhancerCost = float(request.form.get('enhancerCost', '0'))
    enhancerMarkUp = float(request.form.get('enhancerMarkUp', '0'))
    armorCost = float(request.form.get('armorCost', '0'))
    armorMarkUp = float(request.form.get('armorMarkUp', '0'))
    healCost = float(request.form.get('healCost', '0'))
    healDecay = float(request.form.get('healDecay', '0'))
    otherCosts = float(request.form.get('otherCosts', '0'))
    filepath = path

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
                totalSkills += float(skillGains[2])
            if attributeGains != (None, None, None):
                totalSkills += float(attributeGains[2])
            if tierIncreases != (None, None, None):
                #  Do not track tier increases on (L) items.
                if not re.search(r'\(M,L\)|\(L\)', tierIncreases[1]):
                    totalTierIncreases.append(tierIncreases)
            if selfHeals != (None, None, None):
                totalHeals += float(selfHeals[2])
            if dmgInflicted != (None, None, None):
                shots += 1
                if not re.search(r'The target Dodged your attack', dmgInflicted[1]):
                    if dmgInflicted[2] != "":
                        totalDmgInflicted += float(dmgInflicted[2])
            if dmgTaken != (None, None, None):
                hits += hits
                totalDmgTaken += float(dmgTaken[2])
            if playerGlobals != (None, None, None):
                totalGlobals += float(playerGlobals[2])
            if brokenEnhancers != (None, None, None, 0):
                totalBrokenEnhancers += brokenEnhancers[3]
            counter += 1
    totalDmgCost = float((totalDmgTaken / (armorCost * (armorMarkUp - 2) * -1) * 0.01))
    totalHealCost = float((totalHeals / healCost) * 0.01)
    totalEnhancerCost = float(totalBrokenEnhancers * ((enhancerCost * enhancerMarkUp) - enhancerCost))
    totalWeaponCost = float((shots * weaponCost) + (shots * (weaponDecay * weaponMarkUp)) + totalEnhancerCost)
    totalPedCycled = float(totalDmgCost + totalHealCost + totalWeaponCost + otherCosts)
    ttIncrease = ''
    for tier in totalTierIncreases:
        ttIncrease += tier[0] + " :: " + tier[1] + " - " + tier[2] + "<br>"
    stats = Markup("<p>Processed {} lines...<br> \
                    Total Damage Taken: {} Armor Hit Points<br> \
                    Total Damage Cost: {} PED<br> \
                    ---<br> \
                    Total Heals: {} Health Points<br> \
                    Total Heal Cost: {} PED<br> \
                    ---<br> \
                    Total Broken Enhancers: {}<br> \
                    Total Broken Enhancer NET Cost: {} PED<br> \
                    ---<br> \
                    Total Shots Taken: {}<br> \
                    Total Damage Inflicted: {} Mob Hit Points<br> \
                    Total Weapon Cost: {} PED<br> \
                    Other User Specified Costs: {} PED<br> \
                    ---<br> \
                    Total Cycled: {} PED<br> \
                    Average Eco: {} DPP<br> \
                    ---<br> \
                    Total Global Loot: {} PED<br> \
                    Total Skills Gained: {}".format(str(counter), format(totalDmgTaken, '.2f'), format(totalDmgCost, '.2f'), format(totalHeals, '.2f'), format((totalHeals / healCost) * 0.01, '.2f'), str(totalBrokenEnhancers), format(totalEnhancerCost, '.2f'), str(shots), format(totalDmgInflicted, '.2f'), format(totalWeaponCost, '.2f'), str(otherCosts), format(totalPedCycled, '.2f'), format(totalDmgInflicted / (totalPedCycled * 100), '.2f'), str(totalGlobals), format(totalSkills, '.2f')) \
                    + "<br>---<br>Total UL Tier Increases During Run:<br>" + ttIncrease\
                   )
    return stats

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
#player = "Overcooked OC Panda"
# MarCorp Kallous 7 + Omegaton A105 Improved
#weaponCost = 0.24
#weaponDecay = 0.0466
# Mark Up in percentage points, ie) 115% = 1.15
#weaponMarkUp = 1
# Weapon Damage Enhancers 1-9
#enhancerCost = 0.8
# Average Mark Up in percentage points, ie) 310% = 3.1
#enhancerMarkUp = 3.1
# Polaris (L) + Armor Plating Mk. 5B dmg/pec
#armorCost = 22.27
# Average Mark Up in percentage points, ie) 110% = 1.1
#armorMarkUp = 1.1
# Adjusted Restoration Chip heal/pec
#healCost = 159.22
#healDecay = 0
# Other Costs, pills, etc, user specified in PED, for items used during hunt.
#otherCosts = 0

#if __name__ == '__main__':
#    main()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)


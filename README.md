Simple script to parse Entropia Universe chat.log for various statistics using regex.

Configurable options:

# Define Player Variables
player = "Overcooked OC Panda"
# MarCorp Kallous 7 + Omegaton A105 Improved + Weapon Damage Enhancers 1-9
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


Currently you run it with ./entropia-log-parser.py chat.log and it will output .csv files into ./parsed_logs which can then be further processed.

Example Output:

Processed 51972 lines...
Total Damage Taken: 14106.60 Armor Hit Points
Total Damage Cost: 7.04 PED
---
Total Heals: 11081.00 Health Points
Total Heal Cost: 0.70 PED
---
Total Broken Enhancers: 65
Total Broken Enhancer NET Cost: 109.20 PED
---
Total Shots taken: 29815
Total Damage Inflicted: 2551890.30 Mob Hit Points
Total Weapon Cost: 8654.18 PED
Other User Specified Costs: 0 PED
---
Total Cycled: 8661.91 PED
Average Eco: 2.95 DPP
---
UL Tier Increases During Run:
2019-12-26 16:55:11 :: MarCorp Kallous-7 - 9.63
2019-12-26 17:16:03 :: MarCorp Kallous-7 - 9.64
2019-12-27 12:08:28 :: MarCorp Kallous-7 - 9.65
---
Total Global Loot: 2007.0 PED
Total Skills Gained: 1146.84


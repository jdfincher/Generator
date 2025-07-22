#! /usr/bin/env python

"""The Generator 0.1"""

# Import Modules
import random
import uuid
import time
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import pickle

# Global

# Weapon                  (0Name, 1Cost, 2Damage, 3Range, 4Reload, 5Weight, 6Critical, 7Aim, 8Ammo) 
weapons = {'hard knife'   :('hard knife','$20','D4','20ft','--','1lb','19-20','+0','--'),
           'baton'        :('baton','$30','D6','5ft','--','3lbs','19-20','+0','--'),
           'hard blade'   :('hard blade','$80','D8','5ft','--','3lbs','19-20','+0','--'),
           'sling shot'   :('sling shot','$10','D4','60ft','3','1lb','19-20','+0','1 Rd'),
           '22 revolver'  :('22 revolver','$130','D6+1','80ft','10','2lbs','19-20','+0','6 Rds'),
           '22 pistol'    :('22 pistol','$150','D6','60ft','3','3lbs','(19-20)x2','+0','10 Rds'),
           '38 revolver'  :('38 revolver','$550','D8+1','80ft','10','4lbs','19-20','+0','6 Rds'),
           '38 pistol'    :('38 pistol','$350','D8','60ft','3','5lbs','(19-20)x2','+0','10 Rds'),
           '357 revolver' :('357 revolver','$550','D10+1','70ft','10','8lbs','19-20','+0','6 Rds'),
           '45 pistol'    :('45 pistol','$650','D10','60ft','3','10lbs','(19-20)x2','+0','10 Rds'),
           '22 rifle'     :('22 rifle','$200','D6+1','200ft','10','12lbs','19-20','+1','5 Rds'),
           '22 c rifle'   :('22 c rifle','$300','D6+1','200ft','3','12lbs','19-20','+1','10 Rds'),
           '3030 rifle'   :('3030 rifle','$500','D8+1','300ft','10','15lbs','19-20','+1','5 Rds'),
           '3030 c rifle' :('3030 c rifle','$600','D8+1','300ft','3','15lbs','19-20','+1','10 Rds'),
           'shotgun'      :('shotgun','$250','*','*','3','15lbs','19-20','+0','1 Rd'),
           'double barrel':('double barrel','$600','*','*','6','18lbs','19-20','+0','2 Rds'),
           'tec 9'        :('tec 9','$800','D6','60ft','4','12lbs','(20)X2','+0','18 Rds'),
           'ak-47'        :('ak-47','$1000','D8','100ft','4','20lbs','(20)X2','+0','30 Rds')
           }
# Armour                       (0Name,               1Cost, 2Weight, 3ACBonus, 4CHECK PENALTY)
armour = {'padded wire'       :('padded wire'       ,'$150' ,'20lbs','+3','-1'),
          'plastic'           :('plastic'           ,'$400' ,'15lbs','+4','-2'),
          'kevlar vest'       :('kevlar vest'       ,'$500' ,'10lbs','+5','-1'),
          'kevlar suit'       :('kevlar suit'       ,'$1000','35lbs','+7','-2'),
          'hard ware'         :('hard ware'         ,'$3000','30lbs','+7','-3'),
          'plastic mask'      :('plastic mask'      ,'$100' ,'3lbs' ,'+4','-1'),
          'hard mask'         :('hard mask'         ,'$400' ,'8lbs' ,'+7','-1'),
          'kevlar shield'     :('kevlar shield'     ,'$300' ,'10lbs','+1','-1'),
          'hard shield'       :('hard shield'       ,'$800' ,'8lbs' ,'+2','-0')
          }
# Skills (Type : Skill List)-->(Skill : (0attribute,1total,2learned,3mod+)
# Only use 3 Letter abbrev. divided by / for attribute -> set_skills() checks len() of string
skill_sets = {'mystic':{
                        'meditation'      :('wis','0','0','+'),
                        'gut'             :('wis','0','0','+'),
                        'prestidigitation':('dex','0','0','+'),
                        'mystic lore'     :('wis','0','0','+'),
                        'star sense'      :('wis','0','0','+'),
                        'meteorology'     :('wis','0','0','+'),
                        'survival wild'   :('wis','0','0','+'),
                        'empathy bio'     :('wis','0','0','+'),
                        'train animal'    :('cha','0','0','+'),
                        'spot'            :('wis','0','0','+'),
                        'listen'          :('wis','0','0','+'),
                        'mutantology'     :('int','0','0','+'),
                        },
              'techer':{
                        'drive'           :('dex/agi','0','0','+'),
                        'computer'        :('int','0','0','+'),
                        'machina'         :('int','0','0','+'),
                        'law'             :('int','0','0','+'),
                        'electrical'      :('int','0','0','+'),
                        'weaponry'        :('int','0','0','+'),
                        'cybernetic'      :('int','0','0','+'),
                        'demolition'      :('int','0','0','+'),
                        'empathy machine' :('int','0','0','+'),
                        'code break'      :('int','0','0','+'),
                        'pilot'           :('dex','0','0','+'),
                        'scuba dive'      :('dex','0','0','+'),
                        'disable machine' :('int','0','0','+'),
                        'find'            :('wis','0','0','+'),
                       },
              'chemist':{
                        'mutant lore'     :('int','0','0','+'),
                        'chemistry'       :('int','0','0','+'),
                        'first aid'       :('dex','0','0','+'),
                        'field surgeon'   :('dex','0','0','+'),
                        'concoct mixture' :('int','0','0','+'),
                        'distill'         :('int','0','0','+'),
                        'cook'            :('dex','0','0','+'),
                        'drink'           :('fit','0','0','+'),
                        'find'            :('wis','0','0','+'),
                        },
              'seeker':{
                        'spot'            :('wis','0','0','+'),
                        'listen'          :('wis','0','0','+'),
                        'pick lock'       :('dex','0','0','+'),
                        'jump'            :('str','0','0','+'),
                        'sneak'           :('dex/agi','0','0','+'),
                        'hide'            :('dex','0','0','+'),
                        'lip read'        :('int','0','0','+'),
                        'diplomacy'       :('cha/app','0','0','+'),
                        'weaponry'        :('int','0','0','+'),
                        'street wise'     :('wis','0','0','+'),
                        'survival wild'   :('wis','0','0','+'),
                        'gut'             :('wis','0','0','+'),
                        'threaten'        :('cha','0','0','+'),
                        'act'             :('cha','0','0','+'),
                        'befriend'        :('cha','0','0','+'),
                        'find'            :('wis','0','0','+'),
                       },
              'thief':{
                        'listen'          :('wis','0','0','+'),
                        'pick lock'       :('dex','0','0','+'),
                        'tumble'          :('agi','0','0','+'),
                        'pilfer'          :('dex','0','0','+'),
                        'sneak'           :('dex/agi','0','0','+'),
                        'hide'            :('dex','0','0','+'),
                        'lip read'        :('int','0','0','+'),
                        'electrical'      :('int','0','0','+'),
                        'street wise'     :('wis/cha','0','0','+'),
                        'haggle'          :('cha','0','0','+'),
                        'forgery'         :('dex','0','0','+'),
                        'scuba dive'      :('dex','0','0','+'),
                        'find trap'       :('int','0','0','+'),
                        'act'             :('cha','0','0','+'),
                        'find'            :('wis','0','0','+'),
                        'disable trap'    :('dex','0','0','+'),
                      },
              'gunslinger':{
                        'gut'             :('wis','0','0','+'),
                        'star sense'      :('wis','0','0','+'),
                        'meteorology'     :('wis','0','0','+'),
                        'survival wild'   :('wis','0','0','+'),
                        'spot'            :('wis','0','0','+'),
                        'listen'          :('wis','0','0','+'),
                        'mutantology'     :('int','0','0','+'),
                        'diplomacy'       :('cha/app','0','0','+'),
                        'sneak'           :('dex/agi','0','0','+'),
                        'hide'            :('dex','0','0','+'),
                           },
              'thug':{
                        'gut'             :('wis','0','0','+'),
                     },
              'naturalist':{
                        'gut'             :('wis','0','0','+',),   
                           },
              'martial artist':{
                        'gut'             :('wis','0','0','+'),
                               },
              'face':{
                        'gut'             :('wis','0','0','+'),
                     },
              'generic':{
                        'jump'            :('str','0','0','+'),
                        'sing and dance'  :('cha','0','0','+'),
                        'drive'           :('dex/agi','0','0','+'),
                        'computer'        :('int','0','0','+'),
                        'history'         :('int','0','0','+'),
                        'government'      :('int','0','0','+'),
                        'law'             :('int','0','0','+'),
                        'religion'        :('int','0','0','+'),
                        'first aid'       :('dex','0','0','+'),
                        'survival city'   :('wis/cha','0','0','+'),
                        'swim'            :('fit','0','0','+'),
                        'climb'           :('str','0','0','+'),
                        'cook'            :('dex','0','0','+'),
                        'paint'           :('dex/wis','0','0','+'),
                        'nautical'        :('dex','0','0','+'),
                        'fish'            :('wis','0','0','+'),
                        'drink'           :('fit','0','0','+'),
                        }
              }

player = {'name'           :'',
          'race'           :'',
          'type'           :'',
          'level'          :"1",
          'life'           :"0",
          'clicks'         :"0",
          'money'          :"0",
          'initiative'     :"0",
          'aim'            :"0",
          'interrupts'     :"0",
          'strength'       :"0",
          'dexterity'      :"0",
          'fitness'        :"0",
          'agility'        :"0",
          'wisdom'         :"0",
          'intelligence'   :"0",
          'charisma'       :"0",
          'appearance'     :"0",
          'notes'          :"...",
          'inventory'      :[],
          'equipped_armour':[],
          'equipped_weapon':[],
          'race_flag'      :"",
          'type_flag'      :"",
          'skill'          :[],
          'skill_points'   :'0',
          'method'         :[],
          }

armour_set = set(['padded wire',
                  'plastic',
                  'kevlar vest',
                  'kevlar suit',
                  'hard ware',
                  'plastic mask',
                  'hard mask',
                  'kevlar shield',
                  'hard shield'
                  ])

weapon_set = set(['22 revolver',
                  '22 pistol',
                  'hand cannon',
                  '38 revolver',
                  'hard knife',
                  'baton',
                  'hard blade',
                  'sling shot',
                  'short bow',
                  'cross bow',
                  '38 revolver',
                  '38 pistol',
                  '357 revolver',
                  '45 pistol',
                  '22 rile',
                  '22 c rifle',
                  '3030 rifle',
                  '3030 c rifle',
                  'shotgun',
                  'double barrel',
                  'tec 9',
                  'ak-47',
                  ])

# Ansi colors
reset = '\x1b[0m'
yellow = '\x1b[33m'
cyan = '\x1b[36m'
brightmagenta = '\x1b[45m'
brightcyan = '\x1b[46m'

class RollDice(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Dice Roll Simulator")
        self.add_button("Done", 1)
        box = self.get_content_area()
        grid = Gtk.Grid()

        dice = Gtk.Label(label="Number of Dice")
        sides = Gtk.Label(label="Sides per Dice")
        result = Gtk.Label(label="Result of Roll")
        self.dice_value = Gtk.Entry()
        self.dice_value.set_text("1")
        self.sides_value = Gtk.Entry()
        self.sides_value.set_text("20")
        self.result = Gtk.Label(label="0")
        roll = Gtk.Button(label="Roll Dice")
        roll.connect("clicked", self.roll_sim)

        grid.attach(dice,              0, 0, 1, 1)
        grid.attach(sides,             0, 1, 1, 1)
        grid.attach(self.dice_value,   1, 0, 1, 1)
        grid.attach(self.sides_value,  1, 1, 1, 1)
        grid.attach(result,            0, 2, 1, 1)
        grid.attach(self.result,       1, 2, 1, 1)
        grid.attach(roll,              0, 3, 3, 1)
        box.pack_start(grid, True, True, 2)
        self.show_all()

    def roll_sim(self, widget):
        dice = int(self.dice_value.get_text())
        sides = int(self.sides_value.get_text())
        result = 0
        for rolls in range(0, dice):
            result += random.randint(1, sides)
        self.result.set_text(str(result))

class EditInventory(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Add/Remove Equipment")
        box = self.get_content_area()
        armour_grid = Gtk.Grid()
        weapon_grid = Gtk.Grid()
        armour_label = Gtk.Label()
        armour_label.set_markup("<span size='large' weight='bold'>Armour</span>")
        armour_frame = Gtk.Frame()
        armour_frame.set_label_widget(armour_label)
        armour_frame.set_label_align(0.05, 0.5)
        weapon_label = Gtk.Label()
        weapon_label.set_markup("<span size='large' weight='bold'>Weapons</span>")
        weapon_frame = Gtk.Frame()
        weapon_frame.set_label_widget(weapon_label)
        weapon_frame.set_label_align(0.05, 0.5)
        self.add_button("Done", 1)

        orientation = Gtk.Orientation.HORIZONTAL
        arm_type = Gtk.Label(label="Name")
        arm_cost = Gtk.Label(label="Worth")
        arm_weight = Gtk.Label(label="Weight(lbs)")
        arm_bonus = Gtk.Label(label="A/C Bonus")
        arm_check = Gtk.Label(label="Check Penalty")
        arm_sep = Gtk.Separator.new(orientation) 

        wea_type = Gtk.Label.new("Name")
        wea_cost = Gtk.Label.new("Worth")
        wea_damg = Gtk.Label.new("Damage")
        wea_rang = Gtk.Label.new("Range")
        wea_relo = Gtk.Label.new("Reload")
        wea_weig = Gtk.Label.new("Weight")
        wea_crit = Gtk.Label.new("Critical")
        wea_aim  = Gtk.Label.new("Aim Bonus")
        wea_amm  = Gtk.Label.new("Rounds")
        wea_sep = Gtk.Separator.new(orientation)
        
        armour_grid.attach(arm_type,    0, 0, 1, 1)
        armour_grid.attach(arm_cost,    1, 0, 1, 1)
        armour_grid.attach(arm_weight,  2, 0, 1, 1)
        armour_grid.attach(arm_bonus,   3, 0, 1, 1)
        armour_grid.attach(arm_check,   4, 0, 1, 1)
        armour_grid.attach(arm_sep,     0, 1, 9, 1)
        armour_grid.set_column_spacing(10)
        armour_grid.set_row_spacing(   10)
        armour_grid.set_margin_start(  10)
        armour_grid.set_margin_end(    10)
        armour_grid.set_margin_top(    10)
        armour_grid.set_margin_bottom( 10)

        weapon_grid.attach(wea_type,    0, 0, 1, 1)
        weapon_grid.attach(wea_cost,    1, 0, 1, 1)
        weapon_grid.attach(wea_damg,    2, 0, 1, 1)
        weapon_grid.attach(wea_rang,    3, 0, 1, 1)
        weapon_grid.attach(wea_relo,    4, 0, 1, 1)
        weapon_grid.attach(wea_weig,    5, 0, 1, 1)
        weapon_grid.attach(wea_crit,    6, 0, 1, 1)
        weapon_grid.attach(wea_aim,     7, 0, 1, 1)
        weapon_grid.attach(wea_amm,     8, 0, 1, 1)
        weapon_grid.attach(wea_sep,     0, 1,11, 1)
        weapon_grid.set_column_spacing(10)
        weapon_grid.set_row_spacing(10)
        weapon_grid.set_margin_start(10)
        weapon_grid.set_margin_end(10)
        weapon_grid.set_margin_top(10)
        weapon_grid.set_margin_bottom(10)

        
        scroll_weapon = Gtk.ScrolledWindow.new()
        scroll_armour = Gtk.ScrolledWindow.new()
        scroll_weapon.set_propagate_natural_width(True)
        scroll_weapon.set_min_content_height(350)
        scroll_armour.set_min_content_height(350)
        scroll_weapon.add(weapon_grid)
        scroll_armour.add(armour_grid)

        armour_frame.add(scroll_armour)
        weapon_frame.add(scroll_weapon)
        box.pack_start(armour_frame, True, True, 2)
        box.pack_start(weapon_frame, True, True, 2)
        
        col = 0
        row = 2
        atip = ['Name','Worth','Weight','A/C Bonus','Check Penalty']
        aindex = 0
        for key, value in armour.items():
            for element in value:
                if element in armour:
                    new = Gtk.Label.new(element.title())
                    new.set_xalign(1)
                    new.set_tooltip_text(atip[aindex])
                    armour_grid.attach(new, col, row, 1, 1)
                    col += 1
                    aindex += 1
                    new.show()
                else:
                    new = Gtk.Label.new(element.title())
                    new.set_tooltip_text(atip[aindex])
                    armour_grid.attach(new, col, row, 1, 1)
                    col += 1
                    aindex += 1
                    new.show()
                if element in armour:
                    key = element
            add = Gtk.Button.new_with_label("Add")
            add.connect('clicked', self.add_item, key) 
            remove = Gtk.Button.new_with_label("Remove")
            remove.connect('clicked', self.remove_item, key)
            blank1 = Gtk.Label.new("-----------")
            blank2 = Gtk.Label.new("-----------")
            armour_grid.attach(blank1, col, row, 1, 1)
            col += 1
            armour_grid.attach(blank2, col, row, 1, 1)
            col += 1
            armour_grid.attach(add, col, row, 1, 1)
            col += 1
            armour_grid.attach(remove, col, row, 1, 1)  
            col = 0
            row += 1
            aindex = 0
        wtip = ['Name','Worth','Damage','Range','Reload','Weight','Critical','Aim Bonus','Rounds']
        windex = 0
        for key, value in weapons.items(): 
            for element in value:
                if element in weapons:
                    new = Gtk.Label.new(element.title())
                    new.set_xalign(1)
                    new.set_tooltip_text(wtip[windex])
                    weapon_grid.attach(new, col, row, 1, 1)
                    col += 1
                    windex += 1
                    new.show()
                else:
                    new = Gtk.Label.new(element.title())
                    new.set_tooltip_text(wtip[windex])
                    weapon_grid.attach(new, col, row, 1, 1)
                    col += 1
                    windex += 1
                    new.show()
                if element in weapons:
                    key = element
            add = Gtk.Button.new_with_label("Add")
            add.connect('clicked', self.add_item, key)
            remove = Gtk.Button.new_with_label("Remove")
            remove.connect('clicked', self.remove_item, key,)
            weapon_grid.attach(add, col, row, 1, 1)
            weapon_grid.attach(remove, (col+1), row, 1, 1) 
            col = 0
            row += 1
            windex = 0
        self.show_all()
    def add_item(button, dictionary, key,):
        if key in weapon_set:
            item = weapons[key]
            player['inventory'].append(item)
            print(player['inventory'])
        elif key in armour_set:
            item = armour[key]
            player['inventory'].append(item)
            print(player['inventory'])  

    def remove_item(button, dictionary, key):
        try:
            if key in weapon_set:
                item = weapons[key]
                player['inventory'].remove(item)
                print(player['inventory'])
            elif key in armour_set:
                item = armour[key]
                player['inventory'].remove(item)
                print(player['inventory'])
        except Exception as e:
            print(e)
            try:
                if key in weapon_set:
                    item = list(weapons[key])
                    player['inventory'].remove(item)
                elif key in armour_set:
                    item = list(weapons[key])
                    player['inventory'].remove(item)
            except Exception as e:
                print(e)

class EditStats(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Character Stats")
        self.add_buttons("Done", 1)
        self.connect("show", self.show_dialog)  

        # Attribute titles
        STR = Gtk.Label(label="Strength:")
        DEX = Gtk.Label(label="Dexterity:")
        FIT = Gtk.Label(label="Fitness:")
        AGI = Gtk.Label(label="Agility:")
        WIS = Gtk.Label(label="Wisdom:")
        INT = Gtk.Label(label="Intelligence:")
        CHA = Gtk.Label(label="Charisma:")
        APP = Gtk.Label(label="Appearance:")
        LEVEL = Gtk.Label(label="Level:")
        LIFE = Gtk.Label(label="Life:")
        CLICKS = Gtk.Label(label="Clicks:")
        MONEY = Gtk.Label(label="Money:")
        AIM = Gtk.Label(label="Aim:")
        INTER = Gtk.Label(label="Interrupts:")
        SKILL = Gtk.Label.new("Skill Points:")

        # Right Align ALL titles
        STR.set_xalign(1)
        DEX.set_xalign(1)
        FIT.set_xalign(1)
        AGI.set_xalign(1)
        WIS.set_xalign(1)
        INT.set_xalign(1)
        CHA.set_xalign(1)
        APP.set_xalign(1)
        LEVEL.set_xalign(1)
        LIFE.set_xalign(1)
        CLICKS.set_xalign(1)
        MONEY.set_xalign(1)
        AIM.set_xalign(1)
        INTER.set_xalign(1)
        SKILL.set_xalign(1)
        
        # Attribute Entry Fields
        self.STR_entry = Gtk.Entry()
        self.DEX_entry = Gtk.Entry()
        self.FIT_entry = Gtk.Entry()
        self.AGI_entry = Gtk.Entry()
        self.WIS_entry = Gtk.Entry()
        self.INT_entry = Gtk.Entry()
        self.CHA_entry = Gtk.Entry()
        self.APP_entry = Gtk.Entry()
        self.LEVEL_entry = Gtk.Entry()
        self.LIFE_entry = Gtk.Entry()
        self.CLICKS_entry = Gtk.Entry()
        self.MONEY_entry = Gtk.Entry()
        self.AIM_entry = Gtk.Entry()
        self.INTER_entry = Gtk.Entry()
        self.SKILL_entry = Gtk.Entry()
        
        self.STR_entry.set_max_length(2)
        self.DEX_entry.set_max_length(2)
        self.FIT_entry.set_max_length(2)
        self.FIT_entry.set_max_length(2)
        self.AGI_entry.set_max_length(2)
        self.WIS_entry.set_max_length(2)
        self.INT_entry.set_max_length(2)
        self.CHA_entry.set_max_length(2)
        self.APP_entry.set_max_length(2)
        self.LEVEL_entry.set_max_length(2)
        self.LIFE_entry.set_max_length(3)
        self.CLICKS_entry.set_max_length(2)
        self.MONEY_entry.set_max_length(6)
        self.AIM_entry.set_max_length(2)
        self.INTER_entry.set_max_length(2)
        self.SKILL_entry.set_max_length(2)

        # Connect Entry Fields
        self.LEVEL_entry.connect("changed", self.save_level)
        self.LIFE_entry.connect("changed", self.save_life)
        self.CLICKS_entry.connect("changed", self.save_clicks)
        self.MONEY_entry.connect("changed", self.save_money)
        self.AIM_entry.connect("changed", self.save_aim)
        self.INTER_entry.connect("changed", self.save_inter)
        self.STR_entry.connect("changed", self.save_str)
        self.DEX_entry.connect("changed", self.save_dex)
        self.FIT_entry.connect("changed", self.save_fit)
        self.AGI_entry.connect("changed", self.save_agi)
        self.WIS_entry.connect("changed", self.save_wis)
        self.INT_entry.connect("changed", self.save_int)
        self.CHA_entry.connect("changed", self.save_cha)
        self.APP_entry.connect("changed", self.save_app)
        self.SKILL_entry.connect("changed", self.save_skill)

        # Box and Grid
        box = self.get_content_area()
        grid = Gtk.Grid()
        grid.set_column_homogeneous(False) 
        grid.set_column_spacing(2)
        grid.attach(LEVEL,          0, 0, 1, 1)
        grid.attach(LIFE,           0, 1, 1, 1)
        grid.attach(CLICKS,         0, 2, 1, 1)
        grid.attach(MONEY,          0, 3, 1, 1)
        grid.attach(AIM,            0, 4, 1, 1)
        grid.attach(INTER,          0, 5, 1, 1)
        grid.attach(STR,            0, 6, 1, 1)
        grid.attach(DEX,            0, 7, 1, 1)
        grid.attach(FIT,            0, 8, 1, 1)
        grid.attach(AGI,            0, 9, 1, 1)
        grid.attach(WIS,            0,10, 1, 1)
        grid.attach(INT,            0,11, 1, 1)
        grid.attach(CHA,            0,12, 1, 1)
        grid.attach(APP,            0,13, 1, 1)
        grid.attach(SKILL,          0,14, 1, 1)

        grid.attach(self.LEVEL_entry,    1, 0, 1, 1)
        grid.attach(self.LIFE_entry,     1, 1, 1, 1)
        grid.attach(self.CLICKS_entry,   1, 2, 1, 1)
        grid.attach(self.MONEY_entry,    1, 3, 1, 1)
        grid.attach(self.AIM_entry,      1, 4, 1, 1)
        grid.attach(self.INTER_entry,    1, 5, 1, 1)
        grid.attach(self.STR_entry,      1, 6, 1, 1)
        grid.attach(self.DEX_entry,      1, 7, 1, 1)
        grid.attach(self.FIT_entry,      1, 8, 1, 1)
        grid.attach(self.AGI_entry,      1, 9, 1, 1)
        grid.attach(self.WIS_entry,      1,10, 1, 1)
        grid.attach(self.INT_entry,      1,11, 1, 1)
        grid.attach(self.CHA_entry,      1,12, 1, 1)
        grid.attach(self.APP_entry,      1,13, 1, 1)
        grid.attach(self.SKILL_entry,    1,14, 1, 1)
        grid.set_margin_start(10)
        grid.set_margin_end(10)
        grid.set_margin_top(10)
        grid.set_margin_bottom(10)
        
        box.pack_start(grid, True, True, 4)
        self.show_all()

    def save_level(self, widget):
        level = self.LEVEL_entry.get_text()
        player['level'] = level
        print(brightcyan + "Level:",player['level'] + reset)

    def save_life(self, widget):
        life = self.LIFE_entry.get_text()
        player['life'] = life
        print(brightmagenta + "Life:", player['life'] + reset)

    def save_clicks(self, widget):
        clicks = self.CLICKS_entry.get_text()
        player['clicks'] = clicks
        print(brightcyan + "Clicks:", player['clicks'] + reset)

    def save_money(self, widget):
        money = self.MONEY_entry.get_text()
        player['money'] = money
        print(brightmagenta + "Money:", player['money'] + reset)

    def save_aim(self, widget):
        aim = self.AIM_entry.get_text()
        player['aim'] = aim
        print(brightmagenta + "Aim:", player['aim'] + reset)

    def save_inter(self, widget):
        inter = self.INTER_entry.get_text()
        player['interrupts'] = inter
        print(brightcyan + "Interrupts:", player['interrupts'] + reset)

    def save_str(self, widget):
        stre = self.STR_entry.get_text()
        player['strength'] = stre
        print(brightmagenta + "Strength:", player['strength'] + reset)

    def save_dex(self, widget):
        dex = self.DEX_entry.get_text()
        player['dexterity'] = dex
        print(brightcyan + "Dexterity:", player['dexterity'] + reset)

    def save_fit(self, widget):
        fit = self.FIT_entry.get_text()
        player['fitness'] = fit
        print(brightmagenta + "Fitness:", player['fitness'] + reset)

    def save_agi(self, widget):
        agi = self.AGI_entry.get_text()
        player['agility'] = agi
        print(brightcyan + "Agility:", player['agility'] + reset)

    def save_wis(self, widget):
        wis = self.WIS_entry.get_text()
        player['wisdom'] = wis
        print(brightmagenta + "Wisdom:", player['wisdom'] + reset)

    def save_int(self, widget):
        inte = self.INT_entry.get_text()
        player['intelligence'] = inte
        print(brightcyan + "Intelligence:", player['intelligence'] + reset)

    def save_cha(self, widget):
        cha = self.CHA_entry.get_text()
        player['charisma'] = cha
        print(brightmagenta + "Charisma:", player['charisma'] + reset)

    def save_app(self, widget):
        app = self.APP_entry.get_text()
        player['appearance'] = app
        print(brightcyan + "Appearance:", player['appearance'] + reset)
    
    def save_skill(self, widget):
        skill = self.SKILL_entry.get_text()
        player['skill_points'] = skill
        print(brightmagenta + "Skill Points:", player['skill_points'] + reset)

    def show_dialog(self, dialog):
        self.LEVEL_entry.set_text(player['level'])
        self.LIFE_entry.set_text(player['life'])
        self.CLICKS_entry.set_text(player['clicks'])
        self.MONEY_entry.set_text(player['money'])
        self.AIM_entry.set_text(player['aim'])
        self.INTER_entry.set_text(player['interrupts'])
        self.STR_entry.set_text(player['strength'])
        self.DEX_entry.set_text(player['dexterity'])
        self.FIT_entry.set_text(player['fitness'])
        self.AGI_entry.set_text(player['agility'])
        self.WIS_entry.set_text(player['wisdom'])
        self.INT_entry.set_text(player['intelligence'])
        self.CHA_entry.set_text(player['charisma'])
        self.APP_entry.set_text(player['appearance'])
        self.SKILL_entry.set_text(player['skill_points'])

class EditSkillMethod(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Skills & Methods")
        box = self.get_content_area()
        self.add_button('Done', 1)
        
        # Skill Set and Methods - Add/Remove
        skill_method = Gtk.Frame()
        skill_method_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        skill_method_box.set_margin_start(5)
        skill_method_box.set_margin_end(5)
        
        player_type = player['type']
        player_type = player_type.title()
        skill_markup = f"<span size='medium' weight='bold'>{player_type}'s Skill Set</span>"

        skill_frame = Gtk.Frame()
        skill_frame.set_shadow_type(0)
        skill_frame_label = Gtk.Label()
        skill_frame_label.set_markup(skill_markup)
        skill_frame.set_label_widget(skill_frame_label)
        skill_frame.set_label_align(0.5,0.5)
        self.skill_grid = Gtk.Grid()
        skill_title = Gtk.Label.new('Skill')
        skill_total = Gtk.Label.new('Total')
        skill_learned = Gtk.Label.new('Learned')
        skill_mod = Gtk.Label.new('Mod+')
        skill_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        self.skill_grid.attach(skill_title,     0, 0, 1, 1)
        self.skill_grid.attach(skill_total,     1, 0, 1, 1)
        self.skill_grid.attach(skill_learned,   2, 0, 1, 1)
        self.skill_grid.attach(skill_mod,       3, 0, 1, 1)
        self.skill_grid.attach(skill_sep,       0, 1, 4, 1)
        self.skill_grid.set_column_spacing(15)
        self.skill_grid.set_margin_start(10)
        self.skill_grid.set_margin_end(10)
        self.skill_grid.set_margin_top(10)
        self.skill_grid.set_margin_bottom(10)
        skill_frame.add(self.skill_grid)
        
        method_markup = f"<span size='medium' weight='bold'>{player_type} Methods</span>"
        method_frame = Gtk.Frame()
        method_frame.set_shadow_type(0)
        method_frame_label = Gtk.Label()
        method_frame_label.set_markup(method_markup)
        method_frame.set_label_widget(method_frame_label)
        method_frame.set_label_align(0.5,0.5)
        self.method_grid = Gtk.Grid()
        method_title = Gtk.Label.new('Method')
        method_desc = Gtk.Label.new('Description')
        method_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        self.method_grid.attach(method_title,    0, 0, 1, 1)
        self.method_grid.attach(method_desc,     1, 0, 1, 1)
        self.method_grid.attach(method_sep,      0, 1, 2, 1)
        self.method_grid.set_column_spacing(15)
        self.method_grid.set_margin_start(10)
        self.method_grid.set_margin_end(10)
        self.method_grid.set_margin_top(10)
        self.method_grid.set_margin_bottom(10)
        method_frame.add(self.method_grid)
        
        skill_method_box.pack_start(skill_frame, True, True, 2)
        skill_method_box.pack_start(method_frame, True, True, 2)
        skill_method.add(skill_method_box) 
        box.pack_start(skill_method, True, True, 2)
        self.add_skill_method()
        self.show_all()
    
    def add_skill_method(self):
        char_type = player['type']
        char_skills = player['skill']
        skills = skill_sets
        col = 0
        row = 2
        for key, value in skills.items():
            if key == char_type:
                # set skill key as name
                for skill, info in value.items():
                    name = Gtk.Label.new(skill.title())
                    name.set_xalign(1)
                    self.skill_grid.attach(name, col, row, 1, 1)
                    col += 1
                    #iterate through tuple setting values 
                    for item in info:
                        if item == info[0]:
                            continue
                        else:
                            new = Gtk.Label.new(item.title())
                            self.skill_grid.attach(new, col, row, 1, 1)
                            new.show()
                            col += 1
                    add_skill = Gtk.Button(label="Add")
                    add_skill.connect('clicked', self.add_skill, skill, info)
                    sub_skill = Gtk.Button(label="Remove")
                    sub_skill.connect('clicked', self.sub_skill, skill, info) 
                    self.skill_grid.attach(add_skill, col, row, 1, 1)
                    col += 1
                    self.skill_grid.attach(sub_skill, col, row, 1, 1)
                    col = 0
                    row += 1
            if key == 'generic':
                generic = Gtk.Label.new()
                generic.set_markup("<span size='medium' foreground='#0F0F0F' weight='bold'>Generic Skills</span>")
                generic.set_xalign(1)
                sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
                self.skill_grid.attach(generic, col, row, 1, 1)
                self.skill_grid.attach(sep, col, row, 4, 1)
                sep.show()
                generic.show()
                row += 1
                for skill, info in value.items():
                    name = Gtk.Label.new(skill.title())
                    name.set_xalign(1)
                    self.skill_grid.attach(name, col, row, 1, 1)
                    col += 1
                    for item in info:
                        if item == info[0]:
                            continue
                        else:
                            new = Gtk.Label.new(item.title())
                            self.skill_grid.attach(new, col, row, 1, 1)
                            new.show()
                            col +=1
                    add_skill = Gtk.Button(label="Add")
                    sub_skill = Gtk.Button(label="Remove")
                    add_skill.connect('clicked', self.add_skill, skill, info)
                    sub_skill.connect('clicked', self.sub_skill, skill, info)
                    self.skill_grid.attach(add_skill, col, row, 1, 1)
                    col += 1
                    self.skill_grid.attach(sub_skill, col, row, 1, 1)                           
                    col = 0
                    row += 1
    
    def add_skill(button, dictionary, skill, info):
        player_skill = player['skill']
        skills = (skill,) + info 
        print("skill",skill)
        skills = list(skills)
        player_skill.append(skills)
        print(player_skill)
    
    def sub_skill(button, dictionary, skill, info):
        player_skill = player['skill']
        skills = [skill,] + list(info)
        print("**player_skill is -->",player_skill)
        print("**skills is--------->",skills)
        for i in range(len(player_skill)-1,-1,-1):
            if player_skill[i][0] == skills[0]:
                del player_skill[i]

class Shop(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="The Only Shop Around")
        box = self.get_content_area()
        self.add_button('Done', 1)

        armour_grid = Gtk.Grid()
        weapon_grid = Gtk.Grid()
        
        armour_label = Gtk.Label()
        armour_label.set_markup("<span size='large' weight='bold'>Armour</span>")
        armour_frame = Gtk.Frame()
        armour_frame.set_label_widget(armour_label)
        armour_frame.set_label_align(0.05, 0.5)
        weapon_label = Gtk.Label()
        weapon_label.set_markup("<span size='large' weight='bold'>Weapons</span>")
        weapon_frame = Gtk.Frame()
        weapon_frame.set_label_widget(weapon_label)
        weapon_frame.set_label_align(0.05, 0.5)

        orientation = Gtk.Orientation.HORIZONTAL
        arm_type = Gtk.Label(label="Name")
        arm_cost = Gtk.Label(label="Price")
        arm_weight = Gtk.Label(label="Weight(lbs)")
        arm_bonus = Gtk.Label(label="A/C Bonus")
        arm_check = Gtk.Label(label="Check Penalty")
        arm_sep = Gtk.Separator.new(orientation) 

        wea_type = Gtk.Label.new("Name")
        wea_cost = Gtk.Label.new("Price")
        wea_damg = Gtk.Label.new("Damage")
        wea_rang = Gtk.Label.new("Range")
        wea_relo = Gtk.Label.new("Reload")
        wea_weig = Gtk.Label.new("Weight")
        wea_crit = Gtk.Label.new("Critical")
        wea_aim  = Gtk.Label.new("Aim Bonus")
        wea_amm  = Gtk.Label.new("Rounds")
        wea_sep = Gtk.Separator.new(orientation)
        
        armour_grid.attach(arm_type,    0, 0, 1, 1)
        armour_grid.attach(arm_cost,    1, 0, 1, 1)
        armour_grid.attach(arm_weight,  2, 0, 1, 1)
        armour_grid.attach(arm_bonus,   3, 0, 1, 1)
        armour_grid.attach(arm_check,   4, 0, 1, 1)
        armour_grid.attach(arm_sep,     0, 1, 9, 1)
        armour_grid.set_column_spacing(10)
        armour_grid.set_row_spacing(   10)
        armour_grid.set_margin_start(  10)
        armour_grid.set_margin_end(    10)
        armour_grid.set_margin_top(    10)
        armour_grid.set_margin_bottom( 10)

        weapon_grid.attach(wea_type,    0, 0, 1, 1)
        weapon_grid.attach(wea_cost,    1, 0, 1, 1)
        weapon_grid.attach(wea_damg,    2, 0, 1, 1)
        weapon_grid.attach(wea_rang,    3, 0, 1, 1)
        weapon_grid.attach(wea_relo,    4, 0, 1, 1)
        weapon_grid.attach(wea_weig,    5, 0, 1, 1)
        weapon_grid.attach(wea_crit,    6, 0, 1, 1)
        weapon_grid.attach(wea_aim,     7, 0, 1, 1)
        weapon_grid.attach(wea_amm,     8, 0, 1, 1)
        weapon_grid.attach(wea_sep,     0, 1,11, 1)
        weapon_grid.set_column_spacing(10)
        weapon_grid.set_row_spacing(10)
        weapon_grid.set_margin_start(10)
        weapon_grid.set_margin_end(10)
        weapon_grid.set_margin_top(10)
        weapon_grid.set_margin_bottom(10)

        scroll_weapon = Gtk.ScrolledWindow.new()
        scroll_armour = Gtk.ScrolledWindow.new()
        scroll_weapon.set_propagate_natural_width(True)
        scroll_weapon.set_min_content_height(350)
        scroll_armour.set_min_content_height(350)
        scroll_weapon.add(weapon_grid)
        scroll_armour.add(armour_grid)

        armour_frame.add(scroll_armour)
        weapon_frame.add(scroll_weapon)
        box.pack_start(armour_frame, True, True, 2)
        box.pack_start(weapon_frame, True, True, 2)

        col = 0
        row = 2
        atip = ['Name','Price','Weight','A/C Bonus','Check Penalty']
        aindex = 0
        for key, value in armour.items():
            for element in value:
                if element in armour:
                    new = Gtk.Label.new(element.title())
                    new.set_xalign(1)
                    new.set_tooltip_text(atip[aindex])
                    armour_grid.attach(new, col, row, 1, 1)
                    col += 1
                    aindex += 1
                    new.show()
                else:
                    new = Gtk.Label.new(element.title())
                    new.set_tooltip_text(atip[aindex])
                    armour_grid.attach(new, col, row, 1, 1)
                    col += 1
                    aindex += 1
                    new.show()
                if element in armour:
                    key = element
                if '$' in element:
                    price = element
            buy = Gtk.Button.new_with_label("Purchase")
            buy.connect('clicked', self.buy_item, key, price) 
            sell = Gtk.Button.new_with_label("Sell")
            sell.connect('clicked', self.sell_item, key, price)
            blank1 = Gtk.Label.new("-----------")
            blank2 = Gtk.Label.new("-----------")
            armour_grid.attach(blank1, col, row, 1, 1)
            col += 1
            armour_grid.attach(blank2, col, row, 1, 1)
            col += 1
            armour_grid.attach(buy, col, row, 1, 1)
            col += 1
            if value in player['inventory']:
                armour_grid.attach(sell, col, row, 1, 1)  
            col = 0
            row += 1
            aindex = 0
        wtip = ['Name','Price','Damage','Range','Reload','Weight','Critical','Aim Bonus','Rounds']
        windex = 0
        for key, value in weapons.items(): 
            for element in value:
                if element in weapons:
                    new = Gtk.Label.new(element.title())
                    new.set_xalign(1)
                    new.set_tooltip_text(wtip[windex])
                    weapon_grid.attach(new, col, row, 1, 1)
                    col += 1
                    windex += 1
                    new.show()
                else:
                    new = Gtk.Label.new(element.title())
                    new.set_tooltip_text(wtip[windex])
                    weapon_grid.attach(new, col, row, 1, 1)
                    col += 1
                    windex += 1
                    new.show()
                if element in weapons:
                    key = element
                if '$' in element:
                    price = element
            buy = Gtk.Button.new_with_label("Purchase")
            buy.connect('clicked', self.buy_item, key, price)
            sell = Gtk.Button.new_with_label("Sell")
            sell.connect('clicked', self.sell_item, key, price)
            weapon_grid.attach(buy, col, row, 1, 1)
            if value in player['inventory']:
                weapon_grid.attach(sell, (col+1), row, 1, 1) 
            col = 0
            row += 1
            windex = 0
        self.show_all()
    def buy_item(button, dictionary, key, price):
        purse = player['money']
        purse = purse.strip("$")
        purse = int(purse)
        price = price.strip("$")
        price = int(price)
        if price <= purse: 
            if key in weapon_set:
                item = weapons[key]
                player['inventory'].append(item)
                purse -= price
                player['money'] = "$"+str(purse)
            elif key in armour_set:
                item = armour[key]
                player['inventory'].append(item)
                purse -= price
                player['money'] = "$"+str(purse)
        else:
            print(player['money']) 
    def sell_item(button, dictionary, key, price):
        purse = player['money']
        purse = purse.strip("$")
        purse = int(purse)
        price = price.strip("$")
        price = int(price)
        try:
            if key in weapon_set and player['inventory']:
                item = weapons[key]
                purse += price
                player['inventory'].remove(item)
                player['money'] = "$"+str(purse)
            elif key in armour_set and player['inventory']:
                item = armour[key]
                purse += price
                player['inventory'].remove(item)
                player['money'] = "$"+str(purse)
            super().__init__()
        except Exception as e:
            print(e)

class MainWindow(Gtk.Window):
       
    def __init__(self):
        super().__init__(title="The Generator 0.1")
        self.set_icon_from_file("FINGEN.png")
        css = Gtk.CssProvider()
        css.load_from_path('style.css')
        screen = Gdk.Screen.get_default()
        style = Gtk.StyleContext()
        style.add_provider_for_screen(screen, css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Name
        name = Gtk.Label()
        name.set_markup("<span size='x-large' weight='bold'>Name</span>")
        name.set_tooltip_text("Enter your Character's Name")
        self.data_name = Gtk.Entry()
        self.data_name.set_alignment(1)
        self.data_name.connect("changed", self.add_name)
        
        # Race
        race = Gtk.Label()
        race.set_markup("<span size='x-large' weight='bold'>Race</span>")
        race.set_tooltip_text("What Race are you?")
        race.set_xalign(1)
        self.race_selector = Gtk.ComboBoxText.new_with_entry()
        self.race_selector.append_text("     ")
        self.race_selector.append_text("Human")
        self.race_selector.append_text("Midget")
        self.race_selector.append_text("Outsider")
        self.race_selector.append_text("Cyborg")
        self.race_selector.append_text("Mutant")
        self.race_selector.connect("changed", self.add_race)

        # Type
        tyype = Gtk.Label()
        tyype.set_markup("<span size='x-large' weight='bold'>Type</span>")
        tyype.set_tooltip_text("What is your Type?")
        tyype.set_xalign(1)
        self.tyype_selector = Gtk.ComboBoxText.new_with_entry()
        self.tyype_selector.append_text("    ")
        self.tyype_selector.append_text("Thug")
        self.tyype_selector.append_text("Naturalist")
        self.tyype_selector.append_text("Martial Artist")
        self.tyype_selector.append_text("Thief")
        self.tyype_selector.append_text("Chemist")
        self.tyype_selector.append_text("Techer")
        self.tyype_selector.append_text("Mystic")
        self.tyype_selector.append_text("Seeker")
        self.tyype_selector.append_text("Gunslinger")
        self.tyype_selector.append_text("Face")
        self.tyype_selector.connect("changed", self.add_type)
        att_mu = "<span size='large' weight='bold'>0</span>"

        # Level
        level = Gtk.Label()
        level.set_markup("<span size='large' weight='bold'>Level:</span>")
        level.set_tooltip_text("Character Level")
        level.set_width_chars(8)
        level.set_xalign(1)
        self.level_value = Gtk.Label.new()
        self.level_value.set_markup(att_mu)
        self.level_value.set_width_chars(6)
        self.level_value.set_xalign(0)

        # Life
        life = Gtk.Label()
        life.set_markup("<span size='large' weight='bold'>Life:</span>")
        life.set_xalign(1)
        self.life_value = Gtk.Label.new()
        self.life_value.set_markup(att_mu)
        self.life_value.set_xalign(0)

        # Clicks
        clicks = Gtk.Label()
        clicks.set_markup("<span size='large' weight='bold'>Clicks:</span>")
        clicks.set_xalign(1)
        self.clicks_value = Gtk.Label.new()
        self.clicks_value.set_markup(att_mu)
        self.clicks_value.set_xalign(0)
        

        # Money
        money = Gtk.Label()
        money.set_markup("<span size='large' weight='bold'>$$$:</span>")
        money.set_xalign(1)
        self.money_value = Gtk.Label.new()
        self.money_value.set_markup(att_mu)
        self.money_value.set_xalign(0)

        # Initiative
        initiative = Gtk.Label()
        initiative.set_markup("<span size='large' weight='bold'>Initiative:</span>")
        initiative.set_xalign(1)
        self.initiative_value = Gtk.Label.new()
        self.initiative_value.set_markup(att_mu)
        self.initiative_value.set_xalign(0)

        # Aim
        aim = Gtk.Label()
        aim.set_markup("<span size='large' weight='bold'>Aim:</span>")
        aim.set_xalign(1)
        self.aim_value = Gtk.Label.new()
        self.aim_value.set_markup(att_mu)
        self.aim_value.set_xalign(0)

        # Interrupts
        interrupts = Gtk.Label()
        interrupts.set_markup("<span size='large' weight='bold'>Interrupts:</span>")
        interrupts.set_xalign(1)
        self.interrupts_value = Gtk.Label.new()
        self.interrupts_value.set_markup(att_mu)
        self.interrupts_value.set_xalign(0)

        # Strength
        strength = Gtk.Label()
        strength.set_tooltip_text("Strength")
        strength.set_markup("<span size='large' weight='bold'>STR:</span>")
        strength.set_tooltip_text("Strength")
        strength.set_xalign(1)
        self.strength_value = Gtk.Label.new()
        self.strength_value.set_markup(att_mu)
        self.strength_value.set_xalign(0)
        strengthmod = Gtk.Label(label="+")
        strengthmod.set_xalign(1)
        self.strengthmod_value = Gtk.Label(label="0")
        self.strengthmod_value.set_xalign(0)

        # Dexterity
        dexterity = Gtk.Label()
        dexterity.set_tooltip_text("Dexterity")
        dexterity.set_markup("<span size='large' weight='bold'>DEX:</span>")
        dexterity.set_xalign(1)
        self.dexterity_value = Gtk.Label.new()
        self.dexterity_value.set_markup(att_mu)
        self.dexterity_value.set_xalign(0)
        dexteritymod = Gtk.Label(label="+")
        dexteritymod.set_xalign(1)
        self.dexteritymod_value = Gtk.Label(label="0")
        self.dexteritymod_value.set_xalign(0)

        # Fitness
        fitness = Gtk.Label()
        fitness.set_tooltip_text("Fitness")
        fitness.set_markup("<span size='large' weight='bold'>FIT:</span>")
        fitness.set_xalign(1)
        self.fitness_value = Gtk.Label.new()
        self.fitness_value.set_markup(att_mu)
        self.fitness_value.set_xalign(0)
        fitnessmod = Gtk.Label(label="+")
        fitnessmod.set_xalign(1)
        self.fitnessmod_value = Gtk.Label(label="0")
        self.fitnessmod_value.set_xalign(0)

        # Agility
        agility = Gtk.Label()
        agility.set_tooltip_text("Agility")
        agility.set_markup("<span size='large' weight='bold'>AGI:</span>")
        agility.set_xalign(1)
        self.agility_value = Gtk.Label.new()
        self.agility_value.set_markup(att_mu)
        self.agility_value.set_xalign(0)
        agilitymod = Gtk.Label(label="+")
        agilitymod.set_xalign(1)
        self.agilitymod_value = Gtk.Label(label="0")
        self.agilitymod_value.set_xalign(0)

        # Wisdom
        wisdom = Gtk.Label()
        wisdom.set_tooltip_text("Wisdom")
        wisdom.set_markup("<span size='large' weight='bold'>WIS:</span>")
        wisdom.set_xalign(1)
        self.wisdom_value = Gtk.Label.new()
        self.wisdom_value.set_markup(att_mu)
        self.wisdom_value.set_xalign(0)
        wisdommod = Gtk.Label(label="+")
        wisdommod.set_xalign(1)
        self.wisdommod_value = Gtk.Label(label="0")
        self.wisdommod_value.set_xalign(0)

        # Intelligence
        intelligence = Gtk.Label()
        intelligence.set_tooltip_text("Intelligence")
        intelligence.set_markup("<span size='large' weight='bold'>INT:</span>")
        intelligence.set_xalign(1)
        self.intelligence_value = Gtk.Label.new()
        self.intelligence_value.set_markup(att_mu)
        self.intelligence_value.set_xalign(0)
        intelligencemod = Gtk.Label(label="+")
        intelligencemod.set_xalign(1)
        self.intelligencemod_value = Gtk.Label(label="0")
        self.intelligencemod_value.set_xalign(0)

        # Charisma
        charisma = Gtk.Label()
        charisma.set_tooltip_text("Charisma")
        charisma.set_markup("<span size='large' weight='bold'>CHA:</span>")
        charisma.set_xalign(1)
        self.charisma_value = Gtk.Label.new()
        self.charisma_value.set_markup(att_mu)
        self.charisma_value.set_xalign(0)
        charismamod = Gtk.Label(label="+")
        charismamod.set_xalign(1)
        self.charismamod_value = Gtk.Label(label="0")
        self.charismamod_value.set_xalign(0)

        # Appearance
        appearance = Gtk.Label()
        appearance.set_tooltip_text("Appearance")
        appearance.set_markup("<span size='large' weight='bold'>APP:</span>")
        appearance.set_xalign(1)
        self.appearance_value = Gtk.Label.new()
        self.appearance_value.set_markup(att_mu)
        self.appearance_value.set_xalign(0)
        appearancemod = Gtk.Label(label="+")
        appearancemod.set_xalign(1)
        self.appearancemod_value = Gtk.Label(label="0")
        self.appearancemod_value.set_xalign(0)

        # Armour stats
        arm_base = Gtk.Label(label="BASE")
        arm_base.set_tooltip_text("Base Armor Class")
        self.arm_base_value = Gtk.Label(label="10")
        arm_wis = Gtk.Label(label="WIS+")
        self.arm_wis_value = Gtk.Label(label="0")
        arm_equipped = Gtk.Label(label="EQUIPPED")
        self.arm_equipped_value = Gtk.Label(label="0")
        arm_mod = Gtk.Label(label="MOD+")
        self.arm_mod_value = Gtk.Label(label="0")
        arm_agi = Gtk.Label(label="AGI+")
        self.arm_agi_value = Gtk.Label(label="0")
        arm_total = Gtk.Label(label="TOTAL")
        self.arm_total_value = Gtk.Label(label="0")
        self.set_arm_stats()
        
        armour_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        armour_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        armour_box1.pack_start(arm_total, True, True, 1)
        armour_box1.pack_start(arm_base, True, True, 1)
        armour_box1.pack_start(arm_equipped, True, True, 1)
        armour_box1.pack_start(arm_mod, True, True, 1)
        armour_box1.pack_start(arm_agi, True, True, 1)
        armour_box1.pack_start(arm_wis, True, True, 1)

        armour_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        armour_box2.pack_start(self.arm_total_value, True, True, 1)
        armour_box2.pack_start(self.arm_base_value, True, True, 1)
        armour_box2.pack_start(self.arm_equipped_value, True, True, 1)
        armour_box2.pack_start(self.arm_mod_value, True, True, 1)
        armour_box2.pack_start(self.arm_agi_value, True, True, 1)
        armour_box2.pack_start(self.arm_wis_value, True, True, 1)

        armour_box.pack_start(armour_box1, True, True, 1)
        armour_box.pack_start(armour_box2, True, True, 1)
        armour_box.set_margin_start(10)
        armour_box.set_margin_end(10)
        armour_box.set_margin_top(10)
        armour_box.set_margin_bottom(10)
        
        # Armour Frame
        armour = Gtk.Frame()
        armour_label = Gtk.Label()
        armour_label.set_markup("<span size='large' weight='bold'>Armour Class</span>")
        armour.set_label_widget(armour_label)
        armour.set_label_align(0.1, 0.5)
        armour.add(armour_box)
        
        # Resilience stats 
        # Matter
        mat = Gtk.Label(label="MATTER")
        mat.set_xalign(1)
        self.mat_total = Gtk.Label(label="0")
        self.mat_mod = Gtk.Label(label="0")
        self.mat_mod.set_tooltip_text("Average of Strength, Dexterity,\nFitness and Agility mod.")
        self.mat_type = Gtk.Label(label="0")
        self.mat_lvl = Gtk.Label(label="0")

        # Reaction
        react = Gtk.Label(label="REACTION")
        react.set_xalign(1)
        self.react_total = Gtk.Label(label="0")
        self.react_mod = Gtk.Label(label="0")
        self.react_mod.set_tooltip_text("Average of Fitness, Agility,\nWisdom and Intelligence mod.")
        self.react_type = Gtk.Label(label="0")
        self.react_lvl = Gtk.Label(label="0")

        # Mind
        mind = Gtk.Label(label="MIND")
        mind.set_xalign(1)
        self.mind_total = Gtk.Label(label="0")
        self.mind_mod = Gtk.Label(label="0")
        self.mind_mod.set_tooltip_text("Average of Wisdom, Intelligence,\nCharisma and Appearance mod.")
        self.mind_type = Gtk.Label(label="0")
        self.mind_lvl = Gtk.Label(label="0")

        # Titles 
        res_blank0 = Gtk.Label(label=" ")
        res_blank1 = Gtk.Label(label=" ")
        res_blank2 = Gtk.Label(label=" ")
        res_total = Gtk.Label(label="Total")
        res_mod = Gtk.Label(label="Mod+")
        res_type = Gtk.Label(label="Type+")
        res_lvl = Gtk.Label(label="Lvl+")

        res_grid = Gtk.Grid()    #Child, Column, Row, #Columns, #Rows)
        res_grid.attach(res_blank0,       0, 0, 1, 4)
        res_grid.attach(res_blank1,       1, 0, 1, 1)
        res_grid.attach(res_total,        2, 0, 1, 1)
        res_grid.attach(res_mod,          3, 0, 1, 1)
        res_grid.attach(res_type,         4, 0, 1, 1)
        res_grid.attach(res_lvl,          5, 0, 1, 1)
        res_grid.attach(mat,              1, 1, 1, 1)
        res_grid.attach(self.mat_total,   2, 1, 1, 1)
        res_grid.attach(self.mat_mod,     3, 1, 1, 1)
        res_grid.attach(self.mat_type,    4, 1, 1, 1)
        res_grid.attach(self.mat_lvl,     5, 1, 1, 1)
        res_grid.attach(react,            1, 2, 1, 1)
        res_grid.attach(self.react_total, 2, 2, 1, 1)
        res_grid.attach(self.react_mod,   3, 2, 1, 1)
        res_grid.attach(self.react_type,  4, 2, 1, 1)
        res_grid.attach(self.react_lvl,   5, 2, 1, 1)
        res_grid.attach(mind,             1, 3, 1, 1)
        res_grid.attach(self.mind_total,  2, 3, 1, 1)
        res_grid.attach(self.mind_mod,    3, 3, 1, 1)
        res_grid.attach(self.mind_type,   4, 3, 1, 1)
        res_grid.attach(self.mind_lvl,    5, 3, 1, 1)
        res_grid.attach(res_blank2,       0, 4, 6, 1)
        res_grid.set_column_spacing(20)
        res_grid.set_margin_end(10)
        res_grid.set_margin_top(10)

        # Add Frame
        resilience = Gtk.Frame()
        res_label = Gtk.Label()
        res_label.set_markup("<span size='large' weight='bold'>Resilience</span>")
        resilience.set_label_widget(res_label)
        resilience.set_label_align(0.1, 0.5)
        resilience.add(res_grid)
        
        # Equipped Armour
        self.e_arm_grid = Gtk.Grid()
        e_armour = Gtk.Frame()
        e_armour_label = Gtk.Label()
        e_armour_label.set_markup("<span size='large' weight='bold'>Equipped Armour</span>")
        e_armour.set_label_widget(e_armour_label)
        e_armour.set_label_align(0.1, 0.5)
        e_armour_type = Gtk.Label.new("Name")
        e_armour_weight = Gtk.Label.new("Weight")
        e_armour_ac = Gtk.Label.new("A/C Bonus")
        e_armour_check = Gtk.Label.new("Check Penalty")
        self.e_arm_grid.attach(e_armour_type,   0, 0, 1, 1)
        self.e_arm_grid.attach(e_armour_weight, 1, 0, 1, 1)
        self.e_arm_grid.attach(e_armour_ac,     2, 0, 1, 1)
        self.e_arm_grid.attach(e_armour_check,  3, 0, 1, 1)
        self.e_arm_grid.set_column_spacing(15)
        self.e_arm_grid.set_margin_start(10)
        self.e_arm_grid.set_margin_end(10)
        self.e_arm_grid.set_margin_top(10)
        self.e_arm_grid.set_margin_bottom(10)
        e_armour.add(self.e_arm_grid)

        # Armour Inventory
        armour_inv = Gtk.Frame()
        armour_inv.set_shadow_type(0)
        armour_inv_label = Gtk.Label()
        armour_inv_label.set_markup("<span size='medium' weight='bold'>Armour</span>")
        armour_inv.set_label_widget(armour_inv_label)
        armour_inv.set_label_align(0.5, 0.5)
        self.armour_inv_grid = Gtk.Grid()
        armour_name = Gtk.Label(label="Name")
        armour_cost = Gtk.Label(label="Worth")
        armour_weight = Gtk.Label(label="Weight")
        armour_ac = Gtk.Label(label="A/C Bonus")
        armour_check = Gtk.Label(label="Check Penalty")

        armour_cost.set_tooltip_text("Expected value of armour.")
        armour_weight.set_tooltip_text("Weight of armour.")
        armour_ac.set_tooltip_text("Armour Class bonus.")
        armour_check.set_tooltip_text("Penalty taken on checks.")
        
        arm_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        self.armour_inv_grid.attach(armour_name,    0, 0, 1, 1)
        self.armour_inv_grid.attach(armour_cost,    1, 0, 1, 1)
        self.armour_inv_grid.attach(armour_weight,  2, 0, 1, 1)
        self.armour_inv_grid.attach(armour_ac,      3, 0, 1, 1)
        self.armour_inv_grid.attach(armour_check,   4, 0, 1, 1)
        self.armour_inv_grid.attach(arm_sep,        0, 1, 7, 1)
        self.armour_inv_grid.set_column_spacing(20)
        self.armour_inv_grid.set_margin_start(10)
        self.armour_inv_grid.set_margin_end(10)
        self.armour_inv_grid.set_margin_top(10)
        self.armour_inv_grid.set_margin_bottom(10)
        armour_inv.add(self.armour_inv_grid)

        # Weapon Inventory
        weapon_inv = Gtk.Frame()
        weapon_inv.set_shadow_type(0)
        weapon_inv_label = Gtk.Label()
        weapon_inv_label.set_markup("<span size='medium' weight='bold'>Weapons</span>")
        weapon_inv.set_label_widget(weapon_inv_label)
        weapon_inv.set_label_align(0.5, 0.5)
        self.weapon_inv_grid = Gtk.Grid()
        weapon_name = Gtk.Label.new("Name")
        weapon_worth = Gtk.Label.new("Worth")
        weapon_dmg = Gtk.Label.new("Damage")
        weapon_range = Gtk.Label.new("Range")
        weapon_reload = Gtk.Label.new("Reload")
        weapon_weight = Gtk.Label.new("Weight")
        weapon_crit = Gtk.Label.new("Critical")
        weapon_aim = Gtk.Label.new("Aim Bonus")
        weapon_rounds = Gtk.Label.new("Rounds")
        
        weapon_worth.set_tooltip_text("Expected value of the weapon.")
        weapon_dmg.set_tooltip_text("Dice to roll for damage plus bonus if any.")
        weapon_range.set_tooltip_text("Max effective range without taking aim penalty.")
        weapon_reload.set_tooltip_text("The number of Clicks required for a full reload.")
        weapon_weight.set_tooltip_text("Weight of weapon.")
        weapon_crit.set_tooltip_text("Roll needed for a critical hit, X2 requires\
                \n\ttwo 19-20 rolls, x3 three, etc.")
        weapon_aim.set_tooltip_text("Bonus applied to Aim.")
        weapon_rounds.set_tooltip_text("Max shots before reload.")

        weap_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        self.weapon_inv_grid.attach(weapon_name,     0, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_worth,    1, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_dmg,      2, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_range,    3, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_reload,   4, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_weight,   5, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_crit,     6, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_aim,      7, 0, 1, 1)
        self.weapon_inv_grid.attach(weapon_rounds,   8, 0, 1, 1)
        self.weapon_inv_grid.attach(weap_sep,        0, 1, 9, 1)
        self.weapon_inv_grid.set_column_spacing(15)
        self.weapon_inv_grid.set_margin_start(10)
        self.weapon_inv_grid.set_margin_end(10)
        self.weapon_inv_grid.set_margin_top(10)
        self.weapon_inv_grid.set_margin_bottom(10)
        weapon_inv.add(self.weapon_inv_grid)
       
        self.weight_grid = Gtk.Grid()
        weight_label = Gtk.Label()
        weight_label.set_markup("<span weight='bold' size='medium'>Total Weight:</span>")
        weight_label.set_xalign(1)
        self.weight_value = Gtk.Label()
        self.weight_grid.attach(weight_label, 0, 0, 1, 1)
        self.weight_grid.attach(self.weight_value, 1, 0, 1, 1)
        self.weight_grid.set_margin_start(10)
        self.weight_grid.set_margin_end(10)

        # Inventory Frame and Box
        main_inv = Gtk.Frame()
        main_inv_label = Gtk.Label()
        main_inv_label.set_markup("<span size='large' weight='bold'>Inventory</span>")
        main_inv.set_label_widget(main_inv_label)
        main_inv.set_label_align(0.05, 0.5)
        main_inv_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        main_inv_box.pack_start(armour_inv, True, True, 2)
        main_inv_box.pack_start(weapon_inv, True, True, 2)
        main_inv_box.pack_start(self.weight_grid, True, True, 2)
        main_inv.add(main_inv_box)
        
        # Skill Set and Methods - Character
        skill_method = Gtk.Frame()
        skill_method_label = Gtk.Label()
        skill_method_label.set_markup("<span size='large' weight='bold'>Skill &amp; Method</span>")
        skill_method.set_label_widget(skill_method_label)
        skill_method.set_label_align(0.1,0.5)
        skill_method_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        skill_method_box.set_margin_start(5)
        skill_method_box.set_margin_end(5)
        
        skill_frame = Gtk.Frame()
        skill_frame.set_shadow_type(0)
        skill_frame_label = Gtk.Label()
        skill_frame_label.set_markup("<span size='medium' weight='bold'>Skill Set</span>")
        skill_frame.set_label_widget(skill_frame_label)
        skill_frame.set_label_align(0.5,0.5)
        self.skill_grid = Gtk.Grid()
        skill_title = Gtk.Label.new('Skill')
        skill_total = Gtk.Label.new('Total')
        skill_learned = Gtk.Label.new('Learned')
        skill_mod = Gtk.Label.new('Mod+')
        skill_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        skill_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.skill_points = Gtk.Label()
        self.skill_points.set_markup(f"<span weight='bold'>Skill Points to allocate ->{player['skill_points']}</span>")
        cur_sep1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        cur_sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        cur_grid = Gtk.Grid()
        cur_grid.set_halign(Gtk.Align.END)
        cur_grid.set_hexpand(True)
        cur_grid.attach(cur_sep1, 3, 0, 1, 1)
        cur_grid.attach(self.skill_points, 3, 1, 1, 1)
        cur_grid.attach(cur_sep2, 3, 2, 1, 1)
        cur_grid.set_column_spacing(10)
        cur_grid.set_margin_start(10)
        cur_grid.set_margin_end(10)
        
        self.skill_grid.attach(skill_title,     0, 0, 1, 1)
        self.skill_grid.attach(skill_total,     1, 0, 1, 1)
        self.skill_grid.attach(skill_learned,   2, 0, 1, 1)
        self.skill_grid.attach(skill_mod,       3, 0, 1, 1)
        self.skill_grid.attach(skill_sep,       0, 1, 5, 1)
        self.skill_grid.set_column_spacing(15)
        self.skill_grid.set_margin_start(10)
        self.skill_grid.set_margin_end(10)
        self.skill_grid.set_margin_top(10)
        self.skill_grid.set_margin_bottom(10)
        skill_box.pack_start(self.skill_grid, True, True, 0)
        skill_box.pack_start(cur_grid, True, True, 0)
        skill_frame.add(skill_box)

        method_frame = Gtk.Frame()
        method_frame.set_shadow_type(0)
        method_frame_label = Gtk.Label()
        method_frame_label.set_markup("<span size='medium' weight='bold'>Methods</span>")
        method_frame.set_label_widget(method_frame_label)
        method_frame.set_label_align(0.5,0.5)
        self.method_grid = Gtk.Grid()
        method_title = Gtk.Label.new('Method')
        method_desc = Gtk.Label.new('Description')
        method_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        self.method_grid.attach(method_title,    0, 0, 1, 1)
        self.method_grid.attach(method_desc,     1, 0, 1, 1)
        self.method_grid.attach(method_sep,      0, 1, 2, 1)
        self.method_grid.set_column_spacing(15)
        self.method_grid.set_margin_start(10)
        self.method_grid.set_margin_end(10)
        self.method_grid.set_margin_top(10)
        self.method_grid.set_margin_bottom(10)
        method_frame.add(self.method_grid)
        
        skill_scroll = Gtk.ScrolledWindow.new()
        #skill_scroll.set_min_content_height(250)
        skill_scroll.set_propagate_natural_width(True)
        skill_scroll.set_propagate_natural_height(True)
        skill_scroll.add(skill_frame)
        method_scroll = Gtk.ScrolledWindow.new()
        #method_scroll.set_min_content_height(250)
        method_scroll.set_propagate_natural_height(True)
        method_scroll.set_propagate_natural_width(True)
        method_scroll.add(method_frame)

        skill_method_box.pack_start(skill_scroll, True, True, 2)
        skill_method_box.pack_start(method_scroll, True, True, 0)
        skill_method.add(skill_method_box)
    

        # Name, Race, Type
        first_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        first_box.pack_start(name, True, True, 2)
        first_box.pack_start(self.data_name, True, True, 2)
        first_box.pack_start(race, True, True, 2)
        first_box.pack_start(self.race_selector, True, True, 2)
        first_box.pack_start(tyype, True, True, 2)
        first_box.pack_start(self.tyype_selector, True, True, 2)
        
        #Level, Life, Clicks, Money
        second_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        second_box.pack_start(level, True, True, 2)
        second_box.pack_start(self.level_value, True, True, 2)
        second_box.pack_start(life, True, True, 2)
        second_box.pack_start(self.life_value, True, True, 2)
        second_box.pack_start(clicks, True, True, 2)
        second_box.pack_start(self.clicks_value, True, True, 2)
        second_box.pack_start(money, True, True, 2)
        second_box.pack_start(self.money_value, True, True, 2)
        
        #Initiative, Aim, Interrupts
        third_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        third_box.pack_start(initiative, True, True, 1)
        third_box.pack_start(self.initiative_value, True, True, 1)
        third_box.pack_start(aim, True, True, 1)
        third_box.pack_start(self.aim_value, True, True, 1)
        third_box.pack_start(interrupts, True, True, 1)
        third_box.pack_start(self.interrupts_value, True, True, 1)
        
        #Strength, Dexterity, Fitness, Agility...
        fourth_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        fourth_box.pack_start(strength, True, True, 1)
        fourth_box.pack_start(self.strength_value, True, True, 1)
        fourth_box.pack_start(dexterity, True, True, 1) 
        fourth_box.pack_start(self.dexterity_value, True, True, 1)
        fourth_box.pack_start(fitness, True, True, 1)
        fourth_box.pack_start(self.fitness_value, True, True, 1)
        fourth_box.pack_start(agility, True, True, 1)
        fourth_box.pack_start(self.agility_value, True, True, 1)
        fourth_box.pack_start(wisdom, True, True, 1)
        fourth_box.pack_start(self.wisdom_value, True, True, 1)
        fourth_box.pack_start(intelligence, True, True, 1)
        fourth_box.pack_start(self.intelligence_value, True, True, 1)
        fourth_box.pack_start(charisma, True, True, 1)
        fourth_box.pack_start(self.charisma_value, True, True, 1)
        fourth_box.pack_start(appearance, True, True, 1)
        fourth_box.pack_start(self.appearance_value, True, True, 1)

        #Attribute Modifier Values
        fifth_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        fifth_box.pack_start(strengthmod , True, True, 1)
        fifth_box.pack_start(self.strengthmod_value , True, True, 1)
        fifth_box.pack_start(dexteritymod , True, True, 1)
        fifth_box.pack_start(self.dexteritymod_value , True, True, 1)
        fifth_box.pack_start(fitnessmod , True, True, 1)
        fifth_box.pack_start(self.fitnessmod_value , True, True, 1)
        fifth_box.pack_start(agilitymod , True, True, 1)
        fifth_box.pack_start(self.agilitymod_value , True, True, 1)
        fifth_box.pack_start(wisdommod , True, True, 1)
        fifth_box.pack_start(self.wisdommod_value , True, True, 1)
        fifth_box.pack_start(intelligencemod , True, True, 1)
        fifth_box.pack_start(self.intelligencemod_value , True, True, 1)
        fifth_box.pack_start(charismamod , True, True, 1)       
        fifth_box.pack_start(self.charismamod_value , True, True, 1)
        fifth_box.pack_start(appearancemod, True, True, 1)
        fifth_box.pack_start(self.appearancemod_value, True, True, 1)

        # Seperator bars
        hbar1 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        hbar2 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        hbar3 = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        
        # Menu 
        menu_bar = Gtk.MenuBar()
        menu_setup_item = Gtk.MenuItem.new_with_label(label="Setup")
        menu_setup = Gtk.Menu()
        menu_setup_item.set_submenu(menu_setup)

        menu_shop_item = Gtk.MenuItem.new_with_label(label="Shop")
        menu_shop = Gtk.Menu()
        menu_shop_item.set_submenu(menu_shop)

        menu_combat_item = Gtk.MenuItem.new_with_label(label="Combat")
        menu_combat = Gtk.Menu()
        menu_combat_item.set_submenu(menu_combat)

        menu_roll_dice_item = Gtk.MenuItem.new_with_label(label="Roll Dice")

        menu_print = Gtk.MenuItem.new_with_label(label="Print to File")
        menu_edit = Gtk.MenuItem.new_with_label(label="Attributes")
        menu_roll = Gtk.MenuItem.new_with_label(label="Roll Character")
        menu_inve = Gtk.MenuItem.new_with_label(label="Inventory")
        menu_save = Gtk.MenuItem.new_with_label(label="Save Current")
        menu_load = Gtk.MenuItem.new_with_label(label="Load Last")
        menu_skill_method = Gtk.MenuItem.new_with_label(label="Skills/Methods")

        menu_only_shop = Gtk.MenuItem.new_with_label(label="The Only Shop")
    
        menu_print.set_tooltip_text("Prints Character to Text File")
        menu_edit.set_tooltip_text("Edit Character Stats")
        menu_roll.set_tooltip_text("      Roll Character Stats\n*OVERWRITES ALL STATS!*")
        menu_inve.set_tooltip_text("Add/Remove Inventory Items")
        menu_save.set_tooltip_text("Save Current Character")
        menu_load.set_tooltip_text("Load Last Saved Character")
        menu_skill_method.set_tooltip_text("Add/Remove Skills/Methods")

        menu_print.connect("activate", self.print_char_sheet)
        menu_edit.connect("activate", self.editstats)
        menu_roll.connect("activate", self.generate_stats)
        menu_inve.connect("activate", self.edit_inv)
        menu_save.connect("activate", self.save)
        menu_load.connect("activate", self.load)
        menu_roll_dice_item.connect("activate", self.rollsim)
        menu_skill_method.connect("activate", self.skillmethod)
        menu_only_shop.connect("activate", self.go_shopping)

        menu_setup.insert(menu_load, 0)
        menu_setup.insert(menu_save, 1)
        menu_setup.insert(menu_roll, 2)
        menu_setup.insert(menu_print, 3)
        
        menu_shop.insert(menu_only_shop,0)

        menu_bar.append(menu_setup_item)
        menu_bar.append(menu_shop_item)
        menu_bar.append(menu_combat_item)
        menu_bar.append(menu_roll_dice_item)
        menu_bar.append(menu_edit)
        menu_bar.append(menu_inve)
        menu_bar.append(menu_skill_method)

        #Log Area
        log = Gtk.ScrolledWindow()
        self.text = Gtk.Label(label="...")
        log.add(self.text)

        # Notes Area
        notes_frame = Gtk.Frame()
        notes_frame_label = Gtk.Label()
        notes_frame_label.set_markup("<span size='large' weight='bold'>Notes</span>")
        notes_frame.set_label_widget(notes_frame_label)
        notes_frame.set_label_align(0.05, 0.5)
        self.notes = Gtk.TextView.new()
        self.notes.set_name("notes")
        self.notes.set_bottom_margin(4)
        self.notes.set_wrap_mode(2)
        self.notes_buffer = self.notes.get_buffer()
        self.notes_buffer.set_text(player['notes'])
        notes_frame.add(self.notes)
        self.notes_buffer.connect("changed", self.update_notes)

        #Grid (child, column, row, #columns, #rows)
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(8)
        self.grid.attach(menu_bar,     0, 0, 3, 1)
        self.grid.attach(first_box,    0, 1, 3, 1)
        self.grid.attach(second_box,   0, 2, 3, 1)
        self.grid.attach(hbar1,        0, 3, 3, 1)
        self.grid.attach(third_box,    0, 4, 3, 1)
        self.grid.attach(hbar2,        0, 5, 3, 1)
        self.grid.attach(fourth_box,   0, 6, 3, 1)
        self.grid.attach(fifth_box,    0, 7, 3, 1)
        self.grid.attach(hbar3,        0, 8, 3, 1)
        self.grid.attach(skill_method, 2, 9, 1,10)
        self.grid.attach(armour,       0, 9, 1, 2)
        self.grid.attach(resilience,   1, 9, 1, 3)
        self.grid.attach(e_armour,     0,11, 1, 1)
        self.grid.attach(main_inv,     0,12, 2, 7)
        self.grid.attach(notes_frame,  0,19, 2, 4)
        self.grid.attach(log,          0,24, 2, 1)
        self.grid.set_column_spacing(4)
        self.grid.set_column_homogeneous(True)
        self.grid.set_margin_start(5)
        self.grid.set_margin_end(5)
        self.grid.set_margin_top(5)
        self.grid.set_margin_bottom(5)
        
        main_grid = Gtk.Grid()
        main_grid.set_column_spacing(10)
        main_frame = Gtk.Frame()
        main_frame.set_shadow_type(0)
        main_frame.add(self.grid)
        main_grid.attach(main_frame, 1, 1, 1, 1)
        main_grid.set_margin_start(10)
        main_grid.set_margin_end(10)
        main_grid.set_margin_top(5)
        main_grid.set_margin_bottom(5)
        
        self.add(main_grid)


    def set_inv_weight(self):
        arm_grid = self.armour_inv_grid
        arm_rows = arm_grid.get_children()
        arm_rows = (len(arm_rows) // 7) + 2
        arm_col = 2
        arm_weight = 0
        wea_grid = self.weapon_inv_grid
        wea_rows = wea_grid.get_children()
        wea_rows = (len(wea_rows) // 10) + 2
        wea_col = 5
        wea_weight = 0
        total = 0
        for row in range(2,arm_rows):
            try:
                weight = arm_grid.get_child_at(arm_col, row)
                weight = weight.get_text()
                weight = weight.strip("Lbs")
                arm_weight += int(weight)
            except Exception as e:
                print(e,"set_inv_weight func error armour")
        for row in range(2,wea_rows):
            try:
                weight = wea_grid.get_child_at(wea_col, row)
                weight = weight.get_text()
                weight = weight.strip("Lbs")
                wea_weight += int(weight)
            except Exception as e:
                print(e,"set_inv_weight func error weapons")
        total = wea_weight + arm_weight
        if total >= 75:
            overage = total - 75
            overage = str(overage)+" Lbs too heavy"
            total = str(total)+" Lbs"
            max_load = "75 Lbs"
            max_load_markup = f"<span weight='bold' color='#FA7379'> (Max load is currently {max_load})</span>"
            label_markup = f"<span weight='bold' color='#FA7379'>{total}--</span><span weight='bold' color='#FA7379'>{overage}</span>{max_load_markup}"
            self.weight_value.set_markup(label_markup)
        else:
            total = str(total)+" Lbs"
            label_markup = f"<span weight='bold' color='#BBDEF0'>{total}</span>"
            self.weight_value.set_markup(label_markup)


    def set_arm_stats(self):
        base_get = int(self.arm_base_value.get_text())
        wis_get = int(self.wisdommod_value.get_text())
        equip_get = int(self.arm_equipped_value.get_text())
        mod_get = int(self.arm_mod_value.get_text())
        agi_get = int(self.agilitymod_value.get_text())
        total_get = base_get + (wis_get//2) + equip_get + mod_get + agi_get 
        wis_set = str(wis_get//2) 
        agi_set = str(agi_get)
        total_set = str(total_get)
        self.arm_total_value.set_text(total_set)
        self.arm_agi_value.set_text(agi_set)
        self.arm_wis_value.set_text(wis_set) 

    def set_res_stats(self):
        matt_mod = int((int(self.strengthmod_value.get_text()) +
                        int(self.dexteritymod_value.get_text()) + 
                        int(self.fitnessmod_value.get_text()) +
                        int(self.agilitymod_value.get_text()))/4)        
        reac_mod = int((int(self.fitnessmod_value.get_text()) +
                        int(self.agilitymod_value.get_text()) +
                        int(self.wisdommod_value.get_text()) + 
                        int(self.intelligencemod_value.get_text()))/4)
        mind_mod = int((int(self.wisdommod_value.get_text()) +
                        int(self.intelligencemod_value.get_text()) +
                        int(self.charismamod_value.get_text()) +
                        int(self.appearancemod_value.get_text()))/4)
        lvl = 1
        try:
            lvl = int(self.level_value.get_text())//2
        except:
            print('--Level Error: Level is set to 1--')
        matt_type = 0
        reac_type = 0
        mind_type = 0
        race_bonus = 0
        if player['type'] == 'gunslinger':
            if player['level'] in set(['1','2','3','4']):  
                matt_type = 0
                reac_type = 0
                mind_type = 1
            elif player['level'] in set(['5','6','7','8','9']):
                matt_type = 0
                reac_type = 0
                mind_type = 2
            elif player['level'] in set(['10','11','12','13','14']):
                matt_type = 0
                reac_type = 0
                mind_type = 3
            elif player['level'] in set(['15','16','17','18','19']):
                matt_type = 0
                reac_type = 0
                mind_type = 4
            elif player['level'] >= '20':
                matt_type = 0
                reac_type = 0
                mind_type = 5
        elif player['type'] == 'naturalist':
            if player['level'] in set(['1','2','3','4']):  
                matt_type = 1
                reac_type = 1
                mind_type = 1
            elif player['level'] in set(['5','6','7','8','9']):
                matt_type = 2
                reac_type = 2
                mind_type = 2
            elif player['level'] in set(['10','11','12','13','14']):
                matt_type = 3
                reac_type = 3
                mind_type = 3
            elif player['level'] in set(['15','16','17','18','19']):
                matt_type = 4
                reac_type = 4
                mind_type = 4
            elif player['level'] >= '20':
                matt_type = 5
                reac_type = 5
                mind_type = 5
        elif player['type'] == 'martial artist':
            if player['level'] in set(['1','2','3','4']):  
                matt_type = 1
                reac_type = 1
                mind_type = 1
            elif player['level'] in set(['5','6','7','8','9']):
                matt_type = 2
                reac_type = 2
                mind_type = 2
            elif player['level'] in set(['10','11','12','13','14']):
                matt_type = 3
                reac_type = 3
                mind_type = 3
            elif player['level'] in set(['15','16','17','18','19']):
                matt_type = 4
                reac_type = 4
                mind_type = 4
            elif player['level'] >= '20':
                matt_type = 5
                reac_type = 5
                mind_type = 5
        elif player['type'] == 'thief':
            if player['level'] in set(['1','2','3']):  
                matt_type = 0
                reac_type = 1
                mind_type = 0
            elif player['level'] in set(['4','5','6']):
                matt_type = 0
                reac_type = 2
                mind_type = 0
            elif player['level'] in set(['7','8','9','10']):
                matt_type = 0
                reac_type = 3
                mind_type = 0
            elif player['level'] in set(['11','12','13']):
                matt_type = 0
                reac_type = 4
                mind_type = 0
            elif player['level'] in set(['14','15','16']):
                matt_type = 0
                reac_type = 5
                mind_type = 0
            elif player['level'] in set(['17','18','19']):
                matt_type = 0
                reac_type = 6
                mind_type = 0
            elif player['level'] >= '20':
                matt_type = 0
                reac_type = 7
                mind_type = 0
        elif player['type'] == 'thug':
            if player['level'] in set(['1','2','3','4','5']):  
                matt_type = 1
                reac_type = 0
                mind_type = 0
            elif player['level'] in set(['6','7','8','9','10']):
                matt_type = 2
                reac_type = 0
                mind_type = 0
            elif player['level'] in set(['11','12','13','14','15']):
                matt_type = 3
                reac_type = 0
                mind_type = 0
            elif player['level'] in set(['16','17','18','19']):
                matt_type = 4
                reac_type = 0
                mind_type = 0
            elif player['level'] >= '20':
                matt_type = 5
                reac_type = 0
                mind_type = 0
        elif player['type'] == 'mystic':
            if player['level'] == '1':
                matt_type = 0
                reac_type = 0
                mind_type = 2
            if player['level'] == '2':
                matt_type = 0
                reac_type = 0
                mind_type = 3
            if player['level'] == '3':
                matt_type = 1
                reac_type = 1
                mind_type = 3
            if player['level'] == '4':
                matt_type = 1
                reac_type = 1
                mind_type = 4
            if player['level'] == '5':
                matt_type = 2
                reac_type = 2
                mind_type = 4
            if player['level'] == '6':
                matt_type = 2
                reac_type = 2
                mind_type = 5
            if player['level'] == '7':
                matt_type = 3
                reac_type = 3
                mind_type = 5
            if player['level'] =='8':
                matt_type = 3
                reac_type = 3
                mind_type = 6
            if player['level'] == '9':
                matt_type = 3
                reac_type = 3
                mind_type = 7
            if player['level'] >= '10':
                matt_type = 4
                reac_type = 4
                mind_type = 7
        elif player['type'] == 'seeker':
            if player['level'] in set(['1','2','3']):  
                matt_type = 1
                reac_type = 0
                mind_type = 0
            elif player['level'] in set(['4','5','6','7']):
                matt_type = 1
                reac_type = 1
                mind_type = 0
            elif player['level'] in set(['8','9','10','11']):
                matt_type = 2
                reac_type = 1
                mind_type = 0
            elif player['level'] in set(['12','13','14','15']):
                matt_type = 2
                reac_type = 1
                mind_type = 1
            elif player['level'] in set(['16','17','18','19']):
                matt_type = 3
                reac_type = 1
                mind_type = 1
            elif player['level'] >= '20':
                matt_type = 3
                reac_type = 2
                mind_type = 1
        else:
            matt_type = 0
            reac_type = 0
            mind_type = 0
        if player['race'] == 'outsider':
            race_bonus = 2
        matt_tot = str(matt_mod + lvl + matt_type)
        reac_tot = str(reac_mod + lvl + reac_type)
        mind_tot = str(mind_mod + lvl + mind_type + race_bonus)
        self.mat_total.set_text(matt_tot)
        self.mat_mod.set_text(str(matt_mod))
        self.mat_type.set_text(str(matt_type))
        self.react_total.set_text(reac_tot)
        self.react_mod.set_text(str(reac_mod))
        self.react_type.set_text(str(reac_type))
        self.mind_total.set_text(mind_tot)
        self.mind_mod.set_text(str(mind_mod))
        self.mind_type.set_text(str(mind_type))
        self.mat_lvl.set_text(str(lvl))
        self.react_lvl.set_text(str(lvl))
        self.mind_lvl.set_text(str(lvl))

    def set_atts_markup(self):
        INIT = self.dexteritymod_value.get_text()
        level_markup = f"<span size='large' weight='bold'>{player['level']}</span>"
        life_markup = f"<span size='large' weight='bold'>{player['life']}</span>" 
        clicks_markup = f"<span size='large' weight='bold'>{player['clicks']}</span>"
        money_markup = f"<span size='large' weight='bold'>{player['money']}</span>"
        init_markup = f"<span size='large' weight='bold'>{INIT}</span>"
        aim_markup = f"<span size='large' weight='bold'>{player['aim']}</span>"
        inter_markup = f"<span size='large' weight='bold'>{player['interrupts']}</span>"
        str_markup = f"<span size='large' weight='bold'>{player['strength']}</span>"
        dex_markup = f"<span size='large' weight='bold'>{player['dexterity']}</span>"
        fit_markup = f"<span size='large' weight='bold'>{player['fitness']}</span>"
        agi_markup = f"<span size='large' weight='bold'>{player['agility']}</span>"
        wis_markup = f"<span size='large' weight='bold'>{player['wisdom']}</span>"
        int_markup = f"<span size='large' weight='bold'>{player['intelligence']}</span>"
        cha_markup = f"<span size='large' weight='bold'>{player['charisma']}</span>"
        app_markup = f"<span size='large' weight='bold'>{player['appearance']}</span>"
        self.level_value.set_markup(level_markup)
        self.life_value.set_markup(life_markup)
        self.clicks_value.set_markup(clicks_markup)
        self.money_value.set_markup(money_markup)
        self.initiative_value.set_markup(init_markup)
        self.aim_value.set_markup(aim_markup)
        self.interrupts_value.set_markup(inter_markup)
        self.strength_value.set_markup(str_markup)
        self.dexterity_value.set_markup(dex_markup)
        self.fitness_value.set_markup(fit_markup)
        self.agility_value.set_markup(agi_markup)
        self.wisdom_value.set_markup(wis_markup)
        self.intelligence_value.set_markup(int_markup)
        self.charisma_value.set_markup(cha_markup)
        self.appearance_value.set_markup(app_markup)
        self.skill_points.set_markup(f"<span weight='bold'>Skill Points to allocate ->{player['skill_points']}</span>")

    def clear_arm_inv(self):
        row = 2
        row_count = self.armour_inv_grid.get_children()
        row_count = (int(len(row_count))//5)
        for rows in range(1,row_count):
            print(row,"<--Row to remove")
            self.armour_inv_grid.remove_row(row)    

    def set_arm_inv(self):
        inventory = player['inventory']
        col = 0
        row = 2
        self.clear_arm_inv()
        for t in inventory:
            if t[0] in armour_set:
                key = t[0]
                for s in t:
                    new = Gtk.Label.new(s.title())
                    self.armour_inv_grid.attach(new, col, row, 1, 1)
                    col += 1
                    new.show()
                equip = Gtk.Button(label="Equip")
                equip.connect('clicked', self.equip_armour, key)
                equip.show()
                unequip = Gtk.Button(label="Unequip")
                unequip.connect('clicked', self.unequip_armour)
                unequip.show()
                self.armour_inv_grid.attach(equip, col, row, 1, 1)
                self.armour_inv_grid.attach(unequip, col+1, row, 1, 1)
                row += 1 
                col = 0

    def clear_e_arm(self):
        armour = player['equipped_armour']
        row = 2
        for t in armour:
            self.e_arm_grid.remove_row(row)
            armour.remove(t)

    def unequip_armour(self, button):
        armour = player['equipped_armour']
        row = 2
        if armour:
            self.e_arm_grid.remove_row(row)
            armour.clear()
            self.arm_equipped_value.set_text('0')
        self.set_arm_stats()

    def equip_armour(self, button, key):
        armour = player['equipped_armour']
        inventory = player['inventory']
        col = 0
        row = 2
        ac_bonus = ""
        self.clear_e_arm()
        for t in inventory:
            if t[0] in armour_set and t[0] == key and t[0] not in armour:
                for s in t:
                    ac_bonus = t[3]
                    self.arm_equipped_value.set_text(ac_bonus)
                    if s == t[1]:
                        continue
                    elif s != t[1]:
                        new = Gtk.Label.new(s.title())
                        self.e_arm_grid.attach(new, col, row, 1, 1)
                        new.show()
                    col += 1
                row += 1
                col = 0
                armour.append(t)
                self.set_arm_stats()
                break
    def set_e_arm(self):
        armour = player['equipped_armour']
        col = 0 
        row = 2 
        try:
            for t in armour:
                self.e_arm_grid.remove_row(2)
                for s in t:
                    self.arm_equipped_value.set_text(t[3])
                    if s == t[1]:
                        continue
                    elif s != t[1]:
                        new = Gtk.Label.new(s.title())
                        self.e_arm_grid.attach(new,col, row, 1, 1)
                        new.show()
                    col += 1 
                row += 1
                col = 0
        except Exception as e:
            print(e,'<--Error in set_e_arm()')

    def clear_weapon_inv(self):
        row = 2
        row_count = self.weapon_inv_grid.get_children()
        row_count = ((len(row_count))//9)
        for rows in range(1,row_count):
            self.weapon_inv_grid.remove_row(row)

    def set_weapon_inv(self):
        inventory = player['inventory']
        col = 0
        row = 2
        self.clear_weapon_inv()
        for item in inventory:
            if item[0] in weapon_set:
                key = item[0]
                for string in item:
                    new = Gtk.Label.new(string.title())
                    self.weapon_inv_grid.attach(new, col, row, 1, 1)
                    col += 1
                    new.show()
                row += 1
                col = 0

    def generate_stats(self, widget):
        player['strength'] = str(roll())
        player['dexterity'] = str(roll())
        player['fitness'] = str(roll())
        player['agility'] = str(roll())
        player['wisdom'] = str(roll())
        player['intelligence'] = str(roll())
        player['charisma'] = str(roll())
        player['appearance'] = str(roll())
        player['life'] = str(roll(6,6))
        player['money'] = str(roll(6,6))
        player['clicks'] = "6"
        player['level'] = "1"
        player['aim'] = "6"
        self.strength_value.set_text(player['strength'])
        self.dexterity_value.set_text(player['dexterity'])
        self.fitness_value.set_text(player['fitness'])
        self.agility_value.set_text(player['agility'])
        self.wisdom_value.set_text(player['wisdom'])
        self.intelligence_value.set_text(player['intelligence'])
        self.charisma_value.set_text(player['charisma'])
        self.appearance_value.set_text(player['appearance'])
        self.life_value.set_text(player['life'])
        self.money_value.set_text(player['money'])
        self.clicks_value.set_text(player['clicks'])
        self.level_value.set_text(player['level'])
        self.aim_value.set_text(player['aim'])
        self.set_atts_markup()
        self.set_res_stats()
        self.set_mods()
        self.set_arm_stats()
        INIT = self.dexteritymod_value.get_text()
        player['initiative'] = INIT
        self.initiative_value.set_text(player['initiative'])

    def skillmethod(self, widget):
        dialog = EditSkillMethod(self)
        response = dialog.run()
        if response == 1:
            self.set_skills()
            dialog.destroy()

    def rollsim(self, widget):
        dialog = RollDice(self)
        response = dialog.run()
        if response == 1:
            dialog.destroy()

    def update_notes(self, widget):
        buffer = self.notes.get_buffer()
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        player['notes'] = buffer.get_text(start_iter, end_iter, True)
        print(player['notes'])

    def editstats(self, widget):
        dialog = EditStats(self)
        response = dialog.run()
        if response == 1:
            print(yellow + "Character Stats Output to Sheet" + reset)
            self.level_value.set_text(player['level'])
            self.life_value.set_text(player['life'])
            self.clicks_value.set_text(player['clicks'])
            self.money_value.set_text(player['money'])
            self.initiative_value.set_text(player['initiative'])
            self.aim_value.set_text(player['aim'])
            self.interrupts_value.set_text(player['interrupts'])
            self.strength_value.set_text(player['strength'])
            self.dexterity_value.set_text(player['dexterity'])
            self.fitness_value.set_text(player['fitness'])
            self.agility_value.set_text(player['agility'])
            self.wisdom_value.set_text(player['wisdom'])
            self.intelligence_value.set_text(player['intelligence'])
            self.charisma_value.set_text(player['charisma'])
            self.appearance_value.set_text(player['appearance'])
            self.skill_points.set_markup(f"<span weight='bold'>Skill Points to allocate ->{player['skill_points']}</span>")
            self.set_atts_markup()
            self.set_mods()
            self.set_res_stats()
            self.set_arm_stats()
            self.text.set_text(f"--{player['name']} stats were updated--")
        dialog.destroy()

    def set_mods(self):
        strength = int(self.strength_value.get_text())
        dexterity = int(self.dexterity_value.get_text())
        fitness = int(self.fitness_value.get_text())
        agility = int(self.agility_value.get_text())
        wisdom = int(self.wisdom_value.get_text())
        intelligence = int(self.intelligence_value.get_text())
        charisma = int(self.charisma_value.get_text())
        appearance = int(self.appearance_value.get_text())
        if strength <= 11:
            self.strengthmod_value.set_text("0")
        elif 12 <= strength <= 13:
            self.strengthmod_value.set_text("1")
        elif 14 <= strength <= 15:
            self.strengthmod_value.set_text("2")
        elif 16 <= strength <= 17:
            self.strengthmod_value.set_text("3")
        elif 18 <= strength <= 19:
            self.strengthmod_value.set_text("4")
        elif strength >= 20:
            self.strengthmod_value.set_text("5")
        if dexterity <= 11:
            self.dexteritymod_value.set_text("0")
        elif 12 <= dexterity <= 13:
            self.dexteritymod_value.set_text("1")
        elif 14 <= dexterity <= 15:
            self.dexteritymod_value.set_text("2")
        elif 16 <= dexterity <= 17:
            self.dexteritymod_value.set_text("3")
        elif 18 <= dexterity <= 19:
            self.dexteritymod_value.set_text("4")
        elif dexterity >= 20:
            self.dexteritymod_value.set_text("5")
        if fitness <= 11:
            self.fitnessmod_value.set_text("0")
        elif 12 <= fitness <= 13:
            self.fitnessmod_value.set_text("1")
        elif 14 <= fitness <= 15:
            self.fitnessmod_value.set_text("2")
        elif 16 <= fitness <= 17:
            self.fitnessmod_value.set_text("3")
        elif 18 <= fitness <= 19:
            self.fitnessmod_value.set_text("4")
        elif fitness >= 20:
            self.fitnessmod_value.set_text("5")
        if agility <= 11:
            self.agilitymod_value.set_text("0")
        elif 12 <= agility <= 13:
            self.agilitymod_value.set_text("1")
        elif 14 <= agility <= 15:
            self.agilitymod_value.set_text("2")
        elif 16 <= agility <= 17:
            self.agilitymod_value.set_text("3")
        elif 18 <= agility <= 19:
            self.agilitymod_value.set_text("4")
        elif agility >= 20:
            self.agilitymod_value.set_text("5")
        if wisdom <= 11:
            self.wisdommod_value.set_text("0")
        elif 12 <= wisdom <= 13:
            self.wisdommod_value.set_text("1")
        elif 14 <= wisdom <= 15:
            self.wisdommod_value.set_text("2")
        elif 16 <= wisdom <= 17:
            self.wisdommod_value.set_text("3")
        elif 18 <= wisdom <= 19:
            self.wisdommod_value.set_text("4")
        elif wisdom >= 20:
            self.wisdommod_value.set_text("5")
        if intelligence <= 11:
            self.intelligencemod_value.set_text("0")
        elif 12 <= intelligence <= 13:
            self.intelligencemod_value.set_text("1")
        elif 14 <= intelligence <= 15:
            self.intelligencemod_value.set_text("2")
        elif 16 <= intelligence <= 17:
            self.intelligencemod_value.set_text("3")
        elif 18 <= intelligence <= 19:
            self.intelligencemod_value.set_text("4")
        elif intelligence >= 20:
            self.intelligencemod_value.set_text("5")
        if charisma <= 11:
            self.charismamod_value.set_text("0")
        elif 12 <= charisma <= 13:
            self.charismamod_value.set_text("1")
        elif 14 <= charisma <= 15:
            self.charismamod_value.set_text("2")
        elif 16 <= charisma <= 17:
            self.charismamod_value.set_text("3")
        elif 18 <= charisma <= 19:
            self.charismamod_value.set_text("4")
        elif charisma >= 20:
            self.charismamod_value.set_text("5")
        if appearance <= 11:
            self.appearancemod_value.set_text("0")
        elif 12 <= appearance <= 13:
            self.appearancemod_value.set_text("1")
        elif 14 <= appearance <= 15:
            self.appearancemod_value.set_text("2")
        elif 16 <= appearance <= 17:
            self.appearancemod_value.set_text("3")
        elif 18 <= appearance <= 19:
            self.appearancemod_value.set_text("4")
        elif appearance >= 20:
            self.appearancemod_value.set_text("5")

    def add_name(self, widget):
        name = self.data_name.get_text()
        name = name.title()
        self.data_name.set_text(name)
        player['name'] = name
        name = name.title()
        string = f"-- Player Name is set to {name} --"
        self.text.set_text(string)

    # Race Selection Tracker List 
    s_race = []
    def add_race(self, widget):
        race = self.race_selector.get_active_text()
        race = race.lower()
        race_entry = self.race_selector.get_child()
        l_player = player.copy() 
        if race.startswith('h'):
            l_player['race_flag'] = 'human'
            if not l_player['race_flag'] in self.s_race:
                APP = int(l_player['appearance']) + 1
                FIT = int(l_player['fitness']) + 1
                race_entry.set_text('Human')
                l_player['race'] = race
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.append('human')
                race_entry.set_text('Human')
            elif l_player['race_flag'] in self.s_race:
                race_entry.set_text('Human')
                l_player['race'] = race
            if 'midget' in self.s_race:
                AGI = int(l_player['agility']) - 1
                DEX = int(l_player['dexterity']) - 1
                CHA = int(l_player['charisma']) - 1
                l_player['agility'] = str(AGI)
                l_player['dexterity'] = str(DEX)
                l_player['charisma'] = str(CHA)
                self.s_race.remove('midget')
            if 'outsider' in self.s_race:
                INT = int(l_player['intelligence']) - 1
                l_player['intelligence'] = str(INT)
                self.s_race.remove('outsider')
            else:
                pass
        elif race.startswith('mi'):
            l_player['race_flag'] = 'midget'
            if not l_player['race_flag'] in self.s_race:
                AGI = int(l_player['agility']) + 1
                DEX = int(l_player['dexterity']) + 1
                CHA = int(l_player['charisma']) + 1
                race_entry.set_text('Midget')
                l_player['race'] = race
                l_player['agility'] = str(AGI)
                l_player['dexterity'] = str(DEX)
                l_player['charisma'] = str(CHA)
                self.s_race.append('midget')
            elif l_player['race_flag'] in self.s_race:
                race_entry.set_text('Midget')
                l_player['race'] = race
            if 'human' in self.s_race:
                APP = int(l_player['appearance']) - 1
                FIT = int(l_player['fitness']) - 1
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.remove('human')
            if 'outsider' in self.s_race:
                INT = int(l_player['intelligence']) - 1
                l_player['intelligence'] = str(INT)
                self.s_race.remove('outsider')
            else:
                pass
        elif race.startswith('o'):
            l_player['race_flag'] = 'outsider'
            if not l_player['race_flag'] in self.s_race:
                INT = int(l_player['intelligence']) + 1
                race_entry.set_text('Outsider')
                l_player['race'] = race
                l_player['intelligence'] = str(INT)
                self.s_race.append('outsider')
            elif l_player['race_flag'] in self.s_race:
                race_entry.set_text('Outsider')
                l_player['race'] = race
            if 'human' in self.s_race:
                APP = int(l_player['appearance']) - 1
                FIT = int(l_player['fitness']) - 1
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.remove('human')
            if 'midget' in self.s_race:
                AGI = int(l_player['agility']) - 1
                DEX = int(l_player['dexterity']) - 1
                CHA = int(l_player['charisma']) - 1
                l_player['agility'] = AGI
                l_player['dexterity'] = DEX
                l_player['charisma'] = CHA
                self.s_race.remove('midget')
            else:
                pass
        elif race.startswith('c'):
            l_player['race_flag'] = 'cyborg'
            race_entry.set_text('Cyborg')
            l_player['race'] = race
            if 'human' in self.s_race:
                APP = int(l_player['appearance']) - 1
                FIT = int(l_player['fitness']) - 1
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.remove('human')
            if 'midget' in self.s_race:
                AGI = int(l_player['agility']) - 1
                DEX = int(l_player['dexterity']) - 1
                CHA = int(l_player['charisma']) - 1
                l_player['agility'] = AGI
                l_player['dexterity'] = DEX
                l_player['charisma'] = CHA
                self.s_race.remove('midget')
            if 'outsider' in self.s_race:
                INT = int(l_player['intelligence']) - 1
                l_player['intelligence'] = str(INT)
                self.s_race.remove('outsider')
            else:
                pass
        elif race.startswith('mu'):
            race_entry.set_text('Mutant')
            l_player['race'] = race
            if 'human' in self.s_race:
                APP = int(l_player['appearance']) - 1
                FIT = int(l_player['fitness']) - 1
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.remove('human')
            if 'midget' in self.s_race:
                AGI = int(l_player['agility']) - 1
                DEX = int(l_player['dexterity']) - 1
                CHA = int(l_player['charisma']) - 1
                l_player['agility'] = AGI
                l_player['dexterity'] = DEX
                l_player['charisma'] = CHA
                self.s_race.remove('midget')
            if 'outsider' in self.s_race:
                INT = int(l_player['intelligence']) - 1
                l_player['intelligence'] = str(INT)
                self.s_race.remove('outsider')
            else:
                pass
        elif race.startswith(' '):
            race_entry.set_text('----')
            l_player['race'] = race
            if 'human' in self.s_race:
                APP = int(l_player['appearance']) - 1
                FIT = int(l_player['fitness']) - 1
                l_player['appearance'] = str(APP)
                l_player['fitness'] = str(FIT)
                self.s_race.remove('human')
            if 'midget' in self.s_race:
                AGI = int(l_player['agility']) - 1
                DEX = int(l_player['dexterity']) - 1
                CHA = int(l_player['charisma']) - 1
                l_player['agility'] = AGI
                l_player['dexterity'] = DEX
                l_player['charisma'] = CHA
                self.s_race.remove('midget')
            if 'outsider' in self.s_race:
                INT = int(l_player['intelligence']) - 1
                l_player['intelligence'] = str(INT)
                self.s_race.remove('outsider')
            else:
                pass
        string = f"-- Player Race is set to {race.capitalize()} --"
        self.text.set_text(string)
        player['race_flag'] = l_player['race_flag']
        player['race'] = l_player['race']
        player['appearance'] = l_player['appearance']
        player['fitness'] = l_player['fitness']
        player['agility'] = l_player['agility']
        player['dexterity'] = l_player['dexterity']
        player['charisma'] = l_player['charisma']
        player['intelligence'] = l_player['intelligence']
        self.set_res_stats()
        self.set_atts_markup()
        print(player['race'])

    def add_type(self, widget):
        tyype = self.tyype_selector.get_active_text()
        tyype = tyype.lower()
        type_entry = self.tyype_selector.get_child()
        if tyype.startswith('thu'):
            type_entry.set_text('Thug')
            player['type'] = tyype
        elif tyype.startswith('n'):
            type_entry.set_text('Naturalist')
            player['type'] = tyype
        elif tyype.startswith('ma'):
            type_entry.set_text('Martial Artist')
            player['type'] = tyype
        elif tyype.startswith('thi'):
            type_entry.set_text('Thief')
            player['type'] = tyype
        elif tyype.startswith('c'):
            type_entry.set_text('Chemist')
            player['type'] = tyype
        elif tyype.startswith('te'):
            type_entry.set_text('Techer')
            player['type'] = tyype
        elif tyype.startswith('my'):
            type_entry.set_text('Mystic')
            player['type'] = tyype
        elif tyype.startswith('s'):
            type_entry.set_text('Seeker')
            player['type'] = tyype
        elif tyype.startswith('g'):
            type_entry.set_text('Gunslinger')
            player['type'] = tyype
        elif tyype.startswith('f'):
            type_entry.set_text('Face')
            player['type'] = tyype
        elif tyype.startswith(' '):
            type_entry.set_text('----')
            player['type'] = 'generic'
        else:
            tyype = tyype.title()
            type_entry.set_text(tyype)
            player['type'] = tyype
        string = f" -- Player Type is set to {type_entry.get_text()} --"
        print(player['type'])
        self.set_res_stats()
        self.text.set_text(string)

    def skill_clean(self):
        skills = player['skill']
        row = 2
        for t in skills:
            self.skill_grid.remove_row(row)
        self.skill_grid.remove_row(row)

    def set_skills(self):
        skills = player['skill']
        col = 0
        row = 2
        self.skill_clean()
        mod = ''
        for skill in skills:
            for element in skill:
                if element == skill[1]:
                    mod = skill[1]
                    continue
                elif element != skill[4]:
                    if col == 0:
                        new = Gtk.Label.new(element.title())
                        new.set_xalign(1)
                        self.skill_grid.attach(new, col, row, 1, 1)
                        new.show()
                        col += 1
                    else:
                        new = Gtk.Label.new(element.title())
                        self.skill_grid.attach(new, col, row, 1, 1)
                        new.show()
                        col += 1
                else:
                    if len(skill[1]) > 3:
                        mod = mod.split('/')
                    else:
                        mod = [mod,]
                    mod_values = [] 
                    for s in mod:
                        if s == 'str':
                            temp = self.strengthmod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'dex':
                            temp = self.dexteritymod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'fit':
                            temp = self.fitnessmod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'agi':
                            temp = self.agilitymod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'wis':
                            temp = self.wisdommod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'int':
                            temp = self.intelligencemod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'cha':
                            temp = self.charismamod_value.get_text()
                            mod_values.append(temp)
                        elif s == 'app':
                            temp = self.appearancemod_value.get_text()
                            mod_values.append(temp)
                    mod_bonus = 0
                    if len(mod_values) > 1:
                        for i in mod_values:
                            mod_bonus += int(i)
                        mod_bonus = int(mod_bonus/len(mod_values))
                        mod_bonus = str(mod_bonus)
                    elif len(mod_values) == 1:
                        mod_bonus = mod_values[0]
                        mod_bonus = str(mod_bonus)
                    mod_bonus ='+'+ mod_bonus 
                    new = Gtk.Label.new(mod_bonus)
                    self.skill_grid.attach(new, col, row, 1, 1)
                    new.show()
                    col += 1
                    add_point = Gtk.Button(label="+")
                    self.skill_grid.attach(add_point, col, row, 1, 1)
                    add_point.connect("clicked",lambda widget, tag=row: self.add_skill_point(widget,tag))
                    add_point.show()
            row += 1
            col = 0
            self.total_skills()

    def total_skills(self):
        skills = player['skill']
        grid = self.skill_grid
        children = grid.get_children()
        max_row = int(((len(children)-5)/5)+2)
        min_row = 2 
        mod_column = 3
        learned_column = 2
        total_column = 1
        key_column = 0
        try:
            for row in range(min_row, max_row):
                mod = grid.get_child_at(mod_column, row)
                mod = mod.get_text()
                mod = mod.strip('+')
                mod = int(mod)
                learned = grid.get_child_at(learned_column, row)
                learned = learned.get_text()
                learned = int(learned)
                total = grid.get_child_at(total_column, row)
                total_v = total.get_text()
                total_v = int(total_v)
                key = grid.get_child_at(key_column, row)
                key = key.get_text()
                key = key.lower()
                total_v = mod + learned
                total_v = str(total_v)
                total.set_text(total_v)
        except:
            print("----***ERROR TOTALING ROW WITH NO SKILL***----")

    def add_skill_point(self, widget, tag):
        skills = player['skill']
        points = int(player['skill_points'])
        grid = self.skill_grid
        children = grid.get_children()
        max_row = int(((len(children)-5)/5)+2)
        min_row = 2
        learned_column = 2
        key_column = 0
        key = ''
        learned = ''
        for row in range(min_row, max_row):
            key = grid.get_child_at(key_column, row)
            key = key.get_text()
            key = key.lower()
            learned = grid.get_child_at(learned_column, row)
            learned_v = learned.get_text()
            for skill in skills:
                if skill[0] == key and row == tag:
                    if points >= 1:
                        learned_v = int(learned_v) + 1
                        learned_v = str(learned_v)
                        learned.set_text(learned_v)
                        player['skill'][row-2][3] = learned_v
                        points -= 1
                        player['skill_points'] = str(points)
        self.skill_points.set_markup(f"<span weight='bold'>Skill Points to allocate ->{player['skill_points']}</span>")
        self.total_skills()

    def print_char_sheet(self, widget):
        key = uuid.uuid4().hex 
        file_name = f"{player['name']}{key}"
        character = """
        Name: {0}
        Race: {1}
        Type: {2}
        --------------
        Level:{3}
        Life:{4}
        Clicks:{5}
        Money:{6}
        --------------
        Init:{7}
        Aim:{8}
        Inter:{9}
        --------------
        STR:{10}
        DEX:{11}
        FIT:{12}
        AGI:{13}
        WIS:{14}
        INT:{15}
        CHA:{16}
        APP:{17}
        --------------
        Inventory
        ---------
        {18}
        """.format(player['name'], player['race'],
                   player['type'], player['level'],
                   player['life'], player['clicks'],
                   player['money'], player['initiative'],
                   player['aim'], player['interrupts'],
                   player['strength'], player['dexterity'],
                   player['fitness'], player['agility'],
                   player['wisdom'], player['intelligence'],
                   player['charisma'],
                   player['appearance'],
                   player['inventory'])
        string = f"-- File was saved as {file_name} --"
        self.text.set_text(string)
        with open(file_name, 'w') as file:
           file.write(character)

    def edit_inv(self, menuitem):
        dialog = EditInventory(self) 
        response = dialog.run()
        if response == 1:
            print(player['inventory'])
            self.set_arm_inv()
            self.set_weapon_inv()
            self.set_inv_weight()
            
            dialog.destroy()

    def go_shopping(self, menuitem):
        dialog = Shop(self)
        response = dialog.run()
        if response == 1:
            self.set_arm_inv()
            self.set_weapon_inv()
            self.set_inv_weight()
            self.set_atts_markup()
            dialog.destroy()

    def save(self, menuitem):
        try:
            with open('character.pkl', 'wb') as character:
                pickle.dump(player,character)
            print("----SAVE COMPLETE----")
        except Exception as e:
            print("----FILE NOT SAVED----")

    def load(self, menuitem):
        try:
            with open('character.pkl', 'rb') as character:
                global player
                player = pickle.load(character)
            race_index = -1
            type_index = -1
            race = player['race']
            tyype = player['type']
            plrace = race.capitalize()
            pltyype = tyype.capitalize()
            for i, race in enumerate(self.race_selector.get_model()):
                if race[0] == plrace:
                    race_index = i
                    break
            if race_index != -1:
                self.race_selector.set_active(race_index)
            for i, tyype in enumerate(self.tyype_selector.get_model()):
                if tyype[0] == pltyype:
                    type_index = i
                    break
            if type_index != -1:
                self.tyype_selector.set_active(type_index)
            self.data_name.set_text(player['name'])
            self.level_value.set_text(player['level'])
            self.life_value.set_text(player['life'])
            self.clicks_value.set_text(player['clicks'])
            self.money_value.set_text(player['money'])
            self.initiative_value.set_text(player['initiative'])
            self.aim_value.set_text(player['aim'])
            self.interrupts_value.set_text(player['interrupts'])
            self.strength_value.set_text(player['strength'])
            self.dexterity_value.set_text(player['dexterity'])
            self.fitness_value.set_text(player['fitness'])
            self.agility_value.set_text(player['agility'])
            self.wisdom_value.set_text(player['wisdom'])
            self.intelligence_value.set_text(player['intelligence'])
            self.charisma_value.set_text(player['charisma'])
            self.appearance_value.set_text(player['appearance'])
            self.notes_buffer.set_text(player['notes'])
            self.set_mods()
            self.set_arm_inv()
            self.set_weapon_inv()
            self.set_atts_markup()
            self.set_e_arm()
            print(player['inventory'],"<-Player{} inventory")
            print(player['equipped_armour'],"<--Equipped Armour in player{}")
            print("----LOAD COMPLETE----")
            self.text.set_text("----LOAD COMPLETED SUCCESSFULLY----")
        except Exception as e:
            print(e,'<----------Error with this value')
            self.text.set_text("----ERROR: FILE NOT FOUND----")

def roll(sides=6, dice=4):
    """Uses Random module to simulate rolling stats with 4xD6
    drops the lowest value and sums the remaining 3 by default.
    Can be used for any number of dice but will always return 
    sum of all -lowest roll.
    Returns an integer 
    """
    lowest = 7
    rolls = []
    result = 0
    for roll in range(0,dice):
       rolls.append(random.randint(1,sides))
    for i in rolls:
        result += i
        if i < lowest:
            lowest = i
    return (result - lowest)

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()


from typing import List
from random import randint, choice, choices
from chargen import roll, expand, yaml_importer

mork_borg_data = yaml_importer('mork_borg_data/data.yaml')
starting_items = mork_borg_data['starting_items']
scrolls = mork_borg_data['scrolls']
optional_classes = mork_borg_data['optional_classes']


ability_score_bonuses = expand({
        range(1, 5): -3,
        range(5, 7): -2,
        range(7, 9): -1,
        range(9, 13): 0,
        range(13, 15): 1,
        range(15, 17): 2,
        range(17, 20): 3
})

class Container:
    def __init__(self, name: str, size: int):
        self.name = name
        self.maximum_size = size
        self.current_size = size
        self.contents = []

    def add_item(self, item: str):
        if self.current_size >= 1:
            self.contents.append(item)
            self.current_size -= 1
        else:
            pass

    def add_items(self, items: List):
        for item in items:
            self.add_item(item)

    def __repr__(self):
        return f"{self.name} of {self.maximum_size} size.\n    Contains: {', '.join(item for item in self.contents)}"

backpack = Container('Backpack', 7)
sack = Container('Sack', 10)
small_wagon = Container('Small Wagon', 1_000)
toolbox = Container('Toolbox', 4)
toolbox.add_items(['10 Nails', 'Hammer', 'Small Saw', 'Tongs'])

def gen_random_scroll(scroll_type: str, current_scrolls: List = None):
    if scroll_type.lower() not in ["unclean", "sacred"]:
        scroll = None
    else:
        scroll = choice(list(scrolls[scroll_type].keys()))
    if current_scrolls:
        while scroll in current_scrolls:
            scroll = choice(list(scrolls[scroll_type].keys()))
    return scroll

def gen_starting_items(abilities):
    ADD_PACK = False
    prescence = abilities['Prescence']
    item_set_1 = [
        "Nothing",
        "Nothing",
        backpack,
        sack,
        small_wagon,
        "Donkey"
    ]
    item_set_2 = [
        "Rope",
        f"{prescence + 4} torches",
        f"Lanturn with oil for {prescence + 6} hours",
        f"Magnesium Strip",
        f"{gen_random_scroll('unclean')}",
        "Sharp needle",
        f"Medicine chest - {prescence+4} uses (stops bleeding/infection and heals 1d6 health"
        "Metal file and lockpicks",
        "Bear trap (Presence DR14 to spot, 1d8 damage)",
        "Bomb (sealed bottle, 1d10 damage)",
        f"A bottle of red poison with {roll('1d4')} doses (Toughness DR12 or 1d10 damage)"
        "Silver crucifix"
    ]
    item_set_3 = [
        f"Life elixir of {roll('1d4')} doses (heals 1d6 HP and removes infection)",
        f"{gen_random_scroll('sacred')}",
        f"Small but vicious dog ({roll('1d6') + 2}HP, bite 1d4, only obeys you)",
        f"{roll('1d4')} monkeys that ignore but love you (1d4+2 HP, punch/bite 1d4)",
        "exquisite perfume worth 25s",
        toolbox,
        "Heavy chain, 15 feet",
        "grappling hook",
        "shield (-1 HP damage or have the shield break to ignore one attack)",
        "crowbar (1d4 damage)",
        "lard (may function as 5 meals in a pinch)"
        "tent"
    ]
    NOT_BAGGABLE = [item_set_2[6], item_set_3[2], item_set_3[3]]
    item_1 = choice(item_set_1)
    item_2 = choice(item_set_2)
    item_3 = choice(item_set_3)
    return_items = []
    if item_1 in [backpack, sack, small_wagon]:
        ADD_PACK = True
    if ADD_PACK: 
        if item_2 not in NOT_BAGGABLE:
            item_1.add_item(item_2)
        if item_3 not in NOT_BAGGABLE:
            item_1.add_item(item_3)
        if len(item_1.contents) == 2:
            return_items = item_1
            return return_items
        if item_2 in NOT_BAGGABLE:
            return_items.append(item_2)
        if item_3 in NOT_BAGGABLE:
            return_items.append(item_3)
        return_items.append(item_1)
    else:
        return [item_1, item_2, item_3]
            



    return [choice(item_set_1), choice(item_set_2)]


def gen_character(character_class = None, rand_class: bool = False):
    if rand_class:
        character_class = choice([
            'Fanged Deserter',
            'Gutterborn Scum',
            'Esoteric Hermit', 
            'Wretched Royalty',
            'Heretical Priest',
            'Occult Herbmaster'
        ])
    if not character_class:
        ability_rerolls = 2
    hp, party_initiative = 0, 0
    abilities = {'Agility': 0, 'Prescence': 0, 'Strength': 0, 'Toughness': 0}


    for ability in abilities:
        dice_rolls = [roll('1d6') for _ in range(3)]
        if not character_class:
            if ability_score_bonuses[sum(dice_rolls)] < 0 and ability_rerolls > 0:
                dice_rolls.reverse()
                dice_rolls.pop()
                dice_rolls.append(roll('1d6'))
                ability_rerolls -= 1

            abilities[ability] = ability_score_bonuses[sum(dice_rolls)]
        elif ability in list(optional_classes[character_class]['abilities'].keys()):
            abilities[ability] = ability_score_bonuses[sum(dice_rolls)]+ optional_classes[character_class]['abilities'][ability]
    items = gen_starting_items(abilities)
    return f"Abilities: {abilities}\nItems: {items}"



def w():
    hp = abilities['Toughness'] + roll('1d8')
    if hp < 1:
        hp = 1
    carrying_capacity = abilities['Strength'] + 8

    party_initiative = abilities['Agility'] + roll('1d6')
    init_silver = roll("2d6") * 10
    init_food = f'{roll("1d4")} days of food'
    return abilities, hp, party_initiative

print(gen_character(rand_class=True))

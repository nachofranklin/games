extends Resource
class_name Card

#enum available_to {char1, char2, etc}
enum Rarity {COMMON, UNCOMMON, RARE}
enum CardType {ATTACK, SKILL, POWER, STATUS, CURSE}
enum Target {SELF, SINGLE_ENEMY, ALL_ENEMIES, EVERYONE}

@export_group('Card Attributes')
@export var card_name: String
@export var rarity: Rarity
@export var card_type: CardType
@export var target: Target
@export var energy_cost: int
@export var exhausts: bool
@export var starter_card: bool
@export var shop_card: bool


func is_single_targeted() -> bool:
	return target == Target.SINGLE_ENEMY

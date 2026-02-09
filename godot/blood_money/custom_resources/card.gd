extends Resource
class_name Card

enum AvailableTo {ALL, NACHO} # should be ALL and the names of each character
enum Rarity {COMMON, UNCOMMON, RARE}
enum CardType {ATTACK, SKILL, POWER, STATUS, CURSE}
enum Target {SELF, SINGLE_ENEMY, ALL_ENEMIES, EVERYONE}

@export_group('Card Attributes')
@export var card_name: String
@export var available_to: AvailableTo
@export var rarity: Rarity
@export var card_type: CardType
@export var target: Target
@export var energy_cost: int
@export var exhausts: bool
@export var starter_card: bool
@export var shop_card: bool

@export_group('Card Visuals')
@export var art: Texture
@export var short_description: String
@export var tooltip_text: String


func is_single_targeted() -> bool:
	return target == Target.SINGLE_ENEMY


func get_description() -> String:
	return short_description # in the individual card scripts it'll be return short_description % whatever_the_number_represents

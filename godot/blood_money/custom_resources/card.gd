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


func play(targets: Array[Node], char_stats: CharacterStats) -> void:
	Events.card_played.emit(self)
	char_stats.mana -= energy_cost
	apply_effects(_get_targets(targets))


func apply_effects(_targets: Array[Node]) -> void:
	pass


func _get_targets(targets: Array[Node]) -> Array[Node]:
	# targets should either be the CardDropArea or if Card.Target == single_enemy: it will be an enemy
	if not targets:
		return []
	
	var tree: SceneTree = targets[0].get_tree()
	
	match target:
		Target.SELF:
			return tree.get_nodes_in_group('player')
		Target.SINGLE_ENEMY:
			return targets # target already gathered by card_target_selector, after being initially cleared when entering aiming state
		Target.ALL_ENEMIES:
			return tree.get_nodes_in_group('enemies')
		Target.EVERYONE:
			return tree.get_nodes_in_group('player') + tree.get_nodes_in_group('enemies')
		_:
			return []

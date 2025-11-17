extends Resource
class_name Card

enum Type {ATTACK, SKILL, POWER}
enum Target {SELF, SINGLE_ENEMY, ALL_ENEMIES, EVERYONE}
enum Rarity {COMMON, UNCOMMON, RARE}

const RARITY_COLOURS := {
	Card.Rarity.COMMON: Color.GRAY,
	Card.Rarity.UNCOMMON: Color.CORNFLOWER_BLUE,
	Card.Rarity.RARE: Color.GOLD
}

@export_group('Card Attributes')
@export var id: String
@export var type: Type
@export var target: Target
@export var energy_cost: int
@export var rarity: Rarity
@export var exhausts: bool = false

@export_group('Card Visuals')
@export var icon: Texture
@export_multiline var tooltip_text: String
@export var sound: AudioStream


func is_single_targeted() -> bool:
	return target == Target.SINGLE_ENEMY # returns target to be true/false if the card needs you to choose an enemy


func _get_targets(targets: Array[Node]):
	if not targets:
		return []
	
	var tree := targets[0].get_tree()
	
	match target:
		Target.SELF:
			return tree.get_nodes_in_group('player')
		Target.ALL_ENEMIES:
			return tree.get_nodes_in_group('enemies')
		Target.EVERYONE:
			return tree.get_nodes_in_group('player') + tree.get_nodes_in_group('enemies')
		_:
			return []


func play(targets: Array[Node], char_stats: CharacterStats, modifiers: ModifierHandler):
	Events.card_played.emit(self)
	char_stats.mana -= energy_cost
	
	if is_single_targeted():
		apply_effects(targets, modifiers)
	else:
		apply_effects(_get_targets(targets), modifiers)


func apply_effects(_targets: Array[Node], _modifiers: ModifierHandler):
	pass


func get_default_tooltip() -> String:
	return tooltip_text


func get_updated_tooltip(_player_modifiers: ModifierHandler, _enemy_modifiers: ModifierHandler) -> String:
	return tooltip_text

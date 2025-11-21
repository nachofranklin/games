extends Resource
class_name Relic

enum WhenType {START_OF_TURN, START_OF_COMBAT, END_OF_TURN, END_OF_COMBAT, EVENT_BASED}
enum CharacterType {ALL, ASSASSIN, WARRIOR, WIZARD}

@export var relic_name: String
@export var id: String
@export var when_type: WhenType
@export var character_type: CharacterType
@export var starter_relic: bool = false
@export var icon: Texture
@export_multiline var tooltip: String


func initialise_relic(_relic_ui: RelicUI):
	pass


func activate_relic(_relic_ui: RelicUI):
	pass


func deactivate_relic(_relic_ui: RelicUI):
	pass


func get_tooltip() -> String:
	return tooltip


func can_appear_as_reward(character: CharacterStats) -> bool:
	if starter_relic:
		return false
	
	if character_type == CharacterType.ALL:
		return true
	
	var relic_char_name: String = CharacterType.keys()[character_type].to_lower()
	var char_name: String = character.character_name.to_lower()
	
	return relic_char_name == char_name

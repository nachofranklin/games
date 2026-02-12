extends Panel
class_name ManaUI

@export var char_stats: CharacterStats : set = _set_char_stats

@onready var mana_label: Label = $ManaLabel


func _set_char_stats(value: CharacterStats) -> void:
	char_stats = value
	
	if not char_stats.stats_changed.is_connected(_update_mana):
		char_stats.stats_changed.connect(_update_mana)
	
	if not is_node_ready():
		await ready
	
	_update_mana()


func _update_mana() -> void:
	mana_label.text = str(char_stats.mana)

extends CanvasLayer
class_name BattleUI

@export var char_stats: CharacterStats : set = _set_char_stats

@onready var hand_h_box: Hand = $HandHBox
@onready var mana_ui: ManaUI = $ManaUI


func _set_char_stats(value: CharacterStats) -> void:
	char_stats = value
	mana_ui.char_stats = char_stats
	hand_h_box.char_stats = char_stats
	# card char stats is temporary, can delete this when cards are drawn automatically
	for card in hand_h_box.get_children():
		card.char_stats = value

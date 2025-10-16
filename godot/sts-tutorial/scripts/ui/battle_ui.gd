extends CanvasLayer
class_name BattleUI

@export var char_stats: CharacterStats : set = _set_char_stats

@onready var hand: Hand = $Hand as Hand
@onready var mana_ui: ManaUI = $ManaUI as ManaUI
@onready var end_turn_button: Button = $EndTurnButton # i didn't make it a unique name like the tutorial so if something goes wrong that's probably why


func _ready() -> void:
	Events.player_hand_drawn.connect(_on_player_hand_drawn)
	end_turn_button.pressed.connect(_on_end_turn_button_pressed)


func _set_char_stats(value: CharacterStats):
	char_stats = value
	hand.char_stats = char_stats
	mana_ui.char_stats = char_stats


func _on_player_hand_drawn():
	end_turn_button.disabled = false


func _on_end_turn_button_pressed():
	end_turn_button.disabled = true
	Events.player_turn_ended.emit()

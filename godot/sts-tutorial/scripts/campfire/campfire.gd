extends Control
class_name Campfire

@export var char_stats: CharacterStats

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var rest_button: Button = $UILayer/VBoxContainer/RestButton


func _ready() -> void:
	animation_player.play('RESET')
	rest_button.disabled = false


func _on_rest_button_pressed() -> void:
	rest_button.disabled = true
	char_stats.heal(ceili(char_stats.max_health * 0.3))
	animation_player.play('fade_out')


# called from the animation player
func _on_fade_out_finished():
	Events.campfire_exited.emit()

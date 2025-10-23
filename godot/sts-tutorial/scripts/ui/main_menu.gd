extends Control

const CHAR_SELECTOR_SCREEN: PackedScene = preload("res://scenes/ui/character_selector.tscn")

@onready var continue_button: Button = %ContinueButton


func _ready() -> void:
	get_tree().paused = false


func _on_continue_button_pressed() -> void:
	print('continue run')


func _on_new_run_button_pressed() -> void:
	# should probably add some sort of scene transition
	get_tree().change_scene_to_packed(CHAR_SELECTOR_SCREEN)


func _on_exit_button_pressed() -> void:
	get_tree().quit()

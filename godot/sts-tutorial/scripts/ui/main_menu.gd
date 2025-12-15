extends Control

const CHAR_SELECTOR_SCREEN: PackedScene = preload("res://scenes/ui/character_selector.tscn")
const RUN_SCENE: PackedScene = preload("res://scenes/run/run.tscn")

@export var run_startup: RunStartup

@onready var continue_button: Button = %ContinueButton


func _ready() -> void:
	get_tree().paused = false
	continue_button.disabled = SaveGame.load_data() == null


func _on_continue_button_pressed() -> void:
	run_startup.type = RunStartup.Type.CONTINUED_RUN
	get_tree().change_scene_to_packed(RUN_SCENE)


func _on_new_run_button_pressed() -> void:
	# should probably add some sort of scene transition
	get_tree().change_scene_to_packed(CHAR_SELECTOR_SCREEN)


func _on_exit_button_pressed() -> void:
	get_tree().quit()

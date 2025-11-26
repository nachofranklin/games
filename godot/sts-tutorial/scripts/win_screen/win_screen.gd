extends Control
class_name WinScreen

const MAIN_MENU_PATH: String = 'res://scenes/ui/main_menu.tscn'
const MESSAGE: String = 'The %s\nis victorious!'

@export var character: CharacterStats : set = set_character

@onready var character_portrait: TextureRect = %CharacterPortrait
@onready var message: Label = %Message


func set_character(new_character: CharacterStats):
	if not is_node_ready():
		await ready
	
	character = new_character
	message.text = MESSAGE % character.character_name
	character_portrait.texture = character.portrait


func _on_main_menu_button_pressed() -> void:
	get_tree().change_scene_to_file(MAIN_MENU_PATH)

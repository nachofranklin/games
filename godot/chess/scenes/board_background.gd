extends Node2D
class_name BoardBackground

@export var selected_background: Sprite2D


func _ready() -> void:
	for child: Sprite2D in get_children():
		child.hide()
	Events.game_initialised.connect(_on_game_initialised)


func _on_game_initialised(tile_size: float, board_width: int, board_height: int) -> void:
	var board_size: Vector2 = Vector2(tile_size * board_width, tile_size * board_height)
	var texture_size: Vector2 = selected_background.texture.get_size()
	selected_background.scale = board_size / texture_size
	selected_background.show()

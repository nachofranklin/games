extends Node2D
class_name Tile

# set by board
var grid_pos: Vector2i = Vector2i.ZERO
var tile_size: float = 40.0
var base_colour: Color = Color(1.0, 1.0, 1.0, 1.0)
var selected_colour: Color = Color(0.498, 0.659, 1.0, 0.843)
var selected: bool = false

@onready var color_rect: ColorRect = $ColorRect


func set_tile_values(pos: Vector2i, size: float, colour: Color, highlighted_colour: Color) -> void:
	grid_pos = pos
	tile_size = size
	base_colour = colour
	selected_colour = highlighted_colour


func _ready() -> void:
	color_rect.size = Vector2(tile_size, tile_size)
	color_rect.color = base_colour


func _on_color_rect_gui_input(event: InputEvent) -> void:
	if event.is_action_pressed('left_mouse'):
		Events.tile_clicked.emit(grid_pos)
		#print(grid_pos)


func tile_selected() -> void:
	selected = true
	color_rect.color = selected_colour


func tile_unselected() -> void:
	selected = false
	color_rect.color = base_colour

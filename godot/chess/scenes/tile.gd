extends Node2D
class_name Tile

# set by board
var grid_pos: Vector2i = Vector2i.ZERO
var tile_size: float = 40.0
var base_colour: Color = Color(1.0, 1.0, 1.0, 1.0)
var selected_colour: Color = Color(0.498, 0.659, 1.0, 0.843)
var selected: bool = false

@onready var tile_color_rect: ColorRect = %TileColorRect
@onready var enemy_highlight: Sprite2D = %EnemyHighlight
@onready var moveable_square_highlight: Sprite2D = %MoveableSquareHighlight


func set_tile_values(pos: Vector2i, size: float, colour: Color, highlighted_colour: Color) -> void:
	grid_pos = pos
	tile_size = size
	base_colour = colour
	selected_colour = highlighted_colour


func _ready() -> void:
	var scale_factor: float = tile_size / 100.0
	scale = Vector2(scale_factor, scale_factor)
	tile_color_rect.color = base_colour


func _on_color_rect_gui_input(event: InputEvent) -> void:
	if event.is_action_pressed('left_mouse'):
		Events.tile_clicked.emit(grid_pos)
		#print(grid_pos)


func tile_selected() -> void:
	selected = true
	tile_color_rect.color = selected_colour


func tile_unselected() -> void:
	selected = false
	tile_color_rect.color = base_colour


func highlight_tile(is_empty_tile: bool) -> void:
	if is_empty_tile:
		moveable_square_highlight.show()
	elif not is_empty_tile:
		enemy_highlight.show()


func reset_highlighted_tile() -> void:
	moveable_square_highlight.hide()
	enemy_highlight.hide()

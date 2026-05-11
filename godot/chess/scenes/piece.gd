extends Node2D
class_name Piece

@export var piece_resource: PieceResource
@export var grid_pos: Vector2i

@onready var sprite_2d: Sprite2D = $Sprite2D

var possible_moves: Array[Vector2i] = []


#func _ready() -> void: # for testing purposes
	#setup_piece(piece_resource, grid_pos, Vector2(0, 0), 100.0)


func setup_piece(resource: PieceResource, pos: Vector2i, world_pos: Vector2, tile_size: float) -> void:
	piece_resource = resource
	grid_pos = pos
	position = world_pos
	sprite_2d.texture = resource.sprite
	_fit_sprite_to_tile(tile_size)


func _fit_sprite_to_tile(tile_size: float) -> void:
	if sprite_2d.texture == null:
		return
	var texture_size = sprite_2d.texture.get_size()
	var scale_factor = tile_size / max(texture_size.x, texture_size.y)
	sprite_2d.scale = Vector2(scale_factor, scale_factor)


func move_to(new_pos: Vector2i, world_pos: Vector2) -> void:
	grid_pos = new_pos
	position = world_pos
	piece_resource.has_never_moved = false

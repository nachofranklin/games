extends Node2D
class_name Piece

@export var piece_resource: PieceResource
@export var grid_pos: Vector2i

@onready var sprite_2d: Sprite2D = $Sprite2D


#func _ready() -> void:
	#setup_piece(piece_resource, grid_pos, Vector2(100, 100))


func setup_piece(resource: PieceResource, pos: Vector2i, world_pos: Vector2) -> void:
	piece_resource = resource
	grid_pos = pos
	position = world_pos
	sprite_2d.texture = resource.sprite


func move_to(new_pos: Vector2i, world_pos: Vector2) -> void:
	grid_pos = new_pos
	position = world_pos

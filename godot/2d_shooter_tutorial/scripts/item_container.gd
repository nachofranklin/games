extends StaticBody2D

class_name ItemContainer

signal open(pos, direction)

@export var no_of_spawns: int

@onready var current_direction: Vector2 = Vector2.DOWN.rotated(rotation)

var opened: bool = false

func hit():
	# (when hit) hide the lid and get a random spawn position, then send a signal
	if opened == false:
		$LidSprite.hide()
		for i in range(no_of_spawns):
			var pos = $SpawnPositions.get_child(randi() % $SpawnPositions.get_child_count()).global_position
			open.emit(pos, current_direction)
		opened = true
		$AudioStreamPlayer2D.play()

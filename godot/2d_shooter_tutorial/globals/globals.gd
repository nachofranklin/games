extends Node

signal laser_amount_change
signal grenade_amount_change
signal health_change

var laser_amount: int = 20:
	set(value):
		laser_amount = value
		laser_amount_change.emit()
var grenade_amount: int = 5:
	set(value):
		grenade_amount = value
		grenade_amount_change.emit()
var health_amount: int = 60:
	set(value):
		health_amount = min(value, 100)
		health_change.emit()
		player_hit_sound.play() # will probably play if i'm gaining health but can change this easy enough

var player_pos: Vector2
var player_hit_sound: AudioStreamPlayer

func _ready() -> void:
	player_hit_sound = AudioStreamPlayer.new()
	player_hit_sound.stream = load("res://assets/audio/solid_impact.ogg")
	add_child(player_hit_sound)

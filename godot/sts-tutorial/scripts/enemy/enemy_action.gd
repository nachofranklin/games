extends Node
class_name EnemyAction

enum Type {CONDITIONAL, CHANCE_BASED}

@export var intent: Intent
@export var type: Type
@export_range(0.0, 10.0) var chance_weight: float = 0.0

@onready var accumulated_weight: float = 0.0

var enemy: Enemy
var target: Node2D


func is_performable():
	return false


func perform_action():
	pass

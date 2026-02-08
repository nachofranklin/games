extends Resource
class_name Stats

signal stats_changed

@export var max_health: int = 1
@export var base_block: int = 0
@export var art: Texture

var health: int : set = set_health
var block: int : set = set_block


func set_health(value: int) -> void:
	health = clampi(value, 0, max_health)
	stats_changed.emit()


func set_block(value: int) -> void:
	block = clampi(value, 0, 999)
	stats_changed.emit()


func take_damage(damage: int) -> void:
	if damage <= 0:
		return
	
	var initial_damage = damage
	damage = clampi(damage - block, 0, damage)
	self.block = clampi(block - initial_damage, 0, block)
	self.health -= damage


func heal(amount: int) -> void:
	self.health += amount


func create_instance() -> Stats: # duplicating the resource stops multiples of the same enemy sharing the same stats. eg. if i hit one it won't take health from them all
	var instance: Stats = self.duplicate()
	instance.health = max_health
	instance.block = base_block
	return instance

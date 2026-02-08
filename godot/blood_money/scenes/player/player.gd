extends Node2D
class_name Player

@export var char_stats: CharacterStats : set = set_character_stats

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var health_bar_ui: HealthBarUI = $HealthBarUI


func set_character_stats(value: CharacterStats) -> void:
	char_stats = value.create_instance()
	
	if not char_stats.stats_changed.is_connected(update_health_bar):
		char_stats.stats_changed.connect(update_health_bar)
	
	update_player()


func update_player() -> void:
	if not is_inside_tree():
		await ready
	
	sprite_2d.texture = char_stats.art
	update_health_bar()


func update_health_bar() -> void:
	health_bar_ui.update_health_bar(char_stats)


func take_damage(damage: int) -> void:
	if char_stats.health <= 0:
		return
	
	char_stats.take_damage(damage)
	
	if char_stats.health <= 0:
		queue_free()

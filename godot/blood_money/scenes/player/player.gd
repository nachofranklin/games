extends Node2D
class_name Player

@export var stats: CharacterStats : set = set_character_stats # needs to be called stats so that effects can apply to both player and enemy

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var health_bar_ui: HealthBarUI = $HealthBarUI


func set_character_stats(value: CharacterStats) -> void:
	stats = value.create_instance()
	
	if not stats.stats_changed.is_connected(update_health_bar):
		stats.stats_changed.connect(update_health_bar)
	
	update_player()


func update_player() -> void:
	if not is_inside_tree():
		await ready
	
	sprite_2d.texture = stats.art
	update_health_bar()


func update_health_bar() -> void:
	health_bar_ui.update_health_bar(stats)


func take_damage(damage: int) -> void:
	if stats.health <= 0:
		return
	
	stats.take_damage(damage)
	
	if stats.health <= 0:
		queue_free()

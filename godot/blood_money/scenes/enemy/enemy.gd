extends Node2D
class_name Enemy

const ARROW_OFFSET: int = 5

@export var stats: Stats : set = set_enemy_stats

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var arrow: Sprite2D = $Arrow
@onready var collision_shape_2d: CollisionShape2D = $Area2D/CollisionShape2D
@onready var health_bar_ui: HealthBarUI = $HealthBarUI


func set_enemy_stats(value: Stats) -> void:
	stats = value.create_instance()
	
	if not stats.stats_changed.is_connected(update_health_bar):
		stats.stats_changed.connect(update_health_bar)
	
	update_enemy()


func update_enemy() -> void:
	if not is_inside_tree():
		await ready
	
	sprite_2d.texture = stats.art
	var enemy_half_width = collision_shape_2d.shape.size.x / 2
	var arrow_half_width = arrow.texture.get_width() * arrow.scale.x / 2
	arrow.position.x = enemy_half_width + arrow_half_width + ARROW_OFFSET
	update_health_bar()


func update_health_bar() -> void:
	health_bar_ui.update_health_bar(stats)


func take_damage(damage: int) -> void:
	if stats.health <= 0:
		return
	
	stats.take_damage(damage)
	
	if stats.health <= 0:
		queue_free()


func _on_area_2d_area_entered(_area: Area2D) -> void:
	arrow.visible = true


func _on_area_2d_area_exited(_area: Area2D) -> void:
	arrow.visible = false

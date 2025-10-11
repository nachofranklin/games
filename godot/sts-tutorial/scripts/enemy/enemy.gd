class_name Enemy
extends Node2D

const ARROW_OFFSET: int = 5

@export var stats: Stats : set = set_enemy_stats

@onready var enemy_image: Sprite2D = $EnemyImage
@onready var arrow: Sprite2D = $Arrow
@onready var stats_ui: StatsUI = $StatsUI as StatsUI

func set_enemy_stats(value: Stats):
	stats = value.create_instance()
	
	if not stats.stats_changed.is_connected(update_stats):
		stats.stats_changed.connect(update_stats)
	
	update_enemy()

func update_stats():
	stats_ui.update_stats(stats)

func update_enemy():
	if not stats is Stats:
		return
	if not is_inside_tree():
		await ready
	
	enemy_image.texture = stats.art
	arrow.position = Vector2.RIGHT * (enemy_image.get_rect().size.x / 2 + ARROW_OFFSET)
	update_stats()

func take_damage(damage: int):
	if stats.health <= 0:
		return
	
	stats.take_damage(damage)
	
	if stats.health <= 0:
		queue_free()

func _on_enemy_area_area_entered(_area: Area2D) -> void:
	arrow.show()

func _on_enemy_area_area_exited(_area: Area2D) -> void:
	arrow.hide()

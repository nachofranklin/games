extends Node2D
class_name Player

const WHITE_SPRITE_MATERIAL: ShaderMaterial = preload("res://art/white_sprite_material.tres")

@export var stats: CharacterStats : set = set_character_stats

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var stats_ui: StatsUI = $StatsUI as StatsUI
@onready var status_handler: StatusHandler = $StatusHandler
@onready var modifier_handler: ModifierHandler = $ModifierHandler


func set_character_stats(value: CharacterStats):
	stats = value
	
	if not stats.stats_changed.is_connected(update_stats):
		stats.stats_changed.connect(update_stats)
	
	update_player()


func update_player():
	if not stats is CharacterStats:
		return
	if not is_inside_tree():
		await ready
	
	sprite_2d.texture = stats.art
	update_stats()


func update_stats():
	stats_ui.update_stats(stats)


func take_damage(damage: int, which_modifier: Modifier.Type):
	if stats.health <= 0:
		return
	
	sprite_2d.material = WHITE_SPRITE_MATERIAL
	var modified_damage: int = modifier_handler.get_modified_value(damage, which_modifier)
	
	var tween := create_tween()
	tween.tween_callback(Shaker.shake.bind(self, 16, 0.15))
	tween.tween_callback(stats.take_damage.bind(modified_damage))
	tween.tween_interval(0.18)
	
	tween.finished.connect(
		func():
			sprite_2d.material = null # remove the WHITE_SPRITE_MATERIAL
			
			if stats.health <= 0:
				Events.player_died.emit()
				queue_free()
	)

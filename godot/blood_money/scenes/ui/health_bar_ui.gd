extends Control
class_name HealthBarUI

@onready var health_bar: ProgressBar = %HealthBar
@onready var health_label: Label = %HealthLabel
@onready var max_health_label: Label = %MaxHealthLabel
@onready var block_icon: TextureRect = %BlockIcon
@onready var block_amount: Label = %BlockAmount

var sb_health_bar: StyleBoxFlat = preload("res://art/theme/health_bar.tres")
var sb_health_bar_background: StyleBoxFlat = preload("res://art/theme/health_bar_background.tres")
var sb_block_health_bar: StyleBoxFlat = preload("res://art/theme/block_health_bar.tres")
var sb_block_health_bar_background: StyleBoxFlat = preload("res://art/theme/block_health_bar_background.tres")


func update_health_bar(stats: Stats) -> void:
	health_bar.max_value = stats.max_health
	health_bar.value = stats.health
	health_label.text = str(stats.health)
	max_health_label.text = str(stats.max_health)
	block_amount.text = str(stats.block)
	block_icon.visible = stats.block > 0
	
	if stats.block > 0:
		health_bar.add_theme_stylebox_override("fill", sb_block_health_bar)
		health_bar.add_theme_stylebox_override("background", sb_block_health_bar_background)
	else:
		health_bar.add_theme_stylebox_override("fill", sb_health_bar)
		health_bar.add_theme_stylebox_override("background", sb_block_health_bar_background)

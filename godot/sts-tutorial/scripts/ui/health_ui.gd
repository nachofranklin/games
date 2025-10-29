extends HBoxContainer
class_name HealthUI

@export var show_max_hp: bool

@onready var health_label: Label = %HealthLabel
@onready var max_health_hbox: HBoxContainer = %MaxHealthHBox
@onready var max_health_label: Label = %MaxHealthLabel


func update_stats(stats: Stats):
	health_label.text = str(stats.health)
	max_health_label.text = str(stats.max_health)
	max_health_hbox.visible = show_max_hp

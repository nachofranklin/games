extends HBoxContainer
class_name GoldUI

@export var run_stats: RunStats : set = set_run_stats

@onready var amount: Label = $Amount


func _ready() -> void:
	amount.text = '0'


func set_run_stats(new_value: RunStats):
	run_stats = new_value
	
	if not run_stats.gold_changed.is_connected(_update_gold):
		run_stats.gold_changed.connect(_update_gold)
		_update_gold()


func _update_gold():
	amount.text = str(run_stats.gold)

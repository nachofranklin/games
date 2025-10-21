extends Node2D
class_name Enemy

const ARROW_OFFSET: int = 5

@export var stats: EnemyStats : set = set_enemy_stats

@onready var enemy_image: Sprite2D = $EnemyImage
@onready var arrow: Sprite2D = $Arrow
@onready var stats_ui: StatsUI = $StatsUI as StatsUI
@onready var intent_ui: IntentUI = $IntentUI as IntentUI

var enemy_action_picker: EnemyActionPicker
var current_action: EnemyAction : set = set_current_action


func set_current_action(value: EnemyAction):
	current_action = value
	if current_action:
		intent_ui.update_intent(current_action.intent)


func set_enemy_stats(value: EnemyStats):
	stats = value.create_instance()
	
	if not stats.stats_changed.is_connected(update_stats):
		stats.stats_changed.connect(update_stats)
		stats.stats_changed.connect(update_action)
	
	update_enemy()


func setup_ai():
	if enemy_action_picker:
		enemy_action_picker.queue_free() # if we already have an ai then get rid of it so we can add a new one
	
	var new_action_picker: EnemyActionPicker = stats.ai.instantiate()
	add_child(new_action_picker)
	enemy_action_picker = new_action_picker
	enemy_action_picker.enemy = self # i don't fully follow this bit


func update_stats():
	stats_ui.update_stats(stats)


func update_action():
	if not enemy_action_picker:
		print('no ai attached')
		return # this checks if we have an ai attached to the enemy, if not nothing we can do so returns from the function
	
	if not current_action:
		current_action = enemy_action_picker.get_action()
		return # if we don't have a current action then get one, then return from the func
	
	# but if we do have a current action then check what the action would now be (eg a card played by us could change what the enemy intends to do next)
	var new_conditional_action := enemy_action_picker.get_first_conditional_action()
	if new_conditional_action and current_action != new_conditional_action:
		# the reason this works is because a new (conditional) action would be selected as the current action after the condition has been met but when we check again for a new conditional action the already_used var is now true and so is_performable would return as false, meaning the new_conditional_action = false (or null), so now current_action and new_conditional_action don't equal each other but because we also say if new_conditional_action it means the current action doesn't get overwritten. (Took me ages to wrap my head around this lol)
		current_action = new_conditional_action # if the current and new action aren't the same then change the current action to be the new one instead


func update_enemy():
	if not stats is Stats:
		return
	if not is_inside_tree():
		await ready
	
	enemy_image.texture = stats.art
	arrow.position = Vector2.RIGHT * (enemy_image.get_rect().size.x / 2 + ARROW_OFFSET)
	setup_ai()
	update_stats()


func do_turn():
	stats.block = 0
	
	if not current_action:
		return
	
	current_action.perform_action()


func take_damage(damage: int):
	if stats.health <= 0:
		return
	
	var tween := create_tween()
	tween.tween_callback(Shaker.shake.bind(self, 16, 0.15))
	tween.tween_callback(stats.take_damage.bind(damage))
	tween.tween_interval(0.2)
	
	tween.finished.connect(
		func():
			if stats.health <= 0:
				queue_free()
	)


func _on_enemy_area_area_entered(_area: Area2D) -> void:
	arrow.show()


func _on_enemy_area_area_exited(_area: Area2D) -> void:
	arrow.hide()

extends Node
class_name EnemyActionPicker

@export var enemy: Enemy: set = _set_enemy
@export var target: Node2D: set = _set_target

@onready var total_weight: float = 0.0


func _ready() -> void:
	target = get_tree().get_first_node_in_group('player') # target defaults to player
	setup_chances()


func get_action() -> EnemyAction:
	# first tries to get a conditional action, if there are no conditional actions then it will return a chance based action
	var action := get_first_conditional_action()
	if action:
		return action
	
	return get_chance_based_action()


func get_first_conditional_action() -> EnemyAction:
	var action: EnemyAction
	
	for child in get_children():
		action = child as EnemyAction
		if not action or action.type != EnemyAction.Type.CONDITIONAL:
			continue
		
		if action.is_performable():
			return action
	
	return null # null returns false in a boolean context


func get_chance_based_action() -> EnemyAction:
	var action: EnemyAction
	var roll: float = RNG.instance.randf_range(0.0, total_weight)
	
	for child in get_children():
		action = child as EnemyAction
		if not action or action.type != EnemyAction.Type.CHANCE_BASED:
			continue
		
		if action.accumulated_weight > roll:
			return action
	
	return null


func setup_chances():
	var action: EnemyAction
	
	for child in get_children(): # the children are all the available actions
		action = child as EnemyAction
		if not action or action.type != EnemyAction.Type.CHANCE_BASED:
			continue
		
		total_weight += action.chance_weight # do i need to set the .chance weight and .accumulated weight to 0.0 before the for loop?
		action.accumulated_weight = total_weight


func _set_enemy(value: Enemy): # i don't fully understand these setter functions
	enemy = value
	
	for action in get_children():
		action.enemy = enemy


func _set_target(value: Node2D):
	target = value
	
	for action in get_children():
		action.target = target

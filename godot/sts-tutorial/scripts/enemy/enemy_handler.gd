extends Node2D
class_name EnemyHandler

var acting_enemies: Array[Enemy] = []


func _ready() -> void:
	Events.enemy_action_completed.connect(_on_enemy_action_completed)
	Events.enemy_died.connect(_on_enemy_died)


func setup_enemies(battle_stats: BattleStats):
	if not battle_stats:
		return
	
	for enemy: Enemy in get_children():
		enemy.queue_free()
	
	var all_new_enemies := battle_stats.enemies.instantiate()
	
	for new_enemy: Node2D in all_new_enemies.get_children():
		var new_enemy_child := new_enemy.duplicate() as Enemy
		add_child(new_enemy_child)
		new_enemy_child.status_handler.statuses_applied.connect(_on_enemy_statuses_applied.bind(new_enemy_child))
	
	all_new_enemies.queue_free() # we instantiate the battle_stats scene, duplicate the children (which are the enemies), add them as children to the enemy_handler, then we can remove the scene we instantiated as we only needed the enemies from it


func _on_enemy_statuses_applied(when_type: Status.WhenType, enemy: Enemy):
	match when_type:
		Status.WhenType.START_OF_TURN:
			enemy.do_turn()
		Status.WhenType.END_OF_TURN:
			acting_enemies.erase(enemy)
			_start_next_enemy_turn()


func reset_enemy_actions():
	var enemy: Enemy
	for child in get_children():
		enemy = child as Enemy
		enemy.current_action = null
		enemy.update_action()


func start_turn():
	if get_child_count() == 0:
		return
	
	acting_enemies.clear()
	for enemy: Enemy in get_children():
		acting_enemies.append(enemy)
	
	_start_next_enemy_turn()


func _start_next_enemy_turn():
	if acting_enemies.is_empty():
		Events.enemy_turn_ended.emit()
		return
	
	acting_enemies[0].status_handler.apply_statuses_by_type(Status.WhenType.START_OF_TURN)


func _on_enemy_action_completed(enemy: Enemy):
	enemy.status_handler.apply_statuses_by_type(Status.WhenType.END_OF_TURN)


func _on_enemy_died(enemy: Enemy): # this prevents a locking state if the enemy were to die to a status effect
	var is_enemy_turn: bool = acting_enemies.size() > 0
	acting_enemies.erase(enemy)
	
	if is_enemy_turn:
		_start_next_enemy_turn()

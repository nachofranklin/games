extends EnemyAction

@export var block: int = 15
@export var hp_threshold: int = 6

var already_used: bool = false


func is_performable() -> bool:
	if not enemy or already_used:
		#print('not enemy or already used')
		return false
	
	var is_low: bool = enemy.stats.health <= hp_threshold
	# i think this will run into issues as if i do two attacks, one to trigger hp_threshold, sets already_used and is_performable to true, the second attack doesn't kill it but now would set is_performable to false because already_used was true? 
	already_used = is_low # can't just set it to true because then it would trigger even if it wasn't low health
	
	#print('is_low is ')
	#print(is_low)
	return is_low


func perform_action():
	if not enemy or not target:
		return
	
	var block_effect := BlockEffect.new()
	block_effect.amount = block
	block_effect.sound = sound
	block_effect.execute([enemy])
	
	get_tree().create_timer(0.6, false).timeout.connect(
		func():
			Events.enemy_action_completed.emit(enemy)
	) # creates a timer so that enemy actions have a small delay
	
	# could do some kind of tween that adds a big block img over the enemy then tweens the size to be smaller and the alpha to become transparent

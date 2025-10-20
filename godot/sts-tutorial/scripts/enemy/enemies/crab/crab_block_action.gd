extends EnemyAction

@export var block: int = 6


func perform_action():
	if not enemy:
		return
	
	var block_effect := BlockEffect.new()
	block_effect.amount = block
	block_effect.execute([enemy])
	
	get_tree().create_timer(0.6, false).timeout.connect(
		func():
			Events.enemy_action_completed.emit(enemy)
	) # creates a timer so that enemy actions have a small delay
	
	# could do some kind of tween that adds a big block img over the enemy then tweens the size to be smaller and the alpha to become transparent

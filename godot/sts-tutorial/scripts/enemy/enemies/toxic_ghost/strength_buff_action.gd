extends EnemyAction

const STRENGTH_STATUS = preload('res://statuses/strength.tres')

@export var stacks_per_action: int = 2

var hp_threshold: int = 25
var usages: int = 0


func is_performable() -> bool:
	var is_hp_under_threshold: bool = enemy.stats.health <= hp_threshold
	
	if usages == 0 or (usages == 1 and is_hp_under_threshold):
		usages += 1
		return true
	
	return false


func perform_action() -> void:
	if not enemy or not target:
		return
	
	var status_effect := StatusEffect.new()
	var strength := STRENGTH_STATUS.duplicate()
	strength.stacks = stacks_per_action
	status_effect.status = strength
	status_effect.execute([enemy])
	
	SFXPlayer.play(sound)
	
	Events.enemy_action_completed.emit(enemy)

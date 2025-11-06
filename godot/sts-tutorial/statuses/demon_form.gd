extends Status
class_name DemonFormStatus

const STRENGTH_STATUS = preload("res://statuses/strength.tres")

@export var stacks_per_turn: int


#func initialise_status(target: Node):
	#print('Initialise my status for target %s' % target)


func apply_status(target: Node):
	print('applied demon form')
	
	var status_effect := StatusEffect.new()
	var strength := STRENGTH_STATUS.duplicate()
	strength.stacks = stacks_per_turn
	status_effect.status = strength
	status_effect.execute([target])
	
	status_applied.emit(self)

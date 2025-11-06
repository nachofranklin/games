extends Status
class_name VulnerableStatus

const MODIFIER: float = 0.5


func apply_status(target: Node):
	print('%s should take %s%% more damage!' % [target, MODIFIER * 100])
	
	var damage_effect := DamageEffect.new()
	damage_effect.amount = 12 # placeholder
	damage_effect.execute([target])
	
	status_applied.emit(self)

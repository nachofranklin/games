extends Card

const VULNERABLE_STATUS = preload("res://statuses/vulnerable.tres")

var base_damage: int = 5
var vulnerable_duration: int = 2


func apply_effects(targets: Array[Node]) -> void:
	var damage_effect := DamageEffect.new()
	damage_effect.amount = base_damage
	damage_effect.sound = sound
	damage_effect.execute(targets)
	
	var status_effect := StatusEffect.new()
	var vulnerable := VULNERABLE_STATUS.duplicate()
	vulnerable.duration = vulnerable_duration
	status_effect.status = vulnerable
	status_effect.execute(targets)

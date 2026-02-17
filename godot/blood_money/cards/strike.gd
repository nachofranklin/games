extends Card

@export var strike: int


func apply_effects(targets: Array[Node]) -> void:
	var damage_effect := DamageEffect.new()
	damage_effect.amount = strike
	damage_effect.execute(targets)


func get_description() -> String:
	return short_description % strike

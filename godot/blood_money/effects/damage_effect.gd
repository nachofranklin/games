extends Effect
class_name DamageEffect

var amount: int = 0


func execute(targets: Array[Node]) -> void:
	for target in targets:
		if not target:
			continue
		elif target is Enemy or target is Player:
			target.take_damage(amount)

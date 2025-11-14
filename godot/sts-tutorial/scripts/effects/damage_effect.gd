class_name DamageEffect
extends Effect

var amount: int = 0
var receiver_modifier_type := Modifier.Type.DMG_TAKEN


func execute(targets: Array[Node]):
	for target in targets:
		if not target:
			continue
		if target is Enemy or target is Player:
			target.take_damage(amount, receiver_modifier_type)
			SFXPlayer.play(sound)

class_name BlockEffect
extends Effect

var amount: int = 0 # so when block is gained this amount would need to be overridden and then perform the execute func


func execute(targets: Array[Node]):
	for target in targets:
		if not target:
			continue
		if target is Enemy or target is Player:
			target.stats.block += amount
			SFXPlayer.play(sound)

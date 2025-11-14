extends Card

var base_block: int = 5


func apply_effects(targets: Array[Node], _modifiers: ModifierHandler):
	var block_effect := BlockEffect.new()
	block_effect.amount = base_block
	block_effect.sound = sound
	block_effect.execute(targets)

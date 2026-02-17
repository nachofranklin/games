extends Card

@export var block: int


func apply_effects(targets: Array[Node]) -> void:
	var block_effect := BlockEffect.new()
	block_effect.amount = block
	block_effect.execute(targets)


func get_description() -> String:
	return short_description % block

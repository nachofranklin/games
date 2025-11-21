extends Relic

@export var block: int


func activate_relic(relic_ui: RelicUI):
	relic_ui.flash()
	
	var player := relic_ui.get_tree().get_nodes_in_group('player')
	var block_effect := BlockEffect.new()
	block_effect.amount = block
	block_effect.execute(player)

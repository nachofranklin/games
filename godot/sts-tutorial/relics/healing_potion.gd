extends Relic

@export var healing_amount: int


func activate_relic(relic_ui: RelicUI):
	relic_ui.flash()
	
	var player := relic_ui.get_tree().get_first_node_in_group('player') as Player
	if player:
		player.stats.heal(healing_amount)

extends Relic


func activate_relic(relic_ui: RelicUI):
	# this is a slightly lazy way to do things as it's piggy backing off of a signal that isn't really the right signal. I'd be better off creating a new signal of stats reset and connecting to that
	# connect one shot is a way to just call it once rather than every time the signal is emitted. Reason it still works in the next battle is because signals are attached to objects and every battle deletes and instantiates all new things, so it's a new signal that again only works once
	Events.player_hand_drawn.connect(_add_mana.bind(relic_ui), CONNECT_ONE_SHOT)


func _add_mana(relic_ui: RelicUI):
	relic_ui.flash()
	
	var player := relic_ui.get_tree().get_first_node_in_group('player') as Player
	if player:
		player.stats.mana += 1

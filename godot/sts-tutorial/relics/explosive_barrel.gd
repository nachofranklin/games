extends Relic

@export var damage: int


func activate_relic(relic_ui: RelicUI):
	relic_ui.flash()
	
	var enemies := relic_ui.get_tree().get_nodes_in_group('enemies')
	var damage_effect := DamageEffect.new()
	damage_effect.amount = damage
	damage_effect.receiver_modifier_type = Modifier.Type.NO_MODIFIER
	damage_effect.execute(enemies)

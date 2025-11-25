extends Relic

@export_range(1, 100) var discount: int = 50

var relic_ui_mv: RelicUI


func initialise_relic(relic_ui: RelicUI):
	Events.shop_entered.connect(add_shop_modifier) # we don't need to bind shop here because the signal already emits one argument which matches the required argument (shop: Shop)
	relic_ui_mv = relic_ui


func deactivate_relic(_relic_ui: RelicUI):
	Events.shop_entered.disconnect(add_shop_modifier)


func add_shop_modifier(shop: Shop):
	relic_ui_mv.flash()
	
	var shop_cost_modifier := shop.modifier_handler.get_modifier(Modifier.Type.SHOP_COST)
	assert(shop_cost_modifier, 'no shop cost modifier in shop')
	
	var coupons_modifier_value := shop_cost_modifier.get_value('coupons')
	
	if not coupons_modifier_value:
		coupons_modifier_value = ModifierValue.create_new_modifier('coupons', ModifierValue.Type.PERCENT_BASED)
		coupons_modifier_value.percent_value = -1 * discount / 100.0
		shop_cost_modifier.add_new_value(coupons_modifier_value)

extends VBoxContainer
class_name ShopRelic

const RELIC_UI = preload('res://scenes/relic_handler/relic_ui.tscn')

@export var relic: Relic : set = set_relic

@onready var relic_container: CenterContainer = %RelicContainer
@onready var price_h_box: HBoxContainer = %PriceHBox
@onready var price_label: Label = %PriceLabel
@onready var buy_button: Button = %BuyButton
@onready var gold_cost: int = RNG.instance.randi_range(100, 300)


func update(run_stats: RunStats):
	if not relic_container or not price_h_box or not buy_button:
		return
	
	price_label.text = str(gold_cost)
	
	if run_stats.gold >= gold_cost:
		price_label.remove_theme_color_override('font_color')
		buy_button.disabled = false
	else:
		price_label.add_theme_color_override('font_color', Color.RED)
		buy_button.disabled = true


func set_relic(new_relic: Relic):
	if not is_node_ready():
		await ready
	
	relic = new_relic
	
	for relic_ui: RelicUI in relic_container.get_children():
		relic_ui.queue_free()
	
	var new_relic_ui: RelicUI = RELIC_UI.instantiate() as RelicUI
	relic_container.add_child(new_relic_ui)
	new_relic_ui.relic = relic


func _on_buy_button_pressed() -> void:
	Events.shop_relic_bought.emit(relic, gold_cost)
	# queue free everything while leaving the ShopRelic hbox in place so that there's nothing there but everything else (other shop relics/cards) stays in its place
	relic_container.queue_free()
	price_h_box.queue_free()
	buy_button.queue_free()

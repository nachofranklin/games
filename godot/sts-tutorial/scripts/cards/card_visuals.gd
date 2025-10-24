extends Control
class_name CardVisuals

@export var card: Card : set = set_card

@onready var panel: Panel = $Panel
@onready var energy_cost: Label = $EnergyCost
@onready var icon: TextureRect = $Icon
@onready var rarity: TextureRect = $Rarity


func set_card(value: Card):
	if not is_node_ready():
		await ready
	
	card = value
	energy_cost.text = str(card.energy_cost)
	icon.texture = card.icon
	rarity.modulate = Card.RARITY_COLOURS[card.rarity]

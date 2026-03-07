extends Button
class_name CardPileButton

@export var card_pile: CardPile : set = _set_card_pile

@onready var counter_label: Label = $CounterLabel


func _set_card_pile(value: CardPile) -> void:
	card_pile = value
	icon = card_pile.icon
	
	if not card_pile.card_pile_size_changed.is_connected(_on_card_pile_size_changed):
		card_pile.card_pile_size_changed.connect(_on_card_pile_size_changed)
		_on_card_pile_size_changed(card_pile.cards.size())


func _on_card_pile_size_changed(new_amount: int) -> void:
	counter_label.text = str(new_amount)

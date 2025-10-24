extends TextureButton
class_name CardPileOpener

@export var counter: Label
@export var card_pile: CardPile : set = set_card_pile


func set_card_pile(new_value: CardPile):
	card_pile = new_value
	
	if not card_pile.card_pile_size_changed.is_connected(_on_card_pile_size_changed):
		card_pile.card_pile_size_changed.connect(_on_card_pile_size_changed)
		_on_card_pile_size_changed(card_pile.cards.size())


func _on_card_pile_size_changed(cards_amount: int):
	counter.text = str(cards_amount)

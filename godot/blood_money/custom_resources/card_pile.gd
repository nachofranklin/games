extends Resource
class_name CardPile

signal card_pile_size_changed(new_amount)

@export var cards: Array[Card]


#func is_empty() -> bool:
	#return cards.is_empty()


func draw_card() -> Card: # drawing one off the top
	var card: Card = cards.pop_front()
	card_pile_size_changed.emit(cards.size())
	return card


func add_card(card: Card) -> void:
	cards.append(card)
	card_pile_size_changed.emit(cards.size())


func remove_card(card: Card) -> void: # if you've selected a card to move then you could .remove_card(card) from a pile and and .add_card(card) to another
	cards.erase(card)
	card_pile_size_changed.emit(cards.size())


func clear() -> void:
	cards.clear()
	card_pile_size_changed.emit(cards.size())


#func shuffle() -> void:
	#cards.shuffle()

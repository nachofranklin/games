extends Node
class_name PlayerHandler

const HAND_DRAW_INTERVAL: float = 0.25
const HAND_DISCARD_INTERVAL: float = 0.25

@export var hand: Hand

var character: CharacterStats


func _ready() -> void:
	Events.card_played.connect(_on_card_played)


func start_battle(char_stats: CharacterStats):
	character = char_stats
	character.draw_pile = character.deck.duplicate(true)
	character.draw_pile.shuffle()
	character.discard = CardPile.new()
	#character.exhaust_pile = CardPile.new()
	start_turn()


func start_turn():
	character.block = 0
	character.reset_mana()
	draw_cards(character.cards_per_turn)


func end_turn():
	hand.disable_hand()
	discard_cards()


func draw_card():
	reshuffle_deck_from_discard()
	hand.add_card(character.draw_pile.draw_card())
	reshuffle_deck_from_discard() # i don't think the second one is needed as it only reshuffles in sts when trying to add a card from an empty draw pile, not if drawing the card makes the draw pile empty


func draw_cards(amount: int):
	var tween: Tween = create_tween()
	for i in range(amount):
		tween.tween_callback(draw_card)
		tween.tween_interval(HAND_DRAW_INTERVAL)
	
	tween.finished.connect(func(): Events.player_hand_drawn.emit()) # why is this a func?


#func  discard_card(card: Card):
	#pass


func discard_cards():
	if hand.get_child_count() == 0:
		Events.player_hand_discarded.emit()
		return
	
	var tween: Tween = create_tween()
	for card_ui in hand.get_children():
		tween.tween_callback(character.discard.add_card.bind(card_ui.card)) # bind?
		tween.tween_callback(hand.discard_card.bind(card_ui))
		tween.tween_interval(HAND_DISCARD_INTERVAL)
	
	tween.finished.connect(
		func():
			Events.player_hand_discarded.emit()
	)


func reshuffle_deck_from_discard():
	if not character.draw_pile.empty():
		return
	
	while not character.discard.empty():
		character.draw_pile.add_card(character.discard.draw_card())
	
	character.draw_pile.shuffle()


func _on_card_played(card: Card):
	character.discard.add_card(card)

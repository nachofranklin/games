# Player turn order:
# 1. START_OF_TURN Relics
# 2. START_OF_TURN Statuses
# 3. Draw Hand
# 4. End Turn
# 5. END_OF_TURN Relics
# 6. END_OF_TURN Statuses
# 7. Discard Hand

extends Node
class_name PlayerHandler

const HAND_DRAW_INTERVAL: float = 0.25
const HAND_DISCARD_INTERVAL: float = 0.25

@export var relic_handler: RelicHandler
@export var player: Player
@export var hand: Hand

@onready var exhaust_pile_button: CardPileOpener = %ExhaustPileButton

var character: CharacterStats


func _ready() -> void:
	Events.card_played.connect(_on_card_played)


func start_battle(char_stats: CharacterStats):
	character = char_stats
	#character.draw_pile = character.deck.duplicate(true)
	character.draw_pile = character.deck.custom_duplicate()
	character.draw_pile.shuffle()
	character.discard_pile = CardPile.new()
	character.exhaust_pile = CardPile.new()
	relic_handler.relics_activated.connect(_on_relics_activated)
	player.status_handler.statuses_applied.connect(_on_statuses_applied)
	start_turn()


func start_turn():
	character.block = 0
	character.reset_mana()
	relic_handler.activate_relics_by_when_type(Relic.WhenType.START_OF_TURN)


func end_turn():
	hand.disable_hand()
	relic_handler.activate_relics_by_when_type(Relic.WhenType.END_OF_TURN)


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


func discard_cards():
	if hand.get_child_count() == 0:
		Events.player_hand_discarded.emit()
		return
	
	var tween: Tween = create_tween()
	for card_ui in hand.get_children():
		tween.tween_callback(character.discard_pile.add_card.bind(card_ui.card)) # bind?
		tween.tween_callback(hand.discard_card.bind(card_ui))
		tween.tween_interval(HAND_DISCARD_INTERVAL)
	
	tween.finished.connect(
		func():
			Events.player_hand_discarded.emit()
	)


func reshuffle_deck_from_discard():
	if not character.draw_pile.empty():
		return
	
	while not character.discard_pile.empty():
		character.draw_pile.add_card(character.discard_pile.draw_card())
	
	character.draw_pile.shuffle()


func _on_card_played(card: Card):
	if card.type == Card.Type.POWER:
		return
	elif card.exhausts:
		character.exhaust_pile.add_card(card)
		if exhaust_pile_button.visible == false:
			exhaust_pile_button.visible = true
	else:
		character.discard_pile.add_card(card)


func _on_statuses_applied(when_type: Status.WhenType):
	match when_type:
		Status.WhenType.START_OF_TURN:
			draw_cards(character.cards_per_turn)
		Status.WhenType.END_OF_TURN:
			discard_cards()


func _on_relics_activated(when_type: Relic.WhenType):
	match when_type:
		Relic.WhenType.START_OF_TURN:
			player.status_handler.apply_statuses_by_type(Status.WhenType.START_OF_TURN)
		Relic.WhenType.END_OF_TURN:
			player.status_handler.apply_statuses_by_type(Status.WhenType.END_OF_TURN)

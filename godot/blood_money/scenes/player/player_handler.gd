extends Node
class_name PlayerHandler

const CARD_DRAW_INTERVAL: float = 0.25
const CARD_DISCARD_INTERVAL: float = 0.25

@export var hand: Hand

var player_stats: CharacterStats


func _ready() -> void:
	Events.card_played.connect(_on_card_played)


func start_battle(char_stats: CharacterStats) -> void:
	player_stats = char_stats
	player_stats.draw_pile = player_stats.deck.duplicate(true)
	player_stats.draw_pile.shuffle()
	player_stats.discard_pile = CardPile.new()
	player_stats.exhaust_pile = CardPile.new()
	# need to clear the hand in case there's anything still in it
	# apply the effects of the start of battle relics


func start_turn() -> void: # do i need to pass in the turn number as an argument?
	player_stats.block = player_stats.base_block
	player_stats.reset_cards_per_turn()
	player_stats.reset_mana()
	player_stats.stats_changed.emit()
	# apply start of turn relics
	#player_stats.stats_changed.emit() # this might be better applying individually to relics?
	# apply start of turn statuses
	#player_stats.stats_changed.emit() # this might be better applying individually to statuses?
	draw_cards(player_stats.cards_per_turn)


func end_turn() -> void:
	hand.disable_hand()
	# some cards might have end of turn effects, so iterate through all cards left in the hand and apply those effects
	# apply end of turn relics
	# apply end of turn statuses
	discard_cards()


func _draw_card() -> void:
	reshuffle_deck_from_discard()
	hand.add_card(player_stats.draw_pile.draw_card())


func draw_cards(amount_to_draw: int) -> void:
	var tween: Tween = create_tween()
	for i in range(amount_to_draw):
		tween.tween_callback(_draw_card)
		tween.tween_interval(CARD_DRAW_INTERVAL)
	
	tween.finished.connect(
		func(): Events.player_hand_drawn.emit()
	)


func _discard_card(card_ui: CardUI) -> void:
	player_stats.discard_pile.add_card(card_ui.card)
	hand.discard_card(card_ui)


func discard_cards() -> void:
	var cards_left_in_hand: Array[Node] = hand.get_children()
	cards_left_in_hand.reverse() # just nicer visually i think
	var tween: Tween = create_tween()
	
	for card_ui: CardUI in cards_left_in_hand:
		tween.tween_callback(_discard_card.bind(card_ui))
		tween.tween_interval(CARD_DISCARD_INTERVAL)
	
	tween.finished.connect(
		func(): Events.player_hand_discarded.emit()
	)


func reshuffle_deck_from_discard() -> void:
	if not player_stats.draw_pile.is_empty():
		return
	
	while not player_stats.discard_pile.is_empty():
		player_stats.draw_pile.add_card(player_stats.discard_pile.draw_card())
	
	player_stats.draw_pile.shuffle()


func _on_card_played(card: Card) -> void:
	player_stats.discard_pile.add_card(card)

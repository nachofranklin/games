extends CanvasLayer
class_name BattleUI

@export var char_stats: CharacterStats : set = _set_char_stats

@onready var hand_h_box: Hand = %HandHBox
@onready var mana_ui: ManaUI = %ManaUI
@onready var draw_pile_button: CardPileButton = %DrawPileButton
@onready var discard_pile_button: CardPileButton = %DiscardPileButton
@onready var exhaust_pile_button: CardPileButton = %ExhaustPileButton


func _set_char_stats(value: CharacterStats) -> void:
	char_stats = value
	mana_ui.char_stats = char_stats
	hand_h_box.char_stats = char_stats
	# card char stats is temporary, can delete this when cards are drawn automatically
	for card in hand_h_box.get_children():
		card.char_stats = value


func initialise_card_pile_ui() -> void:
	draw_pile_button.card_pile = char_stats.draw_pile
	#draw_pile_button.icon = char_stats.draw_pile.icon
	discard_pile_button.card_pile = char_stats.discard_pile
	#discard_pile_button.icon = char_stats.discard_pile.icon
	exhaust_pile_button.card_pile = char_stats.exhaust_pile
	#exhaust_pile_button.icon = char_stats.exhaust_pile.icon

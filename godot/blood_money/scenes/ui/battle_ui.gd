extends CanvasLayer
class_name BattleUI

@export var char_stats: CharacterStats : set = _set_char_stats

#@onready var hand_h_box: Hand = %HandHBox
@onready var hand: Hand = %Hand
@onready var mana_ui: ManaUI = %ManaUI
@onready var draw_pile_button: CardPileButton = %DrawPileButton
@onready var discard_pile_button: CardPileButton = %DiscardPileButton
@onready var exhaust_pile_button: CardPileButton = %ExhaustPileButton


func _set_char_stats(value: CharacterStats) -> void:
	char_stats = value
	mana_ui.char_stats = char_stats
	hand.char_stats = char_stats


func initialise_card_pile_ui() -> void:
	draw_pile_button.card_pile = char_stats.draw_pile
	discard_pile_button.card_pile = char_stats.discard_pile
	exhaust_pile_button.card_pile = char_stats.exhaust_pile

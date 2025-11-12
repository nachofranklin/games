extends CanvasLayer
class_name BattleUI

@export var char_stats: CharacterStats : set = _set_char_stats

@onready var hand: Hand = $Hand as Hand
@onready var mana_ui: ManaUI = $ManaUI as ManaUI
@onready var end_turn_button: Button = $EndTurnButton # i didn't make it a unique name like the tutorial so if something goes wrong that's probably why
@onready var draw_pile_button: CardPileOpener = %DrawPileButton
@onready var discard_pile_button: CardPileOpener = %DiscardPileButton
@onready var exhaust_pile_button: CardPileOpener = %ExhaustPileButton
@onready var draw_pile_view: CardPileView = %DrawPileView
@onready var discard_pile_view: CardPileView = %DiscardPileView
@onready var exhaust_pile_view: CardPileView = %ExhaustPileView


func _ready() -> void:
	Events.player_hand_drawn.connect(_on_player_hand_drawn)
	end_turn_button.pressed.connect(_on_end_turn_button_pressed)
	draw_pile_button.pressed.connect(draw_pile_view.show_current_view.bind('Draw Pile', true))
	discard_pile_button.pressed.connect(discard_pile_view.show_current_view.bind('Discard Pile'))
	exhaust_pile_button.pressed.connect(exhaust_pile_view.show_current_view.bind('Exhaust Pile'))
	exhaust_pile_button.visible = false


func initialise_card_pile_ui():
	draw_pile_button.card_pile = char_stats.draw_pile
	draw_pile_view.card_pile = char_stats.draw_pile
	discard_pile_button.card_pile = char_stats.discard_pile
	discard_pile_view.card_pile = char_stats.discard_pile
	exhaust_pile_button.card_pile = char_stats.exhaust_pile
	exhaust_pile_view.card_pile = char_stats.exhaust_pile


func _set_char_stats(value: CharacterStats):
	char_stats = value
	hand.char_stats = char_stats
	mana_ui.char_stats = char_stats


func _on_player_hand_drawn():
	end_turn_button.disabled = false


func _on_end_turn_button_pressed():
	end_turn_button.disabled = true
	Events.player_turn_ended.emit()

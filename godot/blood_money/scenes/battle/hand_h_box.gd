extends HBoxContainer
class_name Hand

@export var char_stats: CharacterStats

@onready var card_ui: PackedScene = preload('res://scenes/cards/card_ui.tscn')

var cards_played_this_turn: int = 0


func _ready() -> void:
	Events.card_played.connect(_on_card_played)
	Events.player_hand_drawn.connect(_on_player_hand_drawn)


func add_card(card: Card) -> void:
	var new_card_ui: CardUI = card_ui.instantiate()
	add_child(new_card_ui)
	new_card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)
	new_card_ui.card = card
	new_card_ui.parent = self
	new_card_ui.char_stats = char_stats


func discard_card(card: CardUI) -> void:
	card.queue_free()


func disable_hand() -> void:
	for card in get_children():
		card.disabled = true


func enable_hand() -> void:
	for card in get_children():
		card.disabled = false


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)
	move_child(child, child.original_index)


func _on_card_played(_card: Card) -> void:
	cards_played_this_turn += 1


func _on_player_hand_drawn() -> void:
	enable_hand()

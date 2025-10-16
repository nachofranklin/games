extends HBoxContainer
class_name Hand

@export var char_stats: CharacterStats

@onready var card_ui: PackedScene = preload("res://scenes/card_ui/card_ui.tscn")

var cards_played_this_turn: int = 0


func _ready() -> void:
	Events.card_played.connect(_on_card_played)
	
	# we now get the cards from code from the battle management (battleui) and so there are no longer default children cards
	#for child in get_children():
		#var card_ui := child as CardUI
		#card_ui.parent = self
		#card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)


func add_card(card: Card):
	var new_card_ui := card_ui.instantiate()
	add_child(new_card_ui)
	new_card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)
	new_card_ui.card = card
	new_card_ui.parent = self # i'm not sure how this is different to add_child(new_card_ui) above?
	new_card_ui.char_stats = char_stats


func discard_card(card: CardUI):
	card.queue_free() # do i not also need to add it to the discard pile or is that done elsewhere?


func disable_hand():
	for card in get_children():
		card.disabled = true


func _on_card_played(_card: Card):
	cards_played_this_turn += 1


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)
	var new_index := clampi(child.original_index - cards_played_this_turn, 0, get_child_count()) # clampi is probably overkill but whatever
	move_child.call_deferred(child, new_index)

extends HBoxContainer
class_name Hand

@export var char_stats: CharacterStats

@onready var card_ui: PackedScene = preload("res://scenes/card_ui/card_ui.tscn")


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


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)
	var new_index := clampi(child.original_index, 0, get_child_count()) # clampi is probably overkill but whatever
	move_child.call_deferred(child, new_index)

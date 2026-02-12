extends HBoxContainer
class_name Hand


func _ready() -> void:
	for child in get_children():
		var card_ui: CardUI = child
		card_ui.parent = self
		card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)

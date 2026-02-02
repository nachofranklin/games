extends HBoxContainer
class_name Hand


func _ready() -> void:
	for child in get_children():
		var card_ui: CardUI = child
		#card_ui.parent = self # tutorial gave card_ui a parent var but i'm not sure why?
		card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)

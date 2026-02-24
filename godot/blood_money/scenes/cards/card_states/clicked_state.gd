extends CardState


func enter() -> void:
	card_ui.state_label.text = 'CLICKED'
	card_ui.card_area.monitoring = true
	card_ui.original_index = card_ui.get_index()


func on_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		change_state.emit(self, CardState.State.DRAGGING)

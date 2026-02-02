extends CardState


func enter() -> void:
	card_ui.state_label.text = 'CLICKED'
	print('clicked')
	card_ui.card_area.monitoring = true


func on_input(event: InputEvent) -> void:
	if event is InputEventMouseMotion:
		change_state.emit(self, CardState.State.DRAGGING)

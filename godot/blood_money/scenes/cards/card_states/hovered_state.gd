extends CardState


func enter() -> void:
	card_ui.state_label.text = 'HOVERED'
	card_ui.scale = Vector2(2, 2)


func on_gui_input(event: InputEvent) -> void:
	if event.is_action_pressed('left_mouse'):
		card_ui.pivot_offset = card_ui.get_global_mouse_position() - card_ui.global_position
		transition_requested.emit(self, CardState.State.CLICKED)


func on_mouse_exited() -> void:
	transition_requested.emit(self, CardState.State.BASE)

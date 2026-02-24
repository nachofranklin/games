extends CardState


func enter() -> void:
	card_ui.state_label.text = 'HOVERED'
	card_ui.pivot_offset_ratio = Vector2(0.5, 1)
	card_ui.scale = Vector2(1.25, 1.25)


func on_gui_input(event: InputEvent) -> void:
	var confirm: bool = event.is_action_pressed('left_mouse')
	
	if not card_ui.playable or card_ui.disabled:
		return
	
	elif confirm:
		change_state.emit(self, CardState.State.CLICKED)


func on_mouse_exited() -> void:
	change_state.emit(self, CardState.State.BASE)

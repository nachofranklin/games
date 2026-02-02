extends CardState


func enter() -> void:
	card_ui.state_label.text = 'AIMING'
	card_ui.target_areas.clear()
	card_ui.card_area.monitoring = false
	# need to move the card to the center
	Events.card_aim_started.emit(card_ui)


func exit() -> void:
	Events.card_aim_ended.emit(card_ui)


func on_input(event: InputEvent) -> void:
	if event.is_action_pressed('right_mouse'):
		change_state.emit(self, CardState.State.BASE)
	elif event.is_action_pressed('left_mouse'):
		get_viewport().set_input_as_handled() # look into what this actually does
		change_state.emit(self, CardState.State.RELEASED)

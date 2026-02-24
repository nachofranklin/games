extends CardState


func enter() -> void:
	card_ui.state_label.text = 'AIMING'
	card_ui.targets.clear()
	var hand_global_rect = card_ui.parent.get_global_rect()
	var card_ui_global_rect = card_ui.get_global_rect()
	var offset: Vector2 = Vector2(hand_global_rect.size.x / 2 - card_ui_global_rect.size.x / 2, -card_ui_global_rect.size.y / 3)
	card_ui.animate_to_position(hand_global_rect.position + offset, 0.3)
	card_ui.card_area.monitoring = false
	Events.card_aim_started.emit(card_ui)


func exit() -> void:
	Events.card_aim_ended.emit(card_ui)


func on_input(event: InputEvent) -> void:
	var cancel: bool = event.is_action_pressed('right_mouse')
	var confirm: bool = event.is_action_pressed('left_mouse')
	
	if cancel:
		change_state.emit(self, CardState.State.BASE)
		card_ui.reparent_requested.emit(card_ui)
	elif confirm:
		get_viewport().set_input_as_handled() # look into what this actually does
		change_state.emit(self, CardState.State.RELEASED)

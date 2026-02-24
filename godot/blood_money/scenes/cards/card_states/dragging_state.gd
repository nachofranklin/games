extends CardState

var offset: Vector2


func enter() -> void:
	var ui_layer := get_tree().get_first_node_in_group('ui_layer')
	if ui_layer:
		card_ui.reparent(ui_layer)
	
	card_ui.state_label.text = 'DRAGGING'
	offset = card_ui.global_position - card_ui.get_global_mouse_position()
	Events.card_drag_started.emit(card_ui)


func exit() -> void:
	Events.card_drag_ended.emit(card_ui)


func on_input(event: InputEvent) -> void:
	var single_targeted: bool = card_ui.card.is_single_targeted()
	var mouse_motion: bool = event is InputEventMouseMotion
	var cancel: bool = event.is_action_pressed('right_mouse')
	var confirm: bool = event.is_action_pressed('left_mouse')
	var in_card_drop_area: bool = card_ui.targets.size() > 0
	
	if mouse_motion:
		card_ui.global_position = card_ui.get_global_mouse_position() + offset
	
	if mouse_motion and single_targeted and in_card_drop_area:
		change_state.emit(self, CardState.State.AIMING)
		return
	
	if cancel:
		change_state.emit(self, CardState.State.BASE)
		card_ui.reparent_requested.emit(card_ui)
	elif confirm:
		get_viewport().set_input_as_handled() # what does this do? i think it's to stop us picking up another card but i don't really get it
		change_state.emit(self, CardState.State.RELEASED)

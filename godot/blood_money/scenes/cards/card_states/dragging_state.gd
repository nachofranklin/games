extends CardState

var offset: Vector2


func enter() -> void:
	var ui_layer := get_tree().get_first_node_in_group('ui_layer')
	if ui_layer:
		card_ui.reparent(ui_layer)
	
	card_ui.state_label.text = 'DRAGGING'
	print('dragging')
	offset = card_ui.global_position - card_ui.get_global_mouse_position()


func on_input(event: InputEvent) -> void:
	var single_targeted: bool = card_ui.card.is_single_targeted()
	var mouse_motion := event is InputEventMouseMotion
	var cancel = event.is_action_pressed('right_mouse')
	var confirm = event.is_action_pressed('left_mouse')
	
	if mouse_motion and single_targeted and card_ui.target_areas.size() > 0: # card_ui.target_areas.size() > 0 means if the CardArea and CardDropArea overlap
		change_state.emit(self, CardState.State.AIMING)
		return
	
	if mouse_motion:
		card_ui.global_position = card_ui.get_global_mouse_position() + offset
	
	if cancel:
		change_state.emit(self, CardState.State.BASE)
	elif confirm:
		get_viewport().set_input_as_handled() # what does this do? i think it's to stop us picking up another card but i don't really get it
		change_state.emit(self, CardState.State.RELEASED)

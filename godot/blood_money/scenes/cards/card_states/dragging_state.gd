extends CardState


func enter() -> void:
	var ui_layer := get_tree().get_first_node_in_group('ui_layer')
	if ui_layer:
		card_ui.reparent(ui_layer)
	
	card_ui.scale = Vector2(1, 1)
	card_ui.state_label.text = 'DRAGGING'


func on_input(event: InputEvent) -> void:
	var mouse_motion := event is InputEventMouseMotion
	var cancel = event.is_action_pressed('right_mouse')
	var confirm = event.is_action_pressed('left_mouse')
	
	if mouse_motion:
		card_ui.global_position = card_ui.get_global_mouse_position() - card_ui.pivot_offset
	
	if cancel:
		transition_requested.emit(self, CardState.State.BASE)
	elif confirm:
		get_viewport().set_input_as_handled() # what does this do? i think it's to stop us picking up another card but i don't really get it
		transition_requested.emit(self, CardState.State.RELEASED)

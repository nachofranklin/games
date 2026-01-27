extends CardState


func enter() -> void:
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	card_ui.scale = Vector2(1, 1)
	card_ui.reparent_requested.emit(card_ui)
	card_ui.state_label.text = 'BASE'
	card_ui.pivot_offset = Vector2.ZERO # when clicked/dragging the pivot offset is changed to wherever it's clicked, but when the card returns to the hand it needs to pivot offset resetting back to zero


#func on_gui_input(event: InputEvent) -> void: # this should actually be in hovered not base
	#if event.is_action_pressed('left_mouse'):
		#card_ui.pivot_offset = card_ui.get_global_mouse_position() - card_ui.global_position
		#transition_requested.emit(self, CardState.State.CLICKED)


func on_mouse_entered() -> void:
	transition_requested.emit(self, CardState.State.HOVERED)

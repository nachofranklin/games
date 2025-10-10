extends CardState

const MOUSE_Y_SNAPBACK_THRESHOLD: int = 138 # should come up with a better way of getting this number

func enter():
	card_ui.colour.color = Color.WEB_PURPLE
	card_ui.state.text = 'AIMING'
	card_ui.targets.clear()
	var offset: Vector2 = Vector2(card_ui.parent.size.x / 2 - card_ui.size.x / 2, -card_ui.size.y / 2) # half the size of the hand container - half the card to make it centered, then minus half the height of the card to make it slightly higher than the rest of the hand
	card_ui.animate_to_position(card_ui.parent.global_position + offset, 0.3)
	card_ui.card_area.monitoring = false
	Events.card_aim_started.emit(card_ui)

func exit():
	Events.card_aim_ended.emit(card_ui)

func on_input(event: InputEvent):
	var mouse_motion := event is InputEventMouseMotion
	var mouse_at_bottom := card_ui.get_global_mouse_position().y > MOUSE_Y_SNAPBACK_THRESHOLD
	
	if (mouse_motion and mouse_at_bottom) or event.is_action_pressed('right_mouse'):
		transition_requested.emit(self, CardState.State.BASE)
	elif event.is_action_released('left_mouse') or event.is_action_pressed('left_mouse'):
		get_viewport().set_input_as_handled()
		transition_requested.emit(self, CardState.State.RELEASED)

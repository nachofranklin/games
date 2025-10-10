extends CardState

func enter():
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	if card_ui.tween and card_ui.tween.is_running(): # this is to prevent a bug of the position of a select enemy att card getting stuck in the slightly higher up pos if you move down quickly enough after selecting it due to the tween of moving it into that position taking 0.3 seconds 
		card_ui.tween.kill()
	
	card_ui.reparent_requested.emit(card_ui)
	card_ui.colour.color = Color.WEB_GREEN
	card_ui.state.text = 'BASE'
	card_ui.pivot_offset = Vector2.ZERO

func on_gui_input(event: InputEvent):
	if event.is_action_pressed('left_mouse'):
		card_ui.pivot_offset = card_ui.get_global_mouse_position() - card_ui.global_position
		transition_requested.emit(self, CardState.State.CLICKED)

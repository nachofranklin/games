extends CardState

const DRAG_MIN_THRESHOLD: float = 0.2
var min_drag_time_elapsed: bool = false # stops a quick double click cancelling out what you want to do

func enter():
	var ui_layer = get_tree().get_first_node_in_group('ui_layer')
	if ui_layer:
		card_ui.reparent(ui_layer)
	
	card_ui.colour.color = Color.NAVY_BLUE
	card_ui.state.text = 'DRAGGING'
	
	min_drag_time_elapsed = false
	var threshold_timer: SceneTreeTimer = get_tree().create_timer(DRAG_MIN_THRESHOLD, false)
	threshold_timer.timeout.connect(func(): min_drag_time_elapsed = true)

func on_input(event:InputEvent):
	var mouse_motion := event is InputEventMouseMotion
	var cancel = event.is_action_pressed('right_mouse')
	var confirm = event.is_action_pressed('left_mouse') or event.is_action_released('left_mouse')
	
	if mouse_motion:
		card_ui.global_position = card_ui.get_global_mouse_position() - card_ui.pivot_offset
	
	if cancel:
		transition_requested.emit(self, CardState.State.BASE)
	elif confirm and min_drag_time_elapsed:
		get_viewport().set_input_as_handled()
		transition_requested.emit(self, CardState.State.RELEASED)

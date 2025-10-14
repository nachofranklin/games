extends CardState

const DRAG_MIN_THRESHOLD: float = 0.2
var min_drag_time_elapsed: bool = false # stops a quick double click cancelling out what you want to do

func enter():
	var ui_layer = get_tree().get_first_node_in_group('ui_layer')
	if ui_layer:
		card_ui.reparent(ui_layer)
	
	card_ui.panel.set('theme_override_styles/panel', card_ui.DRAG_STYLEBOX)
	Events.card_drag_started.emit(card_ui)
	
	min_drag_time_elapsed = false
	var threshold_timer: SceneTreeTimer = get_tree().create_timer(DRAG_MIN_THRESHOLD, false)
	threshold_timer.timeout.connect(func(): min_drag_time_elapsed = true)

func exit():
	Events.card_drag_ended.emit(card_ui)

func on_input(event:InputEvent):
	var mouse_motion := event is InputEventMouseMotion
	var cancel = event.is_action_pressed('right_mouse')
	var confirm = event.is_action_pressed('left_mouse') or event.is_action_released('left_mouse')
	var single_targeted: bool = card_ui.card.is_single_targeted()
	
	if single_targeted and mouse_motion and card_ui.targets.size() > 0:
		transition_requested.emit(self, CardState.State.AIMING)
		return # if an att card that needs a target to be chosen then go straight to aiming, otherwise continue
	
	if mouse_motion:
		card_ui.global_position = card_ui.get_global_mouse_position() - card_ui.pivot_offset
	
	if cancel:
		transition_requested.emit(self, CardState.State.BASE)
	elif confirm and min_drag_time_elapsed:
		get_viewport().set_input_as_handled()
		transition_requested.emit(self, CardState.State.RELEASED)

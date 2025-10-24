extends CardState


func enter():
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	if card_ui.tween and card_ui.tween.is_running(): # this is to prevent a bug of the position of a select enemy att card getting stuck in the slightly higher up pos if you move down quickly enough after selecting it due to the tween of moving it into that position taking 0.3 seconds 
		card_ui.tween.kill()
	
	card_ui.card_visuals.panel.set('theme_override_styles/panel', card_ui.BASE_STYLEBOX)
	card_ui.reparent_requested.emit(card_ui)
	card_ui.pivot_offset = Vector2.ZERO
	Events.tooltip_hide_requested.emit()


func on_gui_input(event: InputEvent):
	if not card_ui.playable or card_ui.disabled:
		return
	
	if event.is_action_pressed('left_mouse'):
		card_ui.pivot_offset = card_ui.get_global_mouse_position() - card_ui.global_position
		transition_requested.emit(self, CardState.State.CLICKED)


func on_mouse_entered():
	if not card_ui.playable or card_ui.disabled:
		return
	
	card_ui.card_visuals.panel.set('theme_override_styles/panel', card_ui.HOVER_STYLEBOX)
	Events.card_tooltip_requested.emit(card_ui.card.icon, card_ui.card.tooltip_text)


func on_mouse_exited():
	if not card_ui.playable or card_ui.disabled:
		return
	
	card_ui.card_visuals.panel.set('theme_override_styles/panel', card_ui.BASE_STYLEBOX)
	Events.tooltip_hide_requested.emit()

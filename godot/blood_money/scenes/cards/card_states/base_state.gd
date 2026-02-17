extends CardState


func enter() -> void:
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	if card_ui.tween and card_ui.tween.is_running():
		card_ui.tween.kill()
	
	card_ui.scale = Vector2(1, 1)
	card_ui.pivot_offset_ratio = Vector2(0, 0)
	card_ui.reparent_requested.emit(card_ui)
	card_ui.state_label.text = 'BASE'


func on_mouse_entered() -> void:
	change_state.emit(self, CardState.State.HOVERED)

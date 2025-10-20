extends CardState

func enter():
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	card_ui.card_area.monitoring = true
	card_ui.original_index = card_ui.get_index()

func on_input(event: InputEvent):
	if event is InputEventMouseMotion:
		transition_requested.emit(self, CardState.State.DRAGGING)

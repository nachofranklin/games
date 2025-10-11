extends CardState

func enter():
	if not card_ui.is_node_ready():
		await card_ui.ready
	
	card_ui.colour.color = Color.ORANGE
	card_ui.state.text = 'CLICKED'
	card_ui.card_area.monitoring = true

func on_input(event: InputEvent):
	if event is InputEventMouseMotion:
		transition_requested.emit(self, CardState.State.DRAGGING)

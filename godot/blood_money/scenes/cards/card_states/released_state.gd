extends CardState

var played: bool = false


func enter() -> void:
	card_ui.state_label.text = 'RELEASED'
	
	if not card_ui.targets.is_empty(): # if there is one or more targets (either enemies or CardDropArea)
		played = true
		card_ui.play()


func on_input(_event: InputEvent) -> void:
	if played:
		return
	else:
		change_state.emit(self, CardState.State.BASE)
		card_ui.reparent_requested.emit(card_ui)

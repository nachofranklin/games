extends CardState

var played: bool = false

func enter():
	
	if not card_ui.targets.is_empty(): # if the card does have a target when its released...
		played = true
		card_ui.play()

func on_input(_event: InputEvent):
	if played:
		return
	else:
		transition_requested.emit(self, CardState.State.BASE)

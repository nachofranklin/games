extends CardState

var played: bool = false


func enter() -> void:
	card_ui.state_label.text = 'RELEASED'
	
	if not card_ui.target_areas.is_empty(): # if there is one or more target areas (either enemies or CardDropArea)
		played = true
		# play the card


func on_input(_event: InputEvent) -> void:
	if played:
		#card_ui.state_label.text = 'RELEASED'
		return
		# queue free
	else:
		change_state.emit(self, CardState.State.BASE)


# we need something that checks if playing the card is legit or not
# var played bool = false by default
# but then we can check if the card has a target or not and if it does then it plays
# if not it goes to base
# but then how do we add/remove targets to a card?
# in card_ui connect area entered and exited signals to add/remove areas to targets

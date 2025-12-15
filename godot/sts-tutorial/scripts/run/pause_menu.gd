extends CanvasLayer
class_name PauseMenu

signal save_and_quit

@onready var back_to_game_button: Button = %BackToGameButton
@onready var save_and_quit_button: Button = %SaveAndQuitButton


func _input(event: InputEvent):
	if event.is_action_pressed('pause'):
		if visible:
			_unpause()
		else:
			_pause()
		
		get_viewport().set_input_as_handled() # i don't love this. Without this if i had a deck view open and pressed esc it would pause, press esc again and it will unpause and exit the deckview. But with this it would unpause but still be in deckview. But ideally i'd have it so that i can't pause by pressing esc when in deckview


func _pause():
	show()
	get_tree().paused = true


func _unpause():
	hide()
	get_tree().paused = false


func _on_back_to_game_button_pressed() -> void:
	_unpause()


func _on_save_and_quit_button_pressed() -> void:
	get_tree().paused = false
	save_and_quit.emit()

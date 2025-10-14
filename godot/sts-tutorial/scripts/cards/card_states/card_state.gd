extends Node
class_name CardState

enum State {BASE, CLICKED, DRAGGING, AIMING, RELEASED}

@warning_ignore('UNUSED_SIGNAL')
signal transition_requested(from: CardState, to: State)

@export var state: State

var card_ui: CardUI

func enter():
	pass

func exit():
	pass

func on_input(_event: InputEvent):
	pass

func on_gui_input(_event: InputEvent):
	pass

func on_mouse_entered():
	pass

func on_mouse_exited():
	pass

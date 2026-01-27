extends Node
class_name CardState

@warning_ignore('UNUSED_SIGNAL')
signal transition_requested(from: CardState, to: State) # why is this not from state to state or from cardstate to cardstate? Why is it different?

enum State {BASE, HOVERED, CLICKED, DRAGGING, AIMING, RELEASED}

@export var state: State

var card_ui: CardUI


func enter() -> void:
	pass


func exit() -> void:
	pass


func on_input(_event: InputEvent) -> void:
	pass


func on_gui_input(_event: InputEvent) -> void:
	pass


func on_mouse_entered() -> void:
	pass


func on_mouse_exited() -> void:
	pass

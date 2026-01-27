extends Control
class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(selected_card: CardUI)

@onready var card_area: Area2D = $CardArea
@onready var state_label: Label = $StateLabel # delete
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine


func _ready() -> void:
	card_state_machine.init(self)


func _input(event: InputEvent) -> void:
	card_state_machine.on_input(event)


func _on_gui_input(event: InputEvent) -> void:
	card_state_machine.on_gui_input(event)


func _on_mouse_entered() -> void:
	card_state_machine.on_mouse_entered()


func _on_mouse_exited() -> void:
	card_state_machine.on_mouse_exited()

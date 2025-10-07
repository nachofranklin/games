extends Control

class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(which_card_ui: CardUI)

@onready var colour: ColorRect = $Colour
@onready var state: Label = $State
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine
@onready var card_area: Area2D = $CardArea
@onready var targets: Array[Node] = []

func _ready() -> void:
	card_state_machine.init(self)

func _input(event: InputEvent) -> void:
	card_state_machine.on_input(event)

func _on_gui_input(event: InputEvent):
	card_state_machine.on_gui_input(event)

func _on_mouse_entered():
	card_state_machine.on_mouse_entered()

func _on_mouse_exited():
	card_state_machine.on_mouse_exited()

func _on_card_area_area_entered(area: Area2D) -> void:
	if not targets.has(area):
		targets.append(area)

func _on_card_area_area_exited(area: Area2D) -> void:
	targets.erase(area)

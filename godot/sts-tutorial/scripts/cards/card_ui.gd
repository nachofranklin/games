extends Control

class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(which_card_ui: CardUI)

const BASE_STYLEBOX := preload("res://scenes/card_ui/card_base_stylebox.tres")
const HOVER_STYLEBOX := preload("res://scenes/card_ui/card_hover_stylebox.tres")
const DRAG_STYLEBOX := preload("res://scenes/card_ui/card_dragging_stylebox.tres")

@export var card: Card : set = _set_card

@onready var panel: Panel = $Panel
@onready var energy_cost: Label = $EnergyCost
@onready var icon: TextureRect = $Icon
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine
@onready var card_area: Area2D = $CardArea
@onready var targets: Array[Node] = []

var parent: Control
var tween: Tween

func _ready() -> void:
	card_state_machine.init(self)

func animate_to_position(new_position: Vector2, duration: float):
	tween = create_tween().set_trans(Tween.TRANS_CIRC).set_ease(Tween.EASE_OUT)
	#tween = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT) # different arrow shape option
	tween.tween_property(self, 'global_position', new_position, duration)

func _input(event: InputEvent) -> void:
	card_state_machine.on_input(event)

func _on_gui_input(event: InputEvent):
	card_state_machine.on_gui_input(event)

func _on_mouse_entered():
	card_state_machine.on_mouse_entered()

func _on_mouse_exited():
	card_state_machine.on_mouse_exited()

func _set_card(value: Card):
	if not is_node_ready():
		await ready
	
	card = value
	energy_cost.text = str(card.energy_cost)
	icon.texture = card.icon

func _on_card_area_area_entered(area: Area2D) -> void:
	if not targets.has(area):
		targets.append(area)

func _on_card_area_area_exited(area: Area2D) -> void:
	targets.erase(area)

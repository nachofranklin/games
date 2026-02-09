extends Control
class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(selected_card: CardUI)

@export var card: Card : set = _set_card

@onready var card_area: Area2D = $CardArea
@onready var state_label: Label = $StateLabel # delete
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine
@onready var card_visuals: CardVisuals = $CardVisuals
#@onready var target_areas: Array[Node] = [] # should it be area2d instead of node? and why @onready?
var target_areas: Array[Area2D] = []
var tween: Tween


func _ready() -> void:
	card_state_machine.init(self)


func _set_card(value: Card) -> void:
	if not is_node_ready():
		await ready
	
	card = value
	card_visuals.update_visuals(value)


func animate_to_position(new_position: Vector2, duration: float) -> void:
	tween = create_tween().set_trans(Tween.TRANS_CIRC).set_ease(Tween.EASE_OUT)
	tween.tween_property(self, 'global_position', new_position, duration)


func _input(event: InputEvent) -> void:
	card_state_machine.on_input(event)


func _on_gui_input(event: InputEvent) -> void:
	card_state_machine.on_gui_input(event)


func _on_mouse_entered() -> void:
	card_state_machine.on_mouse_entered()


func _on_mouse_exited() -> void:
	card_state_machine.on_mouse_exited()


func _on_card_area_area_entered(area: Area2D) -> void:
	if not target_areas.has(area):
		target_areas.append(area)
		print(target_areas)


func _on_card_area_area_exited(area: Area2D) -> void:
	target_areas.erase(area)
	print(target_areas)

extends Control
class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(selected_card: CardUI)

@export var card: Card : set = _set_card
@export var char_stats: CharacterStats : set = _set_char_stats

@onready var card_area: Area2D = $CardArea
@onready var state_label: Label = $StateLabel # delete
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine
@onready var card_visuals: CardVisuals = $CardVisuals
#@onready var targets: Array[Node] = [] # why @onready?
var targets: Array[Node] = []
var tween: Tween
var parent: Control


func _ready() -> void:
	card_state_machine.init(self)


func _set_card(value: Card) -> void:
	if not is_node_ready():
		await ready
	
	card = value
	card_visuals.update_visuals(value)


func _set_char_stats(value: CharacterStats) -> void:
	if not is_node_ready():
		await ready
	
	char_stats = value
	char_stats.stats_changed.connect(_on_char_stats_changed)


func play() -> void:
	card.play(targets, char_stats)
	queue_free()


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


func _on_char_stats_changed() -> void:
	pass # this will be to check if i have enough mana to play a card


func _on_card_area_area_entered(area: Area2D) -> void:
	var target = area.get_parent()
	if not targets.has(target):
		targets.append(target)


func _on_card_area_area_exited(area: Area2D) -> void:
	var target = area.get_parent()
	targets.erase(target)

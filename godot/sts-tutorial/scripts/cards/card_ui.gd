extends Control

class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(which_card_ui: CardUI)

const BASE_STYLEBOX := preload("res://scenes/card_ui/card_base_stylebox.tres")
const HOVER_STYLEBOX := preload("res://scenes/card_ui/card_hover_stylebox.tres")
const DRAG_STYLEBOX := preload("res://scenes/card_ui/card_dragging_stylebox.tres")

@export var card: Card : set = _set_card
@export var char_stats: CharacterStats : set = _set_char_stats

@onready var card_visuals: CardVisuals = $CardVisuals
@onready var card_state_machine: CardStateMachine = $CardStateMachine as CardStateMachine
@onready var card_area: Area2D = $CardArea
@onready var targets: Array[Node] = []

var original_index: int = 0
var parent: Control
var tween: Tween
var playable: bool = true : set = _set_playable # based on if mana is available to play the card or not
var disabled: bool = false # based on if one card is being played then all others should be disabled

func _ready() -> void:
	Events.card_aim_started.connect(_on_card_drag_or_aiming_started)
	Events.card_drag_started.connect(_on_card_drag_or_aiming_started)
	Events.card_aim_ended.connect(_on_card_drag_or_aim_ended)
	Events.card_drag_ended.connect(_on_card_drag_or_aim_ended)
	card_state_machine.init(self)

func animate_to_position(new_position: Vector2, duration: float):
	tween = create_tween().set_trans(Tween.TRANS_CIRC).set_ease(Tween.EASE_OUT)
	#tween = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN_OUT) # different arrow shape option
	tween.tween_property(self, 'global_position', new_position, duration)

func play():
	if not card:
		return
	
	card.play(targets, char_stats)
	queue_free()

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
	card_visuals.card = card

func _set_playable(value: bool):
	playable = value
	if not playable:
		card_visuals.energy_cost.add_theme_color_override('font_color', Color.RED)
		card_visuals.icon.modulate = Color(1, 1, 1, 0.5)
	else:
		card_visuals.energy_cost.remove_theme_color_override('font_color')
		card_visuals.icon.modulate = Color(1, 1, 1, 1)

func _set_char_stats(value: CharacterStats):
	char_stats = value
	char_stats.stats_changed.connect(_on_char_stats_changed)

func _on_card_area_area_entered(area: Area2D) -> void:
	if not targets.has(area):
		targets.append(area)

func _on_card_area_area_exited(area: Area2D) -> void:
	targets.erase(area)

func _on_card_drag_or_aiming_started(used_card: CardUI):
	if used_card == self:
		return
	
	disabled = true

func _on_card_drag_or_aim_ended(_card: CardUI):
	disabled = false
	playable = char_stats.can_play_card(card) # sets playable to true/false if mana is greater/smaller than the card's cost

func _on_char_stats_changed():
	playable = char_stats.can_play_card(card)

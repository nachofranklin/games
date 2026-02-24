extends Control
class_name CardUI

@warning_ignore('UNUSED_SIGNAL')
signal reparent_requested(selected_card: CardUI) # this is for if the card was in the hand, nearly got played so was reparented to the ui layer to move around but then wasn't played and so should go back to the hand in the same pos it was before

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
var playable: bool = true : set = _set_playable # based on available mana
var disabled: bool = false # all other availability things (if another card is selected, if enemy stops you playing attack cards, etc)
var original_index: int


func _ready() -> void:
	Events.card_drag_started.connect(_on_card_drag_or_aiming_started)
	Events.card_aim_started.connect(_on_card_drag_or_aiming_started)
	Events.card_drag_ended.connect(_on_card_drag_or_aiming_ended)
	Events.card_aim_ended.connect(_on_card_drag_or_aiming_ended)
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


func _set_playable(value: bool) -> void:
	playable = value
	if not playable:
		# make the energy cost red
		card_visuals.energy_label.add_theme_color_override('font_color', Color.RED)
	else:
		# make it normal looking
		card_visuals.energy_label.remove_theme_color_override('font_color')


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
	self.playable = char_stats.can_play_card(card)


func _on_card_drag_or_aiming_started(dragged_card: CardUI) -> void:
	if dragged_card == self:
		return
	
	disabled = true


func _on_card_drag_or_aiming_ended(_dragged_card: CardUI) -> void:
	disabled = false # will need to do something fancier if i want it to check if it should be disabled for other things
	self.playable = char_stats.can_play_card(card) # this makes all cards check if there's enough mana to be played after playing a card
	# does it need to be self. ?


func _on_card_area_area_entered(area: Area2D) -> void: # this checks if the card is getting dragged to the CardDropArea
	if not targets.has(area):
		targets.append(area)


func _on_card_area_area_exited(area: Area2D) -> void:
	targets.erase(area)

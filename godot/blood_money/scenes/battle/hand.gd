extends Control
class_name Hand

@export var char_stats: CharacterStats
@export var spread_curve: Curve
@export var height_curve: Curve
@export var rotation_curve: Curve

@onready var card_ui: PackedScene = preload('res://scenes/cards/card_ui.tscn')

const BUFFER_PERCENTAGE: float = 1.1 # basically says keep cards a cards width + 20% away from each other where possible
const MAX_ROTATION: float = 10.0

var cards_played_this_turn: int = 0


func _ready() -> void:
	Events.card_played.connect(_on_card_played)
	Events.player_hand_drawn.connect(_on_player_hand_drawn)


func add_card(card: Card) -> void:
	var new_card_ui: CardUI = card_ui.instantiate()
	add_child(new_card_ui)
	new_card_ui.reparent_requested.connect(_on_card_ui_reparent_requested)
	new_card_ui.card = card
	new_card_ui.parent = self
	new_card_ui.char_stats = char_stats
	position_cards()


func discard_card(card: CardUI) -> void:
	card.queue_free()


func disable_hand() -> void:
	for card in get_children():
		card.disabled = true


func enable_hand() -> void:
	for card in get_children():
		card.disabled = false


func position_cards() -> void:
	for card: CardUI in get_children():
		var hand_ratio = _get_hand_ratio(card)
		var x_offset = spread_curve.sample(hand_ratio) * (size.x - card.size.x)
		var y_offset = height_curve.sample(hand_ratio) * card.size.y / 4
		var card_rotation = rotation_curve.sample(hand_ratio) * MAX_ROTATION
		
		card.reset_position_and_rotation()
		card.position.x += x_offset
		card.position.y -= y_offset
		card.rotation_degrees += card_rotation


func _get_hand_ratio(card: CardUI) -> float: # 0.0 -> 1.0
	var hand_ratio: float
	var cards_before_an_overlap: int = floori((size.x) / (card.size.x * BUFFER_PERCENTAGE))
	var x_ratio_gap: float = float((card.size.x * BUFFER_PERCENTAGE) / (size.x - card.size.x))
	
	# fancy maths to get the correct buffer, but looks too big visually i think
	#var buffer: float = abs(cos(deg_to_rad(MAX_ROTATION))) + abs((card.size.y / card.size.x) * sin(deg_to_rad(MAX_ROTATION)))
	#var cards_before_an_overlap: int = floori((size.x) / (card.size.x * buffer))
	#var x_ratio_gap: float = float((card.size.x * buffer) / (size.x - card.size.x))
	
	if get_child_count() <= 1: # keeping this for semantics as technically the width of one card could be too big for the hand and therefore it would try dividing by 0
		hand_ratio = 0.5
	elif get_child_count() <= cards_before_an_overlap:
		hand_ratio = 0.5 - float((get_child_count() - 1)) / 2 * x_ratio_gap + float(card.get_index()) * x_ratio_gap
	else:
		hand_ratio = float(card.get_index()) / float(get_child_count() - 1)
	
	return hand_ratio


func _on_card_ui_reparent_requested(child: CardUI):
	child.reparent(self)
	move_child(child, child.original_index)
	position_cards()


func _on_card_played(_card: Card) -> void:
	cards_played_this_turn += 1
	position_cards()


func _on_player_hand_drawn() -> void:
	enable_hand()

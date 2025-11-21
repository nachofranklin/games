extends Control
class_name RelicsControl

const RELICS_PER_PAGE: int = 5
const TWEEN_SCROLL_DURATION: float = 0.2

@export var left_button: TextureButton
@export var right_button: TextureButton

@onready var relics_h_box: HBoxContainer = %RelicsHBox
@onready var page_width = self.custom_minimum_size.x

var num_of_relics: int = 0
var current_page: int = 1
var max_page: int = 0
var tween: Tween


func _ready() -> void:
	left_button.pressed.connect(_on_left_button_pressed)
	right_button.pressed.connect(_on_right_button_pressed)
	
	for relic_ui: RelicUI in relics_h_box.get_children():
		relic_ui.free() # needs to be .free() not .queue_free() as queue free deletes things at the end of a task but our add_relic(starter_relic) adds it before the placeholders have been removed
	
	relics_h_box.child_order_changed.connect(_on_relics_h_box_child_order_changed)


func update():
	# this if prevents an error when closing the game as it tries to update as the nodes are being deleted from bottom up but right button will have already been deleted
	if not is_instance_valid(right_button):
		return
	
	num_of_relics = relics_h_box.get_child_count()
	max_page = ceili(num_of_relics / float(RELICS_PER_PAGE))
	
	left_button.disabled = current_page <= 1
	right_button.disabled = current_page >= max_page


func _tween_to(x_position: float):
	if tween:
		tween.kill()
	
	tween = create_tween().set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tween.tween_property(relics_h_box, 'position:x', x_position, TWEEN_SCROLL_DURATION)


func _on_left_button_pressed():
	if current_page > 1:
		current_page -= 1
		update()
		_tween_to(relics_h_box.position.x + page_width)


func _on_right_button_pressed():
	if current_page < max_page:
		current_page += 1
		update()
		_tween_to(relics_h_box.position.x - page_width)


func _on_relics_h_box_child_order_changed():
	update()

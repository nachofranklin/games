extends Control
class_name StatusUI

@export var status: Status : set = set_status

@onready var icon: TextureRect = $Icon
@onready var center_container: CenterContainer = $CenterContainer
@onready var duration_label: Label = $CenterContainer/DurationLabel
@onready var stacks_label: Label = $CenterContainer/StacksLabel


func set_status(new_status: Status):
	if not is_node_ready():
		await ready
	
	status = new_status
	icon.texture = status.icon
	duration_label.visible = status.stack_type == Status.StackType.DURATION
	stacks_label.visible = status.stack_type == Status.StackType.STACK
	
	custom_minimum_size = icon.size
	if duration_label.visible:
		var label_size: Vector2 = duration_label.size
		var label_offset: Vector2 = center_container.position + duration_label.position
		var total_width = max(icon.size.x, label_offset.x + label_size.x)
		var total_height = max(icon.size.y, label_offset.y + label_size.y)
		custom_minimum_size = Vector2(total_width, total_height)
	elif stacks_label.visible:
		var label_size: Vector2 = stacks_label.size
		var label_offset: Vector2 = center_container.position + stacks_label.position
		var total_width = max(icon.size.x, label_offset.x + label_size.x)
		var total_height = max(icon.size.y, label_offset.y + label_size.y)
		custom_minimum_size = Vector2(total_width, total_height)
	
	if not status.status_changed.is_connected(_on_status_changed):
		status.status_changed.connect(_on_status_changed)
	
	_on_status_changed()



func _on_status_changed():
	if not status:
		return
	
	if status.can_expire and status.duration <= 0:
		queue_free()
	
	if status.stack_type == Status.StackType.STACK and status.stacks == 0: # a stackable status could be negative
		queue_free()
	
	duration_label.text = str(status.duration)
	stacks_label.text = str(status.stacks)

extends GridContainer
class_name StatusHandler

signal statuses_applied(type: Status.WhenType)

const STATUS_UI = preload('res://scenes/status_handler/status_ui.tscn')
const STATUS_APPLY_INTERVAL: float = 0.25

@export var status_owner: Node2D


func apply_statuses_by_type(when_type: Status.WhenType):
	if when_type == Status.WhenType.EVENT_BASED:
		return # will be handled by specific events not by the status handler
	
	var status_queue: Array[Status] = _get_all_statuses().filter(
		func(status: Status):
			return status.when_type == when_type
	)
	if status_queue.is_empty():
		statuses_applied.emit(when_type)
		return
	
	var tween: Tween = create_tween()
	for status: Status in status_queue:
		tween.tween_callback(status.apply_status.bind(status_owner))
		tween.tween_interval(STATUS_APPLY_INTERVAL)
	
	tween.finished.connect(func(): statuses_applied.emit(when_type))


func add_status(status: Status):
	var stackable: bool = status.stack_type != Status.StackType.NONE
	
	# if it's new...
	if not _has_status(status.id):
		var new_status_ui := STATUS_UI.instantiate() as StatusUI
		add_child(new_status_ui)
		new_status_ui.status = status
		new_status_ui.status.status_applied.connect(_on_status_applied)
		new_status_ui.status.initialise_status(status_owner)
		return
	
	# if we already have it and it can't expire and it's not stackable
	if not status.can_expire and not stackable:
		return
	
	# if we already have it and it's a duration type
	if status.can_expire and status.stack_type == Status.StackType.DURATION:
		_get_status(status.id).duration += status.duration
		return
	
	# if we already have it and it's a stack type
	if status.stack_type == Status.StackType.STACK:
		_get_status(status.id).stacks += status.stacks
		return


func _has_status(id: String) -> bool:
	for status_ui: StatusUI in get_children():
		if status_ui.status.id == id:
			return true
	
	return false


func _get_status(id: String) -> Status:
	for status_ui: StatusUI in get_children():
		if status_ui.status.id == id:
			return status_ui.status
	
	return null


func _get_all_statuses() -> Array[Status]:
	var statuses: Array[Status] = []
	for status_ui: StatusUI in get_children():
		statuses.append(status_ui.status)
	
	return statuses


func _on_status_applied(status: Status):
	if status.can_expire:
		status.duration -= 1

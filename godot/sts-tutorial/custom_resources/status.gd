extends Resource
class_name Status

signal status_applied(status: Status) # have to loop through all the statuses one by one to apply them, this signal indicates it's finished applying the current status
signal status_changed # change in duration or stacks

enum WhenType {START_OF_TURN, END_OF_TURN, EVENT_BASED}
enum StackType {NONE, STACK, DURATION}

@export_group('Status Data')
@export var id: String
@export var when_type: WhenType
@export var stack_type: StackType
@export var can_expire: bool
@export var duration: int : set = set_duration
@export var stacks: int : set = set_stacks

@export_group('Status Visuals')
@export var icon: Texture
@export_multiline var tooltip: String


func initialise_status(_target: Node):
	pass


func apply_status(_target: Node):
	status_applied.emit(self)


func get_tooltip() -> String:
	return tooltip


func set_duration(new_duration: int):
	duration = new_duration
	status_changed.emit()


func set_stacks(new_stacks: int):
	stacks = new_stacks
	status_changed.emit()

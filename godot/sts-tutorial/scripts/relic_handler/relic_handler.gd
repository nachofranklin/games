extends HBoxContainer
class_name RelicHandler

signal relics_activated(when_type: Relic.WhenType)

const RELIC_APPLY_INTERVAL: float = 0.5
const RELIC_UI: PackedScene = preload('res://scenes/relic_handler/relic_ui.tscn')

@onready var relics_control: RelicsControl = $RelicsControl
@onready var relics_h_box: HBoxContainer = %RelicsHBox


func _ready() -> void:
	relics_h_box.child_exiting_tree.connect(_on_relics_child_exiting_tree)


func activate_relics_by_when_type(when_type: Relic.WhenType):
	if when_type == Relic.WhenType.EVENT_BASED:
		return
	
	# eg gets an array of all the RelicUI's a player has that is start of turn activated
	var relic_queue: Array[RelicUI] = _get_all_relic_ui_nodes().filter(
		func(relic_ui: RelicUI):
			return relic_ui.relic.when_type == when_type
	)
	if relic_queue.is_empty():
		relics_activated.emit(when_type)
		return
	
	# eg goes through each start of turn relic and activates them, waits half a sec then activates the next one
	var tween: Tween = create_tween()
	for relic_ui: RelicUI in relic_queue:
		tween.tween_callback(relic_ui.relic.activate_relic.bind(relic_ui))
		tween.tween_interval(RELIC_APPLY_INTERVAL)
	
	# eg when finished it sends out a signal to say it's finished activating all the relics that are start of turn
	tween.finished.connect(func(): relics_activated.emit(when_type))


func add_relics(relics_array: Array[Relic]):
	for relic: Relic in relics_array:
		add_relic(relic)


func add_relic(relic: Relic):
	if has_relic(relic.id):
		return
	
	var new_relic_ui := RELIC_UI.instantiate() as RelicUI
	relics_h_box.add_child(new_relic_ui)
	new_relic_ui.relic = relic
	new_relic_ui.relic.initialise_relic(new_relic_ui)


func has_relic(id: String) -> bool:
	for relic_ui: RelicUI in relics_h_box.get_children():
		if relic_ui.relic.id == id and is_instance_valid(relic_ui):
			return true
	
	return false


func get_all_relics() -> Array[Relic]:
	var relic_ui_nodes: Array[RelicUI] = _get_all_relic_ui_nodes()
	var relics_array: Array[Relic] = []
	
	for relic_ui: RelicUI in relic_ui_nodes:
		relics_array.append(relic_ui.relic)
	
	return relics_array


func _get_all_relic_ui_nodes() -> Array[RelicUI]:
	var relics_ui_array: Array[RelicUI] = []
	for relic_ui: RelicUI in relics_h_box.get_children():
		relics_ui_array.append(relic_ui)
	
	return relics_ui_array


func _on_relics_child_exiting_tree(relic_ui: RelicUI):
	if not relic_ui:
		return
	
	if relic_ui.relic:
		relic_ui.relic.deactivate_relic(relic_ui)

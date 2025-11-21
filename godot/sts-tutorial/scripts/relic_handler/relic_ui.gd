extends Control
class_name RelicUI

@export var relic: Relic : set = set_relic

@onready var icon: TextureRect = $Icon
@onready var animation_player: AnimationPlayer = $AnimationPlayer


func set_relic(new_relic: Relic):
	if not is_node_ready():
		await ready
	
	relic = new_relic
	icon.texture = relic.icon


func flash():
	animation_player.play('flash')


func _on_gui_input(event: InputEvent) -> void:
	if event.is_action_pressed('left_mouse'):
		Events.relic_tooltip_requested.emit(relic)

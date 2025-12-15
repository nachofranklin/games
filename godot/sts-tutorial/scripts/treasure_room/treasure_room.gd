extends Control
class_name Treasure

@export var treasure_relic_pool: Array[Relic]
@export var relic_handler: RelicHandler
@export var char_stats: CharacterStats

@onready var animation_player: AnimationPlayer = %AnimationPlayer

var treasure_relic: Relic


func generate_relic():
	var available_relics: Array[Relic] = treasure_relic_pool.filter(
		func(relic: Relic):
			var can_appear: bool = relic.can_appear_as_reward(char_stats)
			var already_had_it: bool = relic_handler.has_relic(relic.id)
			return can_appear and not already_had_it
	)
	treasure_relic = RNG.array_pick_random(available_relics)


# called from the 'open' animation in the animation player
func _on_treasure_opened():
	Events.treasure_room_exited.emit(treasure_relic)


func _on_treasure_chest_gui_input(event: InputEvent) -> void:
	if animation_player.current_animation == 'open':
		return
	
	if event.is_action_pressed('left_mouse'):
		animation_player.play('open')

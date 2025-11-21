# meta-name: Relic
# meta-description: Create a Relic which can be acquired by the player.
extends Relic

var member_var := 0


func initialise_relic(_relic_ui: RelicUI):
	print('this happens once when we gain a new relic')


func activate_relic(_relic_ui: RelicUI):
	print('this happens at specific times based on the Relic.WhenType property')


func deactivate_relic(_relic_ui: RelicUI):
	print('this gets called when a RelicUI is exiting the SceneTree i.e. getting deleted')
	print('event-based relics should disconnect from the EventBus here')


func get_tooltip() -> String:
	return tooltip

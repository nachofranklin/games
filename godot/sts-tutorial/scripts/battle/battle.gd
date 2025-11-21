extends Node2D
class_name Battle

@export var char_stats: CharacterStats
@export var battle_stats: BattleStats
@export var music: AudioStream
@export var relic_handler: RelicHandler

@onready var battle_ui: BattleUI = $BattleUI
@onready var player_handler: PlayerHandler = $PlayerHandler
@onready var enemy_handler: EnemyHandler = $EnemyHandler
@onready var player: Player = $Player


func _ready() -> void:
	Events.player_turn_ended.connect(player_handler.end_turn)
	Events.player_hand_discarded.connect(enemy_handler.start_turn)
	Events.enemy_turn_ended.connect(_on_enemy_turn_ended)
	Events.player_died.connect(_on_player_died)


func start_battle():
	get_tree().paused = false
	MusicPlayer.play(music, true)
	
	battle_ui.char_stats = char_stats
	player.stats = char_stats
	player_handler.relic_handler = relic_handler
	enemy_handler.setup_enemies(battle_stats)
	enemy_handler.reset_enemy_actions()
	
	relic_handler.relics_activated.connect(_on_relics_activated)
	relic_handler.activate_relics_by_when_type(Relic.WhenType.START_OF_COMBAT)


func _on_enemy_turn_ended():
	player_handler.start_turn()
	enemy_handler.reset_enemy_actions()


func _on_enemy_handler_child_order_changed() -> void:
	if enemy_handler.get_child_count() == 0 and is_instance_valid(relic_handler): # the is instance valid is needed so that we don't get an error message when we close it all down and things are deleted but it still tries to call a func
		relic_handler.activate_relics_by_when_type(Relic.WhenType.END_OF_COMBAT)


func _on_player_died():
	Events.battle_over_screen_requested.emit('Game Over!', BattleOverPanel.Type.LOSE)


func _on_relics_activated(when_type: Relic.WhenType):
	match when_type:
		Relic.WhenType.START_OF_COMBAT:
			player_handler.start_battle(char_stats)
			battle_ui.initialise_card_pile_ui()
		Relic.WhenType.END_OF_COMBAT:
			Events.battle_over_screen_requested.emit('Victorious!', BattleOverPanel.Type.WIN)

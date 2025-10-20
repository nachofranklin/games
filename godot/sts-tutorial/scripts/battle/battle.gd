extends Node2D

@export var char_stats: CharacterStats

@onready var battle_ui: BattleUI = $BattleUI as BattleUI
@onready var player_handler: PlayerHandler = $PlayerHandler as PlayerHandler
@onready var enemy_handler: EnemyHandler = $EnemyHandler as EnemyHandler
@onready var player: Player = $Player as Player


func _ready() -> void:
	# temporary code as normally we'd want to keep our stats from the run rather than start from the base every battle
	var new_stats: CharacterStats = char_stats.create_instance()
	battle_ui.char_stats = new_stats
	player.stats = new_stats
	
	Events.player_turn_ended.connect(player_handler.end_turn)
	Events.player_hand_discarded.connect(enemy_handler.start_turn)
	Events.enemy_turn_ended.connect(_on_enemy_turn_ended)
	
	start_battle(new_stats)


func start_battle(stats: CharacterStats):
	player_handler.start_battle(stats)


func _on_enemy_turn_ended():
	player_handler.start_turn()
	enemy_handler.reset_enemy_actions()

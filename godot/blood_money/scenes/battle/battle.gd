extends Node2D

@export var char_stats: CharacterStats

@onready var player_handler: PlayerHandler = $PlayerHandler
@onready var battle_ui: BattleUI = $BattleUI
@onready var hand_h_box: Hand = $BattleUI/HandHBox
@onready var end_turn_button: Button = $BattleUI/EndTurnButton
@onready var player: Player = $Player

var turn_number: int = 0


func _ready() -> void:
	Events.player_turn_ended.connect(_on_player_turn_ended)
	Events.player_hand_discarded.connect(_on_player_hand_discarded)
	
	# temp code as the char_stats should remain consistent throughout
	var new_stats: CharacterStats = char_stats.create_instance()
	battle_ui.char_stats = new_stats
	player.stats = new_stats
	
	_start_battle(new_stats)


func _start_battle(player_stats: CharacterStats) -> void:
	turn_number = 0
	# clear any children currently in hand h box
	if hand_h_box.get_children().size() == 0:
		print('empty hand on battle start')
	else:
		print('not empty hand on battle start!!!')
	# do an enemy_handler.start_battle func
	player_handler.start_battle(player_stats)
	# initialise win/loss conditions
	_start_players_turn()


func _start_players_turn() -> void:
	turn_number += 1
	player_handler.start_turn()
	# make the cards and the end turn button be available - this happens through the player_hand_drawn signal


func _on_player_turn_ended() -> void:
	# i haven't done anything for cards that might exhaust if left in the hand at the end of the turn uplayed (can't remember the sts name for this)
	player_handler.end_turn()
	# enemy turn starts after the player_hand_discarded signal has finished


func _on_player_hand_discarded() -> void:
	# this should be the last thing that happens when the player ends their turn
	# so this should start the enemies turn
	# but for now i'll restart the players turn
	player_handler.start_turn()

extends Resource
class_name RunStats

signal gold_changed

const STARTING_GOLD: int = 70
const BASE_CARD_REWARDS: int = 3
const BASE_COMMON_WEIGHT: float = 6.0
const BASE_UNCOMMON_WEIGHT: float = 3.7
const BASE_RARE_WEIGHT: float = 0.3

@export var gold: int = STARTING_GOLD : set = set_gold
@export var card_rewards: int = BASE_CARD_REWARDS
@export_range(0.0, 10.0) var common_weight := BASE_COMMON_WEIGHT
@export_range(0.0, 10.0) var uncommon_weight := BASE_UNCOMMON_WEIGHT
@export_range(0.0, 10.0) var rare_weight := BASE_RARE_WEIGHT


func set_gold(new_amount: int):
	gold = new_amount
	gold_changed.emit()


func reset_weights():
	common_weight = BASE_COMMON_WEIGHT
	uncommon_weight = BASE_UNCOMMON_WEIGHT
	rare_weight = BASE_RARE_WEIGHT

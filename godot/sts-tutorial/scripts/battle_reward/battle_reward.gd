extends Control
class_name BattleReward

const REWARD_BUTTON := preload('res://scenes/ui/buttons/reward_button.tscn')
const CARD_REWARDS := preload('res://scenes/ui/card_rewards.tscn')
const GOLD_ICON := preload("res://art/gold.png")
const GOLD_TEXT := '%s gold'
const CARD_ICON := preload("res://art/rarity.png")
const CARD_TEXT := 'Add a card'

@export var run_stats: RunStats
@export var character_stats: CharacterStats

@onready var rewards: VBoxContainer = %Rewards

var card_reward_total_weight: float = 0.0
var card_rarity_weights: Dictionary = {
	Card.Rarity.COMMON: 0.0,
	Card.Rarity.UNCOMMON: 0.0,
	Card.Rarity.RARE: 0.0
}


func _ready() -> void:
	for node: Node in rewards.get_children():
		node.queue_free()


func add_gold_reward(amount: int):
	var gold_reward: RewardButton = REWARD_BUTTON.instantiate() as RewardButton
	gold_reward.reward_icon = GOLD_ICON
	gold_reward.reward_text = GOLD_TEXT % amount
	gold_reward.pressed.connect(_on_gold_reward_taken.bind(amount))
	rewards.add_child.call_deferred(gold_reward)


func add_card_reward():
	var card_reward:= REWARD_BUTTON.instantiate() as RewardButton
	card_reward.reward_icon = CARD_ICON
	card_reward.reward_text = CARD_TEXT
	card_reward.pressed.connect(_show_card_rewards)
	rewards.add_child.call_deferred(card_reward)


func _show_card_rewards():
	if not run_stats or not character_stats:
		return
	
	var card_rewards := CARD_REWARDS.instantiate() as CardRewards
	add_child(card_rewards) # this adds a child to the BattleReward scene, essentially pasting the newly instantiated card rewards scene over the battle reward scene
	card_rewards.card_reward_selected.connect(_on_card_reward_taken)
	
	var card_reward_array: Array[Card] = [] # this will eventually be the three cards we can choose from
	var available_cards: Array[Card] = character_stats.draftable_cards.cards.duplicate(true) # not sure why (true) at the end?
	
	for i in run_stats.card_rewards: # by default this is set to return 3 card rewards
		_setup_card_chances()
		var roll: float = randf_range(0.0, card_reward_total_weight)
		
		for rarity: Card.Rarity in card_rarity_weights:
			if card_rarity_weights[rarity] > roll:
				var picked_card := _get_random_available_card(available_cards, rarity)
				card_reward_array.append(picked_card)
				available_cards.erase(picked_card)
				_modify_weights(rarity) # if no rare card then the next card becomes more likely to be a rare card, or if it is a rare card then reset the weight back to base for rare cards
				break
	
	card_rewards.rewards = card_reward_array
	card_rewards.show()


func _setup_card_chances():
	card_reward_total_weight = run_stats.common_weight + run_stats.uncommon_weight + run_stats.rare_weight
	card_rarity_weights[Card.Rarity.COMMON] = run_stats.common_weight
	card_rarity_weights[Card.Rarity.UNCOMMON] = run_stats.common_weight + run_stats.uncommon_weight
	card_rarity_weights[Card.Rarity.RARE] = run_stats.common_weight + run_stats.uncommon_weight + run_stats.rare_weight


func _modify_weights(rarity_rolled: Card.Rarity):
	if rarity_rolled == Card.Rarity.RARE:
		run_stats.rare_weight = RunStats.BASE_RARE_WEIGHT
	else:
		run_stats.rare_weight = clampf(run_stats.rare_weight + 0.3, run_stats.BASE_RARE_WEIGHT, 5.0)


func _get_random_available_card(available_cards: Array[Card], with_rarity: Card.Rarity) -> Card:
	var all_possible_cards := available_cards.filter( # filter takes an array (available cards) and returns an array back of all the things in the array that returned true, so we pass the below function
		func(card: Card):
			return card.rarity == with_rarity
	)
	return all_possible_cards.pick_random()


func _on_gold_reward_taken(amount: int):
	if not run_stats:
		return
	
	run_stats.gold += amount


func _on_card_reward_taken(card: Card):
	if not character_stats or not card:
		return
	
	character_stats.deck.add_card(card)


func _on_back_button_pressed() -> void:
	Events.battle_reward_exited.emit()

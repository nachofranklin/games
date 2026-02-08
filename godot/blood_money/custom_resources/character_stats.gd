extends Stats
class_name CharacterStats

@export var name: String
@export var primary_colour: Color
@export var base_cards_per_turn: int
@export var base_mana_per_turn: int
@export var starting_deck: CardPile

var deck: CardPile
var hand: CardPile # should this be a CardPile?
var draw_pile: CardPile
var discard_pile: CardPile
var exhaust_pile: CardPile
#var relics: Array[Relic]
#var potions: Array[Potion]
var cards_per_turn: int : set = set_cards_per_turn
var mana: int : set = set_mana


func set_cards_per_turn(value: int) -> void:
	cards_per_turn = value
	stats_changed.emit()


func set_mana(value: int) -> void:
	mana = value
	stats_changed.emit()


func reset_cards_per_turn() -> void:
	cards_per_turn = base_cards_per_turn


func reset_mana() -> void:
	mana = base_mana_per_turn


func can_play_card(card: Card) -> bool:
	return mana >= card.energy_cost


func create_instance() -> CharacterStats:
	var instance: CharacterStats = self.duplicate()
	instance.health = max_health
	instance.block = base_block
	instance.reset_cards_per_turn()
	instance.reset_mana()
	instance.deck = starting_deck
	instance.draw_pile = CardPile.new()
	instance.discard_pile = CardPile.new()
	instance.exhaust_pile = CardPile.new()
	return instance

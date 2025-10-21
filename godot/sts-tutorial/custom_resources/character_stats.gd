class_name CharacterStats
extends Stats

@export var starting_deck: CardPile
@export var cards_per_turn: int
@export var max_mana: int

var mana: int : set = set_mana
var deck: CardPile
var discard: CardPile
var draw_pile: CardPile
#var exhaust_pile: CardPile # not included in tutorial :(

func set_mana(value: int):
	mana = value
	stats_changed.emit()

func reset_mana():
	self.mana = max_mana

func can_play_card(card: Card) -> bool:
	return mana >= card.energy_cost

func create_instance() -> Resource:
	var instance: CharacterStats = self.duplicate()
	instance.health = max_health
	instance.block = 0
	instance.reset_mana()
	instance.deck = instance.starting_deck.duplicate()
	instance.draw_pile = CardPile.new()
	instance.discard = CardPile.new()
	#instance.exhaust_pile = CardPile.new()
	return instance


func take_damage(damage: int):
	var initial_health := health
	super.take_damage(damage) # super means to call a function from the script we extend from (Stats). Seems a bit complicated for me
	if initial_health > health:
		Events.player_hit.emit()

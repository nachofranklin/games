extends Node

# Card-related events
@warning_ignore('UNUSED_SIGNAL')
signal card_drag_started(card_ui: CardUI)
@warning_ignore('UNUSED_SIGNAL')
signal card_drag_ended(card_ui: CardUI)
@warning_ignore('UNUSED_SIGNAL')
signal card_aim_started(card_ui: CardUI)
@warning_ignore('UNUSED_SIGNAL')
signal card_aim_ended(card_ui: CardUI)
@warning_ignore('UNUSED_SIGNAL')
signal card_played(card: Card)

# Player-related events
@warning_ignore('UNUSED_SIGNAL')
signal player_hand_drawn
@warning_ignore('UNUSED_SIGNAL')
signal player_hand_discarded
@warning_ignore('UNUSED_SIGNAL')
signal player_turn_ended

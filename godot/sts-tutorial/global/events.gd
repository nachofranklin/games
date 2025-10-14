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
@warning_ignore('UNUSED_SIGNAL')
signal card_tooltip_requested(card: Card)
@warning_ignore('UNUSED_SIGNAL')
signal tooltip_hide_requested

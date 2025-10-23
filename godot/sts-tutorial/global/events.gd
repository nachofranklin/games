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

# Player-related events
@warning_ignore('UNUSED_SIGNAL')
signal player_hand_drawn
@warning_ignore('UNUSED_SIGNAL')
signal player_turn_ended
@warning_ignore('UNUSED_SIGNAL')
signal player_hand_discarded
@warning_ignore('UNUSED_SIGNAL')
signal player_hit
@warning_ignore('UNUSED_SIGNAL')
signal player_died

# Enemy-related events
@warning_ignore('UNUSED_SIGNAL')
signal enemy_action_completed(enemy: Enemy)
@warning_ignore('UNUSED_SIGNAL')
signal enemy_turn_ended # this is for when all enemies have done their turn

# Battle-related events
@warning_ignore('UNUSED_SIGNAL')
signal battle_over_screen_requested(text: String, type: BattleOverPanel.Type)
@warning_ignore('UNUSED_SIGNAL')
signal battle_won

# Map-related events
@warning_ignore('UNUSED_SIGNAL')
signal map_exited

# Shop-related events
@warning_ignore('UNUSED_SIGNAL')
signal shop_exited

# Campfire-related events
@warning_ignore('UNUSED_SIGNAL')
signal campfire_exited

# Battle Reward-related events
@warning_ignore('UNUSED_SIGNAL')
signal battle_reward_exited

# Treasure Room-related events
@warning_ignore('UNUSED_SIGNAL')
signal treasure_room_exited

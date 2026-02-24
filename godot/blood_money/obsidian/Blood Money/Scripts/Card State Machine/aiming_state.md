---
Extends: CardState
Class Name:
---
#### What it needs to do

- clear the CardDropArea from the card_ui.targets
- create an offset var so that the card can go to the centre of the hand (don't get caught out by the card having been scaled up as this can fuck up the offset)
- animate_to_position the card_ui so that it tweens it nicely to the middle from wherever it was dragged to
- set the card_ui.card_area.monitoring to false (is this because it was just being used to look for the card drop area? I can't quite remember)
- emit the card_aim_started signal primarily to start the card_target_selector where targets will be added/removed to card_ui.targets when the mouse hovers over/exits them
- on exit emit the card_aim_ended signal
- on_input if right mouse clicked then change the state to the [[base_state]]
- move the card back into the hand into the position it was in before - emit reparent_requested
- if left mouse clicked then get_viewport().set_input_as_handled() (tbh idk what this does? need to look into it) and change the state to the [[released_state]]

#### How to do it

- 
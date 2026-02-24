---
Extends: CardState
Class Name:
---
#### What it needs to do

- reparent itself to the ui layer so that it's no longer part of the hand_h_box
- set an offset var = card_ui.global_position - card_ui.get_global_mouse_position() so that when you start dragging the card it doesn't immediately snap the card so that the top left of the card (0, 0) is where the mouse pointer is, but rather wherever you clicked the card is the point it gets dragged around by
- emit the card_drag_started signal
- on exit emit the card_drag_ended signal
- when checking for an on_input event create new variables
	- single_targeted: bool
	- mouse_motion: bool (is InputEventMouseMotion)
	- cancel: bool (is_action_pressed('right_mouse'))
	- confirm: bool (is_action_pressed('left_mouse'))
	- in_card_drop_area: bool (card_ui.targets.size() > 0)
- if mouse_motion then card_ui.global_position = card_ui.get_global_mouse_position() + offset
- if mouse_motion and single_targeted and in_card_drp_area then change the state to [[aiming_state]]
- if cancel then change the state to [[base_state]]
- move the card back into the hand into the position it was in before - emit reparent_requested
- if confirm then change the state to [[released_state]]

#### How to do it

- 
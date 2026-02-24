---
Extends: CardState
Class Name:
---
#### What it needs to do

- make the scale bigger
- to do that without the card going off screen change the pivot_offset_ratio to (0.5, 1) so that it scales up from the bottom middle of the card (do this before scaling)
- for on_gui_input we first check if the card is not playable or if it's disabled in which case we return from the func doing nothing
- elif there's a left mouse click then change state to the [[clicked_state]]
- if the mouse exits the card then change the state back to the [[base_state]]

#### How to do it

- 
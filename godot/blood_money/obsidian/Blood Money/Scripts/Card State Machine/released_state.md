---
Extends: CardState
Class Name:
---
#### What it needs to do

- create a played var
- if the card_ui.targets isn't empty (either has a CardDropArea or enemy) then set played to true
- play the card
- if there's any input and played is true then return as don't need to do anything else
- else change the state to the [[base_state]]
- move the card back into the hand into the position it was in before - emit reparent_requested

#### How to do it

- 
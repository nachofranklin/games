---

kanban-plugin: board

---

## Bugs

- [ ] manaCS doesn't seem to be registering as an area on the card
- [ ] players mana starts at 0


## Backlog

- [ ] fan the hand in the battle scene
- [ ] need to come up with a way to remember the card order to move it back to that position
- [ ] need to make it so that you can click and hold and drag/aim and release or click, drag/aim and click again to release
- [ ] so will probably need to introduce some kind of delay so that it doesn't try to do both incorrectly immediately
- [ ] set the card_target_selector gradient to the players primary colour
- [ ] make it so that if i can't play a card it changes visually
- [ ] need to add something in to check if the card is playable due to mana and playable for non mana reasons (eg if one card is currently selected, all other cards should be unavailable, or if a card is unplayable due to being an unplayable curse/status or perhaps the enemy has put a lock on cards)
- [ ] then need to enforce not being able to play those cards if i can't play them


## Active



## Done

**Complete**
- [x] work on updating the card visuals to reflect the card resource
- [x] then make the cards actually do some damage or add block
- [x] make the card desc correct
- [x] do art needed for cardVisuals scene
- [x] the card in the aiming state is not centering correctly
- [x] add a short desc and tooltip desc to card resource
- [x] make the card visuals reflect the card resource
- [x] add a pointer and an indicator next to enemies for att card selecting targets
- [x] finish the cardtargetselecter (watch tutorial)
- [x] create a card resource
- [x] connect reparent_requested to a hand script which tells the card to go in to the hand
- [x] when cancelling dragging state it goes to base but doesn't snap back to the hand
- [x] not sure what the areas need for monitoring/monitorable
- [x] should only release if it's in the card drop area otherwise go to base
- [x] learn and understand how to create finite state machines
- [x] hovered needs smaller scale and to offset to the centre
- [x] create a card state machine
- [x] do a cardUI scene
- [x] change the viewport to 720p or half that if possible
- [x] find a pixel font that rasterises at less than 8
- [x] failing that find a non pixel font
- [x] learn more on themes
- [x] make a start on building the battle scene for it
- [x] get art for each thing needed in [[Battle]]
- [x] create/find some art
- [x] fill in the plan
- [x] add an alternative names note
- [x] find out how to do 2d art (program)
- [x] check out the apps i screenshotted
- [x] get an icon for the game (money dripping in blood?)




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false]}
```
%%
#### Prerequisites

- [[CardPile]]
- [[CardVisuals]]

#### What should happen

- [ ] show the individual cards from the correct card pile
- [ ] be able to click on the cards for more info

#### What the scene needs

- [ ] back button
- [x] a way to scroll through cards in case there's a lot - scroll container (clips content)
- [x] a background
- [x] a title
- [x] grid container to house the cards
- [ ] card tooltip to be loaded in but not visible by default
- [ ] would be good to be able to sort the pile by various things

#### What images are needed

- [ ] none unless i want to do something fancy with the background

#### Notes

- Because scroll container clips the content i've added another margin container to provide some free space for cards to scale up when hovered without getting immediately cropped out, but if they scale up too much then they'll still get cropped!
- should create a new card ui specifically for these card pile views as the cards don't need all the states or the area - but i guess they do need hover so they can expand plus still need to be able to click on them so either modify the current state machines to do something different if the cardpileview scene is visible or create a different cardui scene that will get used in these cardpileview scenes
- would like to increase the size of the scroll bar but i think i need to do that in code, doesn't seem to be an option in the inspector
- maybe do something a bit fancier with the background in future as its a bit boring atm
- also currently the grid container columns and h/v separation values are hardcoded but might make more sense for them to be created by code (if cards or containers change size then the whole thing will break basically)
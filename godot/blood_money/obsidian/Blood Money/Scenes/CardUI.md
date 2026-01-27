#### Prerequisites

- CardVisuals
- Know what card it should be

#### What should happen

- [ ] fully functioning card state machine
- [ ] it should take the card details and pass it onto CardVisuals

#### What the scene needs

- [x] card area
	- [x] collision shape
- [x] [[CardVisuals]]
- [ ] state machine

#### What images are needed

- [ ] n/a
Optionals
- [ ] n/a

#### Card State Machine

- Base
	- idle, not hovered
- Hovered
	- hovered
- Clicked
	- clicked, but not moving
- Dragging
	- clicked and moving but not if an att card and over a certain y-level
- Aiming
	- clicked and moving and att card and over a certain y-level
- Released
	- no longer clicked (or a second click to release depending on if the user held click while dragging or clicked, immediately released, and then dragged)
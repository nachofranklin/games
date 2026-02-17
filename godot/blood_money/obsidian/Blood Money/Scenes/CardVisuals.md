#### Prerequisites

- It needs to know what card it will be

#### What should happen

- [x] It should show a picture of the card
- [x] name
- [x] energy cost
- [x] basic description
- [ ] when clicked on it should show a full description in a tooltip
- [ ] show what type of card it is
- [x] show the card rarity
- [x] would also like the status effects / key words (like attack, block) to be colour coordinated automatically
- [x] show if it exhausts

#### What the scene needs

- [ ] card visuals
	- [x] icon
	- [x] name of card
	- [x] basic description
		- [x] have key words colour coordinated
	- [x] rarity indicator
	- [x] type indicator (att, skill, power, curse, status)
	- [x] energy cost
		- [ ] perhaps turns red if can't afford?
	- [x] if it exhausts or not
	- [x] background
		- [x] possibly different colours based on character availability / shop specific / special / curse / status

#### What images are needed

- [ ] images for cards
Optionals
- [ ] 

#### Ways to differentiate indicators

- shape
	- sts has icons be different shaped to indicate type
	- could have different shaped cards
	- different shaped borders
	- could have different background texture on the card
- colour
	- sts has the border around the icon change colour to indicate rarity
	- sts has the card background colour be different to indicate character/shop/curse/status
	- change the text colour for energy cost if can't afford it
- ~~placement?~~
	- ~~like for an att card the text could go below the image, but for a power card it goes above. Don't love that though~~
- symbols/images
	- have an image to indicate att, skill, power, etc
- animation?
	- maybe the energy cost image swirls behind the number when it can be played but stops or does something different if it can't?
- text
	- text i already want to colour coordinate key words, so don't want to use text colour to differentiate indicators
	- could simply write 'attack', 'skill', etc at the top?

Will likely copy what sts does with cards having an energy section in the top left, different shaped icons for type, different coloured borders around the icon for rarity. Name above the icon and short description below, exhausts below that.

#### Need to do

- [ ] get better shapes for IconPanelContainer
- [ ] instead of being in a vbox make the icon and the text slightly overlap
- [ ] add a swirling animation for the energy cost
- [ ] if card selected/hovered maybe make the shadow_size bigger?
- [ ] find a better background for the card name than just a panel
- [ ] add a tiny panel at the bottom of the IconPanelContainer to write the card type
- [ ] still need to write the code for it all
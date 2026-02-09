---
Extends: Control
Class Name: CardVisuals
---
#### What it needs to do

- Change the BackgroundPanelContainer (bg_color and border_color) and EnergyBackground colours to be the characters primary colour (if it's one of their cards, if it's a shop card it can be a different colour or if it's a curse/status then different colour) - this probably doesn't work as if you think of prismatic shard (where you can get any characters cards) the card would need to know each characters colour, not just the current characters colour. So, maybe the character: colour dict could be stored in card resource?
- Change the IconPanelContainer panel container style based on the Card.card_type
- Change the IconPanelContainer border_color based on the Card.rarity
- Set the icon = Card.art
- CardDescription = Card.short_description
- set the ExhaustsLabel.visible = Card.exhausts
- CardNameLabel = Card.card_name
- EnergyLabel = Card.energy_cost

#### How to do it

- It needs access to the Card resource for all the card details
- It has a card_colour dictionary which is not linked to [[character_stats]] primary_colour - so if the colour changes in [[character_stats]] then change here too!
- Also has a rarity colour dictionary
- Works by duplicating the StyleBoxFlat that is currently being used, editing that and then overriding it
- For the bg colour - if Card.CardType == status or curse then do their colours, if Card.shop_card == true then do shop card colour, then do if Card.AvailableTo == any character do their colour. Needs to be in that order
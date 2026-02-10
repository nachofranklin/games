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
- For the iconPC and the icon i had to do some tweaking. Main thing was in iconPC it needs a bg color (not transparent) with draw_center = true, then in visibility, clip_children = clip + draw. This means the icon texture is limited to the border you've created. But this creates an issue of the border only getting drawn around the perimeter of a square (fine with a square border, not fine with any other shape), so it gives a patchy border basically. Solution was to remove the border (set border_width = 0) then duplicate the iconPC but this time draw a border. Bonus is that whatever border_width gets set (3) set the expand_margin to the same (3) then it offsets it and feels less box-y. Plan to do this in code so that i don't create loads of styleboxflats. Finally need to change the y order of name and energy to +1 (didn't do this because it created more problems and cba, so icon border now sits over the name).
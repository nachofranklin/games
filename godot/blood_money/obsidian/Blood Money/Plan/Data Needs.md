What data does a system need to exist? Or what data should a component show? (Custom Resources)

##### A card needs:
- name
- energy cost
- effect
- rarity indicator
- type indicator (att, skill, power, curse)
- image
- tooltip text
- sound
- target (one, all, random, player)
- exhausts (bool)
- if it's a starter card or should be available for rewards/shops (can't think of any other scenario as curse and status cards don't qualify as either)

##### Player needs:
- name
- max hp (aka soul?)
- health (aka lifeforce?)
- starting deck
- starting relic
- potions
- modifiers
- deck
- discard pile
- draw pile
- exhaust pile
- relics
- statuses
- block
- energy
- energy per turn
- cards drawn per turn
- image
- draftable cards (list of available cards for rewards/shops) (should this be on the card instead?)
- base number of cards drawn for rewards
- number of cards drawn for rewards
- base card rarity weights
- current card rarity weights (if not got a gold card it makes it more likely to get one next time)

##### An enemy needs:
- name
- max hp
- health
- energy
- modifiers
- block
- statuses
- ai (move selector)
- resistances
- weaknesses

##### A relic needs:
- name
- when it activates
- what characters can have the relic
- if it's a starter relic (bool)
- image
- tooltip

##### An effect needs:
- a list of targets it applies to
- what the effect is (block, damage, etc)
##### A status needs:
- name
- when it activates
- if it stacks, is duration based or is just an effect (meaning playing the same thing again wouldn't do anything and it doesn't deteriorate)
- if it can expire (bool)
- the duration
- the stacks
- image
- tooltip
- tooltip text colour

##### A room needs:
- type of room (monster, treasure, campfire, shop, boss, event)
- row
- column
- position
- a list of next possible rooms
- if it was selected or not (bool)
- if it's a battle it'll need to know info on the battle

##### Loading the game needs:
- if it's a new run or a continued run
- who the player character is

##### To save the game it'll need:
- rng seed (will probably need multiple of these for specific systems)
- rng state
- the players data
- if in a battle, the enemies data
- map data
- last room
- floors climbed
- if you were on the map (bool)

##### The possible groups of enemies you could fight needs:
- the tier of the fight (eg tier 0 could be the first floor, tier 1 could be every other non boss fight in act 1, tier 2 could be all mini boss fights in act 1, tier 3 would be the main boss in act 1, etc)
- the weight of how more or less rare the opponent would be
- health reward min
- health reward max
- enemies (as a PackedScene)
- the accumulated weight

##### Card pile needs:
- list of cards
- access to the card AI

##### Intents need:
- icon
- text
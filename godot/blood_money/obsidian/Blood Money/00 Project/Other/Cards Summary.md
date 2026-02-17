```dataview
TABLE
	available_to AS char,
	rarity,
	card_type AS type,
	target,
	energy_cost AS energy,
	exhausts,
	effect
FROM "Cards"
SORT
	available_to ASC,
	rarity ASC,
	energy_cost ASC
```

(can do things like...

WHERE available_to = "Warrior"
SORT energy_cost ASC

or just copy paste it into excel to sort and filter)
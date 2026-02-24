#### Signals to emit

- card_played(card)

#### Functions needed

- play(targets, char_stats)
	- Events.card_played.emit(self)
	- char_stats.mana -= energy_cost
	- apply_effects(_get_targets(targets))

- apply_effects(_targets)
	- pass - when creating unique cards they will each have to overwrite this func, see [[card]]

- _get_targets(targets: Array[Node]) -> Array[Node]
	- using Card.Target to tell who the target(s) should be (self, single_enemy, all_enemies, everyone)
		- if self: return tree.get_nodes_in_group('player') (I've made groups for players and enemies)
		- if single_enemy, it should return the already targeted enemy (see [[Targeting]] for how that works)
		- if all_enemies or everyone, do the same as self but for enemies and player + enemies
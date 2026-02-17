---
Extends: RefCounted
Class Name: Effect
---
#### What it needs to do

- have an execute function that all the different effects will have to use
- the execute function just needs a list of targets to be passed to it

#### How to do it

- func execute(_targets: Array[Node]) -> void:
	- pass
- then all effect scripts will overwrite this func with whatever that effect is, eg BlockEffect...
	- func execute(targets: Array[Node]) -> void:
		- for target in targets:
			- if not target:
				- continue
			- elif target is Enemy or target is Player: (groups created for player and enemies)
				- target.stats.block += amount
- Then a card script will overwrite apply_effects by doing something like...
	- func apply_effects(targets: Array[Node]) -> void:
		- var block_effect := BlockEffect.new()
		- block_effect.amount = block (an export var to be set in the inspector)
		- block_effect.execute(targets)

#### Note

Resource stores the values in memory but for the effects there's no reason to store those values as they just get used the once and then can be deleted which is why RefCounted is preferred. (I don't fully understand the differences here, but i'll go off of a recommendation)
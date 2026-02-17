---
Extends: Effect
Class Name: DamageEffect
---
#### What it needs to do

- export var amount
- overwrite execute func from [[effect]]

#### How to do it

- for target in targets:
	- if not target:
		- continue
	- elif target is Enemy or target is Player: (groups created for player and enemies)
		- target.take_damage(amount)
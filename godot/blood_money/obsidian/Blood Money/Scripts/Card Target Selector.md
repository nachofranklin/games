---
Extends: Node2D
Class Name: n/a
---

#### What it needs to do

- When a card is selected which is an attack card that targets a single enemy of your choice, the card should be in the aiming state, have snapped/tweened to the centre and now a visual indicator should appear between the top middle of the card and wherever the mouse is pointing to.
- This should be curved
- Starts thin, gets gradually thicker, then goes thin at the end (slightly like an elongated arrow) - this is done in Line2d width curve
- Also when an enemy is being hovered over then a little arrow indicator should appear pointing to that enemy (but that might be better done elsewhere as i guess that should happen even if the attack card targets all enemies, or everyone including the player)
- connect to the card_aim_started and card_aim_ended signals

#### How to do it

- The scene needs a parent node2d, an area and collision shape for the current mouse pos and a line2d with the thickness and thickness variation
- area needs to be able to collide with the enemy layer
- by default it shouldn't be monitoring or monitorable but that can be turned on and off in the code
- size of the collision shape, small, basically give the mouse a bit of a larger hitbox so it can be just off but not too big that it could pick up multiple targets
- set the area2d position to the mouse pos - get_local_mouse_position()
- we'll need to give the line2d points, which we'll need to work out every time the mouse moves
- on card aim starting (/ ending) it needs to set a targeting variable to true, make area2d monitoring/able true, set a current card var to the CardUI attached to the signals. On ending the same in rev but also clear the points in the line2d and set the area2d pos back to zero
- connect to the area entered/exited signals and append/erase the area from current card target areas
- using an ease out cubic curve it should look like...
	- for i in range(ARC_POINTS):
		var t := float(i) / float(ARC_POINTS - 1) # 0 -> 1
		var eased_t := 1.0 - pow(1.0 - t, 3) # ease-out cubic
		
		var x := start.x + distance.x * t
		var y := start.y + distance.y * eased_t
		
		points.append(Vector2(x, y))

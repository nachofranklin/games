extends ItemContainer

#func hit():
	## (when hit) hide the lid and get a random spawn position, then send a signal
	#if opened == false:
		#$LidSprite.hide()
		#for i in range(3):
			#var pos = $SpawnPositions.get_child(randi() % $SpawnPositions.get_child_count()).global_position
			#open.emit(pos, current_direction)
		#opened = true

extends PieceResource


func get_raw_moves(board_state: Array, grid_pos: Vector2i) -> Array[Vector2i]:
	var moves: Array[Vector2i] = []
	
	for dir in directions:
		var new_pos = grid_pos + dir
		if not _is_in_bounds(new_pos, board_state):
			continue
		
		var occupier: Piece = board_state[new_pos.y][new_pos.x]
		if occupier == null:
			moves.append(new_pos)
		elif _is_enemy(occupier):
			moves.append(new_pos)
			continue
		else:
			continue
	
	return moves

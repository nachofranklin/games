extends PieceResource

var attack_directions: Array[Vector2i] = [Vector2i(1, 0), Vector2i(-1, 0)] # add the y direction from the @export var directions as white/black will be different


func get_raw_moves(board_state: Array, grid_pos: Vector2i) -> Array[Vector2i]:
	var moves: Array[Vector2i] = []
	
	for dir in directions: # should be just one for pawns
		
		# normal moving up 1
		var new_pos = grid_pos + dir
		if not _is_in_bounds(new_pos, board_state):
			continue
		
		var occupier: Piece = board_state[new_pos.y][new_pos.x]
		if occupier == null:
			moves.append(new_pos)
			
			# including the starting +2 squares move (this way it has already checked there's nothing one space in front of it)
			if has_never_moved:
				var two_forward = grid_pos + dir * 2
				if _is_in_bounds(two_forward, board_state): # shouldn't be needed but as board size could be custom and dumb i'll keep this in
					var two_forward_occupier = board_state[two_forward.y][two_forward.x]
					if two_forward_occupier == null:
						moves.append(two_forward)
		
		#elif _is_enemy(occupier): # this part doesn't apply as pawns can't take by moving up 1
			#moves.append(new_pos)
			#continue
		#else:
			#continue
		
		# taking pieces diagonally (not including en passant)
		for att_dir in attack_directions:
			var att_pos = grid_pos + dir + att_dir
			if _is_in_bounds(att_pos, board_state):
				var att_pos_occupier = board_state[att_pos.y][att_pos.x]
				if att_pos_occupier != null and _is_enemy(att_pos_occupier):
					moves.append(att_pos)
	
	return moves

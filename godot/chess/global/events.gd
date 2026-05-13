extends Node

# Chess board-related events
@warning_ignore('UNUSED_SIGNAL')
signal tile_clicked(grid_pos: Vector2i)

# Game state-related events
@warning_ignore('UNUSED_SIGNAL')
signal piece_taken(piece: Piece)

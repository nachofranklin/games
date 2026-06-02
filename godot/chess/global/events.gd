extends Node

# Chess board-related events
@warning_ignore('UNUSED_SIGNAL')
signal tile_clicked(grid_pos: Vector2i)

# Game state-related events
@warning_ignore('UNUSED_SIGNAL')
signal piece_taken(piece: Piece)
@warning_ignore('UNUSED_SIGNAL')
signal turn_ended()
@warning_ignore('UNUSED_SIGNAL')
signal turn_started(player: PlayerResource)

# Pawn promotion-related events
@warning_ignore('UNUSED_SIGNAL')
signal pawn_promotion_selection(piece: Piece)
@warning_ignore('UNUSED_SIGNAL')
signal pawn_promoted(pawn: Piece, new_piece: Resource)

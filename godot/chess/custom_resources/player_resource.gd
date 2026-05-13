extends Resource
class_name PlayerResource

enum PlayerType {HUMAN, CPU}

@export var player_name: String
@export var player_type: PlayerType
@export var piece_colour: PieceResource.PieceColour

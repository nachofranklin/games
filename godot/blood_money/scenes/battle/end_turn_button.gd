extends Button


func _ready() -> void:
	Events.player_hand_drawn.connect(_on_player_hand_drawn)


func _on_player_hand_drawn():
	disabled = false


func _on_pressed() -> void:
	disabled = true
	Events.player_turn_ended.emit()

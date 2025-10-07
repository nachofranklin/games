extends LevelParent

func _on_entrace_gate_area_body_entered(_body: Node2D) -> void:
	var tween = create_tween()
	tween.tween_property($Player, "player_speed", 0, 0.5)
	TransitionLayer.change_scene("res://scenes/levels/outside.tscn")

func _on_exit_gate_area_body_entered(_body: Node2D) -> void:
	var tween = create_tween()
	tween.tween_property($Player, "player_speed", 0, 0.5)

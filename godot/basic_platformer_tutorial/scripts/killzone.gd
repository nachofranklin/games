extends Area2D

@onready var timer: Timer = $Timer

# when entering the killzone the timer starts
func _on_body_entered(body: Node2D) -> void:
	print('You Died!')
	Engine.time_scale = 0.5 # slows down time
	body.get_node('CollisionShape2D').queue_free()
	timer.start()

# when the timer ends the game restarts
func _on_timer_timeout() -> void:
	Engine.time_scale = 1 # puts it back to normal speed
	get_tree().reload_current_scene()

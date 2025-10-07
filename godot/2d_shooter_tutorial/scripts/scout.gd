extends CharacterBody2D

var player_nearby: bool = false
var can_laser: bool = true
var right_gun_use = true
var health: int = 30
var invulnerable: bool = false

signal laser(pos, direction)

func _process(_delta: float) -> void:
	if player_nearby:
		look_at(Globals.player_pos)
		if can_laser:
			var laser_marker = $LaserSpawnPositions.get_child(right_gun_use)
			# alternates between left and right gun (marker2d and marker2d2)
			right_gun_use = not right_gun_use
			var pos: Vector2 = laser_marker.global_position
			var direction: Vector2 = (Globals.player_pos - position).normalized()
			laser.emit(pos, direction)
			can_laser = false
			$Timers/LaserCooldown.start()

func _on_attack_area_body_entered(_body: Node2D) -> void:
	player_nearby = true

func _on_attack_area_body_exited(_body: Node2D) -> void:
	player_nearby = false

func _on_laser_cooldown_timeout() -> void:
	can_laser = true

func _on_invulnerable_timer_timeout() -> void:
	invulnerable = false
	$Sprite2D.material.set_shader_parameter('progress', 0)

func hit():
	if invulnerable == false:
		health -= 10
		invulnerable = true
		$Timers/InvulnerableTimer.start()
		$Sprite2D.material.set_shader_parameter('progress', 1)
		$AudioStreamPlayer2D.play()
	if health <= 0:
		queue_free()

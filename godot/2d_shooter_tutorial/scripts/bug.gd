extends CharacterBody2D

var in_sight_range: bool = false
var in_attack_range: bool = false
var can_attack: bool = true
var health: int = 20
var vulnerable: bool = true
var speed: int = 300

func _physics_process(_delta: float) -> void:
	if can_attack:
		if in_attack_range:
			try_attack()
		elif in_sight_range and in_attack_range == false:
			chase_player()
		else:
			idle()

func chase_player():
	look_at(Globals.player_pos)
	$AnimatedSprite2D.play("walk")
	var direction: Vector2 = (Globals.player_pos - position).normalized()
	velocity = direction * speed
	move_and_slide()

func try_attack():
	can_attack = false
	$AnimatedSprite2D.play("attack")
	#$Timers/AttackCooldown.start() # aaa1

func idle():
	$AnimatedSprite2D.stop()
	velocity = Vector2.ZERO
	move_and_slide()

func hit():
	if vulnerable:
		health -= 10
		vulnerable = false
		$Timers/InvulnerableTimer.start()
		$AnimatedSprite2D.material.set_shader_parameter('progress', 1)
		$Particles/HitParticles.emitting = true
		$AudioStreamPlayer2D.play()
	if health <= 0:
		await get_tree().create_timer($Particles/HitParticles.lifetime).timeout
		queue_free()

func _on_notice_area_body_entered(_body: Node2D) -> void:
	in_sight_range = true

func _on_notice_area_body_exited(_body: Node2D) -> void:
	in_sight_range = false

func _on_attack_area_body_entered(_body: Node2D) -> void:
	in_attack_range = true

func _on_attack_area_body_exited(_body: Node2D) -> void:
	in_attack_range = false

#func _on_attack_cooldown_timeout() -> void: # aaa1
	#can_attack = true # aaa1

func _on_invulnerable_timer_timeout() -> void:
	vulnerable = true
	$AnimatedSprite2D.material.set_shader_parameter('progress', 0)

func _on_animated_sprite_2d_animation_finished() -> void:
	# i think this only applies to attack not walk as walk loops so never finishes
	if in_attack_range:
		Globals.health_amount -= 10
	can_attack = true # aaa2 if i want to add a small delay after a bite then comment this out and uncomment the attack cooldown

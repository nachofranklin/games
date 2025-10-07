extends CharacterBody2D

var drone_speed: int = 0
var max_speed: int = 500
var speed_multiplier: int = 1
var active: bool = false
var health: int = 50
var vulnerable: bool = true
var explosion_active: bool = false
var explosion_radius: int = 350

func _ready() -> void:
	$Explosion.hide()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float):
	if active:
		look_at(Globals.player_pos)
		var direction: Vector2 = (Globals.player_pos - position).normalized()
		velocity = direction * drone_speed * speed_multiplier
		var collision = move_and_collide(velocity * _delta)
		if collision:
			explodes()
	
	if explosion_active:
		var targets = get_tree().get_nodes_in_group('Container') + get_tree().get_nodes_in_group('Entity')
		for target in targets:
			var in_range = target.global_position.distance_to(global_position) < explosion_radius
			if 'hit' in target and in_range:
				target.hit()

func hit():
	if vulnerable:
		health -= 10
		vulnerable = false
		$Timers/InvulnerableTimer.start()
		$DroneImage.material.set_shader_parameter('progress', 1)
		$Node2D/HitSound.play()
	if health <= 0:
		explodes()

func explodes():
	speed_multiplier = 0
	explosion_active = true
	$AnimationPlayer.play('explosion') # should probably get rid of the collision shape at the beginning too so that the player can walk through it if it's been killed

func _on_notice_area_body_entered(_body: Node2D) -> void:
	active = true
	var tween = create_tween()
	tween.tween_property(self, 'drone_speed', max_speed, 6)

func _on_invulnerable_timer_timeout() -> void:
	vulnerable = true
	$DroneImage.material.set_shader_parameter('progress', 0)

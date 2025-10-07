extends CharacterBody2D

var active: bool = false
var in_attack_range: bool = false
var speed: int = 200
var vulnerable: bool = true
var health: int = 100

func _ready() -> void:
	$NavigationAgent2D.path_desired_distance = 4.0
	$NavigationAgent2D.target_desired_distance = 4.0
	$NavigationAgent2D.target_position = Globals.player_pos

func _physics_process(_delta: float) -> void:
	if active:
		var next_path_pos: Vector2 = $NavigationAgent2D.get_next_path_position()
		var direction: Vector2 = (next_path_pos - global_position).normalized()
		rotation = direction.angle() + deg_to_rad(90) # instead of look_at(Globals.player_pos) as hunter faces up instead of to the right
		velocity = direction * speed
		move_and_slide()
	if active and not in_attack_range:
		$AnimationPlayer.play('walk')

func attack():
	if in_attack_range:
		Globals.health_amount -= 20

func hit():
	if vulnerable:
		vulnerable = false
		health -= 10
		$Timers/InvulnerableTimer.start()
	if health <= 0:
		queue_free()

func _on_notice_area_body_entered(_body: Node2D) -> void:
	active = true

func _on_notice_area_body_exited(_body: Node2D) -> void:
	active = false

func _on_attack_area_body_entered(_body: Node2D) -> void:
	in_attack_range = true
	$AnimationPlayer.play('attack')

func _on_attack_area_body_exited(_body: Node2D) -> void:
	in_attack_range = false

func _on_navigation_timer_timeout() -> void:
	if active:
		$NavigationAgent2D.target_position = Globals.player_pos

func _on_invulnerable_timer_timeout() -> void:
	vulnerable = true

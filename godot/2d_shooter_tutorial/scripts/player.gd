extends CharacterBody2D

# signals
signal shoot_laser(pos, direction)
signal shoot_grenade(pos, direction)

# variables
@export var player_speed: int = 500
var can_laser: bool = true
var can_grenade: bool = true
@onready var laser_timer: Timer = $LaserTimer
@onready var grenade_timer: Timer = $GrenadeTimer
var vulnerable: bool = true

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float):
	# input
	var direction: Vector2 = Input.get_vector("left", "right", "up", "down")
	velocity = direction * player_speed
	move_and_slide()
	Globals.player_pos = global_position
	
	# rotate
	look_at(get_global_mouse_position())
	
	# laser shooting input
	if Input.is_action_just_pressed("primary action") and can_laser and Globals.laser_amount > 0:
		Globals.laser_amount -= 1
		# create particles when fired
		$GPUParticles2D.emitting = true
		can_laser = false
		laser_timer.start()
		# randomly select a marker2d for the laser start
		var laser_markers = $LaserStartPositions.get_children()
		var selected_laser_pos = laser_markers[randi() % laser_markers.size()].global_position
		var laser_direction: Vector2 = (get_global_mouse_position() - position).normalized()
		# emit the position we selected
		shoot_laser.emit(selected_laser_pos, laser_direction)
	
	# grenade shooting input
	if Input.is_action_just_pressed("secondary action") and can_grenade and Globals.grenade_amount > 0:
		Globals.grenade_amount -= 1
		can_grenade = false
		grenade_timer.start()
		# randomly select a marker2d for the grenade start
		var grenade_markers = $LaserStartPositions.get_children()
		var selected_grenade_pos = grenade_markers[randi() % grenade_markers.size()].global_position
		var grenade_direction = (get_global_mouse_position() - position).normalized()
		# emit the position we selected
		shoot_grenade.emit(selected_grenade_pos, grenade_direction)

func _on_laser_timer_timeout():
	can_laser = true

func _on_grenade_timer_timeout():
	can_grenade = true

func _on_vulnerable_timer_timeout() -> void:
	vulnerable = true

func hit():
	if vulnerable:
		Globals.health_amount -= 10 # this somehow means if i get hit by an enemy firing a laser (or an explosion?)
		vulnerable = false
		$VulnerableTimer.start()

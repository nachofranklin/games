extends PathFollow2D

var in_range: bool = false
var car_speed: float = 0.03

@onready var line1: Line2D = $Turret/RayCast2D/Line2D
@onready var line2: Line2D = $Turret/RayCast2D2/Line2D

func _ready() -> void:
	line2.add_point($Turret/RayCast2D2.target_position)

func _process(delta: float) -> void:
	progress_ratio += car_speed * delta
	if in_range:
		$Turret.look_at(Globals.player_pos)

func fire():
	Globals.health_amount -= 20

func _on_notice_area_body_entered(_body: Node2D) -> void:
	in_range = true
	$AnimationPlayer.play('laser_load')

func _on_notice_area_body_exited(_body: Node2D) -> void:
	in_range = false
	# if player moves away in time, the lasers will fade to width 0
	$AnimationPlayer.pause()
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(line1, 'width', 0, randf_range(0.2, 0.5))
	tween.tween_property(line2, 'width', 0, randf_range(0.2, 0.5))
	await tween.finished
	$AnimationPlayer.stop()

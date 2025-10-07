extends Area2D

var rotation_speed: int = 3
var available_options = ['laser', 'grenade', 'health']
var type = available_options[randi() % len(available_options)]
var direction: Vector2
var distance:int = randi_range(150, 250) # would probably make more sense if it was based off the size of the container

func _ready():
	if type == 'laser':
		$Sprite2D.modulate = Color(0,0,1)
	elif type == 'grenade':
		$Sprite2D.modulate = Color(1,0,0)
	elif type == 'health':
		$Sprite2D.modulate = Color(0,1,0)
	
	# tween - moves the items in the direction the object is facing and increases the size
	var target_pos = position + direction * distance
	var tween = create_tween()
	tween.set_parallel(true)
	tween.tween_property(self, 'position', target_pos, 0.5)
	tween.tween_property(self, 'scale', Vector2(1,1), 0.4).from(Vector2(0,0))

func _process(delta):
	rotation += rotation_speed * delta

func _on_body_entered(_body: Node2D) -> void:
	if type == 'laser':
		Globals.laser_amount += 10
	elif type == 'grenade':
		Globals.grenade_amount += 2
	elif type == 'health':
		Globals.health_amount += 10
	$AudioStreamPlayer2D.play()
	$Sprite2D.hide()
	await $AudioStreamPlayer2D.finished
	queue_free()

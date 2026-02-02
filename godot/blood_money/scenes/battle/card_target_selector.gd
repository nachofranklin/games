extends Node2D

const ARC_POINTS: int = 16

@onready var mouse_pointer_area_2d: Area2D = $MousePointerArea2D
@onready var line_2d: Line2D = $Line2D

var current_card: CardUI
var targeting: bool = false


func _ready() -> void:
	Events.card_aim_started.connect(_on_card_aim_started)
	Events.card_aim_ended.connect(_on_card_aim_ended)


func _process(_delta: float) -> void:
	if not targeting:
		return
	
	mouse_pointer_area_2d.position = get_local_mouse_position()
	line_2d.points = _get_points()


func _get_points() -> Array[Vector2]:
	var points: Array[Vector2] = []
	var start: Vector2 = current_card.global_position
	start.x += current_card.size.x / 2
	var end: Vector2 = get_local_mouse_position()
	var distance: Vector2 = end - start
	
	for i in range(ARC_POINTS):
		var t := float(i) / float(ARC_POINTS - 1) # 0 -> 1
		var eased_t := 1.0 - pow(1.0 - t, 3) # ease-out cubic
		
		var x := start.x + distance.x * t
		var y := start.y + distance.y * eased_t
		
		points.append(Vector2(x, y))
	
	return points


func _on_card_aim_started(card_ui: CardUI) -> void:
	current_card = card_ui
	targeting = true
	mouse_pointer_area_2d.monitoring = true
	#mouse_pointer_area_2d.monitorable = true # do i need this?


func _on_card_aim_ended(_card_ui: CardUI) -> void:
	current_card = null
	targeting = false
	mouse_pointer_area_2d.monitoring = false
	#mouse_pointer_area_2d.monitorable = false # do i need this?
	line_2d.clear_points()
	mouse_pointer_area_2d.position = Vector2.ZERO


func _on_mouse_pointer_area_2d_area_entered(area: Area2D) -> void:
	if not current_card or not targeting:
		return
	
	if not current_card.target_areas.has(area):
		current_card.target_areas.append(area)
		line_2d.gradient.colors = [Color(0,1,1,0.3), Color(0,1,1,1)]


func _on_mouse_pointer_area_2d_area_exited(area: Area2D) -> void:
	if not current_card or not targeting:
		return
	
	if current_card.target_areas.has(area):
		current_card.target_areas.erase(area)
		line_2d.gradient.colors = [Color(0,1,1,0.3), Color.WHITE]


# when the players get a custom resource with a primary colour i can set the colours to that

extends CanvasLayer

@onready var laser_label: Label = $AmmoCounter/GridContainer/LaserCount
@onready var grenade_label: Label = $AmmoCounter/GridContainer/GrenadeCount
@onready var laser_icon: TextureRect = $AmmoCounter/GridContainer/LaserImg
@onready var grenade_icon: TextureRect = $AmmoCounter/GridContainer/GrenadeImg
@onready var health_bar: TextureProgressBar = $MarginContainer/TextureProgressBar

# colours
var green: Color = Color(0,1,0,1)
var red: Color = Color(1,0,0,1)

func _ready() -> void:
	Globals.laser_amount_change.connect(update_laser_text)
	Globals.grenade_amount_change.connect(update_grenade_text)
	Globals.health_change.connect(update_health_text)
	update_laser_text()
	update_grenade_text()
	update_health_text()

func update_laser_text():
	laser_label.text = str(Globals.laser_amount)
	update_colour(Globals.laser_amount, laser_label, laser_icon)
	
func update_grenade_text():
	grenade_label.text = str(Globals.grenade_amount)
	update_colour(Globals.grenade_amount, grenade_label, grenade_icon)
	
func update_health_text():
	health_bar.value = Globals.health_amount
	
func update_colour(amount: int, label: Label, icon: TextureRect):
	if amount > 0:
		label.modulate = green
		icon.modulate = green
	elif amount == 0:
		label.modulate = red
		icon.modulate = red

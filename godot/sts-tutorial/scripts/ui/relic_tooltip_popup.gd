extends Control
class_name RelicTooltipPopup

@onready var relic_icon: TextureRect = %RelicIcon
@onready var relic_description: RichTextLabel = %RelicDescription
@onready var back_button: Button = %BackButton


func _ready() -> void:
	back_button.pressed.connect(hide)
	hide()


func show_tooltip(relic: Relic):
	relic_icon.texture = relic.icon
	relic_description.text = relic.get_tooltip()
	show()


func _input(event: InputEvent) -> void:
	if event.is_action_pressed('ui_cancel') and visible:
		hide()


func _on_gui_input(event: InputEvent) -> void:
	if event.is_action_pressed('left_mouse'):
		hide()

class_name Tooltip
extends PanelContainer

@export var fade_seconds: float = 0.3

@onready var tooltip_icon: TextureRect = %TooltipIcon
@onready var tooltip_text_label: RichTextLabel = %TooltipText

var tween: Tween
var ttip_is_visible: bool = false

func _ready() -> void:
	Events.card_tooltip_requested.connect(show_tooltip)
	Events.tooltip_hide_requested.connect(hide_tooltip)
	modulate = Color.TRANSPARENT
	hide()

func show_tooltip(icon: Texture, text: String):
	ttip_is_visible = true
	if tween:
		tween.kill()
	
	tooltip_icon.texture = icon
	tooltip_text_label.text = text
	tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
	tween.tween_callback(show)
	tween.tween_property(self, 'modulate', Color.WHITE, fade_seconds)

func hide_tooltip():
	ttip_is_visible = false
	if tween:
		tween.kill()
	
	get_tree().create_timer(fade_seconds, false).timeout.connect(hide_animation) # when moving between cards quickly it kept doing the tween making it a bit flashy, this timer stops that

func hide_animation():
	if not ttip_is_visible:
		tween = create_tween().set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
		tween.tween_property(self, 'modulate', Color.TRANSPARENT, fade_seconds)
		tween.tween_callback(hide)

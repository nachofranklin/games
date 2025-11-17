extends Status
class_name VulnerableStatus

const MODIFIER: float = 0.5


func get_tooltip() -> String:
	return tooltip % duration


func initialise_status(target: Node):
	# sets a variable for the existing dmg taken modifier under player/enemy -> ModifierHandler -> DamageTakenModifier
	var dmg_taken_modifier: Modifier = target.modifier_handler.get_modifier(Modifier.Type.DMG_TAKEN)
	# sets a variable for the vulnerable modifier value under DamageTakenModifier (will either already exist or will return null)
	var vulnerable_modifier_value: ModifierValue = dmg_taken_modifier.get_value('vulnerable')
	
	# if there's no existing vulnerable, create a new one
	if not vulnerable_modifier_value:
		vulnerable_modifier_value = ModifierValue.create_new_modifier('vulnerable', ModifierValue.Type.PERCENT_BASED)
		vulnerable_modifier_value.percent_value = MODIFIER
		dmg_taken_modifier.add_new_value(vulnerable_modifier_value) # adds it as a child here
	
	if not status_changed.is_connected(_on_status_changed):
		status_changed.connect(_on_status_changed.bind(dmg_taken_modifier))


func _on_status_changed(dmg_taken_modifier: Modifier):
	if duration <= 0 and dmg_taken_modifier:
		dmg_taken_modifier.remove_value('vulnerable')

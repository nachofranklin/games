extends Status
class_name StrengthStatus


func initialise_status(target: Node):
	status_changed.connect(_on_status_changed.bind(target))
	_on_status_changed(target)


func _on_status_changed(target: Node):
	assert(target.get('modifier_handler'), 'No modifiers on %s' % target)
	
	# sets a variable for the existing dmg dealt modifier under player/enemy -> ModifierHandler -> DamageDealtModifier
	var dmg_dealt_modifier: Modifier = target.modifier_handler.get_modifier(Modifier.Type.DMG_DEALT)
	assert(dmg_dealt_modifier, 'No dmg dealt modifier on %s' % target)
	
	# sets a variable for the strength modifier value under DamageDealtModifier (will either already exist or will return null)
	var strength_modifier_value: ModifierValue = dmg_dealt_modifier.get_value('strength')
	
	if not strength_modifier_value: # if there's not already a strength modifier value, create a new one with zero values for percent and flat value
		strength_modifier_value = ModifierValue.create_new_modifier('strength', ModifierValue.Type.FLAT)
	
	# set the flat value (amount of strength) to whatever it currently is (see player/enemy -> StatusHandler -> find the control node for strength)
	strength_modifier_value.flat_value = stacks
	# if no current strength modifier child then add it as a child, or if existing strength modifier then update the values to the new values
	dmg_dealt_modifier.add_new_value(strength_modifier_value)

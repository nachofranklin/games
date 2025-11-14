extends Node
class_name Modifier

enum Type {DMG_DEALT, DMG_TAKEN, CARD_COST, SHOP_COST, NO_MODIFIER}

@export var type: Type


func get_value(source: String) -> ModifierValue:
	# either return an existing modifier value or return null
	for value: ModifierValue in get_children():
		if value.source == source:
			return value
	
	return null


func add_new_value(value: ModifierValue):
	var existing_modifier_value := get_value(value.source)
	if not existing_modifier_value:
		add_child(value)
	else:
		existing_modifier_value.flat_value = value.flat_value
		existing_modifier_value.percent_value = value.percent_value


func remove_value(source: String):
	for value: ModifierValue in get_children():
		if value.source == source:
			value.queue_free()


func clear_values():
	for value: ModifierValue in get_children():
		value.queue_free()


func get_modified_value(base: int) -> int:
	var flat_result: int = base
	var percent_result: float = 1.0
	
	# apply flat modifiers first
	for value: ModifierValue in get_children():
		if value.type == ModifierValue.Type.FLAT:
			flat_result += value.flat_value
	
	# apply % modifiers after
	for value: ModifierValue in get_children():
		if value.type == ModifierValue.Type.PERCENT_BASED:
			percent_result += value.percent_value
	
	return floori(flat_result * percent_result)

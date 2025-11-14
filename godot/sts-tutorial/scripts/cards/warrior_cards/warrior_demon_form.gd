extends Card

const DEMON_FORM_STATUS = preload('res://statuses/demon_form.tres')


func apply_effects(targets: Array[Node], _modifiers: ModifierHandler) -> void:
	var status_effect := StatusEffect.new()
	var demon_form := DEMON_FORM_STATUS.duplicate()
	status_effect.status = demon_form
	status_effect.execute(targets)

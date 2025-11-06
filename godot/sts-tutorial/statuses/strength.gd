extends Status
class_name StrengthStatus


func initialise_status(_target: Node):
	status_changed.connect(_on_status_changed)
	_on_status_changed()


func _on_status_changed():
	print('Strength status: +%s damage' % stacks)


#func apply_status(target: Node):
	#print('My status targets %s' % target)
	#print('It does %s something' % member_var)
	#
	#status_applied.emit(self)

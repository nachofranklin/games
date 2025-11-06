# meta-name: Status
# meta-description: Create a Status which can be applied to a target.
extends Status
class_name XYZ

var member_var: int = 0


func initialise_status(target: Node):
	print('Initialise my status for target %s' % target)


func apply_status(target: Node):
	print('My status targets %s' % target)
	print('It does %s something' % member_var)
	
	status_applied.emit(self)

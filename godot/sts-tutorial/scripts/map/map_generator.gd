extends Node
class_name MapGenerator

const X_DIST: int = 30
const Y_DIST: int = 25
const PLACEMENT_RANDOMNESS: int = 5
const FLOORS: int = 15
const MAP_COLUMNS: int = 7
const PATHS: int = 6
const MONSTER_ROOM_WEIGHT: float = 10.0
const SHOP_ROOM_WEIGHT: float = 2.5
const CAMPFIRE_ROOM_WEIGHT: float = 4.0

var random_room_type_weights: Dictionary = {
	Room.Type.MONSTER: 0.0,
	Room.Type.CAMPFIRE: 0.0,
	Room.Type.SHOP: 0.0
}
var random_room_type_total_weight: float = 0.0
var map_data: Array[Array]


func generate_map() -> Array[Array]:
	map_data = _generate_initial_grid()
	var starting_points := _get_random_starting_points()
	
	for j in starting_points:
		var current_j := j
		for i in FLOORS - 1:
			current_j = _setup_connection(i, current_j)
	
	_setup_boss_room()
	_setup_random_room_weights()
	_setup_room_types()
	
	return map_data


func _generate_initial_grid() -> Array[Array]:
	var result: Array[Array] = []
	
	for i in FLOORS:
		var adjacent_rooms: Array[Room] = []
		
		for j in MAP_COLUMNS:
			var current_room := Room.new()
			var offset := Vector2(randf(), randf()) * PLACEMENT_RANDOMNESS
			current_room.position = Vector2(j * X_DIST, i * -Y_DIST) + offset
			current_room.row = i
			current_room.column = j
			current_room.next_rooms = []
			
			if i == FLOORS - 1: # boss room
				current_room.position.y = (i + 1) * -Y_DIST # +1 gives it double spacing to normal room on y-axis
			
			adjacent_rooms.append(current_room)
		
		result.append(adjacent_rooms)
	
	return result


func _get_random_starting_points() -> Array[int]:
	var start_points: Array[int]
	var unique_points: int = 0
	
	while unique_points < 2:
		unique_points = 0
		start_points = []
		
		for i in PATHS:
			var starting_point := randi_range(0, MAP_COLUMNS - 1)
			if not start_points.has(starting_point):
				unique_points += 1
			
			start_points.append(starting_point)
	
	return start_points


func _setup_connection(i: int, j: int) -> int:
	var next_room: Room = null
	var current_room := map_data[i][j] as Room
	
	while not next_room or _would_cross_existing_path(i, j, next_room): # while the next room is null or the current candidate is crossing paths, get new values
		var random_j := clampi(randi_range(j - 1, j + 1), 0, MAP_COLUMNS - 1) # i think this would mean that if you're on the edge you'd have a 2/3 chance of staying on the edge and a 1/3 chance moving in. Is that a problem?
		next_room = map_data[i + 1][random_j]
	
	current_room.next_rooms.append(next_room)
	
	return next_room.column


func _would_cross_existing_path(row: int, col: int, next_room: Room) -> bool: # row and col are for the existing pos, next_room.row and .column are for the next floor's pos
	var left_neighbour: Room
	var right_neighbour: Room
	
	# if j == 0, there's no left neighbour
	if col > 0:
		left_neighbour = map_data[row][col - 1]
	# if j == MAP_COLUMNS - 1, there's no right neighbour
	if col < MAP_COLUMNS - 1:
		right_neighbour = map_data[row][col + 1]
	
	# can't cross in right dir if right neighbour goes to the left
	if right_neighbour and next_room.column > col: # saying if we have a right neighbour and our next room is going to the right
		for neighbour_next_room: Room in right_neighbour.next_rooms:
			if neighbour_next_room.column < next_room.column: # meaning our paths have crossed
				return true
	
	# can't cross in left dir if left neighbour goes to the right
	if left_neighbour and next_room.column < col:
		for neighbour_next_room: Room in left_neighbour.next_rooms:
			if neighbour_next_room.column > next_room.column:
				return true
	
	return false


func _setup_boss_room():
	var middle: int = floori(MAP_COLUMNS * 0.5)
	var boss_room: Room = map_data[FLOORS - 1][middle] as Room
	boss_room.type = Room.Type.BOSS
	
	for j in MAP_COLUMNS:
		var current_room = map_data[FLOORS - 2][j] as Room
		if current_room.next_rooms:
			current_room.next_rooms = [] as Array[Room]
			current_room.next_rooms.append(boss_room)


func _setup_random_room_weights():
	random_room_type_weights[Room.Type.MONSTER] = MONSTER_ROOM_WEIGHT
	random_room_type_weights[Room.Type.CAMPFIRE] = MONSTER_ROOM_WEIGHT + CAMPFIRE_ROOM_WEIGHT
	random_room_type_weights[Room.Type.SHOP] = MONSTER_ROOM_WEIGHT + CAMPFIRE_ROOM_WEIGHT + SHOP_ROOM_WEIGHT
	
	random_room_type_total_weight = random_room_type_weights[Room.Type.SHOP] # change to whatever the last room weight is
	
	
func _setup_room_types():
	# first floor is always a battle
	for room: Room in map_data[0]:
		if room.next_rooms.size() > 0:
			room.type = Room.Type.MONSTER
	
	# middle floor is always a trasure
	for room: Room in map_data[floori(FLOORS * 0.5)]:
		if room.next_rooms.size() > 0:
			room.type = Room.Type.TREASURE
	
	# second last floor is always a campfire (last is a boss)
	for room: Room in map_data[FLOORS - 2]:
		if room.next_rooms.size() > 0:
			room.type = Room.Type.CAMPFIRE
	
	# rest of rooms
	for current_floor in map_data:
		for room: Room in current_floor:
			for next_room: Room in room.next_rooms:
				if next_room.type == Room.Type.NOT_ASSIGNED:
					_set_room_randomly(next_room)


func _set_room_randomly(room_to_set: Room):
	var campfire_below_4: bool = true
	var consecutive_campfire: bool = true
	var consecutive_shop: bool = true
	var campfire_on_third_last_floor: bool = true
	
	var type_candidate: Room.Type
	
	while campfire_below_4 or consecutive_campfire or consecutive_shop or campfire_on_third_last_floor:
		type_candidate = _get_random_room_type_by_weight()
		
		var is_campfire: bool = type_candidate == Room.Type.CAMPFIRE
		var has_campfire_on_previous_floor_path: bool = _room_has_parent_of_type(room_to_set, Room.Type.CAMPFIRE)
		var is_shop: bool = type_candidate == Room.Type.SHOP
		var has_shop_on_previous_floor_path: bool = _room_has_parent_of_type(room_to_set, Room.Type.SHOP)
		
		campfire_below_4 = is_campfire and room_to_set.row < 3
		consecutive_campfire = is_campfire and has_campfire_on_previous_floor_path
		consecutive_shop = is_shop and has_shop_on_previous_floor_path
		campfire_on_third_last_floor = is_campfire and room_to_set.row == FLOORS - 3
	
	room_to_set.type = type_candidate


func _room_has_parent_of_type(room: Room, type: Room.Type) -> bool:
	"""
	gets the types of all of the previous floors rooms which has a path to the 
	new `room` and returns True if any of them match the specified `type` given
	"""
	
	var parents: Array[Room] = []
	
	# could and should have simplified the three ifs into just one, oh well
	# left parent
	if room.column > 0 and room.row > 0: # can't have a lower floor parent to the left if on left-most col or if on the first row
		var parent_candidate: Room = map_data[room.row - 1][room.column - 1] as Room # get the room 1 floor down and 1 to the left
		if parent_candidate.next_rooms.has(room): # if that room paths to the room parameter given then append
			parents.append(parent_candidate)
	# parent below
	if room.row > 0:
		var parent_candidate: Room = map_data[room.row - 1][room.column] as Room
		if parent_candidate.next_rooms.has(room):
			parents.append(parent_candidate)
	# right parent
	if room.column < MAP_COLUMNS - 1 and room.row > 0:
		var parent_candidate: Room = map_data[room.row - 1][room.column + 1] as Room
		if parent_candidate.next_rooms.has(room):
			parents.append(parent_candidate)
	
	for parent: Room in parents:
		if parent.type == type:
			return true
	
	return false


func _get_random_room_type_by_weight() -> Room.Type:
	var roll: float = randf_range(0.0, random_room_type_total_weight)
	
	for type: Room.Type in random_room_type_weights:
		if random_room_type_weights[type] > roll:
			return type
	
	print('set the room as a monster as the random weights failed')
	return Room.Type.MONSTER # this shouldn't be needed

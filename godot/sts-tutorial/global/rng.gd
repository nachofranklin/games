extends Node

var instance: RandomNumberGenerator


func _ready() -> void:
	initialise()


func initialise():
	instance = RandomNumberGenerator.new()
	instance.randomize()


func set_from_save_data(which_seed: int, state: int):
	instance = RandomNumberGenerator.new()
	instance.seed = which_seed
	instance.state = state


func array_pick_random(array: Array) -> Variant:
	return array[instance.randi() % array.size()]


func array_shuffle(array: Array):
	if array.size() < 2: # if array has one or less items you can't shuffle it so don't bother
		return
	
	# GPT Summary: Each loop picks a random element from indices 0..i and swaps it into position i, locking that position and shrinking the remaining pool by one
	for i in range(array.size()-1, 0, -1): # eg array of 10 items, 0 - 9, for i in 9 down to 1 (it skips 0 because the last value remaining will automatically be the last one and therefore already in place)
		var j := instance.randi() % (i + 1) # j = a number 0 - 9, then 0 - 8, etc
		var tmp = array[j] # tmp = whatever the value of the jth index of the original array is. So if it was an array of colours, tmp would be a colour
		array[j] = array[i] # in the original array we now replace that colour value with whatever the last item of the array was
		array[i] = tmp # then we replace the last value of the list to be the randomly selected value
		# then it loops through doing it again but now ignoring the last value (which it's already randomised and removed from the available array of one less)

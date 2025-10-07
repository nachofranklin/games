extends Node

var total_coins = 0

@onready var total_coins_label: Label = $TotalCoinsLabel

func add_coin():
	total_coins += 1
	total_coins_label.text = 'You collected ' + str(total_coins) + ' coins'

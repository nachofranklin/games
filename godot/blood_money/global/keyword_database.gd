extends Node

var KEYWORDS: Dictionary = {'damage': {'colour': Color.DARK_RED, 'tooltip': 'Reduces health unless it can be blocked.'}, 'block': {'colour': Color.DODGER_BLUE, 'tooltip': 'Negates damage. Lose all block at the start of your next turn.'}}


func format_keywords(text: String) -> String:
	for keyword in KEYWORDS.keys():
		var colour: Color = KEYWORDS[keyword]['colour']
		var colour_hex = colour.to_html()
		
		text = text.replace(keyword, '[color=#%s]%s[/color]' % [colour_hex, keyword])
		
	return text

extends Control
class_name CardVisuals

@onready var background_panel_container: PanelContainer = %BackgroundPanelContainer
@onready var icon_panel_container: PanelContainer = %IconPanelContainer
@onready var icon: TextureRect = %Icon
@onready var card_description: RichTextLabel = %CardDescription
@onready var exhausts_label: Label = %ExhaustsLabel
@onready var card_name_label: Label = %CardNameLabel
@onready var energy_background: Panel = %EnergyBackground
@onready var energy_label: Label = %EnergyLabel

var cards_theme: Theme = preload('res://art/theme/cards_theme.tres')
var card_colour: Dictionary = {'CURSE': Color.BLACK, 'STATUS': Color.DIM_GRAY, 'SHOP': Color.WHITE, 'NACHO': Color.DEEP_SKY_BLUE} # add more characters here
var rarity_colour: Dictionary = {'COMMON': Color.GRAY, 'UNCOMMON': Color.LIGHT_SKY_BLUE, 'RARE': Color.GOLD}


func update_visuals(card: Card) -> void:
	_update_styleboxes(card)
	icon.texture = card.art
	card_description.text = KeywordDatabase.format_keywords(card.short_description) # still need to get the number amount of whatever the card does so that it's not just text that would need to be manually changed
	exhausts_label.visible = card.exhausts
	card_name_label.text = card.card_name.to_upper()
	energy_label.text = str(card.energy_cost)


func _update_styleboxes(card: Card) -> void:
	var background_colour: Color
	
	# duplicate the StyleBoxFlat used
	var bg_pc_sb: StyleBoxFlat = background_panel_container.get_theme_stylebox('panel').duplicate()
	var mana_p_sb: StyleBoxFlat = energy_background.get_theme_stylebox('panel').duplicate()
	var icon_pc_sb: StyleBoxFlat
	
	match card.card_type: # if curse or status then keep the skill one?
		Card.CardType.ATTACK:
			icon_pc_sb = cards_theme.get_stylebox('att_pc', 'PanelContainer').duplicate()
		Card.CardType.SKILL:
			icon_pc_sb = cards_theme.get_stylebox('skill_pc', 'PanelContainer').duplicate()
		Card.CardType.POWER:
			icon_pc_sb = cards_theme.get_stylebox('power_pc', 'PanelContainer').duplicate()
		Card.CardType.CURSE:
			icon_pc_sb = cards_theme.get_stylebox('skill_pc', 'PanelContainer').duplicate()
		Card.CardType.STATUS:
			icon_pc_sb = cards_theme.get_stylebox('skill_pc', 'PanelContainer').duplicate()
	
	# edit the StyleBoxFlat
	if card.card_type == Card.CardType.CURSE:
		background_colour = card_colour['CURSE']
	elif card.card_type == Card.CardType.STATUS:
		background_colour = card_colour['STATUS']
	elif card.shop_card:
		background_colour = card_colour['SHOP']
	else:
		match card.available_to:
			Card.AvailableTo.NACHO:
				background_colour = card_colour['NACHO']
			# add more characters here
	
	bg_pc_sb.bg_color = background_colour
	bg_pc_sb.border_color = background_colour
	mana_p_sb.bg_color = background_colour
	
	match card.rarity:
		Card.Rarity.COMMON:
			icon_pc_sb.border_color = rarity_colour['COMMON']
		Card.Rarity.UNCOMMON:
			icon_pc_sb.border_color = rarity_colour['UNCOMMON']
		Card.Rarity.RARE:
			icon_pc_sb.border_color = rarity_colour['RARE']
	
	# use that StyleBoxFlat
	background_panel_container.add_theme_stylebox_override('panel', bg_pc_sb)
	energy_background.add_theme_stylebox_override('panel', mana_p_sb)
	icon_panel_container.add_theme_stylebox_override('panel', icon_pc_sb)

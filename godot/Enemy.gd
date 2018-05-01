extends Node2D


func _ready():
	var width = ProjectSettings.get_setting("display/window/size/width")
	var height = ProjectSettings.get_setting("display/window/size/height")
	position.x = rand_range(0, width)
	position.y = rand_range(0, height)

	# add loop component child node
	add_child(load("res://LoopComponent.gd").new())
	
	add_to_group("enemies")

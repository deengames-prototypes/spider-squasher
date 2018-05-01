extends Node

func _physics_process(delta):
	var parent = get_parent()
	var new_vector = Vector2(parent.position.x, parent.position.y)
	
	var screen_width = ProjectSettings.get_setting("display/window/size/width")
	var screen_height = ProjectSettings.get_setting("display/window/size/height")
	
	if new_vector.x > screen_width:
		new_vector.x -= screen_width
	elif new_vector.x < 0:
		new_vector.x += screen_width
	
	
	if new_vector.y > screen_height:
		new_vector.y -= screen_height
	elif new_vector.y < 0:
		new_vector.y += screen_height
	
	parent.position = new_vector

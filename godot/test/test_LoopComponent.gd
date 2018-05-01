extends "res://addons/gut/test.gd"

var LoopComponent = load("res://LoopComponent.gd")

var height = ProjectSettings.get_setting("display/window/size/height")
var width = ProjectSettings.get_setting("display/window/size/width")
var position = Vector2()


func test_physics_process_loops_object_over_map():
	var test_table = [
		[0, 0],
		[width, height],
		[width + 50, height + 50],
		[-50, -50]
	]
	
	for pos in test_table:
		var lp = LoopComponent.new()
		add_child(lp)
		position.x = pos[0]
		position.y = pos[1]
		
		lp._physics_process(0.1)
		
		assert_between(position.x, 0, width)
		assert_between(position.y, 0, height)
	
	

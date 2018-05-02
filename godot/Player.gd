extends KinematicBody2D

export (int) var movement_speed = 300

var linear_velocity = Vector2()


func _ready():
	# place player in the middle of the screen
	position.x = ProjectSettings.get_setting("display/window/size/width") / 2
	position.y = ProjectSettings.get_setting("display/window/size/height") / 2
	
	# add loop component child node
	add_child(load("res://LoopComponent.gd").new())


func _physics_process(delta):
	var target_speed = Vector2()
	
	if Input.is_action_pressed("move_left"):
		target_speed.x -= movement_speed
	if Input.is_action_pressed("move_right"):
		target_speed.x += movement_speed
	if Input.is_action_pressed("move_up"):
		target_speed.y -= movement_speed
	if Input.is_action_pressed("move_down"):
		target_speed.y += movement_speed
	
	linear_velocity.x = lerp(linear_velocity.x, target_speed.x, 0.1)
	linear_velocity.y = lerp(linear_velocity.y, target_speed.y, 0.1)

	collide(move_and_collide(linear_velocity * delta))


func collide(info):
	if info == null:
		return
	if info.collider.is_in_group("enemies"):
		get_tree().quit()
		queue_free()

extends KinematicBody2D

export (float) var movement_speed = 150
export (float) var min_distance_from_player = 300
var player

signal killed_player


func _ready():
	var width = ProjectSettings.get_setting("display/window/size/width")
	var height = ProjectSettings.get_setting("display/window/size/height")
	var player_ref = player.get_ref()
	position.x = player_ref.position.x
	position.y = player_ref.position.y
	while position.distance_to(player_ref.position) < 200:
		position.x = rand_range(0, width)
		position.y = rand_range(0, height)

	# add loop component child node
	add_child(load("res://LoopComponent.gd").new())
	
	add_to_group("enemies")

func _process(delta):
	if player.get_ref():
		var player_ref = player.get_ref()
		var direction = position.angle_to_point(player_ref.position)
		var collision_info = move_and_collide(Vector2(-movement_speed, 0).rotated(direction) * delta)
		
		if collision_info != null:
			if collision_info.collider == player_ref:
				emit_signal('killed_player')

func init(plyr):
	player = weakref(plyr)

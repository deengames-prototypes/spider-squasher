extends KinematicBody2D

export (float) var movement_speed = 150
var player

signal killed_player
signal killed_enemy


func _ready():
	var width = ProjectSettings.get_setting("display/window/size/width")
	var height = ProjectSettings.get_setting("display/window/size/height")
	
	add_to_group("enemies")

func _process(delta):
	if player.get_ref():
		var player_ref = player.get_ref()
		var direction = position.angle_to_point(player_ref.position)
		var collision_info = move_and_collide(Vector2(-movement_speed, 0).rotated(direction) * delta)
		
		if collision_info != null:
			if collision_info.collider == player_ref:
				emit_signal('killed_player')
				
func set_position(x, y):
	position.x = x
	position.y = y
	
func damage(i):
	queue_free()
	emit_signal("killed_enemy")

func init(plyr):
	player = weakref(plyr)

extends KinematicBody2D

export (float) var max_scale = 5
export (float) var plasma_speed = 500

var player
var is_shot = false
var velocity

signal killed_enemy


func init(plyr):
	player = plyr


func _process(delta):
	if not is_shot:
		if Input.is_action_pressed("shoot_plasma"):  # "charge"
			if scale.length() <= max_scale:
				scale *= 1 + delta
		
		elif Input.is_action_just_released("shoot_plasma"):
			is_shot = true
			var direction = position.angle_to_point(get_viewport().get_mouse_position())
			velocity = Vector2(-plasma_speed, 0).rotated(direction)

func _physics_process(delta):
	if not is_shot:
		position.x = player.position.x
		position.y = player.position.y
	else:
		var collision_info = move_and_collide(velocity)
		if collision_info != null:
			if collision_info.collider.is_in_group("enemies"):
				collision_info.collider.queue_free()
				emit_signal("killed_enemy")
extends KinematicBody2D

export (float) var max_scale = 5
export (float) var plasma_speed = 500
export (int) var plasma_damage = 2

var player
var is_shot = false
var velocity


func init(plyr):
	player = plyr


func _process(delta):
	if not is_shot:
		if Input.is_action_pressed("shoot_plasma"):  # "charge"
			if scale.length() <= max_scale:
				scale *= 1 + delta
		
		elif Input.is_action_just_released("shoot_plasma"):
			is_shot = true
			var direction = global_position.angle_to_point(get_global_mouse_position())
			velocity = Vector2(-plasma_speed, 0).rotated(direction)

func _physics_process(delta):
	if not is_shot:
		position.x = player.position.x
		position.y = player.position.y
	else:
		collide(move_and_collide(velocity))
		
				
func collide(info):
	if info == null:
		return
	
	if info.collider.is_in_group("enemies") or info.collider.is_in_group("hives"):
		info.collider.damage(plasma_damage)
		if info.collider.is_in_group("hives"):
			queue_free()
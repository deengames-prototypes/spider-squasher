extends KinematicBody2D

export (float) var bullet_speed = 600

var velocity


func _process(delta):
	collide(move_and_collide(velocity * delta))


func collide(info):
	if info == null:
		return
	if info.collider.is_in_group("enemies"):
		info.collider.queue_free()
		queue_free()


func init(x, y, angle):
	position.x = x
	position.y = y
	velocity = Vector2(-bullet_speed, 0).rotated(angle)
	
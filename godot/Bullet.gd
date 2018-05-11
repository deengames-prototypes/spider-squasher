extends KinematicBody2D

export (float) var bullet_speed = 600
export (int) var bullet_damage = 1

var velocity


func _process(delta):
	collide(move_and_collide(velocity * delta))


func collide(info):
	if info == null:
		return
	if info.collider.is_in_group("enemies") or info.collider.is_in_group("hives"):
		info.collider.damage(bullet_damage)
		queue_free()


func init(x, y, angle):
	position.x = x
	position.y = y
	velocity = Vector2(-bullet_speed, 0).rotated(angle)
	
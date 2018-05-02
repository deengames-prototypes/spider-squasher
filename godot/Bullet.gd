extends KinematicBody2D

var velocity

func _ready():
	# Called every time the node is added to the scene.
	# Initialization here
	pass

func _process(delta):
	collide(move_and_collide(velocity * delta))

func collide(info):
	if info == null:
		return
	if info.collider.is_in_group("enemies"):
		info.collider.queue_free()
		queue_free()
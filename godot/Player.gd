extends KinematicBody2D

export (int) var movement_speed = 300
export (float) var seconds_per_plasma_shot = 2

var linear_velocity = Vector2()
var PlasmaCharge = load("res://PlasmaCharge.tscn")
var time_since_last_plasma = seconds_per_plasma_shot

signal killed
signal shoot_plasma(plasma_ball)


func _ready():
	# place player in the middle of the screen
	position.x = ProjectSettings.get_setting("display/window/size/width") / 2
	position.y = ProjectSettings.get_setting("display/window/size/height") / 2
	
	# add loop component child node
	add_child(load("res://LoopComponent.gd").new())


func _process(delta):
	time_since_last_plasma += delta
	
	if Input.is_action_just_pressed("shoot_plasma") and time_since_last_plasma >= seconds_per_plasma_shot:
		time_since_last_plasma = 0
		var current_plasma_charge = PlasmaCharge.instance()
		current_plasma_charge.init(self)
		emit_signal("shoot_plasma", current_plasma_charge)


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
	if info != null:
		if info.collider.is_in_group("enemies") or info.collider.is_in_group("lava"):
			emit_signal('killed')

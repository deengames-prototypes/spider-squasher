extends Node2D

export (float) var seconds_per_enemy = 2
export (float) var enemy_spawn_rate_delta = 1.5
export (float) var bullet_speed = 600
export (float) var bullets_per_second = 0.5

var Enemy = load("res://Enemy.tscn")
var time_since_enemy_spawn = 0
var time_since_last_fire = 0
var bullet_class = load("res://Bullet.tscn")


func _process(delta):
	time_since_enemy_spawn += delta
	time_since_last_fire += delta
	
	var randomizer = rand_range(-enemy_spawn_rate_delta, enemy_spawn_rate_delta)
	if time_since_enemy_spawn > seconds_per_enemy + randomizer:
		time_since_enemy_spawn = 0
		add_child(Enemy.instance())

	if Input.is_action_pressed("shoot") and time_since_last_fire > bullets_per_second:
		time_since_last_fire = 0
		var angle = $Player.position.angle_to_point(get_viewport().get_mouse_position())
		var bullet = bullet_class.instance()
		add_child(bullet)
		
		bullet.position.x = $Player.position.x
		bullet.position.y = $Player.position.y
		
		bullet.velocity = Vector2(-bullet_speed, 0).rotated(angle)

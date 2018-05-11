extends StaticBody2D

export (float) var enemies_per_second = 0.5
export (float) var enemy_spawn_rate_delta = 1.5
export (float) var enemy_spawn_distance = 100
export (int) var health = 20


signal spawn_enemy(enemy)
signal hive_died

var Enemy = load("res://Enemy.tscn")
var time_since_enemy_spawn = 0


func _ready():
	add_to_group("hives")


func _process(delta):
	time_since_enemy_spawn += delta
	
	var randomizer = rand_range(-enemy_spawn_rate_delta, enemy_spawn_rate_delta)
	if time_since_enemy_spawn > 1/enemies_per_second + randomizer:
		time_since_enemy_spawn = 0
		var enemy = Enemy.instance()
		var x = rand_range(-enemy_spawn_distance, enemy_spawn_distance)
		var y = rand_range(-enemy_spawn_distance, enemy_spawn_distance)
		enemy.set_position(global_position.x + x, global_position.y + y)
		emit_signal("spawn_enemy", enemy)


func damage(i):
	health -= i
	if health < 0:
		queue_free()
		emit_signal("hive_died")
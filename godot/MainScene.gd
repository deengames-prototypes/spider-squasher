extends Node2D

export (float) var enemies_per_second = 0.333
export (float) var enemy_spawn_rate_delta = 0.2

var Enemy = load("res://Enemy.tscn")
var time_since_enemy_spawn = 0


func _process(delta):
	time_since_enemy_spawn += delta
	var randomizer = rand_range(-enemy_spawn_rate_delta, enemy_spawn_rate_delta)
	if time_since_enemy_spawn > enemies_per_second + randomizer:
		add_child(Enemy.instance())

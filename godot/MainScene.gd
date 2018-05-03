extends Node2D

export (float) var seconds_per_enemy = 2
export (float) var enemy_spawn_rate_delta = 1.5

var Enemy = load("res://Enemy.tscn")
var time_since_enemy_spawn = 0


func _process(delta):
	time_since_enemy_spawn += delta
	
	var randomizer = rand_range(-enemy_spawn_rate_delta, enemy_spawn_rate_delta)
	if time_since_enemy_spawn > seconds_per_enemy + randomizer:
		time_since_enemy_spawn = 0
		var enemy = Enemy.instance()
		enemy.init($Player)
		enemy.connect('killed_player', self, '_on_Player_killed')
		add_child(enemy)


func _on_Player_killed():
	get_tree().change_scene('res://MainScene.tscn')


func _on_Player_shoot_plasma(plasma_ball):
	add_child(plasma_ball)


func _on_Player_shoot_bullet(bullet):
	add_child(bullet)

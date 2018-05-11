extends Node2D

export (float) var powerups_per_second = 0.3
export (float) var powerups_delta = 1.5

var PowerUp = preload("res://PowerUp.tscn")

var time_since_powerup = 0

signal spawn_powerup(powerup)

func _process(delta):
	time_since_powerup += delta
	
	var randomizer = rand_range(-powerups_delta, powerups_delta)
	if time_since_powerup > 1/powerups_per_second + randomizer:
		time_since_powerup = 0
		var powerup = PowerUp.instance()
		powerup.set_position(global_position.x, global_position.y)
		emit_signal("spawn_powerup", powerup)


func _on_enemy_spawn(enemy):
	get_parent()._on_enemy_spawn(enemy)


func _on_hive_died():
	get_parent()._on_hive_died()

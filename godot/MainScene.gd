extends Node2D

var score = 0

var powerup_table = [  # attribute, magnitude, duration
	["movement_speed", 100, 5],
	["bullets_per_second", 2, 5],
	["plasma_shots_per_second", 0.5, 5]
]


func _on_spawn_powerup(powerup):
	var powerup_info = powerup_table[randi() % powerup_table.size()]
	powerup.init($Player, powerup_info[0], powerup_info[1], powerup_info[2])
	$Player.connect("killed", self, "_on_Player_killed")
	add_child(powerup)

func _on_Player_killed():
	get_tree().change_scene('res://MainScene.tscn')


func _on_Player_shoot_plasma(plasma_ball):
	add_child(plasma_ball)


func _on_Player_shoot_bullet(bullet):
	add_child(bullet)
	

func _on_enemy_spawn(enemy):
	enemy.init($Player)
	enemy.connect('killed_player', self, '_on_Player_killed')
	enemy.connect('killed_enemy', self, "_on_enemy_killed")
	add_child(enemy)


func _on_enemy_killed():
	score += 10
	$ScoreLabel.set_text(String(score))
	

func _on_hive_died():
	score += 50
	$ScoreLabel.set_text(String(score))
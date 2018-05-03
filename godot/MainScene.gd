extends Node2D

export (float) var enemies_per_second = 0.5
export (float) var enemy_spawn_rate_delta = 1.5

export (float) var powerups_per_second = 0.3
export (float) var powerups_delta = 1.5

var Enemy = load("res://Enemy.tscn")
var PowerUp = preload("res://PowerUp.tscn")

var time_since_enemy_spawn = 0
var time_since_powerup = 0
var score = 0

var powerup_table = [  # attribute, magnitude, duration
	["movement_speed", 100, 5],
	["bullets_per_second", 2, 5],
	["plasma_shots_per_second", 0.5, 5]
]


func _process(delta):
	time_since_enemy_spawn += delta
	time_since_powerup += delta
	
	var randomizer = rand_range(-enemy_spawn_rate_delta, enemy_spawn_rate_delta)
	if time_since_enemy_spawn > 1/enemies_per_second + randomizer:
		time_since_enemy_spawn = 0
		var enemy = Enemy.instance()
		enemy.init($Player)
		enemy.connect('killed_player', self, '_on_Player_killed')
		add_child(enemy)
	
	randomizer = rand_range(-powerups_delta, powerups_delta)
	if time_since_powerup > 1/powerups_per_second + randomizer:
		time_since_powerup = 0
		var powerup_info = powerup_table[randi() % powerup_table.size()]
		var powerup = PowerUp.instance()
		powerup.init($Player, powerup_info[0], powerup_info[1], powerup_info[2])
		$Player.connect("killed", powerup, "_on_Player_killed")
		add_child(powerup)


func _on_Player_killed():
	get_tree().change_scene('res://MainScene.tscn')


func _on_Player_shoot_plasma(plasma_ball):
	add_child(plasma_ball)
	plasma_ball.connect("killed_enemy", self, "_on_enemy_killed")


func _on_Player_shoot_bullet(bullet):
	add_child(bullet)
	bullet.connect("killed_enemy", self, "_on_enemy_killed")


func _on_enemy_killed():
	score += 10
	$ScoreLabel.set_text(String(score))

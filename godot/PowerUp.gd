extends Area2D

var powered_attribute
var magnitude
var player
var is_activated = false


func set_position(x, y):
	var width = ProjectSettings.get_setting("display/window/size/width")
	var height = ProjectSettings.get_setting("display/window/size/height")
	
	position.x = rand_range(0, width) + x
	position.y = rand_range(0, height) + y


func init(_player, attr, magni, duration):
	player = _player
	powered_attribute = attr
	magnitude = magni
	$Timer.set_wait_time(duration)

func _on_PowerUp_body_entered(body):
	if body == player and not is_activated:
		is_activated = true
		player.set(powered_attribute, player.get(powered_attribute) + magnitude)
		hide()
		print(player, ' : ', player.get(powered_attribute))
		$Timer.start()


func _on_Timer_timeout():
	player.set(powered_attribute, player.get(powered_attribute) - magnitude)
	print(powered_attribute, ' ; ', player.get(powered_attribute))


func _on_Player_killed():
	$Timer.stop()
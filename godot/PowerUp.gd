extends Area2D

var powered_attribute
var magnitude
var powered_thing

func _ready():
	var width = ProjectSettings.get_setting("display/window/size/width")
	var height = ProjectSettings.get_setting("display/window/size/height")
	position.x = rand_range(0, width)
	position.y = rand_range(0, height)


func init(attr, magni, duration):
	powered_attribute = attr
	magnitude = magni
	$Timer.set_wait_time(duration)

func _on_PowerUp_body_entered(body):
	if body.get(powered_attribute) != null:
		powered_thing = body
		powered_thing.set(powered_attribute, powered_thing.get(powered_attribute) + magnitude)
		queue_free()
		print(powered_attribute, ' : ', powered_thing.get(powered_attribute))
		$Timer.start()


func _on_Timer_timeout():
	powered_thing.set(powered_attribute, powered_thing.get(powered_attribute) - magnitude)
	print(powered_attribute, ' ; ', powered_thing.get(powered_attribute))


func _on_Player_killed():
	$Timer.stop()
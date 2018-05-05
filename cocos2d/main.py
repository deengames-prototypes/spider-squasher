import random
from math import cos, sin, atan2

import cocos
from pyglet.window import key as K
import cocos.collision_model as cm


MOVEMENT_SPEED = 200
ENEMY_MOVEMENT_SPEED = 150
ENEMIES_PER_SECOND = 0.5
SAFE_RANGE = 100


class CollidableSprite(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y):
        super().__init__(image)
        self.position = (center_x, center_y)
        half_width = self.width / 2
        half_height = self.height / 2

        self.cshape = cm.AARectShape(self.position, half_width, half_height)
        self.schedule(self.loop)

    def loop(self, delta):
        window_x, window_y = cocos.director.director.get_window_size()
        if self.x > window_x:
            self.x -= window_x
        if self.x < 0:
            self.x += window_x
        if self.y > window_y:
            self.y -= window_y
        if self.y < 0:
            self.y += window_y


class Enemy(CollidableSprite):
    def __init__(self, player, center_x, center_y):
        super().__init__('enemy.png', center_x, center_y)
        self.player = player
        self.schedule(self.move)

    def move(self, delta):
        vec = (-ENEMY_MOVEMENT_SPEED, 0)
        ang = atan2(self.y - self.player.y, self.x - self.player.x)
        rotated = (vec[0] * cos(ang) - vec[1] * sin(ang), vec[0] * sin(ang) + vec[1] * cos(ang))

        self.x += rotated[0] * delta
        self.y += rotated[1] * delta


class Game(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()
        window_x, window_y = cocos.director.director.get_window_size()

        self.player = CollidableSprite('player.png', window_x / 2, window_y / 2)
        self.add(self.player)

        self.collision_manager = cm.CollisionManagerBruteForce()
        self.collision_manager.add(self.player)

        self.pressed_keys = set()

        self.schedule(self.update)

        self.time_since_enemy_spawn = 0
        self.schedule(self.spawn_enemies)

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.pressed_keys.remove(key)

    def update(self, delta):
        for key in self.pressed_keys:
            if key == K.UP:
                self.player.y += MOVEMENT_SPEED * delta
            elif key == K.DOWN:
                self.player.y -= MOVEMENT_SPEED * delta
            elif key == K.LEFT:
                self.player.x -= MOVEMENT_SPEED * delta
            elif key == K.RIGHT:
                self.player.x += MOVEMENT_SPEED * delta

    def spawn_enemies(self, delta):
        self.time_since_enemy_spawn += delta
        if self.time_since_enemy_spawn > 1/ENEMIES_PER_SECOND:
            self.time_since_enemy_spawn = 0
            window_x, window_y = cocos.director.director.get_window_size()

            x, y = self.player.x, self.player.y

            while (abs(x - self.player.x) <= SAFE_RANGE
                   or abs(y - self.player.y) <= SAFE_RANGE):
                x, y = random.randrange(0, window_x), random.randrange(0, window_y)

            enemy = Enemy(self.player, x, y)
            self.add(enemy)


if __name__ == '__main__':
    cocos.director.director.init()
    cocos.director.director.run(cocos.scene.Scene(Game()))

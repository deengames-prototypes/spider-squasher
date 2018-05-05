import random

import cocos
from pyglet.window import key as K
import cocos.collision_model as cm


MOVEMENT_SPEED = 200
ENEMIES_PER_SECOND = 0.5
SAFE_RANGE = 100


class CollidableSprite(cocos.sprite.Sprite):
    def __init__(self, image, center_x, center_y):
        super().__init__(image)
        self.position = (center_x, center_y)
        half_width = self.width / 2
        half_height = self.height / 2

        self.cshape = cm.AARectShape(self.position, half_width, half_height)


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

            enemy_pos = self.player.position

            while (abs(enemy_pos[0] - self.player.position[0]) <= SAFE_RANGE
                   or abs(enemy_pos[1] - self.player.position[1]) <= SAFE_RANGE):
                enemy_pos = random.randrange(0, window_x), random.randrange(0, window_y)

            enemy = CollidableSprite('enemy.png', *enemy_pos)
            self.add(enemy)


if __name__ == '__main__':
    cocos.director.director.init()
    cocos.director.director.run(cocos.scene.Scene(Game()))

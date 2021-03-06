import random
from math import cos, sin, atan2

import cocos
from pyglet.window import key as K
from pyglet.window import mouse as M
import cocos.collision_model as cm


MOVEMENT_SPEED = 200
ENEMY_MOVEMENT_SPEED = 200
BULLET_SPEED = 500
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
        self.schedule(self.update_shape)

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

    def update_shape(self, delta):
        self.cshape.center = self.position


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


class Bullet(CollidableSprite):
    def __init__(self, ang, center_x, center_y):
        super().__init__('bullet.png', center_x, center_y)
        vec = (BULLET_SPEED, 0)
        rotated = (vec[0] * cos(ang) - vec[1] * sin(ang), vec[0] * sin(ang) + vec[1] * cos(ang))
        self.velocity = rotated
        self.schedule(self.move)
        self.rotation = ang

    def move(self, delta):
        self.x += self.velocity[0] * delta
        self.y += self.velocity[1] * delta

    def loop(self, delta):
        pass


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

        self.schedule(self.process_keys)

        self.time_since_enemy_spawn = 0
        self.schedule(self.spawn_enemies)

        self.schedule(self.collisions)

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        try:
            self.pressed_keys.remove(key)
        except KeyError:
            pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        if buttons == M.LEFT:
            ang = atan2(y - self.player.y, x - self.player.x)

            bullet = Bullet(ang, self.player.x, self.player.y)
            self.add(bullet)
            self.collision_manager.add(bullet)

    def process_keys(self, delta):
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
            self.collision_manager.add(enemy)

    def collisions(self, delta):
        to_remove = set()

        for collision in self.collision_manager.iter_all_collisions():
            collision = list(collision)
            if self.player in collision:
                collision.remove(self.player)
                if type(collision[0]) is Enemy:
                    self.player.kill()
                    cocos.director.director.run(cocos.scene.Scene(Game()))

            elif {Enemy, Bullet} == {type(obj) for obj in collision}:
                for obj in collision:
                    obj.kill()
                    to_remove.add(obj)

        for obj in to_remove:
            self.collision_manager.remove_tricky(obj)


if __name__ == '__main__':
    cocos.director.director.init()
    cocos.director.director.run(cocos.scene.Scene(Game()))

import math
import random

from kivy.app import App
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import *
from kivy.vector import Vector

MOVEMENT_SPEED = 200
ENEMY_MOVEMENT_SPEED = 100
BULLET_SPEED = 500
ENEMIES_PER_SECOND = 0.5
SAFE_RANGE = 300


class Entity(EventDispatcher):
    x = NumericProperty()
    y = NumericProperty()

    color = None
    size = (None, None)

    def __init__(self, x, y):
        super().__init__()
        self.rect = Rectangle(pos=(x, y), size=self.size)
        self.x = x
        self.y = y

        self.group = InstructionGroup()
        self.group.add(self.color)
        self.group.add(self.rect)

        self.is_alive = True

    def on_x(self, instance, value):
        self.rect.pos = (value, self.rect.pos[1])

    def on_y(self, instance, value):
        self.rect.pos = (self.rect.pos[0], value)

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]

    def intersects(self, other):
        return not (
            self.x > other.x + other.width
            or self.x + self.width < other.x
            or self.y > other.y + other.height
            or self.y + self.height < other.y
        )

    def kill(self):
        self.group.clear()
        self.is_alive = False


class LoopingEntity(Entity):
    def on_x(self, instance, value):
        if self.x > Window.width:
            self.x -= Window.width
        elif self.x < 0:
            self.x += Window.width

        super().on_x(instance, value)

    def on_y(self, instance, value):
        if self.y > Window.height:
            self.y -= Window.height
        elif self.y < 0:
            self.y += Window.height

        super().on_y(instance, value)


class Enemy(LoopingEntity):
    color = Color(1, 0, 0)
    size = (48, 48)

    def update(self, dt, player):
        if self.is_alive:
            ang = math.degrees(math.atan2(self.y - player.y, self.x - player.x))
            rotated = Vector(-ENEMY_MOVEMENT_SPEED, 0).rotate(ang)

            self.x += rotated.x * dt
            self.y += rotated.y * dt
            # print(self.x, ',', self.y, ':', self.is_alive)


class Player(LoopingEntity):
    color = Color(0, 1, 0)
    size = (32, 48)


class Bullet(Entity):
    color = Color(1, 1, 1)
    size = (16, 16)

    def __init__(self, x, y, angle):
        super().__init__(x, y)
        self.angle = angle

    def update(self, dt):
        rotated = Vector(BULLET_SPEED, 0).rotate(self.angle)
        self.x += rotated.x * dt
        self.y += rotated.y * dt


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.player = Player(Window.width / 2, Window.height / 2)
        self.canvas.add(self.player.group)

        self.enemies = set()
        self.bullets = set()

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)
        self.pressed_keys = set()

        Clock.schedule_interval(self.update, 1 / 60)
        Clock.schedule_interval(self.add_enemy, 1 / ENEMIES_PER_SECOND)

    def keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self.on_keyboard_down)
        self.keyboard = None

    def update(self, dt):
        if 'w' in self.pressed_keys:
            self.player.y += MOVEMENT_SPEED * dt
        if 'a' in self.pressed_keys:
            self.player.x -= MOVEMENT_SPEED * dt
        if 's' in self.pressed_keys:
            self.player.y -= MOVEMENT_SPEED * dt
        if 'd' in self.pressed_keys:
            self.player.x += MOVEMENT_SPEED * dt

        for enemy in self.enemies:
            enemy.update(dt, self.player)

            if self.player.intersects(enemy) and enemy.is_alive:
                # this is broke af
                print('dead')

        for bullet in self.bullets.copy():
            bullet.update(dt)

            for enemy in self.enemies.copy():
                if bullet.intersects(enemy) and bullet.is_alive and enemy.is_alive:
                    enemy.kill()
                    bullet.kill()
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(keycode[1])
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.pressed_keys.remove(keycode[1])
        return True

    def on_touch_down(self, touch):
        angle = math.degrees(math.atan2(touch.pos[1] - self.player.y, touch.pos[0] - self.player.x))
        bullet = Bullet(self.player.x, self.player.y, angle)
        self.canvas.add(bullet.group)
        self.bullets.add(bullet)

    def add_enemy(self, dt):
        x, y = random.randint(0, Window.width), random.randint(0, Window.height)
        while Vector(x, y).distance((self.player.x, self.player.y)) <= SAFE_RANGE:
            x, y = random.randint(0, Window.width), random.randint(0, Window.height)
        enemy = Enemy(x, y)
        self.canvas.add(enemy.group)
        self.enemies.add(enemy)


class SpiderSquasherApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    SpiderSquasherApp().run()

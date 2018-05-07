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
ENEMY_MOVEMENT_SPEED = 200
BULLET_SPEED = 500
ENEMIES_PER_SECOND = 0.5
SAFE_RANGE = 100


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

    def on_x(self, instance, value):
        self.rect.pos = (value, self.rect.pos[1])

    def on_y(self, instance, value):
        self.rect.pos = (self.rect.pos[0], value)


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
        ang = math.degrees(math.atan2(self.y - player.y, self.x - player.x))
        rotated = Vector(-ENEMY_MOVEMENT_SPEED, 0).rotate(ang)

        self.x += rotated.x * dt
        self.y += rotated.y * dt


class Player(LoopingEntity):
    color = Color(0, 1, 0)
    size = (32, 48)


class Bullet(Entity):
    color = Color(1, 1, 1)
    size = (8, 8)

    def __init__(self, x, y, angle):
        super().__init__(x, y)
        self.angle = angle
        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        rotated = Vector(BULLET_SPEED, 0).rotate(self.angle)
        self.x += rotated.x * dt
        self.y += rotated.y * dt


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.add_enemy, 1 / ENEMIES_PER_SECOND)

        self.player = Player(Window.width / 2, Window.height / 2)
        self.canvas.add(self.player.group)

        self.enemies = set()

        self.keyboard = Window.request_keyboard(self.keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self.on_keyboard_down, on_key_up=self.on_keyboard_up)
        self.pressed_keys = set()

        Clock.schedule_interval(self.update, 1 / 60)

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

    def add_enemy(self, dt):
        x, y = random.randint(0, Window.width), random.randint(0, Window.height)
        enemy = Enemy(x, y)
        self.canvas.add(enemy.group)
        self.enemies.add(enemy)


class SpiderSquasherApp(App):
    def build(self):
        return GameWidget()


if __name__ == '__main__':
    SpiderSquasherApp().run()

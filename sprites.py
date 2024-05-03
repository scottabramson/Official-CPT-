
import pygame as pg
from settings import *
from tilemap import *
from random import uniform, choice
from test import *
vec = pg.math.Vector2



#COLLISIONS
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            hit = hits[0]
            if sprite.vel.x > 0:  # Moving right
                sprite.hit_rect.right = hit.rect.left
                sprite.pos.x = sprite.hit_rect.centerx  # Adjust sprite center based on updated hit_rect
            elif sprite.vel.x < 0:  # Moving left
                sprite.hit_rect.left = hit.rect.right
                sprite.pos.x = sprite.hit_rect.centerx
            sprite.vel.x = 0  # Stop horizontal movement

    elif dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            hit = hits[0]
            if sprite.vel.y > 0:  # Moving down
                sprite.hit_rect.bottom = hit.rect.top
                sprite.pos.y = sprite.hit_rect.centery
            elif sprite.vel.y < 0:  # Moving up
                sprite.hit_rect.top = hit.rect.bottom
                sprite.pos.y = sprite.hit_rect.centery
            sprite.vel.y = 0  # Stop vertical movement


def check_collisions(player, obstacles):
    for obstacle in obstacles:
        if player.hit_rect.colliderect(obstacle.rect):
            handle_collision(player, obstacle)
def handle_collision(player, obstacle):
    # Example: Stop the player's movement
    player.vel.x = 0
    player.vel.y = 0
    # Optionally, reposition player slightly away from the obstacle
    if player.hit_rect.centerx < obstacle.rect.centerx:
        player.hit_rect.right = obstacle.rect.left
    else:
        player.hit_rect.left = obstacle.rect.right



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.scale_factor = 0.6  # Define scale factor before loading images
        self.load_images()
        self.image = self.idlesprite_images[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, int(self.rect.width * 0.4), int(self.rect.height * 0.4))
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.action = 'idle'
        self.direction = 's'
        self.direction_frames = {'d': 0, 'w': 6, 'a': 12, 's': 18}

    def load_images(self):
        frame_width = 48
        frame_height = 73
        scale = self.scale_factor  # Scale factor from the instance variable

        sprite_sheet = pg.image.load('animations/throw.png').convert_alpha()
        sprite_sheet_run = pg.image.load('animations/run.png').convert_alpha()
        sprite_sheet_idle = pg.image.load('animations/idle.png').convert_alpha()

        self.throwsprite_images = [pg.transform.scale(sprite_sheet.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)),
                                      (int(frame_width * scale), int(frame_height * scale))) for i in range(24)]
        self.runsprite_images = [pg.transform.scale(sprite_sheet_run.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)),
                                    (int(frame_width * scale), int(frame_height * scale))) for i in range(24)]
        self.idlesprite_images = [pg.transform.scale(sprite_sheet_idle.subsurface(pg.Rect(i * frame_width, 0, frame_width, frame_height)),
                                     (int(frame_width * scale), int(frame_height * scale))) for i in range(24)]

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.running = False
        self.throwing = False

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.direction = 'a'
            self.running = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
            self.direction = 'd'
            self.running = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
            self.direction = 'w'
            self.running = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
            self.direction = 's'
            self.running = True
        if keys[pg.K_SPACE]:
            self.throwing = True
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                direction_angle = {
                    'd': 0,  # right
                    'a': 180,  # left
                    'w': 270,  # up
                    's': 90  # down
                }.get(self.direction, 0)
                bullet_dir = vec(1, 0).rotate(direction_angle)  # Rotate the bullet vector based on direction
                bullet_pos = self.pos + bullet_dir * 30  # Example offset, adjust as necessary
                Bullet(self.game, bullet_pos, bullet_dir)
                self.vel += vec(-KICKBACK, 0).rotate(direction_angle)

        if self.vel.length() > 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED



    def update(self):
        self.get_keys()
        self.animate()

        # Apply horizontal movement
        self.pos.x += self.vel.x * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.centerx = self.hit_rect.centerx

        # Apply vertical movement
        self.pos.y += self.vel.y * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.centery = self.hit_rect.centery

    def animate(self):
        now = pg.time.get_ticks()
        if self.running:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 6
                self.image = self.runsprite_images[self.current_frame + self.direction_frames[self.direction]]
        elif self.throwing:
            if self.current_frame < 6:
                self.image = self.throwsprite_images[self.current_frame + self.direction_frames[self.direction]]
                self.current_frame += 1
            else:
                self.throwing = False
                self.current_frame = 0
        else:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                self.image = self.idlesprite_images[self.current_frame + self.direction_frames[self.direction]]


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.original_image = pg.image.load("img/zombie1_hold.png").convert_alpha()
        self.image = pg.transform.scale(self.original_image, (
        int(self.original_image.get_width() * 0.7), int(self.original_image.get_height() * 0.7)))
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, int(self.rect.width * 0.8), int(self.rect.height * 0.8))
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.health = MOB_HEALTH
        self.acc = vec(0, 0)
        self.speed = choice(MOB_SPEEDS)
        self.vision_radius = 500
        self.game.debug_mode = False


    def chase_player(self):
        direction = (self.game.player.pos - self.pos).normalize()
        self.vel = direction * self.speed

    def update(self):
        self.acc = vec(0, 0)
        self.avoid_mobs()
        can_see = self.can_see_player()
        if can_see:
            self.chase_player()
        else:
            self.idle_behavior()

        # Apply velocity based on accumulated acceleration and existing velocity
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.hit_rect.center = self.pos
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

        if self.health <= 0:
            self.kill()

    def idle_behavior(self):
        self.vel = vec(0, 0)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def can_see_player(self):
        if self.pos.distance_to(self.game.player.pos) < self.vision_radius:
            for wall in self.game.walls:
                if wall.rect.clipline(self.pos, self.game.player.pos):
                    return False
            return True
        return False

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)

        # Draw background (empty part of health bar)
        background_bar = pg.Rect(0, 0, self.rect.width, 7)  # Same width as the mob's rect width
        pg.draw.rect(self.image, BLACK, background_bar)

        # Draw health bar
        self.health_bar = pg.Rect(0, 0, width, 7)
        pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > BULLET_LIFETIME:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class FinishTrigger(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.finish_triggers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h), pg.SRCALPHA)  # SRCALPHA makes it transparent
        self.rect = self.image.get_rect(topleft=(x, y))
        self.game = game

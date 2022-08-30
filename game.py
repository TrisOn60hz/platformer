from turtle import pos
import pygame as pg
pg.font.init()
pg.mixer.init()

class Tile(pg.sprite.Sprite):
    def __init__(self, filename, position, size=(64,64)):
        super().__init__()
        self.image = pg.image.load(filename)
        self.image = pg.transform.scale(self.image, size)
        position = (position[0]*size[0], position[1]*size[1])
        self.rect = pg.Rect(position, size)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def update(self, shift):
        self.rect.topleft += pg.Vector2(shift)

class ImageSprite(pg.sprite.Sprite):
    def __init__(self, filename, position, size, speed=(0,0)): # create the constructor (runs when a new object is created)
        super().__init__()
        self.image = pg.image.load(filename)
        self.image = pg.transform.scale(self.image, size)
        self.rect = pg.Rect(position, size)
        self.max_speed = pg.Vector2(speed)
        self.speed = pg.Vector2((0,0))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class TextSprite(pg.sprite.Sprite):
    def __init__(self, text, text_color, position, font_size, rect_color=None, rect_size=(0,0)):
        self.font = pg.font.Font(("ARCADE_N.ttf"), font_size)
        self.image = self.font.render(text, True, text_color)
        self.position = position
        self.rect_color = rect_color
        self.text_color = text_color
        self.rect = pg.Rect(position, rect_size)

    def draw(self, surface, bg=False):
        if bg:
            pg.draw.rect(surface, self.rect_color, self.rect)
        surface.blit(self.image, self.position)
    
    def edit_text(self, new_text):
        self.image = self.font.render(new_text, True, self.text_color)
class Player(ImageSprite):
    def __init__(self, filename, position, size, speed=(0,0)):
        super().__init__(filename, position, size, speed)
        self.original_pos = position
    def reset(self):
        self.rect.topleft = self.original_pos
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.speed.x = -self.max_speed.x
        if keys[pg.K_d]:
            self.speed.x = self.max_speed.x
        if keys[pg.K_w] and self.grounded:
            self.speed.y = -self.max_speed.y
        self.grounded = False



        self.rect.x += self.speed.x

        if self.speed.x > 0.7 or self.speed.x < -0.7:
            if self.speed.x > 0:
                self.speed.x -= 1
            else:
                self.speed.x += 1
        else:
            self.speed.x = 0
        
        tiles = pg.sprite.spritecollide(self, platforms, False)

        for tile in tiles:
            if self.speed.x > 0:
                self.rect.right = tile.rect.left
            elif self.speed.x < 0:
                self.rect.left = tile.rect.right
            self.speed.x = 0



        self.rect.y += self.speed.y
        self.speed.y += 0.5
    
        tiles = pg.sprite.spritecollide(self, platforms, False)
        for tile in tiles:
            if self.speed.y > 0:
                self.rect.bottom = tile.rect.top
                self.grounded = True
            elif self.speed.y < 0:
                self.rect.top = tile.rect.bottom
            self.speed.y = 0



        if self.rect.left < 300:
            self.rect.left = 300
            shift.x = -self.speed.x
        elif self.rect.right > WIDTH - 300:
            self.rect.right = WIDTH - 300
            shift.x = -self.speed.x
        else:
            shift.x = 0
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def is_colliding_with(self, other_sprite):
        return pg.sprite.collide_rect(self, other_sprite)

WIDTH = 800
HEIGHT = 640
points = 0
window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

shift = pg.Vector2((0,0))

level1 = ['WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW', 
          'WWWW                                                         WWWWWWWWW',
          'WW                                                              WWWWWW',
          'W            SSS                       SSSSS                         W',
          'W           S                        SSS g           SS              W',
          'W           S                 SSS      S g                           W',
          'W       SSSSS            S              SSSSSSSSSSS       S        g W',
          'W                 SSSS                                            EEEW',
          'W                                                                   XW',
          'WWWWWWLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLWWWWWWWWWW']

platforms = pg.sprite.Group()
death_tiles = pg.sprite.Group()
coins = pg.sprite.Group()
win = pg.sprite.Group()

platform_sprites = {
    'S': 'stone.jpg',
    'W': 'wall.jpg'
}

death_sprites = {
    'L': 'lavatexture.png',
}

win_sprites = {
    'X': 'png.png'
}

def create_map(level):
    platforms.empty()
    death_tiles.empty()
    coins.empty()
    win.empty()
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile in platform_sprites:
                new_tile = Tile(filename=platform_sprites[tile], position=(x, y))
                platforms.add(new_tile)
            if tile in death_sprites:
                new_tile = Tile(filename=death_sprites[tile], position=(x, y))
                death_tiles.add(new_tile)
            if tile == 'g':
                new_tile = Tile(filename="coin.png", position=(x, y))
                coins.add(new_tile)
            if tile == 'X':
                new_tile = Tile(filename="png.png", position=(x, y))
                win.add(new_tile)



# background = ImageSprite(filename="background.jpg", position=(0,0), size=(WIDTH, HEIGHT))
player = Player(filename="cyborg.png", position=(80, 500), size=(64,64), speed=(8, 14))
score_counter = TextSprite("Score: "+str(points), "white", (75, 20), 30)
create_map(level1)

while not pg.event.peek(pg.QUIT):
    window.fill('black')
    

    platforms.update(shift)
    platforms.draw(window)

    death_tiles.update(shift)
    death_tiles.draw(window)

    coins.update(shift)
    coins.draw(window)

    win.update(shift)
    win.draw(window)

    player.update()
    player.draw(window)
    
    score_counter.update()
    score_counter.draw(window)
    
    death = pg.sprite.spritecollide(player, death_tiles, False)
    if death:
        break
    
    coin_hits = pg.sprite.spritecollide(player, coins, True)
    for hit in coin_hits:
        points += 1
        score_counter.edit_text("Score: "+str(points))
    
    win_hit = pg.sprite.spritecollide(player, win, True)
    if win_hit:
        break

    pg.display.update()
    clock.tick(60)


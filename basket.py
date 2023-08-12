import arcade

WIDTH = 900
HEIGHT = 600

BALL_SPRITE = 'ball.png'
BAR_TEXTURE = 'bar.png'
CURSOR_SPRITE = 'cursor.png'
BASKET_SPRITE = 'hoop.png'
BACKGROUND = ''

WINNING_SCORE = 33
PERFECT_THROW = 20
GRAVITY = .4

class Game(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH,HEIGHT)
        self.basket = Basket()
        self.bar = Bar()
        self.ball = Ball()
        self.show_bar = False

        self.score = 0

    def setup(self):
        self.basket.setup()
        self.bar.setup()
        self.ball.setup()

    def reset(self):
        self.setup()

    def on_draw(self):
        self.clear(arcade.color.AERO_BLUE)
        # self.draw_texture_rectangle(WIDTH/2, HEIGHT/2, WIDTH, HEIGHT, arcade.load_texture(BACKGROUND))
        self.ball.draw()
        self.basket.draw()
        if self.show_bar:
            self.bar.draw()
            self.bar.cursor.draw()
        arcade.draw_text(f'score: {self.score}', WIDTH/2, HEIGHT - 100, arcade.color.BLACK, 30)
    def update(self, delta_time):
        self.ball.update()
        if self.show_bar:
            self.bar.update()
        if arcade.check_for_collision(self.ball, self.basket):
            # print('collision')
            print(self.ball.center_x, self.basket.center_x - 50)
            if self.ball.center_x > self.basket.center_x - 50:
                # print('goal')
                self.reset()
                self.score += 1
            else:
                self.reset()
    def on_key_press(self, key, mod):
        if key == arcade.key.SPACE:
            if not self.show_bar:
                self.show_bar = True
                self.bar.cursor.change_x = 10
            else:
                self.bar.cursor.change_x = 0
                self.show_bar = False
                self.drop_ball(self.set_speed_of_ball())

    def set_speed_of_ball(self):

        def get_value(a, b):
            if a - b == 0:
                return 0
            else:
                return (a - b) / 10

        if self.bar.center_x < self.bar.cursor.center_x:
            speed = (PERFECT_THROW) - get_value(self.bar.cursor.center_x, self.bar.center_x)
        elif self.bar.center_x > self.bar.cursor.center_x:
            speed = (PERFECT_THROW) - get_value(self.bar.center_x, self.bar.cursor.center_x)
        else:
            speed = PERFECT_THROW
        return speed
    
    def drop_ball(self, speed):
        self.ball.change_x = PERFECT_THROW
        self.ball.change_y = speed

class Ball(arcade.Sprite):
    def __init__(self):
        super().__init__(BALL_SPRITE, .01)
        
    def setup(self):
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0

    def update(self):

        if self.change_x != 0:
            self.change_x -= (GRAVITY - .2)
            if self.change_x < 0:
                self.change_x = 0
        if self.change_y != 0:
            self.change_y -= GRAVITY
        # print(self.change_x, self.change_y)
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.right >= WIDTH or self.left <= 0 or self.top >= HEIGHT or self.bottom <= 0:
            game.reset()

        # if self.left <= 0:
        #     self.change_x = 0
        #     self.left = 0

class Basket(arcade.Sprite):
    def __init__(self):
        super().__init__(BASKET_SPRITE, .3)
    def setup(self):
        self.center_x = WIDTH - 150
        self.center_y = HEIGHT/2
    # def update(self):
    #     self.center_x += self.change_x
    #     self.center_y += self.change_y

class Bar(arcade.Sprite):
    def __init__(self):
        super().__init__(BAR_TEXTURE, .3)
        self.cursor = arcade.Sprite(CURSOR_SPRITE, .3)
        self.cursor.change_x = .2
    def setup(self):
        self.center_x = WIDTH/2
        self.center_y = HEIGHT/9
        self.cursor.center_x = WIDTH/2
        self.cursor.center_y = self.center_y
    
    def update(self):
        self.cursor.center_x += self.cursor.change_x
        if self.cursor.left <= self.left or self.cursor.right >= self.right:
            self.cursor.change_x = -self.cursor.change_x
        
game = Game()
game.setup()
arcade.run()

import arcade
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Maddie Hello World"

MOVEMENT_SPEED = 7

arcade.resources.load_kenney_fonts()

#Here is a player class that simply must come first loloo
class Player(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1):
        super().__init__(path_or_texture, scale)
    # def __init__(self, scale):
    #     super().__init__(scale)

        self.walk_textures = []

        texture = arcade.load_texture("./sprites/run_right.png")
        texture_flipped = arcade.load_texture("./sprites/run_left.png")

        self.walk_textures.append(texture)
        self.walk_textures.append(texture_flipped)

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > WINDOW_WIDTH - 5:
            self.right = WINDOW_WIDTH - 5

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > WINDOW_HEIGHT - 5:
            self.top = WINDOW_HEIGHT - 5


# arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
# arcade.Window.background_color = arcade.color.AMARANTH_PURPLE

# arcade.start_render()

# arcade.run()

# Above is a bad, overly simple way to do it. You should define these things inside of main instead:

# Next up, we learn how to write a GameView
class GameView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.AMARANTH_PINK
        self.main_text =  arcade.Text(
            "Hello World", 
            WINDOW_WIDTH/2, 
            WINDOW_HEIGHT/2, 
            arcade.color.VIOLET,
            50,
            font_name="Kenney Pixel Square",
            anchor_x="center",
            anchor_y="center")
        
        # Variables that will hold sprite lists
        self.player_list = arcade.SpriteList()
        self.sprites_list = arcade.SpriteList()

        # Setting "player" sprite (use Player subclass so its update can run)
        self.player_sprite = Player(
            "./sprites/run_right.png",
            scale=.45
        )

        self.player_sprite.center_x = WINDOW_WIDTH / 2
        self.player_sprite.center_y = WINDOW_HEIGHT * .25

        self.player_list.append(self.player_sprite)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.score = 0

        #setting up soot sprite sprites :)
        for i in range(20):
            soot_sprite = arcade.Sprite(
                "./sprites/soot-sprite.png",
                scale=.09
            )

            retry = True

            #picks random place on the screen to place each sprite
            #if random stuff chosen makes it collide with my player, redraw
            while(retry):
                soot_sprite.center_x = random.randrange(20, WINDOW_WIDTH - 20)
                soot_sprite.center_y = random.randrange(20, WINDOW_HEIGHT - 20)
                if not arcade.check_for_collision(self.player_sprite, soot_sprite):
                    retry = False
            

            self.sprites_list.append(soot_sprite)

        #Music and sound
        self.music = arcade.Sound("./sounds/Running-full.mp3")
        self.music.play(volume=1)

        self.sound = arcade.Sound(":resources:/sounds/coin1.wav")


    def setup(self):
        pass


    def on_draw(self):
        self.clear()

        self.main_text.draw()
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, font_size=20, font_name="Kenney Pixel Square")

        for sprite in self.player_list:
            arcade.draw_sprite(sprite)

        for sprite in self.sprites_list:
            arcade.draw_sprite(sprite)


    def on_update(self, delta_time):
        self.player_list.update(delta_time)

        # Call update on all sprites
        self.sprites_list.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.sprites_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for sprite in hit_list:
            self.sound.play(volume=.4)
            sprite.remove_from_sprite_lists()
            self.score += 1

        if(self.score == 20):
            view = GameEndView()
            self.window.show_view(view)

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.texture = self.player_sprite.walk_textures[1]
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.texture = self.player_sprite.walk_textures[0]
            self.player_sprite.change_x = MOVEMENT_SPEED


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = True
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = True
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
            self.update_player_speed()
        elif key == arcade.key.DOWN:
            self.down_pressed = False
            self.update_player_speed()
        elif key == arcade.key.LEFT:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
            self.update_player_speed()

class GameEndView(arcade.View):
    def __init__(self):
        super().__init__()

        self.end_text = arcade.Text(
            "YOU WIN!!",
            WINDOW_WIDTH/2,
            WINDOW_HEIGHT/2,
            arcade.color.WHITE,
            100,
            font_name="Kenney Pixel Square",
            anchor_x="center",
            anchor_y="center"
        )

    #do this instead of what? instead of setup?
    def on_show_view(self):
        self.background_color = arcade.color.YELLOW_ORANGE
    
    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        self.end_text.draw()

def main():

    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
    #window.background_color = arcade.color.AMARANTH_PINK

    start_view = GameView()

    window.show_view(start_view)
    start_view.setup()

    #arcade.start_render()

    arcade.run()

if __name__ == "__main__":
    main()

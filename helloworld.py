import arcade
import random
import math

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Maddie Hello World"

MOVEMENT_SPEED = 5
SPRITES_MOVE_SPEED = 5

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


#Moving Sprites Class- simple sprite that picks a random direction and moves in that direction
#If they pick a direction that leads them out of bounds, they will get stuck on the wall
class MovingSprite(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1):
        super().__init__(path_or_texture, scale)
        self.move_timer = 0
        self.move_duration = 1
        self.change_x = 0
        self.change_y = 0
        self.direction = random.randint(1,4)

    def custom_update(self, delta_time):
        self.move_timer += delta_time
        if self.move_timer >= self.move_duration:
            #pick new direction
            self.direction = random.randint(1,4)
            #reset timer
            self.move_timer = 0
        self.move_in_direction()

    def move_in_direction(self):
        if self.direction == 1:
            self.change_x = SPRITES_MOVE_SPEED
            self.change_y = 0
        elif self.direction == 2:
            self.change_x = -SPRITES_MOVE_SPEED
            self.change_y = 0
        elif self.direction == 3:
            self.change_y = SPRITES_MOVE_SPEED
            self.change_x = 0
        else:
            self.change_y = -SPRITES_MOVE_SPEED
            self.change_x = 0

        #Check for out of bounds (and I let them hide just out of bounds mwahaha)
        if self.left < -50:
            self.left = -50
        elif self.right > WINDOW_WIDTH + 50:
            self.right = WINDOW_WIDTH + 50

        if self.bottom < -70:
            self.bottom = -70
        elif self.top > WINDOW_HEIGHT + 70:
            self.top = WINDOW_HEIGHT + 70


class SpeedySprite(arcade.Sprite):
    def __init__(self, path_or_texture = None, scale = 1):
        super().__init__(path_or_texture, scale)
        self.speed = 10
        self.move_timer = 0
        self.move_duration = 1
        self.change_x = random.uniform(-self.speed, self.speed)
        self.change_y = random.uniform(-self.speed, self.speed)

    def custom_update(self, delta_time):
        self.move_timer += delta_time
        if self.move_timer >= self.move_duration:
            #reset timer
            self.move_timer = 0
            self.pick_new_velocity()

        #Check for out of bounds (and I let them hide just out of bounds mwahaha)
        if self.left < -50:
            self.left = -50
        elif self.right > WINDOW_WIDTH + 50:
            self.right = WINDOW_WIDTH + 50

        if self.bottom < -70:
            self.bottom = -70
        elif self.top > WINDOW_HEIGHT + 70:
            self.top = WINDOW_HEIGHT + 70

    def pick_new_velocity(self):
 
        angle = random.uniform(0, 2 * math.pi)
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed



# arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
# arcade.Window.background_color = arcade.color.AMARANTH_PURPLE

# arcade.start_render()

# arcade.run()

# Above is a bad, overly simple way to do it. You should define these things inside of main instead:

# Next up, we learn how to write a GameView
class GameView(arcade.View):
    
    ### INIT

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
        
        #Music and sound
        self.music = arcade.Sound("./sounds/Running-full.mp3",streaming=False)
        self.music.play(volume=1, loop=True)

        self.sound = arcade.Sound(":resources:/sounds/coin1.wav")

        self.pause_timer = 0
        self.pause_duration = 1
        self.is_paused = False

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
        self.level = 0

        #setting up soot sprite sprites :)
        for i in range(20):
            #CHANGE BACK TO ARCADE.SPRITE WHEN DONE WITH TESTING
            soot_sprite = arcade.Sprite(
                "./sprites/soot-sprite.png",
                scale=.09
            )
            self.place_sprite(soot_sprite, self.player_sprite)
            self.sprites_list.append(soot_sprite)

    ### FUNCTION TO ASSIST WITH PLACING SPRITES

    def place_sprite(self,sprite, player):
        retry = True

        #picks random place on the screen to place each sprite
        #if random stuff chosen makes it collide with my player, redraw
        while(retry):
            sprite.center_x = random.randrange(20, WINDOW_WIDTH - 20)
            sprite.center_y = random.randrange(20, WINDOW_HEIGHT - 20)
            if not arcade.check_for_collision(player, sprite):
                retry = False


    ### DIFFERENT LEVEL FUNCTIONS

    # Level 1 is nice-ish, so the sprites just move up/down or side/side
    def level_1(self):
        self.sprites_list.clear()

        for i in range(20):
            soot_sprite = MovingSprite(
                "./sprites/soot-sprite.png",
                scale=.09
            )

            self.place_sprite(soot_sprite, self.player_sprite)
            self.sprites_list.append(soot_sprite)

    # Level 2 is meaner, so the sprites are smaller and move faster and in more complex directions
    def level_2(self):
        self.sprites_list.clear()

        for i in range(20):
            soot_sprite = SpeedySprite(
                "./sprites/soot-sprite.png",
                scale=.07
            )

            self.place_sprite(soot_sprite, self.player_sprite)
            self.sprites_list.append(soot_sprite)


    # Level 3 is straight-up evil, so the sprites will avoid the player
    # def level_3(self):
    #     self.sprites_list.clear()

    #     for i in range(30):
    #         soot_sprite = RunawaySprite(
    #             "./sprites/soot-sprite"
    #         )


    #### OTHER FUNCTIONS

    def setup(self):
        pass


    def on_draw(self):
        self.clear()

        self.main_text.draw()
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, font_size=20, font_name="Kenney Pixel Square")

        self.main_text.draw()
        arcade.draw_text(f"Level: {self.level}", 10, 50, arcade.color.WHITE, font_size=20, font_name="Kenney Pixel Square")

        for sprite in self.player_list:
            arcade.draw_sprite(sprite)

        for sprite in self.sprites_list:
            arcade.draw_sprite(sprite)


    def on_update(self, delta_time):
        # Check to see if we paused the game while switching between levels/views
        if self.is_paused:
            self.pause_timer += delta_time

            if self.pause_timer >= self.pause_duration:
                self.is_paused = False
                self.pause_timer = 0

            return
        
        self.player_list.update(delta_time)

        # Call update on all sprites based on regular or special sprite
        if (self.level != 0):
            for sprite in self.sprites_list:
                sprite.custom_update(delta_time)
        self.sprites_list.update(delta_time)

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.sprites_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for sprite in hit_list:
            self.sound.play(volume=.4)
            sprite.remove_from_sprite_lists()
            self.score += 1

        # When level 0 is passed, set up next level
        if(self.score == 20 and self.level == 0):
            self.level += 1
            self.is_paused = True
            self.background_color = arcade.color.LIGHT_DEEP_PINK
            self.main_text.text = f"Level {self.level}"
            self.level_1()

        if(self.score == 40 and self.level == 1):
            self.level += 1
            self.is_paused = True
            self.background_color = arcade.color.DARK_PINK
            self.main_text.text = f"Level {self.level}"
            self.level_2()

            
        if(self.score == 60 and self.level == 2):
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

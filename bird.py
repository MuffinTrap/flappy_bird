# Flappy bird made in python 2.7 and pygame
# Images are from OpenGameArt.org
#

# We import the pygame module and random module that gives us random numbers
import pygame, random

# This is the main function that is launched by the last line in this file
def main():
    # Initializing pygame and random number generator
    pygame.init()
    random.seed()

    # Here we declare the window size and tell pygame to
    # create a window with that size
    # The screen is where we draw the game objects
    screen_width = 440
    screen_height= 400
    screen = pygame.display.set_mode((screen_width
                                      , screen_height))

    # Creating and loading game assets from files:

    # This is the game background, it is just a blue surface
    background = pygame.Surface(screen.get_size())
    background.fill((56, 72, 148))



    # Happy little bushes and clouds that are randomly generated to the background
    cloud_color = ((240, 240, 240))
    bush_color = ((130, 240, 150))

    # Bushes on the ground
    for i in range(12):
        pygame.draw.circle(background, bush_color
                           , (random.randrange(0, screen_width), screen_height)
                           , random.randrange(10, 40))
    # Clouds in the air
    for i in range(10):
        pygame.draw.circle(background, cloud_color
                           , (random.randrange(0, screen_width), random.randrange(0, screen_height /2))
                           , random.randrange(5, 20))

    # The .convert() stores the background Surface in a format
    # that is faster to blit to the screen buffer
    background = background.convert()

    # Bird image with hot pink background.
    # image.load returns a Surface object
    bird_image = pygame.image.load("bird.png")
    bird_width = bird_image.get_width()
    bird_height = bird_image.get_height()

    # If you have a bird image with transparent background
    # you can skip setting the color key and use .convert_alpha() instead
    # Setting the colorkey tells pygame what color to treat as if it was
    # transparent
    bird_image.set_colorkey((255,0,255))
    bird_image = bird_image.convert()

    # Starting point of the bird.
    bird_start_x = screen_width / 3;
    bird_start_y = screen_height / 2;

    bird_x = bird_start_x
    bird_y = bird_start_y

    # This is the starting velocity of the bird
    # it tells how fast the bird is moving. Positive value
    # means moving down. There is no velocity_x.
    # The starting acceleration is 0
    bird_velocity_y = 0
    bird_acceleration = 0

    # Obstacle
    # We load a rectangular block image and use it to form
    # obstacles for the bird
    block_image = pygame.image.load("block.png")
    block_image = block_image.convert()
    block_size = block_image.get_width();

    # Opening 
    # This is the opening between obstacles that the bird must fly through
    opening_start_x  = screen_width - block_size
    opening_start_y = screen_height / 2
    opening_height = bird_height * 3
    # This is how fast the opening and obstacles move towards the bird
    opening_speed = 4

    opening_x = opening_start_x
    opening_y = opening_start_y

    # These values affect how the bird moves up and down
    # gravity pulls the bird down and flap_power is given
    # to bird when SPACE BAR is pressed
    gravity = 0.098
    flap_power = 4

    # Clock is an object that stalls the game for a wanted time
    # We use it later in the game loop to limit the framerate
    # so that the game objects move equally fast on different
    # computers. The frame rate is stalled to 30 frames per second (FPS)
    clock = pygame.time.Clock()
    FPS = 30

    # Score of the player, each cleared opening is worth 1 point
    score = 0

    # Here the main loop starts. It contains the gameplay
    # and user input that controls the bird
    running = True
    while running:

        # Default state is that gravity pulls the bird down
        bird_acceleration = gravity

        # Input
        # Windows records events that
        # happen to our window. We go through them here
        # to notice input and closing of the game window
        # Here the user can change bird_acceleration for (and only for)
        # the next movement calculation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # User clicked the closing button on the window
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # User pressed the ESC key
                    running = False
                # Flap key
                if event.key == pygame.K_SPACE:
                    # The accerelation here is negative
                    # because y axis decreases when going up
                    bird_acceleration = -flap_power


        # The calculation here is the equation
        # p1 = p0 + v0 * t + a0 * (t^2)
        # from high school physics, but broken down
        # into parts. We can also omit the t, because
        # we know that this happens every 33 milliseconds
        bird_velocity_y += bird_acceleration
        bird_y += bird_velocity_y

        # This code limits the velocity of the bird
        # so that it is easier to get it fly up.
        # Otherwise it would eventually go down infinitely fast
        max_velocity = 4
        if bird_velocity_y < -max_velocity:
            bird_velocity_y = -max_velocity
        if bird_velocity_y > max_velocity:
            bird_velocity_y = max_velocity

        # We limit the bird inside the window and stop the movement
        # if it hits either top or bottom border
        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0
        if bird_y + bird_height> screen_height:
            bird_y = screen_height - bird_height
            bird_velocity = 0

        # The opening and adjacent obstacles move towards the left
        # side of the window and do not accelerate
        opening_x -= opening_speed

        # The important part : collision check!

        # To make things simpler, we check if the bird goes safely
        # through the opening. Otherwise we know that we have hit either
        # obstacle

        # First we check if bird has already passed the opening. If the
        # butt of the bird is further right than the right side
        # of the opening and obstacles it must be safe
        bird_butt = bird_x
        opening_end = opening_x + block_size

        # If that is not the case, we check if the bird's peak is
        # further left than where the opening starts. If so, it must be safe
        bird_peak = bird_x + bird_width
        opening_start = opening_x

        # If neither of those is true, then we could be in trouble. It
        # depends on the height of the bird
        # The logic is that if the ceiling of the opening is above the bird's
        # head and the floor of the opening is below its feet, the bird
        # is safe.
        opening_ceiling = opening_y
        opening_floor = opening_y + opening_height
        bird_head = bird_y
        bird_feet = bird_y + bird_height

        # Now we do the checks
        # If the bird hits the obstacles, we reset the opening and bird positions
        # and reset the score
        # The pass is a python reserved word that breaks out from the
        # indentation and skips to the end
        if bird_butt > opening_end:
            pass
        elif bird_peak < opening_start:
            pass
        else:
            if opening_ceiling < bird_head and opening_floor > bird_feet:
                pass
            else:
                # Oh no!
                bird_x = bird_start_x
                bird_y = bird_start_y
                opening_x = opening_start_x
                opening_y = opening_start_y
                score = 0


        # After either pass or hit, the execution continues from
        # here

        # Now we check if the obstacle has travelled all the way to
        # the left side and award the player a point and randomize
        # the height of the next opening
        # random.randrange(a,b) gives an integer between the given parameters
        if opening_x < 0 - block_size:
            score += 1
            # Reset opening and obstacles to the right side
            # and randomize a sensible height for the opening
            opening_x = screen_width
            opening_y = random.randrange(opening_height, screen_height - opening_height)

        # Finally we draw the game
        # .blit is a function that copies Surface data to the
        # screen buffer, that is also a Surface. Successive
        # blits draw over earlier ones, so we must start
        # from the back
        screen.blit(background, (0, 0))
        screen.blit(bird_image, (bird_x, bird_y))

        # Draw blocks on the both sides of the opening until
        # they reach the window borders
        # Blocks above are drawn upwards until the next drawn
        # block would no longer be visible on the screen
        block_above_y = opening_y - block_size
        while block_above_y > -block_size:
            screen.blit(block_image, (opening_x, block_above_y))
            block_above_y -= block_size

        # Blocks below are drawn until top left corner is outside screen
        block_below_y = opening_y + opening_height
        while block_below_y < screen_height:
            screen.blit(block_image, (opening_x, block_below_y))
            block_below_y += block_size

        # Finally we update the window title with the score of the player
        # .format( ) places the parameter to the text
        text = "Flappi Byrd - Score {0}".format(score)
        pygame.display.set_caption(text)

        # This call tells Windows that we have drawn everything and that
        # it should update the contents of the window
        pygame.display.flip()

        # tick() stalls execution until wanted time has
        # passed. 30 FPS means to stall for 33 milliseconds
        milliseconds = clock.tick(FPS)
        seconds = milliseconds / 1000.0

    # Main loop ends
    pygame.quit()

    # And thats all folks.

if __name__ == "__main__":
    main()

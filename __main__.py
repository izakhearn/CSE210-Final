import random

from game.casting.actor import Actor
from game.casting.invaders import Invaders
from game.casting.cast import Cast

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 15
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
FONT_SIZE = 40
COLS = 60
ROWS = 40
CAPTION = "Space Invaders"
WHITE = Color(255, 255, 255)
DEFAULT_invadersS = 40


def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(15)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the ship
    x = int(MAX_X / 2)
    y = 500
    position = Point(x, y)

    ship = Actor()
    ship.set_text('_|^|_')
    ship.set_font_size(FONT_SIZE)
    ship.set_color(WHITE)
    ship.set_position(position)
    cast.add_actor("ship", ship)
    
    #Create the first 50 invaders
    for i in range(10):
        rock_gem = '% ^ %'
        text = rock_gem

        x = (COLS - i)
        y = ROWS
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        invaders = Invaders()
        invaders.set_text(text)
        invaders.set_font_size(FONT_SIZE)
        invaders.set_color(color)
        invaders.set_position(position)
        #invaders.set_message(message)
        cast.add_actor("invaders", invaders)
    
    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)



if __name__ == "__main__":
    main()
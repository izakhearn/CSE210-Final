
from game.shared.point import Point
from game.shared.color import Color
from game.casting.invaders import Invaders
from game.casting.bullet import Bullet
from game.casting.cast import Cast
from game.casting.actor import Actor
import random
class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """
    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        self._shooting = False
        self._laser_shooting = False
        self._game_over = False
        self._lives= 3
        self._count = 0
        self._end = False
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._falling_invaders(cast)
            self._shoot(cast)
            self._invader_shoot(cast)
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
            while self._game_over:
                self._end_game(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the ship.
        
        Args:
            cast (Cast): The cast of actors.
        """
        ship = cast.get_first_actor("ship")
        velocity = self._keyboard_service.get_direction()
        ship.set_velocity(velocity)
        X = ship.get_position().get_x()
        Y = ship.get_position().get_y()
        if ship.get_position().get_y() < 450:
            ship.set_position(Point(ship.get_position().get_x(),559))
        if ship.get_position().get_y() > 560:
            ship.set_position(Point(ship.get_position().get_x(),451))
        

    def _do_updates(self, cast):
        """Updates the ship's position and resolves any collisions with invaders.
        
        Args:
            cast (Cast): The cast of actors.
        """
        banner = cast.get_first_actor("banners")
        ship = cast.get_first_actor("ship")
        invaders = cast.get_actors("invaders")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        ship.move_next(max_x, max_y)
        
        for invaders in invaders:
            pos_x = ship.get_position().get_x()
            pos_y = ship.get_position().get_y()
            art_y = invaders.get_position().get_y()
            art_x = invaders.get_position().get_x()
            hit_x = pos_x - art_x
            hit_y = pos_y - art_y
            if (-10 < hit_x < 10) and (-10 < hit_y < 10):
                if invaders.get_text() == "o":
                    self._score += -1
                if invaders.get_text() == "*":
                    self._score += 1
                cast.remove_actor("invaders", invaders)
        banner.set_text(f"Score: {self._score}"+f" Lives: {self._lives}")    
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
    
    def _falling_invaders(self, cast):
        """Makes the invaders fall.
        
        Args:
            cast (Cast): The cast of actors.
        """

    #Move Invaders by 10 in one direction then in 10 the opposite direction
        invaders = cast.get_actors("invaders")
        for invaders in invaders:
            if self._count < 20:
                invaders.set_position(Point(invaders.get_position().get_x()-5,invaders.get_position().get_y()))
            if self._count >= 20:
                invaders.set_position(Point(invaders.get_position().get_x()+5,invaders.get_position().get_y()))
        if self._count == 40:
            self._count = 0
        self._count += 1

        invaders = cast.get_actors("invaders")
        if len(invaders) < 20:
            for i in range(1):
                COLS = 60
                ROWS = 40
                CELL_SIZE = 15
                FONT_SIZE = 15
                rock_gem = '% ^ %'
                text = rock_gem

                x = random.randint(1, COLS - 1)
                y = (random.randint(0, 5))
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

    def _shoot(self, cast):
        """Makes the ship shoot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        ship = cast.get_first_actor("ship")
        if (self._keyboard_service.get_spacebar()) and (self._shooting == False):
                    self._shooting == True
                    bullet = Bullet()
                    bullet.set_text("o")
                    bullet.set_font_size(10)
                    bullet.set_color(Color(255, 255, 255))
                    bullet.set_position(ship.get_position().add(Point(0, -10)))
                    bullet.set_velocity(Point(0, -1))
                    cast.add_actor("bullet", bullet)
        try :
            bullet = cast.get_first_actor("bullet")
            if bullet != None:
                bullet = cast.get_first_actor("bullet")
                bullet.set_position(bullet.get_position().add(Point(0, -25)))
                bullet.set_text("o")
                bullet.set_color(Color(255, 255, 255))
                bullet.set_velocity(Point(0, -1))
                bullet.set_font_size(15)
                if bullet.get_position().get_y() < -10:
                    cast.remove_actor("bullet", bullet)
                    self._shooting = False
            # Check if bullet hit an invdader
            invaders = cast.get_actors("invaders")
            for invaders in invaders:
                pos_x = bullet.get_position().get_x()
                pos_y = bullet.get_position().get_y()
                art_y = invaders.get_position().get_y()
                art_x = invaders.get_position().get_x()
                hit_x = pos_x - art_x
                hit_y = pos_y - art_y
                if (-30 < hit_x < 30) and (-15 < hit_y < 15):
                    self._score += 1
                    cast.remove_actor("bullet", bullet)
                    cast.remove_actor("invaders", invaders)
                    self._shooting = False
        except:
            pass

    def _invader_shoot(self,cast):
        #Invader shoot laser down at random
        shooter = cast.get_actors("invaders")
        shooter = random.choice(shooter)
        laser = cast.get_actors("laser")
        if (len(laser)<5) or (laser==None):
                    self._laser_shooting == True
                    laser = Bullet()
                    laser.set_text("|")
                    laser.set_font_size(10)
                    laser.set_color(Color(255, 255, 255))
                    laser.set_position(shooter.get_position().add(Point(0, 10)))
                    cast.add_actor("laser", laser)
        try :
            laser = cast.get_actors("laser")
            for laser in laser:
                laser.set_position(laser.get_position().add(Point(0, 25)))
                laser.set_text("|")
                laser.set_color(Color(255, 255, 255))
                laser.set_velocity(Point(0, 1))
                laser.set_font_size(15)
                if laser.get_position().get_y() > 600:
                    cast.remove_actor("laser", laser)
                    self._laser_shooting = False
                ship = cast.get_first_actor("ship")
                pos_x = laser.get_position().get_x()
                pos_y = laser.get_position().get_y()
                art_y = ship.get_position().get_y()
                art_x = ship.get_position().get_x()
                hit_x = pos_x - art_x
                hit_y = pos_y - art_y
                if (-40 < hit_x < 40) and (-30 < hit_y < 30):
                    self._lives += -1
                    cast.remove_actor("laser", laser)
                    self._laser_shooting = False
                if self._lives == 0:
                    self._game_over = True
            # Check if laser hit an invader
        except:
            pass

    def _end_game(self, cast):
        """Ends the game.
        
        Args:
            cast (Cast): The cast of actors.
        """
        message = Actor()
        message.set_text("Game Over!")
        position = Point(100, 100)
        message.set_position(position)
        message.set_font_size(40)
        cast.add_actor("messages", message)
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()


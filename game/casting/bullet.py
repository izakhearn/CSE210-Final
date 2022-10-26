from game.casting.actor import Actor

# TODO: Implement the invaders class here. Don't forget to inherit from Actor!

class Bullet(Actor):

    def __init__(self):
        super().__init__()
    
    def set_message(self, message):
        self.message = message
    
    def get_message(self):
        return self.message
        
    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_font_size(self, font_size):
        self.font_size = font_size
    


    
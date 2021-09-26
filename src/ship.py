from laser import *
from constantes import *

class Ship:
   
    COOLDOWN = 30
   
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
        
    def draw(self, window):
        # Simulation vaisseau (ligne en-dessous)
        # pygame.draw.rect(window, (255,0,0), (self.x, self.y, 50, 50), 1)
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)
    
    # Revoir passage cooldown des tirs
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
        
    # Si je tire, je dois récupérer
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser) 
            self.cool_down_counter = 1
        
    # Récupérer les dimensions du vaisseau (joueur ou ennemi)
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

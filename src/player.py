from constantes import *
from ship import Ship

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)  # cf Classe parente
        self.ship_img = yellow_sprite
        self.laser_img = yellow_laser
        self.COOLDOWN = 20
        
        # Détection de pixels pour créer le masque de collision
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
                
    # Création barre de santé        
    def healthbar(self, window):
        # Santé max en fonction de la largeur du player
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 2))
        # Santé actuelle avec l'argument health (création pourcentages)
        pygame.draw.rect(window, (255,181,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 2))
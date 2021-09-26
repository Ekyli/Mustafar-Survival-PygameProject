from constantes import *
from ship import Ship

class Enemy(Ship):
    
    # Créer array pour vaisseaux couleur différente
    generate_color = {
        "red": (red_sprite, red_laser),
        "green": (green_sprite, green_laser),
        "blue": (blue_sprite, blue_laser)
    }
    
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health) # cf Classe parente
        self.ship_img, self.laser_img = self.generate_color[color]
        
        # Détection de pixels pour créer le masque de collision
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel
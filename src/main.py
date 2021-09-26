import random
from constantes import *

from player import *
from enemy import *

pygame.font.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projet Python | Lucas Schrever")


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def move_lasers(tab_laser, vel, objs):
    for laser in tab_laser:
        laser.move(vel)
        if laser.off_screen(HEIGHT):
            tab_laser.remove(laser)
        else:
            for obj in objs:
                if collide(laser, obj):
                    if type(obj) == Player:
                        obj.health -= 10
                    else:
                        objs.remove(obj)
                    if laser in tab_laser:
                        tab_laser.remove(laser)

def main():
    run = True
    FPS = 60
    level = 0   # Fait partie du HUD
    pv = 1   # Fait partie du HUD
    HUD = pygame.font.SysFont("edgeofthegalaxyregular", 20)
    lossphrase = pygame.font.SysFont("edgeofthegalaxyposter", 50)
    
    enemies = []
    wave_length = 0   # Fait partie du HUD
    enemy_vel = 1
    
    player_vel = 3
    laser_vel = 3
    
    player = Player(250, 550)

    clock = pygame.time.Clock() 
    
    defeat = False
    loss_count = 0

    def redraw_window():
        WIN.blit(BG, (0,0))
        
        # Je teste une différenciation de couleurs (par exemple, les PVs en vert, les vagues d'ennemis en rouge, et le level en jaune)        
        pv_label = HUD.render(f"PV :", 1, (116,116,116))
        level_label = HUD.render(f"Niveau :", 1, (116,116,116))
        enemy_counter = HUD.render(f"Vague d'ennemis", 1, (116,116,116))
        WIN.blit(pv_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 20,10))
        WIN.blit(enemy_counter, (WIDTH/2 - enemy_counter.get_width()/2,10))
        
        pv_span = HUD.render(f"{pv}", 1, (47,234,0))
        enemy_counter_span = HUD.render(f"{wave_length}", 1, (233,0,0))
        level_span = HUD.render(f"{level}", 1, (224,217,0))
        WIN.blit(pv_span, (pv_label.get_width()+15,10))    # Offset en tâtonnant pour les 6 positions
        WIN.blit(level_span, (WIDTH-15,10))
        WIN.blit(enemy_counter_span, (WIDTH/2 - enemy_counter_span.get_width()/2,40))
        
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)
        
        # Faire apparaître message de défaite
        if defeat == True:
            loss_label = lossphrase.render("VOUS N'ETES PAS L'ELU", 1, (220,129,14))
            WIN.blit(loss_label, (WIDTH/2 - loss_label.get_width()/2, HEIGHT/2))
        
        
        pygame.display.update()

    while run:
        player.cooldown()
        clock.tick(FPS) 
        redraw_window()
         
        if pv <= 0 or player.health <= 0:
            defeat = True
            loss_count += 1
             
        # Si la défaite est déclarée, le jeu s'arrête 3 secondes plus tard (calcul en fonction du FPS établi)
        if defeat:
            if loss_count > FPS * 3:
                run = False
            else:
                continue

        # Si compteur d'ennemis égal à 0 (j'ai battu tout le monde), alors passage niveau supérieur
        if len(enemies) == 0:
            level += 1
            pv += 2
            wave_length += 3
            laser_vel += 1
            
            if pv >= 10:
                player.health = 100
            
            # Faire apparaître les ennemis à une position aléatoire au dessus du canvas
            for i in range(wave_length):
                enemy = Enemy(random.randrange(70, WIDTH-70), random.randrange(-600, -100), random.choice(["red", "blue", "green"])) # Revoir la commande random.randrange
                enemies.append(enemy)

        for event in pygame.event.get():   
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            run = False
            start_menu()
        
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # Vélocité + position horiontale + largeur du player inférieures à la largeur d'écran
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # Vélocité + position verticale + hauteur du player inférieures à la hauteur d'écran (+ n pour la healthbar)
            player.y += player_vel
            
        if keys[pygame.K_a]:
            player.shoot()
            
        # Si un ennemi touche le bas de l'écran, je perds une vie et l'ennemi disparaît
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(0, 2*60) == 1: # l'ennemi shoote au pif
                enemy.shoot()
                
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                pv -= 1
                enemies.remove(enemy)
                
        # Le laser_vel doit être négatif pour que le tir aille en haut
        player.move_lasers(-laser_vel, enemies)

def start_menu():
    headline = pygame.font.SysFont("edgeofthegalaxyposter", 60)
    click = pygame.font.SysFont("consolas", 18)
    run = True
    
    while run:
        WIN.blit(BG, (0,0))
        titlephrase = headline.render("Mustafar Survival", 1, (141,16,16))
        clickphrase = click.render("(clic-gauche) > Initiation combat", 1, (253,148,148))
        rulesphrase = click.render("(touche i) > Feuille de mission", 1, (253,148,148))
        WIN.blit(titlephrase, (WIDTH/2 - titlephrase.get_width()/2, HEIGHT/2-50))
        WIN.blit(clickphrase, (WIDTH/2 - titlephrase.get_width()/2, HEIGHT/3*2-50))
        WIN.blit(rulesphrase, (WIDTH/2 - titlephrase.get_width()/2, HEIGHT/3*2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                main()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    rules()
                
    pygame.quit()
                      
def rules():
    rules_headline = pygame.font.SysFont("edgeofthegalaxyposter", 30)
    rules_typo = pygame.font.SysFont("consolas", 16)
    run = True
    
    while run:
        WIN.blit(BG, (0,0))
        rules_title = rules_headline.render("VOTRE OBJECTIF DE MISSION", 1, (141,16,16))
        rules_title = rules_headline.render("VOTRE OBJECTIF DE MISSION", 1, (141,16,16))
        rules_content = rules_typo.render("Nom de code de la mission : Space Invaders", 1, (163,163,163))
        rules_content1 = rules_typo.render("Toute source hostile sur votre radar doit être éliminée", 1, (163,163,163))
        rules_content2 = rules_typo.render("Vous vous battrez indéfiniment et sans possibilité d'extraction", 1, (163,163,163))
        rules_content3 = rules_typo.render("Vous allez être challengé sur votre endurance", 1, (163,163,163))
        rules_content4 = rules_typo.render("Que la force soit avec vous...", 1, (163,163,163))
        rules_content_start = rules_typo.render("(clic-gauche) > Initier le combat", 1, (228,228,228))
        WIN.blit(rules_title, (WIDTH/2 - rules_title.get_width()/2, HEIGHT/3))
        WIN.blit(rules_content, (WIDTH/2 - rules_content.get_width()/2, HEIGHT/2-50))
        WIN.blit(rules_content1, (WIDTH/2 - rules_content1.get_width()/2, HEIGHT/2-30))
        WIN.blit(rules_content2, (WIDTH/2 - rules_content2.get_width()/2, HEIGHT/2-10))
        WIN.blit(rules_content3, (WIDTH/2 - rules_content3.get_width()/2, HEIGHT/2+20))
        WIN.blit(rules_content4, (WIDTH/2 - rules_content4.get_width()/2, HEIGHT/2+50))
        WIN.blit(rules_content_start, (WIDTH/2 - rules_content4.get_width()/2, HEIGHT/2+100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_menu()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                main()
                
    pygame.quit()
    
start_menu()





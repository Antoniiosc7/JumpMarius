from entities import Player, Enemy
from utils import load_image, load_images, Animation
from tilemap import Tilemap
from clouds import Clouds
from spark import Spark
import random, math, sys, pygame, os, utils
import menus.index as menus
from particle import Particle
class Juego:
    def __init__(self, resolution=None):
        pygame.init()
        if resolution:
            self.current_resolution = resolution
            self.screen = pygame.display.set_mode(self.current_resolution)
        else:
            self.current_resolution = resolution
        self.selected_character = "Player1"  
        self.screen = pygame.display.set_mode(self.current_resolution)
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.display.set_caption("Jump Marius")
        self.screen_display = (640, 480)
        self.current_resolution = self.screen_display
        self.display = pygame.Surface((320, 240), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((320, 240))
        image_path = os.path.join("recursos/visualizaciones/", f"{self.selected_character}.png")
        self.icon = pygame.image.load("recursos/logo.png")
        pygame.display.set_icon(self.icon)
        self.death_count = 0  # Contador de muertes
        self.clock = pygame.time.Clock()
        self.movement = [False, False]
        self.puntuacion = 0  


        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'hierba': load_images('tiles/newTiles/blocksHierba'),
            'nevados': load_images('tiles/newTiles/blocksNevados'),
            'quemados': load_images('tiles/newTiles/blocksQuemados'),
            'normal': load_images('tiles/newTiles/normalBlocks'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'gun': load_image('gun.png'),
            'projectile': load_image('projectile.png'),
            'spawners': load_images('tiles/spawners'),
            'final': load_images('tiles/final')
        }
        self.sfx = {
            'jump': pygame.mixer.Sound('recursos/sfx/jump.wav'),
            'dash': pygame.mixer.Sound('recursos/sfx/dash.wav'),
            'hit': pygame.mixer.Sound('recursos/sfx/hit.wav'),
            'shoot': pygame.mixer.Sound('recursos/sfx/shoot.wav'),
            'dead': pygame.mixer.Sound('recursos/sfx/dead.mp3'),
            'ambience': pygame.mixer.Sound('recursos/sfx/ambience.wav'),
            'fondo': pygame.mixer.Sound('recursos/sfx/music.wav')
        }
        
        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)
        self.sfx['dead'].set_volume(0.3)
        self.sfx['fondo'].set_volume(0.1)
        self.load_configuration()
        self.clouds = Clouds(self.assets['clouds'], count=16)  
        self.player = Player(self, (50, 50), (8, 15))
        self.level = 0
        self.tilemap = Tilemap(self, tile_size=16)
        self.load_level()
        self.screenshake = 0
        self.scroll = [0, 0]
    
    def load_level(self):
        selected_level = utils.load_selected_level_from_csv()
        selected_character = utils.load_selected_character_from_csv()
        self.load_configuration()
        #self.tilemap.load('mapas/map' + str(map_id)    + '.json')
        map_path = os.path.join('mapas/', f'{selected_level}.json')
        self.selected_character = selected_character
            # Cargar el nivel desde el archivo JSON
        self.tilemap.load(map_path)

        #self.tilemap.load('map.json')
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0

    def load_configuration(self):
        
        print("player seleccionado :", self.selected_character )
        # Cargar configuración desde el archivo config.csv
        config_path = 'config.csv'
        with open(config_path, 'r') as config_file:
            lines = config_file.readlines()
            for line in lines:
                values = list(map(str.strip, line.split(',')))
                if len(values) == 2:
                    key, value = values
                    if key == 'Character':
                        self.selected_character = value

        # Actualizar las rutas de las imágenes y animaciones según el personaje seleccionado
        character_path = f'entities/{self.selected_character.lower()}'
        self.assets['player'] = load_image(f'{character_path}/player.png')
        self.assets['player/idle'] = Animation(load_images(f'{character_path}/idle'), img_dur=6)
        self.assets['player/run'] = Animation(load_images(f'{character_path}/run'), img_dur=4)
        self.assets['player/jump'] = Animation(load_images(f'{character_path}/jump'))
        self.assets['player/slide'] = Animation(load_images(f'{character_path}/slide'))
        self.assets['player/wall_slide'] = Animation(load_images(f'{character_path}/wall_slide'))
    def reset_game(self):
        # Restablecer todas las variables del juego a su estado inicial
        self.movement = [False, False]
        # Reiniciar el jugador
        self.player.reset_position()
        self.player.reset_state()

        # Reiniciar el mapa de tiles
        self.tilemap = Tilemap(self, tile_size=16)
        self.load_level()  # Asegúrate de cargar el nivel nuevamente

        # Reiniciar las nubes
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Reiniciar el desplazamiento
        self.scroll = [0, 0]


    
    def run(self):
        while True:
            
            menus.index(self.screen, self, 1)  # Ejecutar el menú antes del bucle principal del juego
            while True:               
                self.display.blit(self.assets['background'], (0, 0))
                self.screenshake = max(0, self.screenshake - 1)               
                if self.dead:
                    self.dead += 1
                    self.death_count += 1
                    game_over_option = menus.index(self.screen, self,3)

                    # Realiza acciones basadas en la opción seleccionada
                    if game_over_option == "restart":
                        self.reset_game()
                    elif game_over_option == "main_menu":
                        return menus.index(self.screen, self,1)
                    if self.dead > 40:
                        self.load_level()
                
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                #self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                
                self.clouds.update()
                self.clouds.render(self.display, offset=render_scroll)
                
                self.tilemap.render(self.display, offset=render_scroll)

                for enemy in self.enemies.copy():
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy)
                
                if not self.dead:
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)
                
                # [[x, y], direction, timer]
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['projectile']
                    self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                    if self.tilemap.solid_check(projectile[0]):
                        self.projectiles.remove(projectile)
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif projectile[2] > 360:
                        self.projectiles.remove(projectile)
                        
                    elif abs(self.player.dashing) < 50:
                        if self.player.rect().collidepoint(projectile[0]):
                            self.projectiles.remove(projectile)
                            self.dead += 1
                            self.sfx['hit'].play()
                            self.screenshake = max(16, self.screenshake)
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 5
                                self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                                self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                            
                    
                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)
                display_mask = pygame.mask.from_surface(self.display)
                display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))
                for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    self.display_2.blit(display_sillhouette, offset)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)
                
                for enemy in self.enemies.copy():
                    kill_enemy = Player.check_enemy_collision(self.player, enemy)
                    enemy.render(self.display, offset=render_scroll)
                    if kill_enemy:
                        self.enemies.remove(enemy)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill: 
                        self.particles.remove(particle)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movement[1] = True
                        if event.key == pygame.K_UP: # Check if the player is on the ground
                            self.player.jump()  # Call the jump method
                            self.sfx['jump'].play()
                        if event.key == pygame.K_x:
                            self.player.dash()
                        elif event.key == pygame.K_ESCAPE:
                            restart_option = menus.index(self.screen, self,2)  # Llama a la función del menú de reinicio
                            if restart_option == "restart":
                                self.reset_game()
                                break  # Salir del bucle interno para reiniciar el juego
                            elif restart_option == "main_menu":
                                break  # Salir del bucle interno para volver al menú principal

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movement[0] = False
                        elif event.key == pygame.K_RIGHT:
                            self.movement[1] = False
                final = self.tilemap.get_x_of_final_block() - 8
                #print("Final: ", final)
                #print("Player: ", self.player.pos[0])
                if self.player.pos[0] >= final:
                    print("Has ganado")
                    menus.index(self.screen, self,4)
    
                player_rect = pygame.Rect(self.player.pos[0], self.player.pos[1], self.player.size[0], self.player.size[1])

                font = pygame.font.Font(None, 36)
                text = font.render(f"Puntuacion: {self.puntuacion}", True, (255, 255, 255))
                text_rect = text.get_rect()
                text_rect.topleft = (self.current_resolution[0] - text_rect.width - 10, 10)
                self.display_2.blit(self.display, (0, 0))
                 

                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)
                pygame.display.update()
                self.clock.tick(60)
    def change_resolution(self, resolution):
        self.current_resolution = resolution
        self.screen = pygame.display.set_mode(self.current_resolution)
    def get_selected_character(self):
        return self.selected_character
    def set_selected_character(self, new_character):
        self.selected_character = new_character
        print("Establecido como personaje: " + self.selected_character)
    def change_resolution(self, resolution):
        self.current_resolution = resolution
        self.screen = pygame.display.set_mode(self.current_resolution)
        self.display = pygame.Surface((resolution[0] // 2, resolution[1] // 2), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((resolution[0] // 2, resolution[1] // 2))
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
      
        

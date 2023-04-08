import pygame, sys, os, random
from pygame.locals import *

vec = pygame.math.Vector2

offset = vec(0, 0)

# define current path.
current_path = os.path.dirname(__file__)

# define image path.
image_path = os.path.join(current_path, "images")

class button(pygame.sprite.Sprite):
    def __init__(self):
        super(button, self).__init__()

        size = (320, 110)
        
        self.images = [pygame.image.load(os.path.join(image_path, "start.png")),
                       pygame.image.load(os.path.join(image_path, "startreverse.png"))] 

        self.rect = pygame.Rect((240, 350), size)
        self.image = self.images[0]

    def update(self):
        global gamestart, is_tutorial
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_L, button_M, button_R = pygame.mouse.get_pressed()

        if self.rect.collidepoint(mouse_x, mouse_y) == True:
            self.image = self.images[1]
            if button_L == 1:
                is_tutorial = True
        else:
            self.image = self.images[0]

class restart(pygame.sprite.Sprite):
    def __init__(self):
        super(restart, self).__init__()

        size = (110, 110)

        self.image = pygame.image.load(os.path.join(image_path, "restart.png"))
        self.rect = pygame.Rect((345, 550), size)

    def update(self):
        global gamestart, is_tutorial, enemy_spawn, reason1, reason2, reason3, Flag, boss_appear, pattern_excute, pattern1_effect, pattern2_effect, boss_music
        global tutorial_time, MAX_ENEMY, create_time, zombie_kill, nohit_time, diff_offset, pattern0_time, warning_time, pattern_choose
        global Button, Restart, User, User_weapon, Boss, effect, time_machine
        global main_sprites, all_sprites, ending_sprites, zombies
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_L, button_M, button_R = pygame.mouse.get_pressed()

        size = (110, 110)

        self.rect = pygame.Rect((345, 350), size)
        
        if self.rect.collidepoint(mouse_x, mouse_y) == True:
            if button_L == 1:
                gamestart = False
                self.rect = pygame.Rect((345, 550), size)

                tutorial_time = 0
                MAX_ENEMY = 50
                create_time = 0
                zombie_kill = 0
                nohit_time = 0
                diff_offset = vec(0, 0)
                pattern0_time = 0
                warning_time = 0
                pattern_choose = 3

                gamestart = False
                is_tutorial = False
                enemy_spawn = True
                reason1 = False
                reason2 = False
                reason3 = False
                Flag = True
                boss_appear = False
                pattern_excute = False
                pattern1_effect = False
                pattern2_effect = False
                boss_music = False

                Button = button()
                Restart = restart()

                User = player()
                User_weapon = weapon()

                for i in zombies[:]:
                        i.rect.y -= 500
                        zombies.remove(i)
                
                Boss = boss()
                effect = boss_effect()

                time_machine = timemachine()

                main_sprites = pygame.sprite.Group(Button)

                all_sprites = pygame.sprite.Group(time_machine)
                all_sprites.add(User_weapon)
                all_sprites.add(User)
                all_sprites.add(effect)
                all_sprites.add(Boss)

                ending_sprites = pygame.sprite.Group(Restart)


    
class player(pygame.sprite.Sprite):
    """player Class"""

    def __init__(self):
        super(player, self).__init__()

        size = (48, 48)

        self.walkRight = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "move1.png")), size),
                          pygame.transform.scale(pygame.image.load(os.path.join(image_path, "move2.png")), size),
                          pygame.transform.scale(pygame.image.load(os.path.join(image_path, "move3.png")), size),
                          pygame.transform.scale(pygame.image.load(os.path.join(image_path, "move4.png")), size)]
        
        self.walkLeft = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "move1.png")), True, False), size),
                         pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "move2.png")), True, False), size),
                         pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "move3.png")), True, False), size),
                         pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "move4.png")), True, False), size)]


        self.health_bar = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp0.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp1.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp2.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp3.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp4.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp5.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp6.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp7.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp8.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp9.png")), (140, 20)),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "hp10.png")), (140, 20))]


        stopRight = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "stop.png")), size)
        stopLeft = pygame.transform.flip((pygame.transform.scale(pygame.image.load(os.path.join(image_path, "stop.png")), size)), True, False)
        self.stopMotion = [stopRight, stopLeft]

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "stop.png")), size)
        self.index = 0

        self.images = self.walkRight
        
        self.rect = pygame.Rect((376, 390), size)
    
        self.current_time = 0
        self.animation_time = 0.05


        self.health = 10
        
        self.F = 0
        self.v = 5
        self.m = 1
    
    def movement(self):
        global moveLeft
        global moveRight
        global boss_appear
        
        if moveLeft and self.rect.left > 0:
            if self.rect.centerx == 400:
                if offset.x <= -875 or boss_appear is True:
                    self.rect.centerx -= 5
                else:
                    offset.x -= 5
            else:
                self.rect.centerx -= 5
                
        if moveRight and self.rect.right < WINDOWWIDTH:
            if self.rect.centerx == 400:
                if offset.x >= 875 or boss_appear is True:
                    self.rect.centerx += 5
                else:
                    offset.x += 5
            else:   
                self.rect.centerx += 5

    def jump(self):
        global isjump
        if isjump:
            # calculate force (F). F = 1 / 2 * mass * velocity ^ 2.
            self.F =(1 / 2) * self.m * (self.v ** 2)
               
            # change in the y co-ordinate
            self.rect.centery -= self.F
               
            # decreasing velocity while going up and become negative while coming down
            self.v = self.v - 0.5
            # object reached its maximum height
            if self.v < 0:
                # negative sign is added to counter negative velocity
                self.m = -1

            if self.rect.bottom > WINDOWHEIGHT - 60:
                self.rect.bottom = WINDOWHEIGHT - 60
            
            # objected reaches its original state
            if self.v == -7:
                # making isjump equal to false 
                isjump = False
      
                # setting original values to v and m
                self.v = 5
                self.m = 1

    def update(self):
        global mt
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if mouse_x > self.rect.centerx:
                self.images = self.walkRight
                if moveRight or moveLeft is True:
                    self.index += 1

                    if self.index >= len(self.images):
                        self.index = 0
                        
                    self.image = self.images[self.index]
                    
                else:
                    self.image = self.stopMotion[0]
            else:
                self.images = self.walkLeft
                if moveRight or moveLeft is True:
                    self.index += 1

                    if self.index >= len(self.images):
                        self.index = 0

                    self.image = self.images[self.index]
                    
                else:
                    self.image = self.stopMotion[1]

class weapon(pygame.sprite.Sprite):
    """player's weapon class"""
    def __init__(self):
        super(weapon, self).__init__()

        size = (48, 48)

        self.swordmotion = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword1.png")), size),
                            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword2.png")), size),
                            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword3.png")), size),
                            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword4.png")), size),
                            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword5.png")), size),
                            pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword6.png")), size),]
        
        self.filp_swordmotion = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword1.png")), True, False), size),
                                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword2.png")), True, False), size),
                                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword3.png")), True, False), size),
                                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword4.png")), True, False), size),
                                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword5.png")), True, False), size),
                                 pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "attack_sword6.png")), True, False), size),]

        
        self.rect = pygame.Rect((5, 400), (64, 64))

        self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "attack_sword1.png")), size)
        self.images = self.swordmotion

        self.current_time = 0
        self.animation_time = 0.02
        
        self.index = 0

        self.is_attack = 0
            
        self.status = "sword"

    def tracking_player(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_x > User.rect.centerx:
            self.rect.centerx = User.rect.right - 8
            self.image = self.swordmotion[0]
        else:
            self.rect.centerx = User.rect.left + 24
            self.image = self.filp_swordmotion[0]
            
        self.rect.centery = User.rect.centery

    def attack(self):
        button_L, button_M, button_R = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.current_time += mt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if button_L == 1:
                if mouse_x > User.rect.centerx:
                    self.images = self.swordmotion
                else:
                    self.images = self.filp_swordmotion

                self.index += 1

                if self.index >= len(self.images):
                    self.index = 0
                        
                self.image = self.images[self.index]

                self.is_attack = 0

            else:
                self.is_attack = 1

class zombie(pygame.sprite.Sprite):
    """Zombie Class"""
    def __init__(self):
        super(zombie, self).__init__()
        self.spawnpoint = random.randint(0, 1)
        self.target = random.randint(0, 1)
        self.type = random.randint(0, 9)

        size = (48, 48)

        if self.type >= 0 and self.type <= 5:
            # define default type
            self.motion = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "zombie_move1.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "zombie_move2.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "zombie_move3.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "zombie_move4.png")), size)]
        
            self.filp_motion = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "zombie_move1.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "zombie_move2.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "zombie_move3.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "zombie_move4.png")), True, False), size)]
            
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "zombie_move1.png")), size)

            self.health = 5
            self.movespeed = 2
            self.attack_point = 2
            
        elif self.type >= 6 and self.type <= 8:
            # define speed type
            self.motion = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "speed_move1.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "speed_move2.png")), size)]
        
            self.filp_motion = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "speed_move1.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "speed_move2.png")), True, False), size)]
            
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "speed_move1.png")), size)

            self.health = 3
            self.movespeed = 3
            self.attack_point = 1
                        
        else:
            # defnie power type
            self.motion = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move1.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move2.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move3.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move4.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move5.png")), size),
                           pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move6.png")), size)]
        
            self.filp_motion = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move1.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move2.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move3.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move4.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move5.png")), True, False), size),
                                pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "power_move6.png")), True, False), size)]
            
            self.image = pygame.transform.scale(pygame.image.load(os.path.join(image_path, "power_move1.png")), size)

            self.health = 10
            self.movespeed = 1
            self.attack_point = 4
        
        self.images = self.motion

        self.index = 0
        
        if self.spawnpoint == 0:
            self.rect = pygame.Rect((-400, 395), size)
        else:
            self.rect = pygame.Rect((1200, 395), size)

    def update(self):
        if self.target == 0:
            if User.rect.centerx < self.rect.centerx:
                self.images = self.motion
            else:
                self.images = self.filp_motion
        else:
            if time_machine.rect.centerx < self.rect.centerx:
                self.images = self.motion
            else:
                self.images = self.filp_motion

        self.index += 1

        if self.index >= len(self.images):
            self.index = 0
                    
        self.image = self.images[self.index]
        

    def movement(self):

        global offset
        
        # 0 is player
        if self.target == 0:
            if User.rect.centerx > self.rect.centerx:
                self.rect.centerx += self.movespeed
            else:
                self.rect.centerx -= self.movespeed

        # 1 is timemachine
        else:
            if time_machine.rect.left > self.rect.right:
                self.rect.centerx += self.movespeed
            elif time_machine.rect.right < self.rect.left:
                self.rect.centerx -= self.movespeed

        
    def collision(self, weapon):
        if pygame.Rect.colliderect(self.rect, weapon.rect) == 1 and weapon.is_attack == 0:
            if User.rect.centerx > self.rect.centerx:
                self.rect.centerx -= 30
            else:
                self.rect.centerx += 30

            self.health -= 3

class timemachine(pygame.sprite.Sprite):
    def __init__(self):
        super(timemachine, self).__init__()


        self.rect = pygame.Rect((280, 280), (78, 162))
        self.image = pygame.image.load(os.path.join(image_path, "timemachine2.png"))
        self.health = 150

class boss(pygame.sprite.Sprite):
    def __init__(self):
        super(boss, self).__init__()


        size = (180, 160)
        size2 = (140, 160)

        self.pattern1_image = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern1.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern2.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern3.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern4.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern5.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern6.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern7.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern8.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern9.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern10.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern11.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern12.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern13.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern14.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern15.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern16.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern17.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern18.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern19.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern20.png")), size), True, False),
                              pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern21.png")), size), True, False)]

        self.pattern2_image = [pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_1.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_2.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_3.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_4.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_5.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_6.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_7.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_8.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_9.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_10.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_11.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_12.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_13.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_14.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_15.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_16.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_17.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_18.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_19.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_20.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_21.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_22.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_23.png")), size2),
                               pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern_2_24.png")), size2)]

        self.pattern3_image = [pygame.image.load(os.path.join(image_path, "boss_stand1.png")),
                               pygame.image.load(os.path.join(image_path, "boss_stand2.png")),
                               pygame.image.load(os.path.join(image_path, "boss_stand3.png")),
                               pygame.image.load(os.path.join(image_path, "boss_stand4.png")),
                               pygame.image.load(os.path.join(image_path, "boss_stand5.png")),
                               pygame.image.load(os.path.join(image_path, "boss_stand6.png"))]

        self.rect = pygame.Rect((-270, 270), size)
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(os.path.join(image_path, "pattern1.png")), size), True, False)
        self.images = self.pattern1_image
        self.index = 0
        self.current_time = 0
        self.x = random.randint(100, 600)
        self.repeat = 0
        self.health = 1000
        
    def pattern1_motion(self):
        global mt, pattern1_effect
        
        size = (180, 180)
        self.current_time += mt
        if self.current_time >= 0.1:
            self.current_time = 0
            
            self.images = self.pattern1_image
            self.rect = pygame.Rect((0, 295), size)
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
                pattern1_effect = True
                        
            self.image = self.images[self.index]
            
    def pattern2_motion(self):
        global mt, pattern2_effect
        
        size = (140, 160)
        self.current_time += mt
        if self.current_time >= 0.15:
            self.current_time = 0
            
            self.images = self.pattern2_image
            self.rect = pygame.Rect((0, 295), size)
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
                pattern2_effect = True
                        
            self.image = self.images[self.index]

    def pattern3_motion(self):
        global mt, pattern_excute
        
        size = (100, 160)
        self.current_time += mt
        if self.current_time >= 0.2:
            self.current_time = 0
            
            self.images = self.pattern3_image
            self.rect = pygame.Rect((self.x, 295), size)
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
                self.x = random.randint(100, 600)
                self.repeat += 1
                pattern3_sfx.set_volume(0.7)
                pattern3_sfx.play()
                if self.repeat >= 3:
                    self.repeat = 0
                    pattern_excute = False
                
            self.image = self.images[self.index]

    def collision(self, weapon):
        if pygame.Rect.colliderect(self.rect, weapon.rect) == 1 and weapon.is_attack == 0:
            self.health -= 3
        
        
        
class boss_effect(pygame.sprite.Sprite):
    def __init__(self):
        super(boss_effect, self).__init__()

        self.pattern0_laser = [pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect1.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect2.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect3.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect4.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect5.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect6.png")), True, False), (800, 30)),
                               pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect7.png")), True, False), (800, 30))]

        self.pattern1_effect = [pygame.image.load(os.path.join(image_path, "pattern_0_effect_1.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_0_effect_2.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_0_effect_3.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_0_effect_4.png"))]

        self.pattern2_effect = [pygame.image.load(os.path.join(image_path, "pattern_2_effect1.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect2.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect3.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect4.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect5.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect6.png")),
                                pygame.image.load(os.path.join(image_path, "pattern_2_effect7.png"))]
        
        self.x = random.randint(180, 700)
        
        self.warning_line = pygame.image.load(os.path.join(image_path, "warning.png"))
        self.warning_line2 = pygame.image.load(os.path.join(image_path, "warning2.png"))

        self.images = self.pattern0_laser
        self.index = 0
        self.current_time = 0
        self.repeat = 0
        self.pattern0_count = 0

        self.rect = pygame.Rect((0, -100), (800, 30))
        
        self.image = pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join(image_path, "pattern_1_effect1.png")), True, False), (800, 30))

    def pattern0(self):
        global mt, pattern_excute

        self.current_time += mt
        if self.current_time >= 0.04:
            self.current_time = 0
        
            self.rect = pygame.Rect((0, 420), (800, 30))
            self.images = self.pattern0_laser

            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
                self.pattern0_count += 1
                pattern_excute = True
                        
            self.image = self.images[self.index]

        if self.pattern0_count >= 1:
            self.rect = pygame.Rect((0, -100), (800, 30))

    def pattern1(self):
        global mt, pattern_excute, pattern1_effect

        self.current_time += mt
        if self.current_time >= 0.03:
            self.current_time = 0
        
            self.rect = pygame.Rect((180 + self.repeat * 60, 380), (60, 60))
            self.images = self.pattern1_effect

            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
                self.repeat += 1
                pattern1_sfx.set_volume(0.7)
                pattern1_sfx.play()
                if self.repeat > 12:
                    pattern_excute = False
                    pattern1_effect = False
                    self.repeat = 0
                        
            self.image = self.images[self.index]
            
    def pattern2(self):
        global mt, pattern_excute, pattern2_effect, warning_time

        self.current_time += mt
        if self.current_time >= 0.05:
            self.current_time = 0
            self.rect = pygame.Rect((self.x, -110), (90, 550))
            self.images = self.pattern2_effect

            self.index += 1
            
            if self.index >= len(self.images):
                self.index = 0
                self.repeat += 1
                self.x = random.randint(180, 700)
                warning_time = 0
                if self.repeat > 3:
                    self.rect = pygame.Rect((self.x, 550), (90, 550))
                    pattern_excute = False
                    pattern2_effect = False
                    self.repeat = 0
                    
            self.image = self.images[self.index]

    def warning(self):
        self.rect = pygame.Rect((0, 410), (800, 30))
        self.image = self.warning_line

    def warning2(self):
        self.rect = pygame.Rect((self.x, -110), (90, 550))
        self.image = self.warning_line2
                               

# Set up pygame.
pygame.init()
pygame.mixer.init()

# Set up the window.
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
canvas = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))


main_screen = pygame.image.load(os.path.join(image_path, "gametitle.png"))
background = pygame.image.load(os.path.join(image_path, "background.png"))
tutorial = pygame.image.load(os.path.join(image_path, "tutorial.png"))
gameover1 = pygame.image.load(os.path.join(image_path, "game_over_1.png"))
gameover2 = pygame.image.load(os.path.join(image_path, "game_over_2.png"))
victory = pygame.image.load(os.path.join(image_path, "victory.png"))

pattern0_sfx = pygame.mixer.Sound("sounds\pattern0.wav")
pattern1_sfx = pygame.mixer.Sound("sounds\pattern1.wav")
pattern3_sfx = pygame.mixer.Sound("sounds\pattern3.wav")

boss_bgm = pygame.mixer.music.load("boss_bgm.mp3")

pygame.mixer.music.load("background.mp3")

pygame.mixer.music.play(-1)

# Set up movement variables.
moveLeft = False
moveRight = False
isjump = False

tutorial_time = 0
MAX_ENEMY = 50
create_time = 0
zombie_kill = 0
nohit_time = 0
diff_offset = vec(0, 0)
pattern0_time = 0
warning_time = 0
pattern_choose = 2 # default 3

gamestart = False
is_tutorial = False
enemy_spawn = True
reason1 = False
reason2 = False
reason3 = False
Flag = True
boss_appear = False
pattern_excute = False
pattern1_effect = False
pattern2_effect = False
boss_music = False

pygame.display.set_caption("Time Keeper")

Button = button()
Restart = restart()

clock = pygame.time.Clock()

User = player()
User_weapon = weapon()

Boss = boss()
effect = boss_effect()

time_machine = timemachine()

zombies = []

main_sprites = pygame.sprite.Group(Button)

all_sprites = pygame.sprite.Group(time_machine)
all_sprites.add(User_weapon)
all_sprites.add(User)
all_sprites.add(effect)
all_sprites.add(Boss)

ending_sprites = pygame.sprite.Group(Restart)

while Flag:
    if gamestart is True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_w:
                    isjump = True
                     
            if event.type == KEYUP:
                if event.key == K_ESCAPE:   
                    pygame.quit()
                    sys.exit()
                if event.key == K_a:
                    moveLeft = False
                if event.key == K_d:
                    moveRight = False

        mt = clock.tick(60) / 1000
        diff_offset.x = offset.x
        
        User.movement()
        User.jump()

        User.update()
        User_weapon.tracking_player()
        User_weapon.attack()

        diff_offset.x -= offset.x
        
        create_time += mt
        nohit_time -= mt

        if create_time > 0.4 and enemy_spawn is True:
            if len(zombies) <= MAX_ENEMY:
                zombies.append(zombie())

            create_time = 0

        for i in range(0, len(zombies)):
            zombies[i].movement()
            zombies[i].update()
            zombies[i].rect.centerx += diff_offset.x
            zombies[i].collision(User_weapon)

            if zombies[i].target == 1:
                if pygame.Rect.colliderect(zombies[i].rect, time_machine.rect) == 1:
                    time_machine.health -= zombies[i].attack_point
            else:
                if pygame.Rect.colliderect(zombies[i].rect, User.rect) == 1:
                    if nohit_time < 0:
                        User.health -= zombies[i].attack_point
                        nohit_time = 0.5

            all_sprites.add(zombies[i])

        for zombie_array in zombies[:]:
            if zombie_array.health <= 0:
                zombie_array.rect.y -= 500
                zombies.remove(zombie_array)
                zombie_kill += 1

        # zombie kill than n, boss appear
        if zombie_kill > 30:
            enemy_spawn = False
            boss_appear = True

        time_machine.rect.x += diff_offset.x

        if boss_appear is True:
            if boss_music is False:
                pygame.mixer.music.fadeout(10)
                pygame.mixer.music.load("boss_bgm.mp3")
                pygame.mixer.music.play(-1)
                boss_music = True
            
            if effect.pattern0_count == 0:
                pattern0_time += mt
                if pattern0_time > 0.5:
                    effect.pattern0()
                    pattern0_sfx.set_volume(0.7)
                    pattern0_sfx.play()
                    
                    if pygame.Rect.colliderect(User.rect, effect.rect):
                        User.health -= 0.2
                        
                    for i in zombies[:]:
                        i.rect.y -= 500
                        zombies.remove(i)
                    
                else:
                    effect.warning()
            else:
                if pattern_excute is True:
                    if pattern_choose == 1:
                        if pattern1_effect is True:
                            effect.pattern1()
                            if pygame.Rect.colliderect(User.rect, effect.rect):
                                User.health -= 0.2
                        else:
                            Boss.pattern1_motion()
                            
                    elif pattern_choose == 2:
                        if pattern2_effect is True:
                            if warning_time > 0.5:
                                pattern0_sfx.set_volume(0.7)
                                pattern0_sfx.play()
                                effect.pattern2()
                                if pygame.Rect.colliderect(User.rect, effect.rect):
                                    User.health -= 0.2
                            else:
                                effect.warning2()
                                warning_time += mt
                                    
                        else:
                            Boss.pattern2_motion()
                    else:
                        Boss.pattern3_motion()
                else:
                    if effect.pattern0_count == 1:
                        pattern_excute = True
                        pattern_choose = random.randint(1, 3)
        
        Boss.collision(User_weapon)
        
        if Boss.health <= 0:
            reason3 = True
        
        if time_machine.health <= 0:
            reason1 = True

        if User.health <= 0:
            reason2 = True
        
        windowSurface.blit(canvas, (0,0))
        
        all_sprites.draw(windowSurface)

        windowSurface.blit(User.health_bar[round(User.health)], (0, 0))

        canvas.blit(background, (-875 - offset.x, -50 - offset.y))

        if reason1 is True:
            enemy_spawn = False
            windowSurface.blit(gameover2, (0, 0))
            Restart.update()
            ending_sprites.draw(windowSurface)

        elif reason2 is True:
            enemy_spawn = False
            windowSurface.blit(gameover1, (-25, 0))
            Restart.update()
            ending_sprites.draw(windowSurface)

        elif reason3 is True:
            enemy_spawn = False
            windowSurface.blit(victory, (0, 0))
            Restart.update()
            ending_sprites.draw(windowSurface)
    else:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        mt = clock.tick(60) / 1000

        if is_tutorial is True:
            tutorial_time += mt
            windowSurface.blit(tutorial, (0, 0))

            if tutorial_time > 3:
                gamestart = True
        else:
            windowSurface.blit(main_screen, (-50, 0))
            enemy_spawn = True
            Button.update()
            main_sprites.draw(windowSurface)
    
    pygame.display.update()


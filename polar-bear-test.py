import pygame
import random
pygame.init()

# Sound files
sound = pygame.mixer.Sound("Jump_effect.wav")
pygame.mixer.music.load("Synthesia_I_Need_A_Hero_125.wav")
pygame.mixer.music.play(-1, 0.0)
 
# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)

# Font
font = pygame.font.SysFont("Courier New", 20, True, False)

# Loop until the user clicks the close button.
done = False

#Instruction Variables
display_instructions = True
instruction_page = 1
 
# -------- Instruction Page Loop -----------
while not done and display_instructions:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
            	instruction_page += 1
            	if instruction_page == 4:
                    display_instructions = False
    clock = pygame.time.Clock()

    # Set the screen background
    screen.fill(BLUE)
 
    # Instructions: Page 1
    if instruction_page == 1:
        # Draw instructions, page 1
        logo = pygame.image.load("logo.png")
        logo_rect = logo.get_rect()
        screen.blit(logo, [125, 100])
 
        text = font.render("Press the Right key to continue instructions", True, WHITE)
        screen.blit(text, [125, 400])
        text = font.render("Press M to mute during the game", True, WHITE)
        screen.blit(text, [125, 425])

    # Instructions: Page 2
    if instruction_page == 2:
        # Draw instructions, page 2
        text = font.render("Get to the end while saving your cubs on the way!", True, WHITE)
        screen.blit(text, [100, 30])
        text = font.render("Save your cubs by stopping near them.", True, WHITE)
        screen.blit(text, [100, 55])
        
        image = pygame.image.load("New Piskel 4.png")
        screen.blit(image, [250, 250])
    
    # Instructions: Page 3
    if instruction_page == 3:
        text = font.render("Press the up key to jump.", True, WHITE)
        screen.blit(text, [150, 20])
        image = pygame.image.load("New Piskel.png")
        screen.blit(image, [200, 40])
        
        text = font.render("Press the left and right keys to move.", True, WHITE)
        screen.blit(text, [150, 300])
        image = pygame.image.load("New Piskel2 2.png")
        screen.blit(image, [170, 350])

    # Limit to 60 frames per second
    clock.tick(60)
 
    # Updates the screen with what we've drawn.
    pygame.display.flip()
    

# Class: Snowflake
class SnowFlake():
    def __init__(self, size, position, wind=False):
        self.size = size
        self.position = position
        self.wind = wind 
    
    def fall(self, speed):
        self.position[1] += speed
        if self.wind:
            self.position[0] += random.randint(-speed, speed) 
        
    def draw(self):
        pygame.draw.circle(screen, WHITE, self.position, 5)       
        
    def stop(self):
    	return  

speed = 50
snow_list = []

# Class: Player
class Player(pygame.sprite.Sprite):
    def __init__(self): 
        # Call the parent's constructor
        super().__init__()
 
        self.image = pygame.image.load("polar-bear.png")
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
 
    def update(self):  # Moves the player. 
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                
        block2_hit_list = pygame.sprite.spritecollide(self, self.level.platform2_list, False)
        for block2 in block2_hit_list:
        	if self.change_x > 0:
        		self.rect.right = block2.rect.left
        	elif self.change_x < 0:
        		self.rect.left = block2.rect.right
        		
        block3_hit_list = pygame.sprite.spritecollide(self, self.level.platform3_list, False)
        for block3 in block3_hit_list:
        	if self.change_x > 0:
        		self.rect.right = block3.rect.left
        	elif self.change_x < 0:
        		self.rect.left = block3.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
            
        block2_hit_list = pygame.sprite.spritecollide(self, self.level.platform2_list, False)
        for block2 in block2_hit_list:
        	if self.change_y > 0:
        		self.rect.bottom = block2.rect.top
        	elif self.change_y < 0:
        		self.rect.top = block2.rect.bottom
        	
        	
        block3_hit_list = pygame.sprite.spritecollide(self, self.level.platform3_list, False)
        for block3 in block3_hit_list:
        	if self.change_y > 0:
        		self.rect.bottom = block3.rect.top
        	elif self.change_y < 0:
        		self.rect.top = block3.rect.bottom
        		
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 5
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        
        self.rect.y += 2
        platform2_hit_list = pygame.sprite.spritecollide(self, self.level.platform2_list, False)
        self.rect.y -= 2
        
        self.rect.y += 2
        platform3_hit_list = pygame.sprite.spritecollide(self, self.level.platform3_list, False)
        self.rect.y -= 2
        
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
            
        if len(platform2_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
            
        if len(platform3_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
# Class: Low Stage Platform
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, image, rect):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.image.load("platform.png") 
        self.rect = self.image.get_rect()
        
# Class: Medium Stage Platform
class Platform2(pygame.sprite.Sprite):
	def __init__(self, image, rect):
		super().__init__()
		self.image = pygame.image.load("platform2.png")
		self.rect = self.image.get_rect()
		
# Class: High Stage Platform
class Platform3(pygame.sprite.Sprite):
	def __init__(self, image, rect):
		super().__init__()
		self.image = pygame.image.load("platform3.png")
		self.rect = self.image.get_rect()

# Class : Cub
class Cub(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("baby_cub.png")
        self.rect = self.image.get_rect()
        

# Parent Class: Level
class Level(object):
    platform_list = None
    platform2_list = None
    platform3_list = None
 	
    world_shift = 0
    level_limit = -1000
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.platform2_list = pygame.sprite.Group()
        self.platform3_list = pygame.sprite.Group()
        self.cub_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everything on this level
    def update(self):
        self.platform_list.update()
        self.platform2_list.update()
        self.platform3_list.update()
        self.cub_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(BLUE)
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.platform2_list.draw(screen)
        self.platform3_list.draw(screen)
        self.cub_list.draw(screen)
        
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
            
        for platform2 in self.platform2_list:
        	platform2.rect.x += shift_x
        	
        for platform3 in self.platform3_list:
        	platform3.rect.x += shift_x
        
        for cub in self.cub_list:
            cub.rect.x += shift_x

 
# Child Class: Level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Calls the parent constructor
        Level.__init__(self, player)
 
        # Width, Height, and Coordinates of the Low Stage Platform
        level = [[210, 70, 200, 500],
                 [210, 70, 900, 450],
                 [210, 70, 1600, 400],
                 [210, 70, 2300, 300],
                 [210, 70, 3000, 500],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        
        # Width, Height, and Coordinates of the Cubs
        level_cub = [[210, 70, 400, 430],
                 	[210, 70, 1100, 380],
                 	[210, 70, 1900, 330],
                 	[210, 70, 2500, 230],
                 	[210, 70, 3200, 430],
                 	
                 	[210, 70, 3520, 430],
                 	[210, 70, 4130, 380],
                 	[210, 70, 4600, 280],
                 	[210, 70, 5200, 280],
                 	[210, 70, 5830, 330],
                 	
                 	[210, 70, 6380, 430],
                 	[210, 70, 6920, 380],
                 	[210, 70, 7480, 280],
                 	[210, 70, 8030, 330],
                 	[210, 70, 8500, 390],
                 	]
                 	
        # Array with width, height, x, and y of cub
        for cub in level_cub:
            bae = Cub()
            bae.rect.x = cub[2]
            bae.rect.y = cub[3]
            self.cub_list.add(bae)
            
        # Width, Height, and Coordinates of the Medium Stage Platform
        level_2 = [[800, 70, 3320, 500],
                 [800, 70, 3930, 450],
                 [800, 70, 4540, 350],
                 [800, 70, 5150, 350],
                 [800, 70, 5760, 400],
                 ]
                 
        # Go through the array above and add platforms2
        for platform2 in level_2:
            block2 = Platform2(platform2[0], platform2[1])
            block2.rect.x = platform2[2]
            block2.rect.y = platform2[3]
            block2.player = self.player
            self.platform2_list.add(block2)
        
        # Width, Height, and Coordinates of the High Stage Platform
        level_3 = [[900, 70, 6310, 500], \
                  [900, 70, 6860, 450], \
                  [900, 70, 7410, 350], \
                  [900, 70, 7960, 400], \
                  [900, 70, 8510, 450], \
                  ]
        
        for platform3 in level_3:
        	block3 = Platform3(platform3[0], platform3[1])
        	block3.rect.x = platform3[2]
        	block3.rect.y = platform3[3]
        	block3.player = self.player
        	self.platform3_list.add(block3)

            
def main():
    """ Main Program """
    pygame.init()
 
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Polar Bear Run")
 
    # Create the player
    player = Player()
 
    # Create the level
    level_list = []
    level1 = Level_01(player)
    level_list.append( level1 )

 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 250
    player.rect.y = 200
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    #fact2 = fact_list[random.randint(0,6)]
    
    if pygame.mixer.music.play and sound.play:
    	music = True 
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            i = 0
            for baby in level1.cub_list:
                if (baby.rect.x < 390):
                    baby.rect.x = -1000

                i += 1
 
            if event.type == pygame.KEYDOWN and player.rect.bottom < 600:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                    pygame.mixer.init()
                    sound.play()
                if event.key == pygame.K_m:
                    if music == True:
                        pygame.mixer.music.stop()
                        sound.set_volume(0)
                    else: 
                        pygame.mixer.music.play(-1, 0.0)
                        sound.set_volume(1)
                    music = not music
            
            if event.type == pygame.KEYDOWN:
            	if event.key == pygame.K_c:
            		pygame.mixer.music.load("Synthesia_I_Need_A_Hero_125.wav")
            		pygame.mixer.music.play(-1, 0.0)
            		player.rect.x = 0
            		player.rect.y = 200
            		#level_list = []
            		level_list.append( Level_01(player) )
            		current_level_no = 0
            		current_level = level_list[current_level_no]
            		player.level = current_level

            		i = 0
            		for baby in level1.cub_list:
            		    if (baby.rect.x < 390):
            		        baby.rect.x = -1000
            		    i += 1
            		
            	if event.key == pygame.K_w:
            		player.rect.x = 8500
            		player.rect.y = 200
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
        
        # Test Code for player.rect.bottom
        #print(player.rect.bottom)
        
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        snowflake = SnowFlake(5, [random.randint(0, 750), 0], wind = True)
        snow_list.append(snowflake)
        
        snowing = True
        if current_level.world_shift <= -2750:
           	 snowing = False
           	 
        if snowing:
            for snowflake in snow_list:
                snowflake.draw()
                snowflake.fall(3)

        # Bear reaction to snow stopping
        if current_level.world_shift <= -2850:
            snowflake.stop()
            bear_talks = font.render("Huh? The snow stopped...", True, WHITE)
            snow_stopped_rect = bear_talks.get_rect()
            snow_stopped_x = screen.get_width() / 2 - snow_stopped_rect.width /2
            snow_stopped_y = (screen.get_height() / 2 - snow_stopped_rect.height /2) - 200
            screen.blit(bear_talks, [snow_stopped_x, snow_stopped_y])
       
       # Bear reaction to High Stage Platform
        if current_level.world_shift <= -6310:
            pygame.draw.rect(screen, BLUE, (snow_stopped_x - 100, snow_stopped_y, 400, 25), 0)
            bear_talks = font.render("The ice is getting smaller...!", True, WHITE)
            screen.blit(bear_talks, [snow_stopped_x, snow_stopped_y])
       
		#If player touches ground, game over
        if player.rect.bottom >= 600 and current_level.world_shift >= -8450:
             screen.fill(RED)
             game_over = font.render("Game over!", True, WHITE)
             game_over_rect = game_over.get_rect()
             game_over_x = screen.get_width() / 2 - game_over_rect.width /2
             game_over_y = (screen.get_height() / 2 - game_over_rect.height /2)
             screen.blit(game_over, [game_over_x, game_over_y - 100])
            
             replay = font.render("Press C to continue.", True, WHITE)
             replay_rect = replay.get_rect()
             replay_x = screen.get_width() / 2 - replay_rect.width /2
             replay_y = (screen.get_height() / 2 - replay_rect.height /2)
             screen.blit(replay, [replay_x, replay_y + 100])

          
		#If player finishes, game over
        if player.rect.bottom >= 600 and current_level.world_shift <= -8450:
             screen.fill(BLACK)
             pygame.mixer.music.play(1, 0.0)
             
             game_over2 = font.render("There were no icebergs left... The bear and all her cubs drowned.", True, WHITE)
             game_over_rect2 = game_over2.get_rect()
             game_over_x2 = screen.get_width() / 2 - game_over_rect2.width / 2
             game_over_y2 = screen.get_height() / 2 - game_over_rect2.height / 2
             screen.blit(game_over2, [game_over_x2, game_over_y2 - 100])
             
             our_fault = font.render("And it's all our fault.", True, WHITE)
             our_fault_rect = our_fault.get_rect()
             our_fault_x = screen.get_width() / 2 - our_fault_rect.width /2
             our_fault_y = screen.get_height() / 2 - our_fault_rect.height /2
             screen.blit(our_fault, [our_fault_x, our_fault_y - 50])
             
             fact1 = font.render("Scientists predict that as the Arctic ", True, WHITE)
             fact_rect = fact1.get_rect()
             fact_rect_x = screen.get_width() /2 - fact_rect.width /2
             fact_rect_y = screen.get_height() / 2 - fact_rect.height /2
             screen.blit(fact1, [fact_rect_x, fact_rect_y])
             
             fact2 = font.render("continues to warm, two thirds of the ", True, WHITE)
             fact_rect = fact2.get_rect()
             fact_rect_x = screen.get_width() /2 - fact_rect.width /2
             fact_rect_y = screen.get_height() / 2 - fact_rect.height /2
             screen.blit(fact2, [fact_rect_x, fact_rect_y + 25])
             
             fact3 = font.render("world's polar bears could disappear within this century.", True, WHITE)
             fact_rect = fact3.get_rect()
             fact_rect_x = screen.get_width() /2 - fact_rect.width /2
             fact_rect_y = screen.get_height() / 2 - fact_rect.height /2
             screen.blit(fact3, [fact_rect_x, fact_rect_y + 50])
             
             check = font.render("Check our website for more information.", True, WHITE)
             fact_rect = check.get_rect()
             fact_rect_x = screen.get_width() /2 - fact_rect.width /2
             fact_rect_y = screen.get_height() / 2 - fact_rect.height /2
             screen.blit(check, [fact_rect_x, fact_rect_y + 100])
             
             website = font.render("sabrinas78.github.io/final-master/PolarBearRun/index.html", True, WHITE)
             website_rect = website.get_rect()
             website_rect_x = screen.get_width() /2 - website_rect.width /2
             website_rect_y = screen.get_width() /2 - website_rect.height /2
             screen.blit(website, [website_rect_x, website_rect_y + 100])
             
             
             #play_more = font.render("Press R to play again.", True, WHITE)
             #fact_rect = play_more.get_rect()
             #fact_rect_x = screen.get_width() /2 - fact_rect.width /2
             #fact_rect_y = screen.get_height() / 2 - fact_rect.height /2
             #screen.blit(play_more, [fact_rect_x, fact_rect_y + 200])
             
             #----
             #fact = font.render(fact2, True, WHITE)
             #fact_rect = fact.get_rect()
             #fact_x = screen.get_width() / 2 - fact_rect.width /2
             #fact_y = (screen.get_height() /2 - fact_rect.height /2)
             #screen.blit(fact, [fact_x, fact_y + 150])

        
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
 
        # Limit to 60 frames per second
        clock.tick(60)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
 
if __name__ == "__main__":
    main()

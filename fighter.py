import pygame

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offest = data[2]
        self.flip_offset = [self.size - self.offest[0] - 30, self.offest[1]]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180)) #80 180
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        # Extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps): # another way to keep track of iterations
            temo_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x*self.size, y*self.size, self.size, self.size)
                temo_img_list.append(pygame.transform.scale(temp_img, (self.size*self.image_scale, self.size*self.image_scale)))
            animation_list.append(temo_img_list)
        return animation_list
    
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Get keypresses
        key = pygame.key.get_pressed()
        # Can only peform other actions if not currently attacking
        if self.attking == False:
            # Movement
            if key[pygame.K_a]:
                dx = -SPEED 
                self.running = True
            if key[pygame.K_d]:
                dx = +SPEED
                self.running = True
            # Jump
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            # Attack
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                # Determine attack type was ued
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2
        
        # Apply Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 20:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 20 - self.rect.bottom
        
        # Ensure players face eachother
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        #apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy
    
    # Handle animation updates
    def update(self):
        # Check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attking == True:
            if self.attack_type == 1:
                self.update_action(3)  # Attack type 1 animation
            elif self.attack_type == 2:
                self.update_action(4)  # Attack type 2 animation
        elif self.jump == True:
            self.update_action(2)  # Jump animation
        elif self.running == True:
            self.update_action(1)  # Running animation
        else:
            self.update_action(0)  # Idle animation

        animation_cooldown = 50
        # Update image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        # Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # If the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed and reset attacking state
                if self.action == 3 or self.action == 4:
                    self.attking = False  # Reset attacking state after attack animation
                    self.attack_cooldown = 20
                # Check if damage was taken
                if self.action == 5:
                    self.hit = False
                    # If the player was in the middle of an attack, then the attack is stopped
                    self.attking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attking = True
            attacking_rect = pygame.Rect(self.rect.right - (2 * self.rect.width * self.flip), self.rect.top, self.rect.width*1.4, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255,0), attacking_rect)

    def update_action(self, new_action):
        # Check if the new action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    
    def draw(self, surface):
        # Flip the image if needed
        img = pygame.transform.flip(self.image, self.flip, False)
        
        # Adjust the x-coordinate for flipping
        if self.flip:
            draw_x = self.rect.x - (self.flip_offset[0] * self.image_scale)
        else:
            draw_x = self.rect.x - (self.offest[0] * self.image_scale)
        
        # Adjust the y-coordinate (flipping doesn't affect vertical offsets)
        draw_y = self.rect.y - (self.offest[1] * self.image_scale)
        
        # Draw the rect for debugging (optional)
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
        
        # Draw the sprite
        surface.blit(img, (draw_x, draw_y))

#def draw(self, surface):
     #   img = pygame.transform.flip(self.image, self.flip, False)
      #  pygame.draw.rect(surface, (255, 0, 0), self.rect)
       # surface.blit(img, (self.rect.x - (self.offest[0] * self.image_scale), self.rect.y - (self.offest[1] * self.image_scale)))



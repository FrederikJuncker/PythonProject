import pygame

class Fighter():
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, player_num):
        self.player_num = player_num  # Add player number to differentiate controls
        self.size = data[0]
        self.image_scale = data[1]
        self.offest = data[2]
        self.flip_offset = [self.size - self.offest[0] - 30, self.offest[1] + 10]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:run #2:jump #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
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
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                try:
                    x_coord = x * self.size
                    y_coord = y * self.size + 5
                    
                    if x_coord >= sprite_sheet.get_width() or y_coord >= sprite_sheet.get_height():
                        raise ValueError(f"Sprite coordinates out of bounds: {x_coord}, {y_coord}")
                    
                    temp_img = sprite_sheet.subsurface(x_coord, y_coord, self.size, self.size)
                    scaled_img = pygame.transform.scale(temp_img, (
                        int(self.size * self.image_scale),
                        int(self.size * self.image_scale)
                    ))
                    
                    temp_img_list.append(scaled_img)
                    
                except pygame.error as e:
                    print(f"Error loading sprite at position {x}, {y}: {e}")
                    continue
                    
            if temp_img_list:
                animation_list.append(temp_img_list)
            else:
                print(f"Warning: No sprites loaded for animation row {y}")
        
        if not animation_list:
            raise ValueError("No sprites were loaded from the sprite sheet!")
            
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

        # Only perform actions if not attacking and alive
        if not self.attking and self.alive:
            # Controls for Player 1
            if self.player_num == 1:
                # Movement
                if key[pygame.K_a]:
                    dx = -SPEED 
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(surface, target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # Controls for Player 2
            if self.player_num == 2:
                # Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # Jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                # Attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
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
        
        # Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        # Apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    # Rest of the methods remain the same
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit:
            self.update_action(5)
        elif self.attking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attking = False
                    self.attack_cooldown = 20

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attking = True
            attacking_rect = pygame.Rect(self.rect.right - (2 * self.rect.width * self.flip), 
                                      self.rect.top, self.rect.width*1.4, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255,0), attacking_rect)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        
        if self.flip:
            draw_x = self.rect.x - (self.flip_offset[0] * self.image_scale)
        else:
            draw_x = self.rect.x - (self.offest[0] * self.image_scale)
        
        draw_y = self.rect.y - (self.offest[1] * self.image_scale)
        
        pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
        surface.blit(img, (draw_x, draw_y))

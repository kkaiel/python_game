
import pygame
from config import *

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.persona = PERSONA_CHIRON # Default persona
        self.color = CHIRON_COLOR
        self.speed = PLAYER_SPEED
        self.last_dx = 0
        self.last_dy = -1 # Default direction: up
        self.last_dx = 0
        self.last_dy = -1 # Default direction: up

    def move(self, dx, dy, walls, transparent_walls):
        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy

        # Determine which walls to collide with for this move.
        collidable_walls = walls
        if self.persona != PERSONA_MORA:
            collidable_walls = walls + transparent_walls

        # --- ROBUST COLLISION LOGIC ---
        # Move X axis
        self.rect.x += dx * self.speed
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dx > 0: # Moving right
                    self.rect.right = wall.left
                if dx < 0: # Moving left
                    self.rect.left = wall.right

        # Move Y axis
        self.rect.y += dy * self.speed
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dy > 0: # Moving down
                    self.rect.bottom = wall.top
                if dy < 0: # Moving up
                    self.rect.top = wall.bottom
        # --- END ROBUST COLLISION LOGIC ---

    def set_persona(self, persona):
        self.persona = persona
        if self.persona == PERSONA_CHIRON:
            self.color = CHIRON_COLOR
            self.speed = PLAYER_SPEED
        elif self.persona == PERSONA_ERIDA:
            self.color = ERIDA_COLOR
            self.speed = PLAYER_SPEED * 1.5 # Erida is faster
        elif self.persona == PERSONA_MORA:
            self.color = MORA_COLOR
            self.speed = PLAYER_SPEED

        print(f"Persona changed to: {self.persona}") # For debugging

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def break_wall(self, maze):
        wall_to_break_x = self.rect.centerx // TILE_SIZE + self.last_dx
        wall_to_break_y = self.rect.centery // TILE_SIZE + self.last_dy

        for wall in maze.walls:
            if wall.x // TILE_SIZE == wall_to_break_x and wall.y // TILE_SIZE == wall_to_break_y:
                maze.walls.remove(wall)
                # Also update the grid representation
                grid_y = wall_to_break_y
                grid_x = wall_to_break_x
                if 0 <= grid_y < len(maze.grid) and 0 <= grid_x < len(maze.grid[0]):
                    row = list(maze.grid[grid_y])
                    row[grid_x] = ' '
                    maze.grid[grid_y] = "".join(row)
                break

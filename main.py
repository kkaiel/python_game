
import pygame
from config import *
from player import Player
from maze import Maze

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Persona Maze")
    clock = pygame.time.Clock()

    maze = Maze()
    player = Player(maze.start_pos[0], maze.start_pos[1])

    hint_path = None
    hint_timer = 0
    slow_motion = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.set_persona(PERSONA_CHIRON)
                elif event.key == pygame.K_2:
                    player.set_persona(PERSONA_ERIDA)
                elif event.key == pygame.K_3:
                    player.set_persona(PERSONA_MORA)
                elif event.key == pygame.K_h and player.persona == PERSONA_CHIRON:
                    hint_path = maze.find_path(maze.start_pos, maze.end_pos)
                    hint_timer = 300 # Show hint for 5 seconds (60fps * 5s)
                elif event.key == pygame.K_b and player.persona == PERSONA_ERIDA:
                    player.break_wall(maze)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
        if keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        if keys[pygame.K_DOWN]:
            dy = 1

        if player.persona == PERSONA_MORA and keys[pygame.K_s]:
            slow_motion = True
        else:
            slow_motion = False
        
        player.move(dx, dy, maze.walls, maze.transparent_walls)

        screen.fill(WHITE)
        maze.draw(screen)
        if hint_path and hint_timer > 0:
            for pos in hint_path:
                pygame.draw.rect(screen, HINT_COLOR, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            hint_timer -= 1
        player.draw(screen)
        pygame.display.flip()

        if slow_motion:
            clock.tick(20) # Slow motion
        else:
            clock.tick(60) # Normal speed

    pygame.quit()

if __name__ == "__main__":
    main()

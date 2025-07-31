
import pygame
from config import *
import heapq

class Maze:
    def __init__(self):
        self.grid = [
            "XXXXXXXXXXXXXXXXXXXX",
            "X P        X       X",
            "X XXX XXXX XXXXXXX X",
            "X   X T XX X   X   X",
            "X XXXXX XX XXX X XXX",
            "X X     XX   X X   X",
            "X X XXX XXXX X XXX X",
            "X X X   X    X X   X",
            "X XXX XXXXXX XXX XXX",
            "X   X        X     X",
            "X XXX XXXXXX XXXXX X",
            "X X   X      X   X X",
            "X X XXX XXXX XXX X X",
            "X X     XX   X   X E",
            "XXXXXXXXXXXXXXXXXXXX",
        ]
        self.tile_width = len(self.grid[0])
        self.tile_height = len(self.grid)
        self.walls = []
        self.transparent_walls = []
        self.start_pos = None
        self.end_pos = None

        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == 'X':
                    self.walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == 'T':
                    self.transparent_walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == 'P':
                    self.start_pos = (x, y)
                elif char == 'E':
                    self.end_pos = (x, y)

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        for wall in self.transparent_walls:
            pygame.draw.rect(screen, (128, 128, 128), wall) # Gray for transparent walls

    def find_path(self, start_node, end_node):
        open_set = []
        heapq.heappush(open_set, (0, start_node))
        came_from = {}
        g_score = { (x,y): float('inf') for y, row in enumerate(self.grid) for x, char in enumerate(row) }
        g_score[start_node] = 0
        f_score = { (x,y): float('inf') for y, row in enumerate(self.grid) for x, char in enumerate(row) }
        f_score[start_node] = self.heuristic(start_node, end_node)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_node)
                return path[::-1]

            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < self.tile_width and 0 <= neighbor[1] < self.tile_height:
                    if self.grid[neighbor[1]][neighbor[0]] == 'X':
                        continue

                    tentative_g_score = g_score[current] + 1
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end_node)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

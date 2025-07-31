
# maze.py
# 미로의 구조를 정의하고, 미로 내의 다양한 요소(벽, 발판 등)를 관리하며,
# 미로를 화면에 그리는 역할을 담당하는 파일입니다.

import pygame
from config import *
import heapq # A* 알고리즘을 위한 우선순위 큐 구현

# 움직이는 발판 클래스
class MovingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        움직이는 발판을 초기화합니다.
        Args:
            x (int): 발판의 초기 X 좌표 (픽셀)
            y (int): 발판의 초기 Y 좌표 (픽셀)
        """
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE * 2, TILE_SIZE // 2)) # 발판 이미지 생성
        self.image.fill(BLUE) # 발판 색상 설정
        self.rect = self.image.get_rect(topleft=(x, y)) # 발판의 위치와 크기 설정
        self.start_x = x # 발판의 시작 X 좌표
        self.end_x = x + TILE_SIZE * 5 # 발판의 이동 끝 X 좌표 (5타일 오른쪽)
        self.speed = 2 # 발판의 이동 속도

    def update(self):
        """
        매 프레임마다 발판의 위치를 업데이트하고, 이동 범위를 벗어나면 방향을 바꿉니다.
        """
        self.rect.x += self.speed
        # 발판이 이동 범위를 벗어나면 방향을 반전시킵니다.
        if self.rect.left < self.start_x or self.rect.right > self.end_x:
            self.speed *= -1


# 미로 클래스
class Maze:
    def __init__(self, level_data):
        """
        미로를 초기화합니다. 주어진 레벨 데이터에 따라 미로를 구성합니다.
        Args:
            level_data (list): 2D 문자열 배열 형태의 미로 레벨 데이터
        """
        self.grid = level_data # 미로의 2D 배열 데이터
        self.tile_width = len(self.grid[0]) # 미로의 가로 타일 개수
        self.tile_height = len(self.grid) # 미로의 세로 타일 개수
        self.walls = [] # 일반 벽 Rect 객체 리스트
        self.transparent_walls = [] # 투명한 벽 Rect 객체 리스트 (모라 통과 가능)
        self.breakable_walls = [] # 부술 수 있는 벽 Rect 객체 리스트 (에리다 파괴 가능)
        self.moving_platforms = pygame.sprite.Group() # 움직이는 발판 Sprite 그룹
        self.start_pos = None # 플레이어 시작 위치 (타일 좌표)
        self.end_pos = None # 미로 탈출구 위치 (타일 좌표)

        # 레벨 데이터를 파싱하여 미로 요소들을 초기화합니다.
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == 'X': # 일반 벽
                    self.walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == 'T': # 투명한 벽
                    self.transparent_walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == 'B': # 부술 수 있는 벽
                    self.breakable_walls.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                elif char == 'H': # 움직이는 발판
                    self.moving_platforms.add(MovingPlatform(x * TILE_SIZE, y * TILE_SIZE))
                elif char == 'P': # 플레이어 시작 위치
                    self.start_pos = (x, y)
                elif char == 'E': # 미로 탈출구
                    self.end_pos = (x, y)

    def draw(self, screen):
        """
        미로의 모든 요소를 화면에 그립니다.
        Args:
            screen (pygame.Surface): 게임 화면 Surface 객체
        """
        # 일반 벽 그리기
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        # 투명한 벽 그리기 (회색)
        for wall in self.transparent_walls:
            pygame.draw.rect(screen, (128, 128, 128), wall) # Gray for transparent walls
        # 부술 수 있는 벽 그리기 (갈색)
        for wall in self.breakable_walls:
            pygame.draw.rect(screen, (139, 69, 19), wall) # Brown for breakable walls
        # 움직이는 발판 그리기
        self.moving_platforms.draw(screen)

    def find_path(self, start_node, end_node):
        """
        A* 알고리즘을 사용하여 시작 노드에서 끝 노드까지의 최단 경로를 찾습니다.
        Args:
            start_node (tuple): 시작 지점의 (x, y) 타일 좌표
            end_node (tuple): 끝 지점의 (x, y) 타일 좌표
        Returns:
            list: 최단 경로를 구성하는 타일 좌표 리스트 (없으면 None)
        """
        open_set = []
        heapq.heappush(open_set, (0, start_node)) # (f_score, node) 형태로 우선순위 큐에 추가
        came_from = {} # 경로 재구성을 위한 이전 노드 저장
        # 각 노드의 g_score (시작점에서 현재 노드까지의 실제 비용)
        g_score = { (x,y): float('inf') for y, row in enumerate(self.grid) for x, char in enumerate(row) }
        g_score[start_node] = 0
        # 각 노드의 f_score (g_score + 휴리스틱 비용)
        f_score = { (x,y): float('inf') for y, row in enumerate(self.grid) for x, char in enumerate(row) }
        f_score[start_node] = self.heuristic(start_node, end_node)

        while open_set:
            _, current = heapq.heappop(open_set) # f_score가 가장 낮은 노드 추출

            # 목표 지점에 도달했으면 경로 재구성
            if current == end_node:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_node)
                return path[::-1] # 경로를 역순으로 반환

            # 현재 노드의 이웃 탐색
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 상하좌우 이동
                neighbor = (current[0] + dx, current[1] + dy)
                
                # 이웃 노드가 미로 범위 내에 있는지 확인
                if 0 <= neighbor[0] < self.tile_width and 0 <= neighbor[1] < self.tile_height:
                    # 이웃 노드가 벽(X)이면 통과 불가
                    if self.grid[neighbor[1]][neighbor[0]] == 'X':
                        continue

                    # 새로운 g_score 계산
                    tentative_g_score = g_score[current] + 1
                    
                    # 새로운 g_score가 더 좋으면 업데이트
                    if tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, end_node)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        return None # 경로를 찾지 못함

    def heuristic(self, a, b):
        """
        맨해튼 거리 휴리스틱 함수를 사용하여 두 지점 간의 예상 비용을 계산합니다.
        Args:
            a (tuple): 첫 번째 지점의 (x, y) 타일 좌표
            b (tuple): 두 번째 지점의 (x, y) 타일 좌표
        Returns:
            int: 두 지점 간의 맨해튼 거리
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

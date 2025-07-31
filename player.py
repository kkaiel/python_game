
# player.py
# 게임 내 플레이어 캐릭터의 동작, 상태, 그리고 인격별 능력을 관리하는 파일입니다.

import pygame
from config import *

class Player:
    def __init__(self, x, y):
        """
        플레이어 객체를 초기화합니다.
        Args:
            x (int): 플레이어의 초기 X 타일 좌표
            y (int): 플레이어의 초기 Y 타일 좌표
        """
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE) # 플레이어의 위치와 크기
        self.persona = PERSONA_CHIRON # 현재 활성화된 페르소나 (기본값: 카이론)
        self.color = CHIRON_COLOR # 현재 페르소나에 따른 플레이어 색상
        self.speed = PLAYER_SPEED # 플레이어 이동 속도
        self.last_dx = 0 # 마지막 X축 이동 방향 (벽 부수기 능력에 사용)
        self.last_dy = -1 # 마지막 Y축 이동 방향 (벽 부수기 능력에 사용, 기본값: 위)

    def move(self, dx, dy, walls, transparent_walls, moving_platforms):
        """
        플레이어를 이동시키고 벽 및 움직이는 발판과의 충돌을 처리합니다.
        Args:
            dx (int): X축 이동량 (-1: 왼쪽, 0: 없음, 1: 오른쪽)
            dy (int): Y축 이동량 (-1: 위, 0: 없음, 1: 아래)
            walls (list): 일반 벽 Rect 객체 리스트
            transparent_walls (list): 투명한 벽 Rect 객체 리스트
            moving_platforms (pygame.sprite.Group): 움직이는 발판 Sprite 그룹
        """
        # 이동 방향이 있을 경우 마지막 이동 방향을 업데이트합니다.
        if dx != 0 or dy != 0:
            self.last_dx = dx
            self.last_dy = dy

        # 현재 페르소나에 따라 충돌을 검사할 벽 목록을 결정합니다.
        # 모라가 아닐 경우 일반 벽과 투명한 벽 모두와 충돌 검사합니다.
        collidable_walls = walls
        if self.persona != PERSONA_MORA:
            collidable_walls = walls + transparent_walls

        # X축 이동 및 충돌 처리
        self.rect.x += dx * self.speed
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dx > 0: # 오른쪽으로 이동 중 충돌
                    self.rect.right = wall.left
                if dx < 0: # 왼쪽으로 이동 중 충돌
                    self.rect.left = wall.right

        # Y축 이동 및 충돌 처리
        self.rect.y += dy * self.speed
        for wall in collidable_walls:
            if self.rect.colliderect(wall):
                if dy > 0: # 아래로 이동 중 충돌
                    self.rect.bottom = wall.top
                if dy < 0: # 위로 이동 중 충돌
                    self.rect.top = wall.bottom

        # 움직이는 발판과의 충돌 처리
        for platform in moving_platforms:
            if self.rect.colliderect(platform):
                # 플레이어가 발판 위에 있을 경우 발판과 함께 이동
                self.rect.bottom = platform.rect.top # 발판 위에 플레이어 위치 고정
                self.rect.x += platform.speed # 발판의 속도만큼 플레이어도 이동

    def set_persona(self, persona):
        """
        플레이어의 페르소나를 변경하고, 그에 따른 색상 및 속도를 설정합니다.
        Args:
            persona (str): 변경할 페르소나 (PERSONA_CHIRON, PERSONA_ERIDA, PERSONA_MORA 중 하나)
        """
        self.persona = persona
        if self.persona == PERSONA_CHIRON:
            self.color = CHIRON_COLOR
            self.speed = PLAYER_SPEED
        elif self.persona == PERSONA_ERIDA:
            self.color = ERIDA_COLOR
            self.speed = PLAYER_SPEED * 1.5 # 에리다는 이동 속도 1.5배 증가
        elif self.persona == PERSONA_MORA:
            self.color = MORA_COLOR
            self.speed = PLAYER_SPEED

        print(f"Persona changed to: {self.persona}") # 디버깅용 출력

    def draw(self, screen):
        """
        플레이어 캐릭터를 화면에 그립니다.
        Args:
            screen (pygame.Surface): 게임 화면 Surface 객체
        """
        pygame.draw.rect(screen, self.color, self.rect) # 현재 페르소나 색상으로 플레이어 그리기

    def break_wall(self, maze):
        """
        에리다의 능력: 플레이어가 바라보는 방향의 부술 수 있는 벽을 파괴합니다.
        Args:
            maze (Maze): 현재 미로 객체
        """
        # 플레이어의 현재 위치와 마지막 이동 방향을 기반으로 부술 벽의 타일 좌표를 계산합니다.
        wall_to_break_x = self.rect.centerx // TILE_SIZE + self.last_dx
        wall_to_break_y = self.rect.centery // TILE_SIZE + self.last_dy

        # 부술 수 있는 벽 목록을 순회하며 해당 벽을 찾습니다.
        for wall in maze.breakable_walls:
            if wall.x // TILE_SIZE == wall_to_break_x and wall.y // TILE_SIZE == wall_to_break_y:
                maze.breakable_walls.remove(wall) # 벽 목록에서 제거
                
                # 미로의 그리드 데이터도 업데이트하여 해당 위치를 빈 공간으로 만듭니다.
                grid_y = wall_to_break_y
                grid_x = wall_to_break_x
                if 0 <= grid_y < len(maze.grid) and 0 <= grid_x < len(maze.grid[0]):
                    row = list(maze.grid[grid_y])
                    row[grid_x] = ' ' # 벽을 빈 공간으로 변경
                    maze.grid[grid_y] = "".join(row)
                break # 벽을 찾아서 부쉈으면 반복 중단


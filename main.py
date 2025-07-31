
# main.py
# 게임의 메인 루프를 포함하며, Pygame 초기화, 이벤트 처리, 화면 업데이트,
# 그리고 게임 상태(레벨 진행, 승리 등)를 관리하는 파일입니다.

import pygame
from config import *
from player import Player
from maze import Maze
from levels import LEVELS

def main():
    """
    게임의 메인 함수입니다. Pygame을 초기화하고 게임 루프를 실행합니다.
    """
    pygame.init() # Pygame 모듈 초기화
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # 게임 화면 설정
    pygame.display.set_caption("Persona Maze") # 창 제목 설정
    clock = pygame.time.Clock() # 게임 프레임 속도 제어를 위한 Clock 객체 생성

    current_level_index = 0 # 현재 플레이 중인 레벨 인덱스
    maze = None # 현재 미로 객체
    player = None # 현재 플레이어 객체

    hint_path = None # 카이론의 힌트 경로
    hint_timer = 0 # 힌트 표시 시간 타이머
    slow_motion = False # 모라의 슬로우 모션 활성화 여부
    hint_cooldown_timer = 0 # 힌트 능력 쿨다운 타이머
    break_wall_cooldown_timer = 0 # 벽 부수기 능력 쿨다운 타이머

    def load_level(level_index):
        """
        지정된 인덱스의 레벨을 불러와 미로와 플레이어를 초기화합니다.
        Args:
            level_index (int): 불러올 레벨의 인덱스
        """
        nonlocal maze, player # 외부 스코프의 maze, player 변수를 사용
        maze = Maze(LEVELS[level_index]) # 새로운 미로 객체 생성
        player = Player(maze.start_pos[0], maze.start_pos[1]) # 플레이어 시작 위치에 초기화

    load_level(current_level_index) # 첫 번째 레벨 불러오기

    running = True # 게임 루프 실행 여부 플래그
    while running:
        # 이벤트 처리 루프
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 창 닫기 버튼 클릭 시
                running = False # 게임 종료
            if event.type == pygame.KEYDOWN: # 키보드 눌림 이벤트
                # 페르소나 전환
                if event.key == pygame.K_1:
                    player.set_persona(PERSONA_CHIRON)
                elif event.key == pygame.K_2:
                    player.set_persona(PERSONA_ERIDA)
                elif event.key == pygame.K_3:
                    player.set_persona(PERSONA_MORA)
                # 카이론 능력: 힌트 표시 (쿨다운 적용)
                elif event.key == pygame.K_h and player.persona == PERSONA_CHIRON:
                    if hint_cooldown_timer == 0:
                        hint_path = maze.find_path(maze.start_pos, maze.end_pos) # 최적 경로 계산
                        hint_timer = 300 # 힌트 표시 시간 설정 (5초)
                        hint_cooldown_timer = HINT_COOLDOWN # 쿨다운 시작
                # 에리다 능력: 벽 부수기 (쿨다운 적용)
                elif event.key == pygame.K_b and player.persona == PERSONA_ERIDA:
                    if break_wall_cooldown_timer == 0:
                        player.break_wall(maze) # 벽 부수기
                        break_wall_cooldown_timer = BREAK_WALL_COOLDOWN # 쿨다운 시작

        # 키 입력 상태 확인 (연속적인 이동 처리)
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
        
        # 모라 능력: 슬로우 모션 (S 키를 누르고 있는 동안 활성화)
        if player.persona == PERSONA_MORA and keys[pygame.K_s]:
            slow_motion = True
        else:
            slow_motion = False
        
        # 쿨다운 타이머 감소
        if hint_cooldown_timer > 0:
            hint_cooldown_timer -= 1
        if break_wall_cooldown_timer > 0:
            break_wall_cooldown_timer -= 1

        # 움직이는 발판 업데이트
        maze.moving_platforms.update()
        # 플레이어 이동 및 충돌 처리
        player.move(dx, dy, maze.walls, maze.transparent_walls, maze.moving_platforms)

        # 레벨 완료 조건 확인
        if player.rect.colliderect(pygame.Rect(maze.end_pos[0] * TILE_SIZE, maze.end_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)):
            current_level_index += 1 # 다음 레벨로 이동
            if current_level_index < len(LEVELS): # 모든 레벨을 완료하지 않았다면
                load_level(current_level_index) # 다음 레벨 불러오기
            else:
                # 게임 승리 화면
                screen.fill(BLACK) # 화면을 검은색으로 채움
                win_font = pygame.font.Font(None, 74) # 큰 폰트 설정
                win_text = win_font.render("YOU WIN!", True, GREEN) # 승리 메시지 렌더링
                win_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)) # 화면 중앙에 위치
                screen.blit(win_text, win_rect) # 화면에 메시지 그리기
                pygame.display.flip() # 화면 업데이트
                pygame.time.wait(3000) # 3초 동안 승리 화면 보여주기
                running = False # 게임 종료

        # 화면 그리기
        screen.fill(WHITE) # 배경을 흰색으로 채움
        maze.draw(screen) # 미로 그리기
        # 카이론 힌트 경로 그리기 (힌트가 활성화되어 있고 타이머가 남아있을 경우)
        if hint_path and hint_timer > 0:
            for pos in hint_path:
                pygame.draw.rect(screen, HINT_COLOR, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            hint_timer -= 1 # 힌트 타이머 감소
        player.draw(screen) # 플레이어 그리기

        # UI 그리기
        font = pygame.font.Font(None, 24) # UI 폰트 설정

        # 현재 인격 표시
        persona_text = ""
        persona_color = WHITE
        if player.persona == PERSONA_CHIRON:
            persona_text = "현재 인격: 카이론 (1)"
            persona_color = CHIRON_COLOR
        elif player.persona == PERSONA_ERIDA:
            persona_text = "현재 인격: 에리다 (2)"
            persona_color = ERIDA_COLOR
        elif player.persona == PERSONA_MORA:
            persona_text = "현재 인격: 모라 (3)"
            persona_color = MORA_COLOR
        
        persona_display = font.render(persona_text, True, persona_color) # 인격 텍스트 렌더링
        screen.blit(persona_display, (10, 10)) # 화면에 인격 텍스트 표시

        # 능력 쿨다운 표시
        # 쿨다운 시간을 초 단위로 변환하여 표시 (60프레임 = 1초)
        hint_cooldown_text = f"힌트 쿨다운: {hint_cooldown_timer // 60}초"
        break_wall_cooldown_text = f"벽 부수기 쿨다운: {break_wall_cooldown_timer // 60}초"

        hint_display = font.render(hint_cooldown_text, True, UI_TEXT_COLOR) # 힌트 쿨다운 텍스트 렌더링
        break_wall_display = font.render(break_wall_cooldown_text, True, UI_TEXT_COLOR) # 벽 부수기 쿨다운 텍스트 렌더링

        screen.blit(hint_display, (10, 40)) # 힌트 쿨다운 표시
        screen.blit(break_wall_display, (10, 70)) # 벽 부수기 쿨다운 표시

        pygame.display.flip() # 화면 전체 업데이트

        # 게임 프레임 속도 제어
        if slow_motion: # 슬로우 모션 활성화 시
            clock.tick(20) # 20 FPS로 느리게
        else:
            clock.tick(60) # 60 FPS로 정상 속도

    pygame.quit() # Pygame 종료

if __name__ == "__main__":
    main() # 메인 함수 실행

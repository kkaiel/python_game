# config.py
# 게임의 전반적인 설정 및 상수를 정의하는 파일입니다.

# 화면 크기 설정
SCREEN_WIDTH = 800  # 게임 화면의 너비
SCREEN_HEIGHT = 600 # 게임 화면의 높이

# 미로 설정
TILE_SIZE = 50      # 미로 타일 하나의 크기 (픽셀)
MAZE_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 미로의 가로 타일 개수
MAZE_HEIGHT = SCREEN_HEIGHT // TILE_SIZE # 미로의 세로 타일 개수

# 색상 정의 (RGB 값)
WHITE = (255, 255, 255) # 흰색
BLACK = (0, 0, 0)       # 검은색 (벽 색상)
RED = (255, 0, 0)       # 빨간색
GREEN = (0, 255, 0)     # 초록색 (힌트 경로 색상)
BLUE = (0, 0, 255)      # 파란색

WALL_COLOR = BLACK      # 일반 벽 색상
HINT_COLOR = GREEN      # 힌트 경로 색상
PATH_COLOR = BLUE       # (현재 사용되지 않음)

# 플레이어 설정
PLAYER_SPEED = 5        # 플레이어 이동 속도

# 페르소나 전환 키 설정
PERSONA_CHIRON = '1'    # 카이론 페르소나 전환 키
PERSONA_ERIDA = '2'     # 에리다 페르소나 전환 키
PERSONA_MORA = '3'      # 모라 페르소나 전환 키

# 페르소나별 캐릭터 색상
CHIRON_COLOR = BLUE     # 카이론 (이성) 색상: 파란색 계열
ERIDA_COLOR = RED       # 에리다 (감정) 색상: 빨간색 계열
MORA_COLOR = (128, 128, 128) # 모라 (관조) 색상: 회색 계열 (기존 보라색에서 변경)

# 능력 쿨다운 설정 (프레임 단위, 60프레임 = 1초)
HINT_COOLDOWN = 300     # 힌트 능력 쿨다운 (5초)
BREAK_WALL_COOLDOWN = 180 # 벽 부수기 능력 쿨다운 (3초)

# UI 색상 설정
UI_TEXT_COLOR = WHITE   # UI 텍스트 색상
UI_BACKGROUND_COLOR = (50, 50, 50) # UI 배경 색상 (어두운 회색)

PLAYER_COLOR = RED      # (현재 사용되지 않음, 페르소나별 색상 사용)

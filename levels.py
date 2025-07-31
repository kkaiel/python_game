
# levels.py
# 게임의 각 미로 레벨 데이터를 정의하는 파일입니다.
# 각 레벨은 2D 문자열 배열로 표현됩니다.

# 미로 타일 종류:
# 'X': 일반 벽 (통과 불가)
# 'P': 플레이어 시작 위치
# 'E': 미로 탈출구 (목표 지점)
# 'T': 투명한 벽 (모라만 통과 가능)
# 'B': 부술 수 있는 벽 (에리다만 파괴 가능)
# 'H': 움직이는 발판 (수평 이동)
# ' ': 빈 공간 (이동 가능)

# 레벨 1: 기본 미로 (튜토리얼)
# - 기본적인 이동과 미로 구조에 익숙해지기 위한 레벨입니다.
LEVEL_1 = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X P                X",
    "X XXXXXXX XXXXXXXX X",
    "X       X X        X",
    "X XXXXX X X XXXXXX X",
    "X X   X X X X      X",
    "X XXX X X X XXXXXX X",
    "X   X   X   X      X",
    "XXX XXXXXXX XXXXXX X",
    "X   X         X    X",
    "X XXXXX XXXXX X XX X",
    "X     X X   X X  X X",
    "X XXX XXXXX X XX X X",
    "X   X       X    X E",
    "XXXXXXXXXXXXXXXXXXXX",
]

# 레벨 2: 움직이는 플랫폼이 있는 미로
# - 움직이는 발판(H)을 활용하여 이동해야 하는 레벨입니다.
LEVEL_2 = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X P     X          X",
    "X XXXXX X XXXXXXXX X",
    "X       X          X",
    "X XXXXX XXXXX XXXX X",
    "X          H       X",
    "XXXXX XXXX XXXXXXX X",
    "X     X  X         X",
    "X XXXXX  X XXXXXXX X",
    "X X      X X       X",
    "X X  XXXXX X XXXXX X",
    "X X    H     X     X",
    "X XXXXXXX XXXXXX X X",
    "X                X E",
    "XXXXXXXXXXXXXXXXXXXX",
]

# 레벨 3: 각 인격의 능력이 필수인 복합 미로
# - 카이론(힌트), 에리다(벽 부수기), 모라(투명 벽 통과) 능력이 모두 필요한 레벨입니다.
LEVEL_3 = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X P X              X",
    "X X X XXXXXXXXXXXX X",
    "X   X            T X",
    "X X XXXXXXXXXXXX X X",
    "X X B            X X",
    "X X XXXXXXXXXXXX X X",
    "X X              X X",
    "X XXXXXXXXXXXXXX X X",
    "X                X X",
    "X XXXXXXXXXXXXXX X X",
    "X  H             X X",
    "X XXXXXXXXXXXXXX X X",
    "X                X E",
    "XXXXXXXXXXXXXXXXXXXX",
]

# 모든 레벨 데이터를 리스트로 묶어 관리합니다.
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]

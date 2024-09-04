import cv2
import os
from ultralytics import YOLO
import matplotlib.pyplot as plt

# YOLOv8 모델 불러오기 (pre-trained COCO dataset)
model = YOLO('firee.pt')

# 지정할 디렉토리
input_directory = '/home/orin/fireweb/bul'
output_directory = '/home/orin/fireweb/output'  # 결과 이미지를 저장할 디렉토리

# 결과 이미지를 저장할 디렉토리가 없다면 생성
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Get the list of all files in the input directory
files_and_folders = os.listdir(input_directory)
fire = []
firee = []

# 이미지 처리 및 저장
for item in files_and_folders:
    # 이미지 읽기
    image_path = os.path.join(input_directory, item)
    image = cv2.imread(image_path)

    # 이미지가 제대로 읽혔는지 확인
    if image is None:
        print(f"Error reading image {item}. Skipping.")
        continue

    # 이미지 분석 (객체 감지)
    results = model(image)

    # 감지된 객체가 포함된 이미지 시각화
    annotated_image = results[0].plot()

    # 결과 이미지 저장 - ensure the file extension is valid
    #save_path = os.path.join(output_directory, f"result_{os.path.splitext(item)[0]}.jpg")
    #cv2.imwrite(save_path, annotated_image)
    #print(f"Saved annotated image to {save_path}")

    # 이미지 출력 (선택 사항)
  #  plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
   # plt.axis('off')
    #plt.show()

    # 감지된 객체가 없는 경우 1 추가, 감지된 객체가 있는 경우 0 추가
    if len(results[0].boxes) == 0:  # No detections
        firee.append(1)
    else:
        firee.append(0)

    # 3개의 결과마다 한 번 fire 리스트에 추가
    if len(firee) == 3:
        fire.append(firee)
        firee = []





import pygame
import sys
import os

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 불이 난 상태를 표현하는 리스트 (7층부터 1층까지 내림차순)
#fire = [
#    [1, 0, 0],  # 7층
#    [1, 0, 0],  # 6층
#    [0, 0, 0],  # 5층
#    [0, 0, 0],  # 4층
#    [0, 0, 0],  # 3층
#    [0, 0, 0],  # 2층
#    [0, 0, 0],  # 1층
#]

# Pygame 초기화 및 화면 설정
pygame.init()
screen_width, screen_height = 1920, 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Building Evacuation Plan")

# 이미지 로딩 및 스케일링
floor_plan_img = pygame.image.load('평면도1.png')  # 평면도 이미지를 로드
floor_plan_img = pygame.transform.scale(floor_plan_img, (1920, 1080))  # 화면 크기에 맞게 조정
fire_img = pygame.image.load("불.png")  # 불 이미지 로드
fire_img = pygame.transform.scale(fire_img, (200, 200))  # 불 이미지 크기 조정

# 폰트 설정 (글자 크기 증가)
font = pygame.font.SysFont(None, 250)

# 불이 난 위치 좌표 (1번, 2번, 3번 통로 위치)
fire_positions = [
    (250, 660),   # 1번 통로 (기존보다 100 상향)
    (1340, 672),  # 2번 통로 (기존보다 100 상향)
    (1630, 300),  # 3번 통로 (기존보다 100 상향)
]

# 저장할 디렉토리 생성 및 이전 파일 삭제
output_dir = "/home/orin/fireweb/sever/static/uploads" 
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    # 디렉토리가 존재하는 경우 기존 파일 삭제
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

# 게임 루프
running = True

# 각 층에 대해 이미지를 생성
for i, floor in enumerate(fire):
    screen.fill(WHITE)

    # 배경 이미지 렌더링
    screen.blit(floor_plan_img, (0, 0))

    # 불이 난 경우에만 불 이미지 렌더링
    if any(floor):
        for j, status in enumerate(floor):
            if status == 1:
                fire_x, fire_y = fire_positions[j]  # 통로 위치에 따라 좌표 설정
                screen.blit(fire_img, (fire_x, fire_y))

    # 층 번호 텍스트 렌더링 (층 번호를 "1F", "2F" 등으로 표시)
    floor_text = font.render(f'{7-i}F', True, BLACK)
    screen.blit(floor_text, (50, 50))  # 층 번호 위치 조정

    # 화면을 업데이트하고 이미지를 저장
    pygame.display.flip()
    output_path = os.path.join(output_dir, f'{7-i}층.png')
    pygame.image.save(screen, output_path)  # 각 층의 이미지를 저장

pygame.quit()


##대피 경로 코드
from collections import deque
rt=[]
yt=0
y=0
passage = 3
floor = 7
fire = [
    [1, 0, 1],
    [0, 0, 0],
    [1, 0, 1],
    [1, 0, 0],
    [1, 0, 0],
    [0, 0, 0],
    [1, 0, 1],
]
print(fire)
for i in fire:
    print(i)
print()

escape_direction = [['' for _ in range(passage)] for _ in range(floor)]
queue = deque()

# 출구는 맨 아래층의 모든 칸
for j in range(passage):
    if fire[floor-1][j] == 0:
        queue.append((floor-1, j))
        escape_direction[floor-1][j] = '출구'

# BFS를 사용하여 각 칸에서 출구로 가는 경로를 찾음
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
direction_names = ['위', '아래', '오른쪽', '왼쪽']

while queue:
    y, x = queue.popleft()
    
    for (dy, dx), dir_name in zip(directions, direction_names):
        ny, nx = y + dy, x + dx
        if 0 <= ny < floor and 0 <= nx < passage and fire[ny][nx] == 0 and escape_direction[ny][nx] == '':
            queue.append((ny, nx))
            if ny == floor-1:
                escape_direction[ny][nx] = '출구'
            else:
                if (dy, dx) == (-1, 0):  # 위에서 내려오는 경우
                    escape_direction[ny][nx] = '아래'
                elif (dy, dx) == (1, 0):  # 아래에서 올라오는 경우
                    escape_direction[ny][nx] = '위'
                elif (dy, dx) == (0, -1):  # 왼쪽에서 오는 경우
                    escape_direction[ny][nx] = '오른쪽'
                elif (dy, dx) == (0, 1):  # 오른쪽에서 오는 경우
                    escape_direction[ny][nx] = '왼쪽'
# 필요한 경우 방향을 조정하여 모든 칸에 대해 올바른 방향을 설정
for i in range(floor):
    for j in range(passage):
        if escape_direction[i][j] == '':
            if i < floor - 1 and escape_direction[i + 1][j] == '출구':
                escape_direction[i][j] = '아래'
            elif j < passage - 1 and escape_direction[i][j + 1] == '출구':
                escape_direction[i][j] = '오른쪽'
            elif j > 0 and escape_direction[i][j - 1] == '출구':
                escape_direction[i][j] = '왼쪽'
            elif i > 0 and escape_direction[i - 1][j] == '출구':
                escape_direction[i][j] = '위'

for i in escape_direction:
    print(i)
    rt.append(i)
##print(y)





r=len(fire)
firee=[]
while r:
    r=r-1
    firee.append(fire[r])
a=firee
##print(a)
b=len(a)
c=0
h=[]
hh=[]
hhh=[]
hhhh=[]
q=[]
yt=0
yy=0
yyy=0
yyyy=0
while b:
    b=b-1
##    print(a[c])
    g=-1
    if 1 in a[c]:
##        print('잡았다 요놈',c)
        d=3
        r=0
        while d:
            d=d-1
            g=g+1
            if a[c][g]==1:
                r=r+1
                if g==0:
                    h.append(c+1)
                    yy=1
                if g==1:
                    hh.append(c+1)
                    yyy=1
                if g==2:
                    hhh.append(c+1)
                    yyyy=1
        if r==3:
            hhhh.append(c+1)
            yt=1
        q.append(c)
    c=c+1
print('1번 통로 불', h)
print('2번 통로 불', hh)
print('3번 통로 불', hhh)
print('3통로 다 불',hhhh)
if yt==1:
    print(str(hhhh[0])+"층부터 7층은 옥상으로 대피")
if y!=0:
    print(str(floor-y+1)+"층부터 7층은 옥상으로 대피하십시오")

print(i,rt)
##대피 경로 코드












##전체도 코드
import pygame
import sys
import os

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 예시 데이터 (fire 대신 실제 데이터를 넣어야 함)
##bulding = [
##    ['오른쪽', '아래', '왼쪽'],
##    ['', '아래', ''],
##    ['오른쪽', '', '왼쪽'],
##    ['아래', '오른쪽', ''],
##    ['왼쪽', '', '아래'],
##    ['', '오른쪽', ''],
##    ['왼쪽', '', '오른쪽'],
##]
bulding = rt
# Pygame 초기화 및 화면 설정
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("건물 대피로 사진")

# 이미지 로딩 및 스케일링
b = pygame.image.load(os.path.join("불.png"))
b = pygame.transform.scale(b, (150, 150))
c = pygame.image.load(os.path.join("오른.png"))
c = pygame.transform.scale(c, (100, 100))
d = pygame.image.load(os.path.join("아래.png"))
d = pygame.transform.scale(d, (100, 100))
e = pygame.image.load(os.path.join("왼.png"))
e = pygame.transform.scale(e, (100, 100))
f = pygame.image.load(os.path.join("위.png"))
f = pygame.transform.scale(f, (100, 100))

# 폰트 설정
font = pygame.font.SysFont(None, 36)

# 층 및 통로 설정
floor = 7
passage = 3
floor_height = screen_height // floor
floor_width = 400
floor_x = (screen_width - floor_width) // 2
passage_width = floor_width // passage

# 저장할 디렉토리 생성
output_dir = "/home/orin/fireweb/sever/static/uploads"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 화면 그리기
screen.fill(WHITE)

# 층과 통로 그리기
for i in range(floor):
    floor_y = i * floor_height  # 층을 위에서 아래로 그리기
    pygame.draw.rect(screen, BLACK, (floor_x, floor_y, floor_width, floor_height), 5)
    for j in range(passage):
        passage_x = floor_x + j * passage_width
        pygame.draw.rect(screen, BLACK, (passage_x, floor_y, passage_width, floor_height), 2)

# 사각형 위치 업데이트
for r in range(floor):
    for rr in range(passage):
        x = floor_x + rr * passage_width
        y = r * floor_height
        if bulding[r][rr] == '':
            screen.blit(b, (x, y - 30))
        if bulding[r][rr] == '오른쪽':
            screen.blit(c, (x, y - 30))
        if bulding[r][rr] == '왼쪽':
            screen.blit(e, (x, y - 30))
        if bulding[r][rr] == '위쪽':
            screen.blit(f, (x, y - 30))
        if bulding[r][rr] == '아래':
            screen.blit(d, (x, y - 30))

# "overall view" 텍스트 추가
text = font.render("overall view", True, BLACK)
text_rect = text.get_rect(center=(100,20))  # 화면 하단 중앙에 배치
screen.blit(text, text_rect)  # 텍스트를 화면에 그리기

# 이미지 저장
pygame.image.save(screen, os.path.join(output_dir, '전체도.png'))

# Pygame 종료
pygame.quit()
sys.exit()




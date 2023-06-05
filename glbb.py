import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()
clock = pygame.time.Clock()

#warna
hitam = (0, 0, 0)
merah = (255, 0, 0)
coklat = (205, 133, 63)
putih = (255, 255, 255)
salju =(238, 246, 247)

warna_background = (202, 201, 255)
warna_gravitasi = (255,100,100)
warna_benda = (255, 0, 0)
warna_button = (0,0,0)
warna_garis = (0, 0, 0)
warna_teks = (0, 0, 0)
warna_teks2 = (255, 255, 255)


width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
surface = pygame.Surface((width, height), pygame.SRCALPHA)
pygame.Surface.fill(surface, (warna_background))
pygame.display.set_caption("GLBB")



# properti bola
radius_bola = 50
ball_x, ball_y = 500, 0
bayangan = []

# inputan
v_input = "100"  # input kecepatan
ball_vx, ball_vy = int(v_input) / 100, 0
g = 9.8 / 10000
dt = 0
time = 0
angle = 0
laju = 100

box_theme = pygame.Rect(width-70,20,25,25)

# Batas bola agar tidak melebihi window
side_Top = ball_y - 30
side_Bot = ball_y + 450
side_Left = ball_x - 40
side_Right = ball_x + 900

# tambahan
dragging_x, dragging_y = False, False
fall = True
rotation = True
hold = False
theme = False
gravitasi = True
gravitasiLine = 1

# Input
playBox = [
    (499, 539, 52, 52),  # Border luar
    (502, 542, 46, 46),  # border putih
    ((515, 550), (540, 565), (515, 580)),  # Play
    (515, 550, 7, 30),  # Pause
    (530, 550, 7, 30),  # Pause
    (561, 550, 30, 30),  # Play Kanan
    (459, 550, 30, 30),  # Play Kiri
    pygame.Rect(369, 550, 200, 30),  # input nilai kecepatan
]


def button(teks, xywh, color, active_color):
    mouse = pygame.mouse.get_pos()
    x, y, w, h = xywh[0], xywh[1], xywh[2], xywh[3]
    pygame.draw.rect(screen, color, (x, y, w, h), 0, 5)
    smallText = pygame.font.SysFont("Arial", 20)
    textSurf, textRect = text_objects(teks, smallText, warna_teks2)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h), 0, 5)
        smallText = pygame.font.SysFont("Arial", 20)
        textSurf, textRect = text_objects(teks, smallText, putih)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

class Lingkaran(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        radius1 = random.randint(1, 4)  # Radius lingkaran
        self.warna = salju

        # Membuat permukaan lingkaran dengan ukuran diameter
        self.image = pygame.Surface((radius1 * 2, radius1 * 2), pygame.SRCALPHA)

        # Menggambar lingkaran pada permukaan dengan warna putih
        pygame.draw.circle(self.image, (self.warna), (radius1, radius1), radius1, 0)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(-300, 2000)
        self.rect.y = 500
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed - 1
        if self.rect.y > 495:
            self.rect.x = random.randint(-300, 2000)
            self.rect.y = random.randint(-450, -100)
            self.speed = random.randint(2, 5)


lingkaran_group = pygame.sprite.Group()

for _ in range(5):
    for i in range(60):
        lingkaran = Lingkaran()
        lingkaran_group.add(lingkaran)


while True:
    latest_x, latest_y = ball_x, ball_y

    
    # Mendapatkan input dari pengguna =====================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if slider[0].collidepoint(event.pos) or slider[1].collidepoint(event.pos):
                x, y = event.pos
                if x > 50 and x < 900:
                    ball_x = x
                    dragging_x = True
                    hold = True
            if slider[2].collidepoint(event.pos) or slider[3].collidepoint(event.pos):
                x, y = event.pos
                if y > 30 and y < 450:
                    ball_y = y
                    dragging_y = True
                    hold = True
            if (
                play[0].collidepoint(event.pos)
                or play[1].collidepoint(event.pos)
                or play[2].collidepoint(event.pos)
            ):
                if hold or not hold:
                    hold = not hold

            if pygame.draw.rect(surface, putih, playBox[5]).collidepoint(event.pos):
                if v_input == '':
                    v_input = "0"
                    ball_vx = int(v_input) / laju
                else:
                    ball_vx = int(v_input) / laju
                # ball_vx = -int(v_input) / laju
                if hold:
                    hold = not hold
                print("kanan")
            if pygame.draw.rect(surface, putih, playBox[6]).collidepoint(event.pos):
                if v_input == '':
                    v_input = "0"
                    ball_vx = -int(v_input) / laju
                else:
                    ball_vx = -int(v_input) / laju
                # ball_vx = -int(v_input) / laju
                if hold:
                    hold = not hold
                print("kiri")

            if pygame.draw.rect(surface, warna_benda, box_theme, 0, 10).collidepoint(event.pos):
                if theme:
                    theme = False
                else:
                    theme = True
            if gravitasiButton.collidepoint(event.pos):
                if gravitasi:
                    gravitasi = not gravitasi
                else:
                    gravitasi = not gravitasi

        if event.type == pygame.MOUSEBUTTONUP:
            dragging_x, dragging_y = False, False

        if event.type == pygame.MOUSEMOTION:
            if dragging_x:
                x, y = event.pos
                if x > 50 and x < 900:
                    ball_x = x
                
            if dragging_y:
                x, y = event.pos
                if y > 30 and y < 450:
                    ball_y = y
                    hold = True

        if event.type == pygame.KEYDOWN:
            # input
            if event.key == pygame.K_BACKSPACE:
                v_input = v_input[:-1]
            elif event.key >= pygame.K_0 and event.key <= pygame.K_9:
                if len(v_input) <= 3:
                    v_input += pygame.key.name(event.key)
                    # Pop-up alert jika nilai input lebih dari 1000
                    if int(v_input) >= 1000:
                        tk.Tk().withdraw()
                        messagebox.showinfo("Out of Range", "Mohon Input angka kurang dari 1000!")
                        v_input = '0'
                        ball_x, ball_y = width/2, height/2
                        ball_vx = 0
                else:
                    # Pop-up alert jika digit input lebih dari 3
                    tk.Tk().withdraw()
                    messagebox.showinfo("Out of Range", "Input angka melebihi 3 digit!")
                    ball_x, ball_y = width/2, height/2
                    ball_vx = 0
            elif event.key == pygame.K_RETURN:
                if v_input == '':
                    v_input = "0"
                    ball_vx = int(v_input) / 300
                else:
                    ball_vx = int(v_input) / 300
                # ball_vx = int(v_input) / 300
                if hold:
                    hold = not hold

            elif event.key == pygame.K_SPACE:
                v_input = '0'
                ball_vx = 0 

            else:
                diklik = event.unicode
                try:
                    cek = int(diklik)
                    if v_input == "0":
                        v_input = ""
                    if v_input == "":
                        v_input = "0"
                    v_input += diklik
                except:
                    pass
  

    
    lingkaran_group.update()
    lingkaran_group.draw(screen)
    surface.fill(warna_background)
    dt = clock.tick_busy_loop(60)


    # slider
    slider = [
        pygame.draw.line(surface, (warna_garis), (50, 530), (900, 530), 4),  # slid Horizontal
        pygame.draw.circle(surface, merah, (ball_x, 531), 6),  # titik horizontal
        pygame.draw.line(surface, (warna_garis), (980, 30), (980, 450), 4),  # slider vertikal
        pygame.draw.circle(surface, merah, (981, ball_y), 6),  # titik vertikal
    ]
    
    # pergerakan bola
    if not hold:
        ## gerakan bola horizontal ======================
        if ball_vx != 0:
            ball_x += ball_vx * dt
            ball_vx -= ball_vx / 325
            if ball_vx > -0.02 and ball_vx < 0.02:
                ball_vx = 0
            # memantul dibagian sisi kiri dan kanan window
            if ball_x <= 50 or ball_x >= 900:
                ball_vx = -ball_vx

        ## manipulasi gravitasi, pantulan dan gerakan vertikal =======================
        if gravitasi:
            if fall and side_Bot <= height:
                ball_y += g * (time**2) * dt
                time += 1
            if ball_y >= side_Bot:
                fall = False
                time = time / 1.2
            if not fall:
                ball_y -= g * (time**2) * dt
                time -= 1
            if time < 1:
                fall = True
                time = 0

    ##bola mengecil dan membatasi agar tidak melebihi window ================
    if ball_y <= 30:
        radius_bola = 20
        ball_y = 30
    # bola membesar
    elif ball_y >= 450:
        radius_bola = 50
        ball_y = 450
    #  transisi bola dari kecil ke besar
    else:
        radius_bola = 50 + (20 - 50) * (1 - ball_y / 400)

    ## putaran bola ================================
    if latest_x < ball_x:
        angle -= ((abs(ball_x - latest_x) * 360) / (3.14)) / 200
    if latest_x > ball_x:
        angle += ((abs(ball_x - latest_x) * 360) / (3.14)) / 200

    ## menghitung garis bola ==============================
    cos = math.cos(math.radians(angle) * -1)
    sin = math.sin(math.radians(angle) * -1)

    x = [
        (
            ball_x + (-radius_bola * cos) - (0 * sin),
            (-radius_bola * sin) + (0 * cos) + ball_y,
        ),
        (
            ball_x + (radius_bola * cos) - (0 * sin),
            (radius_bola * sin) + (0 * cos) + ball_y,
        ),
        (
            ball_x + (0 * cos) - (-radius_bola * sin),
            (0 * sin) + (-radius_bola * cos) + ball_y,
        ),
        (
            ball_x + (0 * cos) - (radius_bola * sin),
            (0 * sin) + (radius_bola * cos) + ball_y,
        ),
    ]

    bola = [
        pygame.draw.circle(surface, merah, (ball_x, ball_y), radius_bola + 2),
        pygame.draw.circle(surface, hitam, (ball_x, ball_y), radius_bola + 3, 2),
        (pygame.draw.line(surface, hitam, x[1], x[0], 3)),  # garis
        (pygame.draw.line(surface, hitam, x[3], x[2], 3)),  # garis
        pygame.draw.line(surface, (coklat), (0, 506), (1000, 506), 7),  # ground
        pygame.draw.line(surface, (salju), (0, 500), (1000, 500), 4),  # ground
    ]

    button1 = [
        button(">", playBox[5], warna_button, merah),
        button("<", playBox[6], warna_button, merah),
    ]

    input_rect = playBox[7]
    base_font_input = pygame.font.Font(None, 35)
    pygame.draw.rect(screen, merah, input_rect, width=3)
    text_surface = base_font_input.render(v_input, True, warna_teks)
    screen.blit(text_surface, (input_rect.x + 7, input_rect.y + 3))
    input_rect.w = max(70, text_surface.get_width() + 10)

    # Play Button
    if hold:
        play = [
            pygame.draw.rect(surface, merah, playBox[0], 0, 18),
            pygame.draw.rect(surface, putih, playBox[1], 0, 18),
            pygame.draw.polygon(surface, merah, playBox[2]),
        ]
    else:
        play = [
            pygame.draw.rect(surface, merah, playBox[0], 0, 18),
            pygame.draw.rect(surface, putih, playBox[1], 0, 18),
            pygame.draw.rect(surface, merah, (515, 550, 7, 30), 0, 18),
            pygame.draw.rect(surface, merah, (530, 550, 7, 30), 0, 18),
        ]

    gravitasiButton = pygame.draw.circle(surface, warna_gravitasi, (width-60, height-40), 20, gravitasiLine)
    if gravitasi:
        warna_gravitasi =  (255, 100, 100)
        gravitasiLine = 1
    else:
        warna_gravitasi = (255, 100, 100)
        gravitasiLine = 100

    #THEME
    pygame.draw.rect(surface, warna_benda, box_theme, 0, 10)
    if theme:
        warna_benda, warna_garis, warna_teks = (255,255,255), (255,255,255), (255, 255, 255)
        warna_background = (30, 30, 30)
        warna_button = (255, 255, 255)
        warna_teks2 = (0,0,0)
        bulan = [
                    pygame.draw.circle(surface, (246, 241, 213), (50, 50), 30),
                    pygame.draw.circle(surface, (30, 30, 30), (44, 48), 26)
                ]

    else:
        warna_benda, warna_garis, warna_teks = (0, 0, 0), (0, 0, 0), (0, 0, 0)
        warna_background = (202, 201, 255)
        warna_button = (0,0,0)
        warna_teks2 = (255,255,255)
    # END THEME

    pygame.display.flip()
    pygame.display.update()
    screen.blit(surface, (0, 0))
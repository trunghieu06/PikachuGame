import pygame
import random
import sys
import os
import glob
import math
import json
import time

# Màu sắc (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
DARK_GRAY = (169, 169, 169)
PURPLE = (128, 0, 128)
ICE_BLUE = (173, 216, 230)
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1600, 900
SETTING_WIDTH, SETTING_HEIGHT = 800, 600
button = pygame.image.load('button.png')
button_pressed = pygame.image.load('button_pressed.png')
med_button = pygame.image.load('med_button.png')
med_button_pressed = pygame.image.load('med_button_pressed.png')
setting_button = pygame.image.load('setting.png')
setting_pressed_button = pygame.image.load('setting_pressed.png')
setting_button = pygame.transform.scale(setting_button, (100, 100))
setting_pressed_button = pygame.transform.scale(setting_pressed_button, (100, 100))
on_button, off_button = pygame.image.load('on_button.png'), pygame.image.load('off_button.png')
skill_button = pygame.image.load('skill.png')
skill_pressed_button = pygame.image.load('skill_pressed.png')
skill_button, skill_pressed_button = pygame.transform.scale(skill_button, (100, 100)), pygame.transform.scale(skill_pressed_button, (100, 100))
fire = pygame.image.load('fire.png')
fire = pygame.transform.scale(fire, (80, 80))
on_button = pygame.transform.scale(on_button, (100, 50))
off_button = pygame.transform.scale(off_button, (100, 50))
typing_box = pygame.image.load('typing_box.png')
frame = pygame.image.load('frame.png')
background = pygame.image.load('background.png')
game_background = pygame.image.load('game_background.png')
background = pygame.transform.scale(background, (int(WIDTH * 1.2), int(HEIGHT * 1.2)))
game_background = pygame.transform.scale(game_background, (int(WIDTH * 1.2), int(HEIGHT * 1.2)))
setting_background = pygame.image.load('setting_background.png')
pokemon_background = pygame.image.load('pokemon_background.png')
pokemon_ball = pygame.image.load('pokemon_ball.png')
pokemon_background = pygame.transform.scale(pokemon_background, (170, 170))
pokemon_ball = pygame.transform.scale(pokemon_ball, (170, 170))
setting_background.set_alpha(240)
bg_width, bg_height = background.get_size()
font_logo = pygame.font.Font('Knewave-Regular.ttf', 100)
# font_mess = pygame.font.Font('Anton-Regular.ttf', 80)
font_big = pygame.font.Font('Anton-Regular.ttf', 60)
font_reg = pygame.font.Font('Anton-Regular.ttf', 32)
font_mini = pygame.font.Font('Anton-Regular.ttf', 20)
IMAGE_SIZE = (50, 40)
path = [i.replace('\\', '/') for i in glob.glob('./DataSet/*.png')]
NO_IMAGE = len(path)
pokemon_images = [pygame.image.load(path[i]) for i in range(NO_IMAGE)]
path = [i.replace('\\', '/') for i in glob.glob('./Pokemon/*.png')]
NO_CHAR = len(path)
character_images = [pygame.image.load(path[i]) for i in range(NO_CHAR)]
character_images = [pygame.transform.scale(i, (120, 120)) for i in character_images]
button_selected_sound = pygame.mixer.Sound('Sound/button_selected.mp3')
pop_sound = pygame.mixer.Sound('Sound/pop.mp3')
path = [i.replace('\\', '/') for i in glob.glob('./Background music/*.mp3')]
background_music = [pygame.mixer.Sound(path[i]) for i in range(len(path))]
background_music_names = [
    'Kirby Dream Land',
    'Mario',
    'Nintendo Wii',
    'Sanctuary Guardians'
]
volume_on, sound_on, music_on, music_id = True, True, True, 2
background_music[music_id].play(-1)
clock = pygame.time.Clock()

def draw_img(screen, img, x, y):
    screen.blit(img, (x, y))

def draw_img_center(screen, img, x, y):
    screen.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
    
def draw_text(screen, font, text, color, x, y, idx = -1):
    text_colors = []
    for i in range(len(text)):
        text_colors.append(color)
    if idx != -1 and idx < len(text):
        for i in range(len(text)):
            if i == idx:
                text_colors[i] = WHITE
            else:
                brightness = max(128, 255 - abs(i - idx) * 30) 
                text_colors[i] = (brightness, brightness, brightness)
    for i in range(len(text)):
        text_ = font.render(text[i], True, text_colors[i])
        screen.blit(text_, (x, y))
        x += font.size(text[i])[0]
    
def draw_text_center(screen, font, text, color, x, y, idx = -1):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


class Player:    
    def __init__(self, username, password, cash = 0, inventory = [0], row = 4, col = 4, timer = -100, mode = 'no timer', cd = 0, lose = False, grid = [[-1] * (4 + 3) for _ in range(4 + 3)]):
        self.username = username
        self.password = password
        self.cash = cash
        self.inventory = inventory
        self.row = row
        self.col = col
        self.timer = timer
        self.mode = mode
        self.cd = cd
        self.lose = lose
        self.grid = grid
        self.cods = [[-1] * (self.col + 3) for _ in range(self.row + 3)]
        self.grid_button = [[pygame.Rect(0, 0, 0, 0)] * (self.col) for _ in range(self.row)]
        x = (HEIGHT - self.row * IMAGE_SIZE[0]) // 2
        for i in range(self.row):
            y = (WIDTH - self.col * IMAGE_SIZE[1]) // 2
            for j in range(self.col):
                self.grid_button[i][j] = pygame.Rect(y, x, IMAGE_SIZE[1], IMAGE_SIZE[0])
                self.cods[i + 1][j + 1] = (y + IMAGE_SIZE[1] // 2, x + IMAGE_SIZE[0] // 2)
                y += IMAGE_SIZE[1]
            x += IMAGE_SIZE[0]
        for i in range(1, self.col + 1):
            self.cods[0][i] = (self.cods[1][i][0], self.cods[1][i][1] - IMAGE_SIZE[0])
            self.cods[self.row + 1][i] = (self.cods[self.row][i][0], self.cods[self.row][i][1] + IMAGE_SIZE[0])
        for i in range(1, self.row + 1):
            self.cods[i][0] = (self.cods[i][1][0] - IMAGE_SIZE[1], self.cods[i][1][1])
            self.cods[i][self.col + 1] = (self.cods[i][self.col][0] + IMAGE_SIZE[1], self.cods[i][self.col][1])
        self.reset_grid()
    def reset_grid(self):
        if self.timer != -100:
            self.timer = self.row * self.col
        self.cods = [[-1] * (self.col + 3) for _ in range(self.row + 3)]
        self.grid_button = [[pygame.Rect(0, 0, 0, 0)] * (self.col) for _ in range(self.row)]
        x = (HEIGHT - self.row * IMAGE_SIZE[0]) // 2
        for i in range(self.row):
            y = (WIDTH - self.col * IMAGE_SIZE[1]) // 2
            for j in range(self.col):
                self.grid_button[i][j] = pygame.Rect(y, x, IMAGE_SIZE[1], IMAGE_SIZE[0])
                self.cods[i + 1][j + 1] = (y + IMAGE_SIZE[1] // 2, x + IMAGE_SIZE[0] // 2)
                y += IMAGE_SIZE[1]
            x += IMAGE_SIZE[0]
        for i in range(1, self.col + 1):
            self.cods[0][i] = (self.cods[1][i][0], self.cods[1][i][1] - IMAGE_SIZE[0])
            self.cods[self.row + 1][i] = (self.cods[self.row][i][0], self.cods[self.row][i][1] + IMAGE_SIZE[0])
        for i in range(1, self.row + 1):
            self.cods[i][0] = (self.cods[i][1][0] - IMAGE_SIZE[1], self.cods[i][1][1])
            self.cods[i][self.col + 1] = (self.cods[i][self.col][0] + IMAGE_SIZE[1], self.cods[i][self.col][1])
        pre_img = random.randint(0, NO_IMAGE - 1)
        cnt = 1
        self.grid = [[-1] * (self.col + 3) for _ in range(self.row + 3)]
        self.grid[1][1] = pre_img
        while cnt < self.row * self.col:
            i, j = random.randint(1, self.row), random.randint(1, self.col)
            while self.grid[i][j] != -1:
                i, j = random.randint(1, self.row), random.randint(1, self.col)
            self.grid[i][j] = pre_img
            if cnt == self.row * self.col - 1:
                break
            pre_img = random.randint(0, NO_IMAGE - 1)
            while self.grid[i][j] != -1:
                i, j = random.randint(1, self.row), random.randint(1, self.col)
            self.grid[i][j] = pre_img
            cnt += 2
        if self.mode != 'no timer':
            self.timer = self.row * self.col * 2
        self.cd = 0
    def check_1(self, pt1, pt2):
        # 2 cases
        if pt1[0] == pt2[0]:
            if pt1[1] > pt2[1]:
                pt1, pt2 = pt2, pt1
            for i in range(pt1[1] + 1, pt2[1]):
                if self.grid[pt1[0]][i] != -1:
                    return False
            return True
        elif pt1[1] == pt2[1]:
            if pt1[0] > pt2[0]:
                pt1, pt2 = pt2, pt1
            for i in range(pt1[0] + 1, pt2[0]):
                if self.grid[i][pt1[1]] != -1:
                    return False
            return True
        else:
            return False

    def check_2(self, screen, pt1, pt2, dr):
        pt3 = (pt1[0], pt2[1])
        if self.grid[pt3[0]][pt3[1]] == -1 and self.check_1(pt1, pt3) and self.check_1(pt3, pt2):
            if dr == True:
                return [(pt1, pt3), (pt3, pt2)]
            return True
        pt3 = (pt2[0], pt1[1])
        if self.grid[pt3[0]][pt3[1]] == -1 and self.check_1(pt1, pt3) and self.check_1(pt3, pt2):
            if dr == True:
                return [(pt1, pt3), (pt3, pt2)]
            return True
        return False

    def check_3(self, screen, pt1, pt2, dr):
        # case 1:
        if pt1[1] > pt2[1]:
            pt1, pt2 = pt2, pt1
        i = pt1[0] - 1
        while i >= 0:
            if self.grid[i][pt1[1]] != -1:
                break
            if self.check_2(screen, (i, pt1[1]), pt2, dr):
                if dr == True:
                    rs = self.check_2(screen, (i, pt1[1]), pt2, True)
                    rs.append((pt1, (i, pt1[1])))
                    return rs
                return True
            i -= 1
        # case 2:
        i = pt1[0] + 1
        while i <= self.row + 1:
            if self.grid[i][pt1[1]] != -1:
                break
            if self.check_2(screen, (i, pt1[1]), pt2, dr):
                if dr == True:
                    rs = self.check_2(screen, (i, pt1[1]), pt2, True)
                    rs.append((pt1, (i, pt1[1])))
                    return rs
                return True
            i += 1
        # case 3:
        i = pt1[1] - 1
        while i >= 0:
            if self.grid[pt1[0]][i] != -1:
                break
            if self.check_2(screen, (pt1[0], i), pt2, dr):
                if dr == True:
                    rs = self.check_2(screen, (pt1[0], i), pt2, True)
                    rs.append((pt1, (pt1[0], i)))
                    return rs
                return True
            i -= 1
        # case 4:
        i = pt1[1] + 1
        while i <= self.col + 1:
            if self.grid[pt1[0]][i] != -1:
                break
            if self.check_2(screen, (pt1[0], i), pt2, dr):
                if dr == True:
                    rs = self.check_2(screen, (pt1[0], i), pt2, True)
                    rs.append((pt1, (pt1[0], i)))
                    return rs
                return True
            i += 1
        return False
    def is_valid(self, screen, pt1, pt2, dr):
        if self.check_1(pt1, pt2):
            if dr == True:
                return [(pt1, pt2)]
            return True
        elif self.check_2(screen, pt1, pt2, dr):
            return self.check_2(screen, pt1, pt2, dr)
        elif self.check_3(screen, pt1, pt2, dr):
            return self.check_3(screen, pt1, pt2, dr)
        else:
            return False
    def find_move(self, screen):
        for i in range(self.row):
            for j in range(self.col):
                for ii in range(self.row):
                    for jj in range(self.col):
                        if i == ii and j == jj:
                            continue
                        if self.grid[i + 1][j + 1] != -1 and self.grid[i + 1][j + 1] == self.grid[ii + 1][jj + 1] and self.is_valid(screen, (i + 1, j + 1), (ii + 1, jj + 1), False):
                            return (i + 1, j + 1), (ii + 1, jj + 1)
        return -1
    def suffle(self):
        a = []
        for i in range(self.row):
            for j in range(self.col):
                if self.grid[i + 1][j + 1] != -1:
                    a.append(self.grid[i + 1][j + 1])
                    self.grid[i + 1][j + 1] = 0
        random.shuffle(a)
        ind = 0
        for i in range(self.row):
            for j in range(self.col):
                if self.grid[i + 1][j + 1] == 0:
                    self.grid[i + 1][j + 1] = a[ind]
                    ind += 1
                    
    def is_winning(self):
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if self.grid[i][j] != -1:
                    return False
        return True
    
    def choose_size(self, screen):
        # 4x4, 6x6, 8x8, 10x10, 16x16, custom
        idx = [1] * 6
        text = [
            "4 x 4",
            "6 x 6",
            "8 x 8",
            "10 x 10",
            "12 x 12",
            "Custom"
        ]
        button_ = [
            pygame.Rect(WIDTH // 2 - WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 + WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 - WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 6 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 + WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 6 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 - WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 + WIDTH // 6 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2 - button.get_height() // 2, button.get_width(), button.get_height())
        ]
        exit1_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2.7 - med_button.get_height() // 2, med_button.get_width(), med_button.get_height())
        running = True
        customizming = False
        row, col = '', ''
        status = 'row'
        confirm_idx, exit_idx = -1, -1
        exit1_idx = -1
        mess = "ROW MUST BE IN RANGE [4, 16] AND COLUMN MUST BE IN RANGE [4, 24]"
        mess_counter = 0
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_ratio = mouse_x / WIDTH
            y_ratio = mouse_y / HEIGHT
            bg_x = -int((bg_width - WIDTH) * x_ratio)
            bg_y = -int((bg_height - HEIGHT) * y_ratio)
            bg_x = max(min(bg_x, 0), WIDTH - bg_width)
            bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
            screen.blit(game_background, (bg_x, bg_y))
            draw_text_center(screen, font_logo, "CHOOSE SIZE", GRAY, WIDTH // 2, HEIGHT // 4)
            
            if customizming == True:
                
                # draw image
                row_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.3 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
                col_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
                confirm_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2 - button.get_height() // 2, button.get_width(), button.get_height())        
                exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3 - med_button.get_height() // 2, 150, 50)
                draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.3)
                draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8)
                draw_img_center(screen, button_pressed if confirm_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2)
                draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3)
                # draw text username and password
                if row_box.collidepoint(*pygame.mouse.get_pos()) == False and row == '':
                    draw_text_center(screen, font_reg, "ENTER NUMBER OF ROW", GRAY, WIDTH // 2, HEIGHT // 2.3)
                else:
                    draw_text(screen, font_reg, row, GRAY, WIDTH // 2 - font_reg.size(row)[0] // 2, HEIGHT // 2.3 - font_reg.size(row)[1] // 2)
                if col_box.collidepoint(*pygame.mouse.get_pos()) == False and col == '':
                    draw_text_center(screen, font_reg, "ENTER NUMBER OF COLUMN", GRAY, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8)
                else:
                    draw_text(screen, font_reg, col, GRAY, WIDTH // 2 - font_reg.size(col)[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 - font_reg.size(col)[1] // 2)
                if status == 'row' and row != '' and pygame.time.get_ticks() % 1000 < 500:
                    draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(row)[0] // 2 + 5, HEIGHT // 2.3)
                if status == 'col' and col != '' and pygame.time.get_ticks() % 1000 < 500:
                    draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(col)[0] // 2 + 5, HEIGHT // 2.3 + HEIGHT // 8)
                # draw text login, exit and mess
                if confirm_button.collidepoint(*pygame.mouse.get_pos()):
                    if confirm_idx == -1:
                        confirm_idx = 0
                else:
                    confirm_idx = -1
                draw_text(screen, font_reg, "CONFIRM", GRAY, WIDTH // 2 - font_reg.size("CONFIRM")[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2 - font_reg.size("CONFIRM")[1] // 2, confirm_idx)
                if confirm_idx != -1:
                    confirm_idx += 1
                if exit_button.collidepoint(*pygame.mouse.get_pos()):
                    if exit_idx == -1:
                        exit_idx = 0
                else:
                    exit_idx = -1
                draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3 - font_reg.size("EXIT")[1] // 2, exit_idx)
                if exit_idx != -1:
                    exit_idx += 1
                if mess_counter > 0:
                    draw_text_center(screen, font_reg, mess, RED, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 4)
                    mess_counter -= 1
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if row_box.collidepoint(event.pos):
                            status = 'row'
                        if col_box.collidepoint(event.pos):
                            status = 'col'
                        if confirm_button.collidepoint(event.pos):
                            if row == '' or col == '':
                                mess = "ROW AND COLUMN MUST BE NOT EMPTY"
                                mess_counter = 30
                            elif not row.isdigit() or not col.isdigit():
                                mess = "ROW AND COLUMN MUST BE NUMERIC"
                                mess_counter = 30
                            elif int(row) % 2 != 0 or int(col) % 2 != 0:
                                    mess = "ROW AND COLUMN MUST BE EVEN NUMBER"
                                    mess_counter = 30
                            elif int(row) < 4 or int(row) > 16 or int(col) < 4 or int(col) > 30:
                                mess = "ROW MUST BE IN RANGE [4, 16] AND COLUMN MUST BE IN RANGE [4, 30]"
                                mess_counter = 30
                            else:
                                self.row, self.col = int(row), int(col)
                                self.reset_grid()
                                return 'size choosen'
                        if exit_button.collidepoint(event.pos):
                            customizming = False
                    if event.type == pygame.KEYDOWN:
                        if status == 'row':
                            if event.key == pygame.K_BACKSPACE:
                                row = row[:-1]
                            elif event.key == pygame.K_RETURN:
                                status = 'col'
                            else:
                                row += event.unicode
                        elif status == 'col':
                            if event.key == pygame.K_BACKSPACE:
                                col = col[:-1]
                            elif event.key == pygame.K_RETURN:
                                if not row.isdigit() or not col.isdigit():
                                    mess = "ROW AND COLUMN MUST BE NUMERIC"
                                    mess_counter = 30
                                elif row == '' or col == '':
                                    mess = "ROW AND COLUMN MUST BE NOT EMPTY"
                                    mess_counter = 30
                                elif int(row) % 2 != 0 or int(col) % 2 != 0:
                                    mess = "ROW AND COLUMN MUST BE EVEN NUMBER"
                                    mess_counter = 30
                                elif int(row) < 4 or int(row) > 16 or int(col) < 4 or int(col) > 30:
                                    mess = "ROW MUST BE IN RANGE [4, 16] AND COLUMN MUST BE IN RANGE [4, 30]"
                                    mess_counter = 30
                                else:
                                    self.row, self.col = int(row), int(col)
                                    self.reset_grid()
                                    return 'size choosen'
                            else:
                                col += event.unicode
                            
                pygame.display.flip()
                pygame.time.delay(15)
                continue
            
            # draw button
            draw_img_center(screen, button_pressed if button_[0].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 - WIDTH // 6, HEIGHT // 2.3)
            draw_img_center(screen, button_pressed if button_[1].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 + WIDTH // 6, HEIGHT // 2.3)
            draw_img_center(screen, button_pressed if button_[2].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 - WIDTH // 6, HEIGHT // 2.3 + HEIGHT // 6)
            draw_img_center(screen, button_pressed if button_[3].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 + WIDTH // 6, HEIGHT // 2.3 + HEIGHT // 6) 
            draw_img_center(screen, button_pressed if button_[4].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 - WIDTH // 6, HEIGHT // 2.3 + HEIGHT // 6 * 2)
            draw_img_center(screen, button_pressed if button_[5].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2 + WIDTH // 6, HEIGHT // 2.3 + HEIGHT // 6 * 2) 
            draw_img_center(screen, med_button_pressed if exit1_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2.7)
            # draw text
            for i in range(6):
                if idx[i] != -1:
                    idx[i] += 1
                if button_[i].collidepoint(*pygame.mouse.get_pos()):
                    if idx[i] == -1:
                        idx[i] = 0
                        button_selected_sound.play()
                else:
                    idx[i] = -1
            if exit1_idx != -1:
                exit1_idx += 1
            if exit1_button.collidepoint(*pygame.mouse.get_pos()):
                if exit1_idx == -1:
                    exit1_idx = 0
                    button_selected_sound.play()
            else:
                exit1_idx = -1
            draw_text(screen, font_reg, text[0], GRAY, WIDTH // 2 - WIDTH // 6 - font_reg.size(text[0])[0] // 2, HEIGHT // 2.3 - font_reg.size(text[0])[1] // 2, idx[0])
            draw_text(screen, font_reg, text[1], GRAY, WIDTH // 2 + WIDTH // 6 - font_reg.size(text[1])[0] // 2, HEIGHT // 2.3 - font_reg.size(text[1])[1] // 2, idx[1])
            draw_text(screen, font_reg, text[2], GRAY, WIDTH // 2 - WIDTH // 6 - font_reg.size(text[2])[0] // 2, HEIGHT // 2.3 + HEIGHT // 6 - font_reg.size(text[2])[1] // 2, idx[2])
            draw_text(screen, font_reg, text[3], GRAY, WIDTH // 2 + WIDTH // 6 - font_reg.size(text[3])[0] // 2, HEIGHT // 2.3 + HEIGHT // 6 - font_reg.size(text[3])[1] // 2, idx[3]) 
            draw_text(screen, font_reg, text[4], GRAY, WIDTH // 2 - WIDTH // 6 - font_reg.size(text[4])[0] // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2 - font_reg.size(text[4])[1] // 2, idx[4])
            draw_text(screen, font_reg, text[5], GRAY, WIDTH // 2 + WIDTH // 6 - font_reg.size(text[5])[0] // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2 - font_reg.size(text[5])[1] // 2, idx[5]) 
            draw_text(screen, font_reg, "Exit", GRAY, WIDTH // 2 - font_reg.size("Exit")[0] // 2, HEIGHT // 2.3 + HEIGHT // 6 * 2.7 - font_reg.size("Exit")[1] // 2, exit1_idx)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_[0].collidepoint(event.pos):
                        self.row, self.col = 4, 4
                        self.reset_grid()
                        return 'size choosen'
                    if button_[1].collidepoint(event.pos):
                        self.row, self.col = 6, 6
                        self.reset_grid()
                        return 'size choosen'
                    if button_[2].collidepoint(event.pos):
                        self.row, self.col = 8, 8
                        self.reset_grid()
                        return 'size choosen'
                    if button_[3].collidepoint(event.pos):
                        self.row, self.col = 10, 10
                        self.reset_grid()
                        return 'size choosen'
                    if button_[4].collidepoint(event.pos):
                        self.row, self.col = 12, 12
                        self.reset_grid()
                        return 'size choosen'
                    if button_[5].collidepoint(event.pos):
                        customizming = True
                    if exit1_button.collidepoint(event.pos):
                        return 'back'
                            
            pygame.display.flip()
            pygame.time.delay(15)
    
    def timer_color(self, ratio):
        red = int(255 * (1 - ratio))
        green = int(255 * ratio)
        return (red, green, 0) 
    
    def count(self):
        cnt = 0
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if self.grid[i][j] != -1:
                    cnt += 1
        return cnt
    
    def skill4(self):
        pairs = []
        cnt = [0] * (NO_IMAGE + 1)
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if cnt[self.grid[i][j]] == 0:
                    cnt[self.grid[i][j]] = 1
                else:
                    pairs.append(self.grid[i][j])
                    cnt[self.grid[i][j]] = 0
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                self.grid[i][j] = -1
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if len(pairs) > 0 and j % 2 == 1:
                    self.grid[i][j] = pairs.pop()
                    self.grid[i][j + 1] = self.grid[i][j]
                    
    def out_skill4(self, old, removed):
        print('out skill4 called')
        print(removed)
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if old[i][j] != -1:
                    if old[i][j] in removed:
                        removed.remove(old[i][j])
                        old[i][j] = -1
                self.grid[i][j] = old[i][j]
    
    def skill5(self, screen):
        for i in range(5):
            if self.is_winning() == True:
                return
            while self.find_move(screen) == -1:
                self.suffle()
            hint1, hint2 = self.find_move(screen)
            self.grid[hint1[0]][hint1[1]] = -1
            self.grid[hint2[0]][hint2[1]] = -1
    def game(self, screen, p_id = 0):
        global volume_on, sound_on, music_on, music_id
        pre_hint1, pre_hint2 = -1, -1
        pa_idx, exit_idx = -1, -1
        exit1_idx = -1
        last = None
        drawing = False
        draw_counter = 0
        lines = []
        mess = 'Suffling ...'
        mess_counter = 0
        setting = False   
        running = True
        pa_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.1 - button.get_height() // 2, button.get_width(), button.get_height())
        exit_button = pygame.Rect(WIDTH // 2 -  med_button.get_width() // 2, HEIGHT // 2.1 + HEIGHT // 8 - med_button.get_height() // 2, med_button.get_width(), med_button.get_height())
        stting_button = pygame.Rect(120 - setting_button.get_width() // 2, 120 - setting_button.get_height() // 2, setting_button.get_width(), setting_button.get_height())
        skll_button = pygame.Rect(WIDTH - 120 - setting_button.get_width() // 2, 120 - setting_button.get_height() // 2, setting_button.get_width(), setting_button.get_height())
        setting_center_x, setting_center_y = WIDTH // 2, HEIGHT // 2
        casting_skill2 = False
        casting_skill3 = 0
        casting_skill4 = 0
        grid_copy = self.grid.copy()
        removed_by_skill4 = []
        show_setting_menu = False
        floating_money = []
        dragging = False
        while running:
            # draw background
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_ratio = mouse_x / WIDTH
            y_ratio = mouse_y / HEIGHT
            bg_x = -int((bg_width - WIDTH) * x_ratio)
            bg_y = -int((bg_height - HEIGHT) * y_ratio)
            bg_x = max(min(bg_x, 0), WIDTH - bg_width)
            bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
            screen.blit(game_background, (bg_x, bg_y))
            
            if self.lose == True:
                draw_text_center(screen, font_logo, "YOU LOSE", GRAY, WIDTH // 2, HEIGHT // 4)
                
                # draw button
                draw_img_center(screen, button_pressed if pa_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.1)
                draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.1 + HEIGHT // 8)
                # draw text
                if pa_button.collidepoint(*pygame.mouse.get_pos()):
                    if pa_idx == -1:
                        pa_idx = 0
                        button_selected_sound.play()
                else:
                    pa_idx = -1
                draw_text(screen, font_reg, "PLAY AGAIN", GRAY, WIDTH // 2 - font_reg.size("PLAY AGAIN")[0] // 2, HEIGHT // 2.1 - font_reg.size("PLAY AGAIN")[1] // 2, pa_idx)
                if pa_idx != -1:
                    pa_idx += 1
                if exit_button.collidepoint(*pygame.mouse.get_pos()):
                    if exit_idx == -1:
                        exit_idx = 0
                        button_selected_sound.play()
                else:
                    exit_idx = -1
                draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.1 + HEIGHT // 8 - font_reg.size("EXIT")[1] // 2, exit_idx)
                if exit_idx != -1:
                    exit_idx += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pa_button.collidepoint(event.pos):
                            print('play again')
                            op = self.choose_size(screen)
                            pre_hint1, pre_hint2 = -1, -1
                            last = None
                            drawing = False
                            draw_counter = 0
                            lines = []
                            mess_counter = 0
                            self.lose = False
                            self.timer = self.row * self.col * 2
                            print('start: ', self.timer / (self.row * self.col * 2))
                            if op == 'quit':
                                return 'quit'
                        if exit_button.collidepoint(event.pos):
                            print('exit')
                            self.reset_grid()
                            return 'exit'
                
                pygame.display.flip()
                pygame.time.delay(15)
                continue
            
            if self.is_winning() == True:
                draw_text_center(screen, font_logo, "YOU WIN", GRAY, WIDTH // 2, HEIGHT // 4)
                
                # draw button
                draw_img_center(screen, button_pressed if pa_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.1)
                draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.1 + HEIGHT // 8)
                # draw text
                if pa_button.collidepoint(*pygame.mouse.get_pos()):
                    if pa_idx == -1:
                        pa_idx = 0
                        button_selected_sound.play()
                else:
                    pa_idx = -1
                draw_text(screen, font_reg, "PLAY AGAIN", GRAY, WIDTH // 2 - font_reg.size("PLAY AGAIN")[0] // 2, HEIGHT // 2.1 - font_reg.size("PLAY AGAIN")[1] // 2, pa_idx)
                if pa_idx != -1:
                    pa_idx += 1
                if exit_button.collidepoint(*pygame.mouse.get_pos()):
                    if exit_idx == -1:
                        exit_idx = 0
                        button_selected_sound.play()
                else:
                    exit_idx = -1
                draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.1 + HEIGHT // 8 - font_reg.size("EXIT")[1] // 2, exit_idx)
                if exit_idx != -1:
                    exit_idx += 1
                                    
                # draw_text_center(screen, font_reg, "PLAY AGAIN", GRAY, WIDTH // 2, HEIGHT // 2.1)
                # draw_text_center(screen, font_reg, "EXIT", GRAY, WIDTH // 2, HEIGHT // 2.1 + HEIGHT // 8)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pa_button.collidepoint(event.pos):
                            print('play again')
                            op = self.choose_size(screen)
                            pre_hint1, pre_hint2 = -1, -1
                            last = None
                            drawing = False
                            draw_counter = 0
                            lines = []
                            mess_counter = 0
                            if op == 'quit':
                                return 'quit'
                        if exit_button.collidepoint(event.pos):
                            print('exit')
                            self.reset_grid()
                            return 'exit'
                
                pygame.display.flip()
                pygame.time.delay(15)
                continue
            
            # draw_text_center(screen, font_logo, "PIKACHU GAME", GRAY, WIDTH // 2, HEIGHT // 4)
            
            if mess_counter > 0:
                draw_text_center(screen, font_big, mess, RED, WIDTH // 2, HEIGHT // 2)
                if mess == 'Suffling ...' and mess_counter % 10 == 0:
                    mess = 'Suffling ..'
                elif mess == 'Suffling ..' and mess_counter % 10 == 0:
                    mess = 'Suffling .'
                elif mess == 'Suffling .' and mess_counter % 10 == 0:
                    mess = 'Suffling ...'
                mess_counter -= 1
                pygame.display.flip()
                pygame.time.delay(15)
                continue
            
            # check impossible
            if self.find_move(screen) == -1:
                mess_counter = 20
                self.suffle()
                continue
            
            # draw image
            for i in range(self.row):
                for j in range(self.col):
                    if self.grid[i + 1][j + 1] != -1:
                        img_copy = pokemon_images[self.grid[i + 1][j + 1]].copy()
                        if last is not None and last == (i + 1, j + 1):
                            img_copy.set_alpha(150)
                        x, y = self.cods[i + 1][j + 1]
                        draw_img_center(screen, img_copy, x, y)

            # settings and skill
            draw_img_center(screen, setting_pressed_button if stting_button.collidepoint(pygame.mouse.get_pos()) else setting_button, 120, 120)
            if p_id != 0:
                if self.cd <= 0:
                    if skll_button.collidepoint(pygame.mouse.get_pos()) or casting_skill2 == True or casting_skill3 > 0 or casting_skill4 > 0:
                        draw_img_center(screen, skill_pressed_button, WIDTH - 120, 120)
                    else:
                        draw_img_center(screen, skill_button, WIDTH - 120, 120)
                    draw_img_center(screen, fire, WIDTH - 120, 120)
                else:
                    draw_img_center(screen, skill_button, WIDTH - 120, 120)
                    draw_img_center(screen, fire, WIDTH - 120, 120)
                    self.cd = round(self.cd, 2)
                    draw_text_center(screen, font_mini, str(self.cd), BLACK, WIDTH - 120, 120)
                    if show_setting_menu == False:
                        self.cd -= 1 / 60
            for i in range(len(floating_money)):
                x, y, money = floating_money[i]
                draw_text_center(screen, font_reg, f"+{money}", GRAY, x, y)
                floating_money[i] = (x, y - 1, money)
            for i in range(len(floating_money) - 1, -1, -1):
                y = floating_money[i][1]
                if y < HEIGHT - 300:
                    floating_money.pop(i)
            draw_text_center(screen, font_reg, f"${self.cash}", GRAY, WIDTH - 120, HEIGHT - 120)
            
            # process timer and skill
            if self.mode != 'no timer':
                pygame.draw.rect(screen, WHITE, (120 - 25, 200, 50, 600))
                ratio = self.timer / (self.row * self.col * 2)
                # print(self.timer, self.row, self.col)
                pygame.draw.rect(screen, self.timer_color(ratio) if casting_skill3 <= 0 else ICE_BLUE, (120 - 25, 200 + 600 * (1 - ratio), 50, 600 * ratio))
            if show_setting_menu == False:
                if self.mode == 'timer':
                    self.timer -= 1 / 60
                elif self.mode == 'devil':
                    self.timer -= 1 / 30
            if show_setting_menu == False:
                if casting_skill3 > 0:
                    if self.mode != 'devil':
                        casting_skill3 -= 1 / 60
                    else:
                        casting_skill3 -= 1 / 30
                    if casting_skill3 <= 0:
                        self.cd = 30
                if casting_skill4 > 0:
                    if self.mode != 'devil':
                        casting_skill4 -= 1 / 60
                    else:
                        casting_skill4 -= 1 / 30
                    if casting_skill4 <= 0:
                        self.cd = 30
                        self.out_skill4(grid_copy, removed_by_skill4)
            if self.timer < 0:
                self.lose = True
                continue
            
            hint1, hint2 = self.find_move(screen)
            
            if show_setting_menu == True:
                draw_img_center(screen, setting_background, setting_center_x, setting_center_y)
                volume_button = pygame.Rect(setting_center_x + 10 - 75, setting_center_y - 100 - 25, 150, 50)
                sound_button = pygame.Rect(setting_center_x + 10 - 75, setting_center_y - 25, 150, 50)
                music_button = pygame.Rect(setting_center_x + 10 - 75, setting_center_y + 100 - 25, 150, 50)
                exit1_button = pygame.Rect(setting_center_x - 75, setting_center_y + 200 - 25, 150, 50)
                # draw button
                draw_img_center(screen, on_button if volume_on else off_button, setting_center_x + 10, setting_center_y - 100)
                draw_img_center(screen, on_button if sound_on else off_button, setting_center_x + 10, setting_center_y)
                draw_img_center(screen, on_button if music_on else off_button, setting_center_x + 10, setting_center_y + 100)
                draw_img_center(screen, med_button_pressed if exit1_button.collidepoint(*pygame.mouse.get_pos()) else med_button, setting_center_x, setting_center_y + 200)
                
                # draw text
                draw_text_center(screen, font_logo, "SETTINGS", BLACK, setting_center_x, setting_center_y - 230)
                draw_text_center(screen, font_reg, "VOLUME :", BLACK, setting_center_x - 100, setting_center_y - 100)
                draw_text_center(screen, font_reg, "SOUND :", BLACK, setting_center_x - 100, setting_center_y)
                draw_text_center(screen, font_reg, "MUSIC :", BLACK, setting_center_x - 100, setting_center_y + 100)
                if exit1_idx != -1:
                    exit1_idx += 1
                if exit1_button.collidepoint(*pygame.mouse.get_pos()):
                    if exit1_idx == -1:
                        exit1_idx = 0
                        button_selected_sound.play()
                else:
                    exit1_idx = -1
                draw_text(screen, font_reg, "EXIT", BLACK, setting_center_x - font_reg.size("EXIT")[0] // 2, setting_center_y + 200 - font_reg.size("EXIT")[1] // 2, exit1_idx)
                draw_text_center(screen, font_reg, "ON" if volume_on else "OFF", BLACK, setting_center_x + 10, setting_center_y - 100)
                draw_text_center(screen, font_reg, "ON" if sound_on else "OFF", BLACK, setting_center_x + 10, setting_center_y)
                draw_text_center(screen, font_reg, "ON" if music_on else "OFF", BLACK, setting_center_x + 10, setting_center_y + 100)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if exit1_button.collidepoint(event.pos):
                            return 'back'
                        if stting_button.collidepoint(event.pos):
                            show_setting_menu = False
                        if volume_button.collidepoint(event.pos):
                            volume_on = not volume_on
                            if volume_on:
                                sound_on, music_on = True, True
                                pop_sound.set_volume(1)
                                button_selected_sound.set_volume(1)
                                background_music[music_id].play(-1)
                            else:
                                sound_on, music_on = False, False
                                pop_sound.set_volume(0)
                                button_selected_sound.set_volume(0)
                                background_music[music_id].stop()
                        if sound_button.collidepoint(event.pos):
                            sound_on = not sound_on
                            if sound_on:
                                volume_on = True
                                pop_sound.set_volume(1)
                                button_selected_sound.set_volume(1)
                            else:
                                pop_sound.set_volume(0)
                                button_selected_sound.set_volume(0)
                        if music_button.collidepoint(event.pos):
                            music_on = not music_on
                            if music_on:
                                volume_on = True
                                background_music[music_id].play(-1)
                            else:
                                background_music[music_id].stop()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            show_setting_menu = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return 'quit'
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for i in range(self.row):
                            for j in range(self.col):
                                if self.grid_button[i][j].collidepoint(event.pos):
                                    if last is None and self.grid[i + 1][j + 1] != -1:
                                        last = (i + 1, j + 1)
                                        print("1 :", last)
                                    elif last is not None:
                                        if last == (i + 1, j + 1):
                                            last = None
                                            break
                                        print("2 :", (i + 1, j + 1))
                                        if self.grid[i + 1][j + 1] == self.grid[last[0]][last[1]]:
                                            if casting_skill2 == True:
                                                self.grid[i + 1][j + 1], self.grid[last[0]][last[1]] = -1, -1
                                                pop_sound.play()
                                                last = None
                                                casting_skill2 = False
                                                self.cd = 30
                                                continue
                                            if self.is_valid(screen, (i + 1, j + 1), last, True) != False:
                                                lines = self.is_valid(screen, (i + 1, j + 1), last, True)
                                                if casting_skill4 > 0:
                                                    removed_by_skill4.append(self.grid[i + 1][j + 1])
                                                    removed_by_skill4.append(self.grid[last[0]][last[1]])
                                                self.grid[i + 1][j + 1], self.grid[last[0]][last[1]] = -1, -1
                                                self.timer += 1
                                                self.timer = min(self.timer, self.row * self.col * 2)
                                                if self.mode == 'no timer':
                                                    self.cash += 2
                                                    floating_money.append([WIDTH - 120, HEIGHT - 150, 2])
                                                elif self.mode == 'timer':
                                                    self.cash += 4
                                                    floating_money.append([WIDTH - 120, HEIGHT - 150, 4])
                                                else:
                                                    self.cash += 6
                                                    floating_money.append([WIDTH - 120, HEIGHT - 150, 6])
                                                pop_sound.play()
                                                drawing, draw_counter = True, 20
                                        last = None
                        if stting_button.collidepoint(event.pos):
                            show_setting_menu = True
                        if skll_button.collidepoint(event.pos) and p_id != 0 and self.cd <= 0:
                            if p_id == 1:
                                lines = self.is_valid(screen, hint1, hint2, True)
                                drawing, draw_counter = True, 1000
                                self.cd = 15
                            elif p_id == 2:
                                casting_skill2 = True
                            elif p_id == 3:
                                if self.timer == -100:
                                    self.cd = 30
                                else:
                                    casting_skill3 = 5
                            elif p_id == 4:
                                casting_skill4 = 4
                                grid_copy = [[-1] * (self.col + 3) for _ in range(self.row + 3)]
                                for i in range(1, self.row + 1):
                                    for j in range(1, self.col + 1):
                                        grid_copy[i][j] = self.grid[i][j]
                                removed_by_skill4 = []
                                self.skill4()
                            elif p_id == 5:
                                self.skill5(screen)
                                self.cd = 40
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            show_setting_menu = True
            
                if drawing == True:
                    for l in lines:
                        pygame.draw.line(screen, RED, self.cods[l[0][0]][l[0][1]], self.cods[l[1][0]][l[1][1]], 4)
                    draw_counter -= 1
                    if draw_counter < 0:
                        lines, draw, draw_counter = [], False, 0
                        
            pygame.display.flip()
            pygame.time.delay(15)
        return 'quit'
    
    def change_mode(self, screen):
        # No Timer, Timer, Devil
        
        button_ = [
            pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.7 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.7 + HEIGHT // 6 - button.get_height() // 2, button.get_width(), button.get_height()),
            pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.7 + HEIGHT // 6 * 2 - button.get_height() // 2, button.get_width(), button.get_height())
        ]
        exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.7 + HEIGHT // 6 * 3 - med_button.get_height() // 2, med_button.get_width(), med_button.get_height())
        
        idx = [-1] * 4
        text = [
            "NO TIMER",
            "TIMER",
            "DEVIL",
            "EXIT"
        ]
        
        running = True
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_ratio = mouse_x / WIDTH
            y_ratio = mouse_y / HEIGHT
            bg_x = -int((bg_width - WIDTH) * x_ratio)
            bg_y = -int((bg_height - HEIGHT) * y_ratio)
            bg_x = max(min(bg_x, 0), WIDTH - bg_width)
            bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
            screen.blit(game_background, (bg_x, bg_y))
            draw_text_center(screen, font_logo, "CHOOSE MODE", GRAY, WIDTH // 2, HEIGHT // 4)
            
            # draw img
            draw_img_center(screen, button_pressed if button_[0].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.7)
            draw_img_center(screen, button_pressed if button_[1].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.7 + HEIGHT // 6)
            draw_img_center(screen, button_pressed if button_[2].collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.7 + HEIGHT // 6 * 2)
            draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.7 + HEIGHT // 6 * 3)
            # draw text
            for i in range(4):
                if idx[i] != -1:
                    idx[i] += 1
                if i != 3:
                    if button_[i].collidepoint(*pygame.mouse.get_pos()):
                        if idx[i] == -1:
                            idx[i] = 0
                            button_selected_sound.play()
                    else:
                        idx[i] = -1
                else:
                    if exit_button.collidepoint(*pygame.mouse.get_pos()):
                        if idx[i] == -1:
                            idx[i] = 0
                            button_selected_sound.play()
                    else:
                        idx[i] = -1
                draw_text(screen, font_reg, text[i], GRAY, WIDTH // 2 - font_reg.size(text[i])[0] // 2, HEIGHT // 2.7 + HEIGHT // 6 * i - font_reg.size(text[i])[1] // 2, idx[i])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_[0].collidepoint(event.pos):
                        self.mode = 'no timer'
                        return 'no timer'
                    if button_[1].collidepoint(event.pos):
                        self.mode = 'timer'
                        self.timer = self.row * self.col * 2
                        print(self.timer, self.row, self.col)
                        return 'timer'
                    if button_[2].collidepoint(event.pos):
                        self.mode = 'devil'
                        self.timer = self.row * self.col * 2
                        return 'devil'
                    if exit_button.collidepoint(event.pos):
                        return 'back'
            
            pygame.display.flip()
            pygame.time.delay(15)
    
    def shop_func(self, screen):
        running = True
        
        button_ = [
            pygame.Rect(WIDTH // 6 - 300 // 2, HEIGHT // 2.7 - 300 // 2, 300, 300),
            pygame.Rect(WIDTH // 2.1 + WIDTH // 6 - 300 // 2, HEIGHT // 2.7 - 300 // 2, 300, 300),
            pygame.Rect(WIDTH // 6 - 300 // 2, HEIGHT // 2.7 + HEIGHT // 5 - 300 // 2, 300, 300),
            pygame.Rect(WIDTH // 2.1 + WIDTH // 6 - 300 // 2, HEIGHT // 2.7 + HEIGHT // 5 - 300 // 2, 300, 300),
            pygame.Rect(WIDTH // 6 - 300 // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2 - 300 // 2, 300, 300),
            pygame.Rect(WIDTH // 2.1 + WIDTH // 6 - 300 // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2 - 300 // 2, 300, 300)
        ]
        exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2.5 - med_button.get_height() // 2, med_button.get_width(), med_button.get_height())
        exit_idx = -1
        center = [
            (WIDTH // 6, HEIGHT // 2.7),
            (WIDTH // 2.1 + WIDTH // 6, HEIGHT // 2.7),
            (WIDTH // 6, HEIGHT // 2.7 + HEIGHT // 5),
            (WIDTH // 2.1 + WIDTH // 6, HEIGHT // 2.7 + HEIGHT // 5),
            (WIDTH // 6, HEIGHT // 2.7 + HEIGHT // 5 * 2),
            (WIDTH // 2.1 + WIDTH // 6, HEIGHT // 2.7 + HEIGHT // 5 * 2)
        ]
        prices = [0, 100, 200, 500, 3000, 3000]
        checking = -1
        mess = "NOT ENOUGH MONEY"
        mess_counter = 0
        while running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x_ratio = mouse_x / WIDTH
            y_ratio = mouse_y / HEIGHT
            bg_x = -int((bg_width - WIDTH) * x_ratio)
            bg_y = -int((bg_height - HEIGHT) * y_ratio)
            bg_x = max(min(bg_x, 0), WIDTH - bg_width)
            bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
            screen.blit(game_background, (bg_x, bg_y))
            draw_text_center(screen, font_logo, "POKEMON SHOP", GRAY, WIDTH // 2, HEIGHT // 5)
            
            # draw img
            draw_text(screen, font_big, f"${self.cash}", GRAY, 100, 100)
            for i in range(6):
                img_copy = character_images[i].copy()
                # img_copy = pygame.transform.scale(img_copy, (200, 200))
                draw_img_center(screen, pokemon_background, center[i][0], center[i][1])     
                draw_img_center(screen, img_copy, center[i][0], center[i][1])
                if i not in self.inventory:
                    img_copy = pokemon_ball.copy()
                    if checking == i:
                        img_copy.set_alpha(240)
                    draw_img_center(screen, img_copy, center[i][0], center[i][1])
                    draw_text(screen, font_reg, f"${prices[i]}", GRAY, center[i][0] + 100, center[i][1] - 10)
            draw_img_center(screen, med_button_pressed if exit_button.collidepoint(pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2.5)
            if exit_button.collidepoint(*pygame.mouse.get_pos()):
                if exit_idx == -1:
                    exit_idx = 0
                    button_selected_sound.play()
            else:
                exit_idx = -1
            draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2.5 - font_reg.size("EXIT")[1] // 2, exit_idx)
            if exit_idx != -1:
                exit_idx += 1
            if mess_counter > 0:
                draw_text_center(screen, font_reg, mess, RED, WIDTH // 2, HEIGHT // 2.7 + HEIGHT // 5 * 2.7)
                mess_counter -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(6):
                        if button_[i].collidepoint(event.pos) and i not in self.inventory:
                            if checking != i:
                                checking = i
                                mess = 'Click again to buy'
                                mess_counter = 30
                            else:
                                if self.cash >= prices[i]:
                                    self.inventory.append(i)
                                    self.cash -= prices[i]
                                else:
                                    mess, mess_counter = 'Not enough money', 30
                                    checking = -1
                    if exit_button.collidepoint(event.pos):
                        return 'back'
            pygame.display.flip()
            pygame.time.delay(15)
    
    def show(self):
        for row in self.grid:
            for e in row:
                print(e, end = ' ')
            print()
                    
                    
if __name__ == "__main__":
    print(NO_IMAGE)
                    
        
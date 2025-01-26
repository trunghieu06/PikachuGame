from player import *

volume = [True, True, True, 2]
background_music[volume[3]].play(-1)

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

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pikachu Game")
clock = pygame.time.Clock()
players = []

def load_data():
    if os.path.getsize("players.json") == 0:
        print("File JSON is empty")
        return
    players_data = dict()
    with open("players.json", "r") as f:
        players_data = json.load(f)
    for username in players_data.keys():
        cur_player = Player(username, players_data[username]["password"],\
            players_data[username]["cash"],\
            players_data[username]["inventory"],\
            players_data[username]["row"],\
            players_data[username]["col"],\
            players_data[username]["timer"],\
            players_data[username]["mode"],\
            players_data[username]["cd"],\
            players_data[username]["lose"],\
            players_data[username]["grid"])
        players.append(cur_player)

def save_data():
    print('save_data called')
    players_data = dict()
    for player in players:
        players_data[player.username] = {
            "password": player.password,
            "cash": player.cash,
            "inventory": player.inventory,
            "row": player.row,
            "col": player.col,
            "timer": player.timer,
            "mode": player.mode,
            "cd": player.cd,
            "lose": player.lose,
            "grid": player.grid
        }
    with open("players.json", "w") as f:
        json.dump(players_data, f, indent = 4)

def check_login(username, password):
    for i in range(len(players)):
        if players[i].username == username and players[i].password == password:
            return i
    return -1

player_index = -1

def login_func():
    global player_index
    login_idx, exit_idx = -1, -1
    running = True
    username, password, status = '', '', 'username'
    mess, mess_counter = '', 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(*event.pos):
                    print("Login")
                    check_log = check_login(username, password)
                    if check_log != -1:
                        print("Login successfully")
                        player_index = check_log
                        return check_log
                    else:
                        print("Login failed")
                        mess, mess_counter = 'Username or password is incorrect', 30
                if username_box.collidepoint(*event.pos):
                    status = 'username'
                if password_box.collidepoint(*event.pos):
                    status = 'password'
                if exit_button.collidepoint(*event.pos):    
                    return -1
            if event.type == pygame.KEYDOWN:    
                if status == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        status = 'password'
                    else:
                        username += event.unicode
                elif status == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("Login")
                        check_log = check_login(username, password)
                        if check_log != -1:
                            print("Login successfully")
                            player_index = check_log
                            return check_log
                        else:
                            print("Login failed")
                            mess, mess_counter = 'Username or password is incorrect', 30
                    else:
                        password += event.unicode
                               
        # draw
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_ratio = mouse_x / WIDTH
        y_ratio = mouse_y / HEIGHT
        bg_x = -int((bg_width - WIDTH) * x_ratio)
        bg_y = -int((bg_height - HEIGHT) * y_ratio)
        bg_x = max(min(bg_x, 0), WIDTH - bg_width)
        bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
        screen.blit(background, (bg_x, bg_y))
        draw_text_center(screen, font_logo, "PIKACHU GAME", GRAY, WIDTH // 2, HEIGHT // 4)
        
        # draw button : username typing box, password typing box, login button
        username_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.3 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
        password_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
        login_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2 - button.get_height() // 2, button.get_width(), button.get_height())        
        exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3 - med_button.get_height() // 2, 150, 50)
        draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.3)
        draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8)
        draw_img_center(screen, button_pressed if login_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2)
        draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3)
        # draw text username and password
        if username_box.collidepoint(*pygame.mouse.get_pos()) == False and username == '':
            draw_text_center(screen, font_reg, "USERNAME", GRAY, WIDTH // 2, HEIGHT // 2.3)
        else:
            draw_text(screen, font_reg, username, GRAY, WIDTH // 2 - font_reg.size(username)[0] // 2, HEIGHT // 2.3 - font_reg.size(username)[1] // 2)
        if password_box.collidepoint(*pygame.mouse.get_pos()) == False and password == '':
            draw_text_center(screen, font_reg, "PASSWORD", GRAY, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8)
        else:
            draw_text(screen, font_reg, password, GRAY, WIDTH // 2 - font_reg.size(password)[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 - font_reg.size(password)[1] // 2)
        if status == 'username' and username != '' and pygame.time.get_ticks() % 1000 < 500:
            draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(username)[0] // 2 + 5, HEIGHT // 2.3)
        if status == 'password' and password != '' and pygame.time.get_ticks() % 1000 < 500:
            draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(password)[0] // 2 + 5, HEIGHT // 2.3 + HEIGHT // 8)
        # draw text login, exit and mess
        if login_button.collidepoint(*pygame.mouse.get_pos()):
            if login_idx == -1:
                login_idx = 0
                button_selected_sound.play()
        else:
            login_idx = -1
        draw_text(screen, font_reg, "LOG IN", GRAY, WIDTH // 2 - font_reg.size("LOG IN")[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2 - font_reg.size("LOG IN")[1] // 2, login_idx)
        if login_idx != -1:
            login_idx += 1
        if exit_button.collidepoint(*pygame.mouse.get_pos()):
            if exit_idx == -1:
                exit_idx = 0
                button_selected_sound.play()
        else:
            exit_idx = -1
        draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.3 + HEIGHT // 8 * 3 - font_reg.size("EXIT")[1] // 2, exit_idx)
        if exit_idx != -1:
            exit_idx += 1
        if mess_counter > 0:
            draw_text_center(screen, font_reg, mess, RED, WIDTH // 2, HEIGHT // 2.3 + HEIGHT // 8 * 2.5)
            mess_counter -= 1
        pygame.display.flip()
        pygame.time.delay(15)
    save_data()
    pygame.quit()
    sys.exit()
    return -1
    
def register_func():
    global player_index
    register_idx, exit_idx = -1, -1
    running = True
    username, password, repassword, status = '', '', '', 'username'
    mess, mess_counter = '', 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if register_button.collidepoint(*event.pos):
                    print("register")
                    if password != repassword:
                        mess, mess_counter = 'Password and re-password do not match', 30
                        continue
                    if username == '' or password == '':
                        mess, mess_counter = 'Username or password is empty', 30
                        continue
                    username_existing = False
                    for player in players:
                        if player.username == username:
                            username_existing = True
                            break
                    if username_existing == True:
                        mess, mess_counter = 'Username already exists', 30
                        continue
                    players.append(Player(username, password))
                    save_data()
                    player_index = len(players) - 1
                    return len(players) - 1
                if username_box.collidepoint(*event.pos):
                    status = 'username'
                if password_box.collidepoint(*event.pos):
                    status = 'password'
                if repassword_box.collidepoint(*event.pos):
                    status = 'repassword'
                if exit_button.collidepoint(*event.pos):
                    return -1
            if event.type == pygame.KEYDOWN:
                if status == 'username':
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        status = 'password'
                    else:
                        username += event.unicode
                elif status == 'password':
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        status = 'repassword'
                    else:
                        password += event.unicode
                elif status == 'repassword':
                    if event.key == pygame.K_BACKSPACE:
                        repassword = repassword[:-1]
                    elif event.key == pygame.K_RETURN:
                        print("register")
                        if password != repassword:
                            mess, mess_counter = 'Password and re-password do not match', 30
                            continue
                        if username == '' or password == '':
                            mess, mess_counter = 'Username or password is empty', 30
                            continue
                        username_existing = False
                        for player in players:
                            if player.username == username:
                                username_existing = True
                                break
                        if username_existing == True:
                            mess, mess_counter = 'Username already exists', 30
                            continue
                        players.append(Player(username, password))
                        save_data()
                        player_index = len(players) - 1
                        return len(players) - 1
                    else:
                        repassword += event.unicode                               
        # draw
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_ratio = mouse_x / WIDTH
        y_ratio = mouse_y / HEIGHT
        bg_x = -int((bg_width - WIDTH) * x_ratio)
        bg_y = -int((bg_height - HEIGHT) * y_ratio)
        bg_x = max(min(bg_x, 0), WIDTH - bg_width)
        bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
        screen.blit(background, (bg_x, bg_y))
        draw_text_center(screen, font_logo, "PIKACHU GAME", GRAY, WIDTH // 2, HEIGHT // 4)
        
        # draw button : username typing box, password typing box, login button
        username_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.5 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
        password_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
        repassword_box = pygame.Rect(WIDTH // 2 - typing_box.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2 - typing_box.get_height() // 2, typing_box.get_width(), typing_box.get_height())
        register_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3 - button.get_height() // 2, button.get_width(), button.get_height())        
        exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4 - med_button.get_height() // 2, 150, 50)
        draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.5)
        draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8)
        draw_img_center(screen, typing_box, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2)
        draw_img_center(screen, button_pressed if register_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3)
        draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4)
        # draw text username and password
        if username_box.collidepoint(*pygame.mouse.get_pos()) == False and username == '':
            draw_text_center(screen, font_reg, "USERNAME", GRAY, WIDTH // 2, HEIGHT // 2.5)
        else:
            draw_text(screen, font_reg, username, GRAY, WIDTH // 2 - font_reg.size(username)[0] // 2, HEIGHT // 2.5 - font_reg.size(username)[1] // 2)
        if password_box.collidepoint(*pygame.mouse.get_pos()) == False and password == '':
            draw_text_center(screen, font_reg, "PASSWORD", GRAY, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8)
        else:
            draw_text(screen, font_reg, password, GRAY, WIDTH // 2 - font_reg.size(password)[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 - font_reg.size(password)[1] // 2)
        if repassword_box.collidepoint(*pygame.mouse.get_pos()) == False and repassword == '':
            draw_text_center(screen, font_reg, "RE-PASSWORD", GRAY, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2)
        else:
            draw_text(screen, font_reg, repassword, GRAY, WIDTH // 2 - font_reg.size(repassword)[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2 - font_reg.size(repassword)[1] // 2)
        if status == 'username' and username != '' and pygame.time.get_ticks() % 1000 < 500:
            draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(username)[0] // 2 + 5, HEIGHT // 2.5)
        if status == 'password' and password != '' and pygame.time.get_ticks() % 1000 < 500:
            draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(password)[0] // 2 + 5, HEIGHT // 2.5 + HEIGHT // 8)
        if status == 'repassword' and repassword != '' and pygame.time.get_ticks() % 1000 < 500:
            draw_text_center(screen, font_reg, '|', GRAY, WIDTH // 2 + font_reg.size(repassword)[0] // 2 + 5, HEIGHT // 2.5 + HEIGHT // 8 * 2)
        # draw text login, exit and mess
        if register_button.collidepoint(*pygame.mouse.get_pos()):
            if register_idx == -1:
                register_idx = 0
                button_selected_sound.play()
        else:
            register_idx = -1
        draw_text(screen, font_reg, "REGISTER", GRAY, WIDTH // 2 - font_reg.size("REGISTER")[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3 - font_reg.size("REGISTER")[1] // 2, register_idx)
        if register_idx != -1:
            register_idx += 1
        if exit_button.collidepoint(*pygame.mouse.get_pos()):
            if exit_idx == -1:
                exit_idx = 0
                button_selected_sound.play()
        else:
            exit_idx = -1
        draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4 - font_reg.size("EXIT")[1] // 2, exit_idx)
        if exit_idx != -1:
            exit_idx += 1
        if mess_counter > 0:
            draw_text_center(screen, font_reg, mess, RED, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3.5)
            mess_counter -= 1
        pygame.display.flip()
        pygame.time.delay(15)
    save_data()
    pygame.quit()
    sys.exit()
    
def settings_func():
    # sound, msic, exit
    volume_idx, sound_idx, volume_idx, change_idx, exit_idx = -1, -1, -1, -1, -1
        
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_button.collidepoint(event.pos):
                    volume[0] = not volume[0]
                    if volume[0]:
                        volume[1] = True
                        volume[2] = True
                        pop_sound.set_volume(1)
                        electric_sound.set_volume(1)
                        winning_sound.set_volume(1)
                        button_selected_sound.set_volume(1)
                        background_music[volume[3]].play(-1)
                    else:
                        volume[1] = False
                        volume[2] = False
                        pop_sound.set_volume(0)
                        electric_sound.set_volume(0)
                        winning_sound.set_volume(0)
                        button_selected_sound.set_volume(0)
                        background_music[volume[3]].stop()
                    print(volume[0], volume[1], volume[2])
                if sound_button.collidepoint(event.pos):
                    volume[1] = not volume[1]
                    if volume[1]:
                        volume[0] = True
                        pop_sound.set_volume(1)
                        electric_sound.set_volume(1)
                        winning_sound.set_volume(1)
                        button_selected_sound.set_volume(1)
                    else:
                        pop_sound.set_volume(0)
                        electric_sound.set_volume(0)
                        winning_sound.set_volume(0)
                        button_selected_sound.set_volume(0)
                if music_button.collidepoint(event.pos):
                    volume[2] = not volume[2]
                    if volume[2]:
                        volume[0] = True
                        background_music[volume[3]].play(-1)
                    else:
                        background_music[volume[3]].stop()
                if change_button.collidepoint(event.pos):
                    background_music[volume[3]].stop()
                    volume[3] = (volume[3] + 1) % len(background_music)
                    if volume[2]:
                        background_music[volume[3]].play(-1)
                if exit_button.collidepoint(event.pos):
                    return
        # draw
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_ratio = mouse_x / WIDTH
        y_ratio = mouse_y / HEIGHT
        bg_x = -int((bg_width - WIDTH) * x_ratio)
        bg_y = -int((bg_height - HEIGHT) * y_ratio)
        bg_x = max(min(bg_x, 0), WIDTH - bg_width)
        bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
        screen.blit(background, (bg_x, bg_y))
        draw_text_center(screen, font_logo, "SETTINGS", GRAY, WIDTH // 2, HEIGHT // 4)
        
        # draw buttons
        volume_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.5 - button.get_height() // 2, button.get_width(), button.get_height())
        sound_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 - button.get_height() // 2, button.get_width(), button.get_height())
        music_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2 - button.get_height() // 2, button.get_width(), button.get_height())
        change_button = pygame.Rect(WIDTH // 2 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3 - button.get_height() // 2, button.get_width(), button.get_height())
        exit_button = pygame.Rect(WIDTH // 2 - med_button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4 - med_button.get_height() // 2, 150, 50)
        draw_img_center(screen, button_pressed if volume_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.5)
        draw_img_center(screen, button_pressed if sound_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8)
        draw_img_center(screen, button_pressed if music_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2)
        draw_img_center(screen, button_pressed if change_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3)
        draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4)
        
        # draw text
        if volume_button.collidepoint(*pygame.mouse.get_pos()):
            if volume_idx == -1:
                volume_idx = 0
                button_selected_sound.play()
        else:
            volume_idx = -1
        volume_text = "VOLUME : ON" if volume[0] else "VOLUME : OFF"
        draw_text(screen, font_reg, volume_text, GRAY, WIDTH // 2 - font_reg.size(volume_text)[0] // 2, HEIGHT // 2.5 - font_reg.size(volume_text)[1] // 2, volume_idx)
        if volume_idx != -1:
            volume_idx += 1
        if sound_button.collidepoint(*pygame.mouse.get_pos()):
            if sound_idx == -1:
                sound_idx = 0
                button_selected_sound.play()
        else:
            sound_idx = -1
        sound_text = "SOUND : ON" if volume[1] else "SOUND : OFF"
        draw_text(screen, font_reg, sound_text, GRAY, WIDTH // 2 - font_reg.size(sound_text)[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 - font_reg.size(sound_text)[1] // 2, sound_idx)
        if sound_idx != -1:
            sound_idx += 1
        if music_button.collidepoint(*pygame.mouse.get_pos()):
            if music_idx == -1:
                music_idx = 0
                button_selected_sound.play()
        else:
            music_idx = -1
        music_text = "MUSIC : ON" if volume[2] else "MUSIC : OFF"
        draw_text(screen, font_reg, music_text, GRAY, WIDTH // 2 - font_reg.size(music_text)[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2 - font_reg.size(music_text)[1] // 2, music_idx)
        if music_idx != -1:
            music_idx += 1
        if change_button.collidepoint(*pygame.mouse.get_pos()):
            if change_idx == -1:
                change_idx = 0
                button_selected_sound.play()
        else:
            change_idx = -1
        music_name = "MUSIC : " + background_music_names[volume[3]]
        draw_text(screen, font_reg, music_name, GRAY, WIDTH // 2 - font_reg.size(music_name)[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3 - font_reg.size(music_name)[1] // 2, change_idx)
        if change_idx != -1:
            change_idx += 1
        if exit_button.collidepoint(*pygame.mouse.get_pos()):
            if exit_idx == -1:
                exit_idx = 0
                button_selected_sound.play()
        else:
            exit_idx = -1
        draw_text(screen, font_reg, "EXIT", GRAY, WIDTH // 2 - font_reg.size("EXIT")[0] // 2, HEIGHT // 2.5 + HEIGHT // 8 * 4 - font_reg.size("EXIT")[1] // 2, exit_idx)
        if exit_idx != -1:
            exit_idx += 1        
        pygame.display.flip()
        pygame.time.delay(15)
    save_data()
    pygame.quit()
    sys.exit()
    
def home_screen():
    global player_index
    # 4 button: login, register, guest, settings
    login_idx, register_idx, guest_idx, settings_idx = -1, -1, -1, -1
    running = True
    while running:
        cont = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if login_button.collidepoint(*event.pos):
                    print("Login")
                    login_func()
                    cont = True
                if register_button.collidepoint(*event.pos):
                    print("Register")
                    register_func()
                    cont = True
                if guest_button.collidepoint(*event.pos):
                    print("Guest")
                    # guest_func()
                    player_index = -2
                    cont = True
                if settings_button.collidepoint(*event.pos):
                    print("Settings")
                    settings_func()
                    cont = True
        if player_index != -1:
            return
        if cont == True:
            continue
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_ratio = mouse_x / WIDTH
        y_ratio = mouse_y / HEIGHT
        bg_x = -int((bg_width - WIDTH) * x_ratio)
        bg_y = -int((bg_height - HEIGHT) * y_ratio)
        bg_x = max(min(bg_x, 0), WIDTH - bg_width)
        bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
        screen.blit(background, (bg_x, bg_y))
        draw_text_center(screen, font_logo, "PIKACHU GAME", GRAY, WIDTH // 2, HEIGHT // 4)
        # draw button
        login_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 - button.get_height() // 2, button.get_width(), button.get_height())
        register_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 - button.get_height() // 2, button.get_width(), button.get_height())
        guest_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 2 - button.get_height() // 2, button.get_width(), button.get_height())
        settings_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 8 * 3 - button.get_height() // 2, button.get_width(), button.get_height())
        draw_img_center(screen, button_pressed if login_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5)
        draw_img_center(screen, button_pressed if register_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 8)
        draw_img_center(screen, button_pressed if guest_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 8 * 2)
        draw_img_center(screen, button_pressed if settings_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 8 * 3)
        
        # draw text
        if login_button.collidepoint(*pygame.mouse.get_pos()):
            if login_idx == -1:
                login_idx = 0
                button_selected_sound.play()
        else:
            login_idx = -1
        if register_button.collidepoint(*pygame.mouse.get_pos()):
            if register_idx == -1:
                register_idx = 0
                button_selected_sound.play()
        else:
            register_idx = -1
        if guest_button.collidepoint(*pygame.mouse.get_pos()):
            if guest_idx == -1:
                guest_idx = 0
                button_selected_sound.play()
        else:
            guest_idx = -1
        if settings_button.collidepoint(*pygame.mouse.get_pos()):
            if settings_idx == -1:
                settings_idx = 0
                button_selected_sound.play()
        else:
            settings_idx = -1
        draw_text(screen, font_reg, "LOG IN", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2, login_idx)
        if login_idx != -1:
            login_idx += 1
            # if login_idx >= len("LOG IN"):
            #     login_idx = 0
        draw_text(screen, font_reg, "REGISTER", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 8, register_idx)
        if register_idx != -1:
            register_idx += 1
            # if register_idx >= len("REGISTER"):
            #     register_idx = 0
        draw_text(screen, font_reg, "PLAY AS GUEST", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 8 * 2, guest_idx)
        if guest_idx != -1:
            guest_idx += 1
            # if guest_idx >= len("PLAY AS GUEST"):
            #     guest_idx = 0
        draw_text(screen, font_reg, "SETTINGS", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 8 * 3, settings_idx)
        if settings_idx != -1:
            settings_idx += 1
            # if settings_idx >= len("SETTINGS"):
            #     settings_idx = 0    
        pygame.display.flip()
        pygame.time.delay(15)
        # clock.tick(60)
    save_data()
    pygame.quit()
    sys.exit()
    
guest = Player('guest', 'guest')
    
def player_screen():
    global player_index
    player = None
    if player_index == -2:
        player = guest
        player.reset_grid()
    else:
        player = players[player_index]
    # continue, new game, change mode, pokemon, setting, exit
    continue_idx, newgame_idx, changemode_idx, pokemon_idx, setting_idx, exit_idx = -1, -1, -1, -1, -1, -1
    CENTER_X, CENTER_Y = WIDTH // 4 * 3, HEIGHT // 2.7 + 20 + 250
    RADIUS = 150
    angle_offset = 0
    mouse_speed = 0.005
    drag = False
    prev_mouse_x, prev_mouse_y = CENTER_X, CENTER_Y
    character_box = pygame.Rect(CENTER_X - 200, CENTER_Y - 200, 400, 400)
    ball = pygame.transform.scale(pokemon_ball, (120, 120))
    mess, mess_counter = '', 0
    status = 'home'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                drag = False
            if character_box.collidepoint(*pygame.mouse.get_pos()):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    drag = True
                    prev_mouse_x, prev_mouse_y = event.pos
                if event.type == pygame.MOUSEMOTION and drag == True:
                    if event.pos[0] > CENTER_X:
                        if event.pos[1] > CENTER_Y:
                            angle_offset -= mouse_speed * ( - prev_mouse_x + event.pos[0] + prev_mouse_y - event.pos[1]) % (math.pi * 2)
                        else:
                            angle_offset -= mouse_speed * (prev_mouse_x - event.pos[0] - event.pos[1] + prev_mouse_y) % (math.pi * 2)
                    else:
                        if event.pos[1] > CENTER_Y:
                            angle_offset -= mouse_speed * ( - prev_mouse_x + event.pos[0] - prev_mouse_y + event.pos[1]) % (math.pi * 2)
                        else:
                            angle_offset -= mouse_speed * (prev_mouse_x - event.pos[0] + event.pos[1] - prev_mouse_y) % (math.pi * 2)
                    prev_mouse_x, prev_mouse_y = event.pos
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(*event.pos):
                        print("Continue")
                        if min_id not in player.inventory:
                            mess, mess_counter = 'Choose another pokemon', 30
                            continue
                        op = player.game(screen, min_id, volume)
                        if op == 'quit':
                            running = False
                    if newgame_button.collidepoint(*event.pos):
                        print("New game")
                        if min_id not in player.inventory:
                            mess, mess_counter = 'Choose another pokemon', 30
                            continue
                        op = player.choose_size(screen)
                        if op == 'quit':
                            running = False
                        elif op == 'back':
                            continue
                        else:
                            op = player.game(screen, min_id, volume)
                            if op == 'quit':
                                running = False
                    if changemode_button.collidepoint(*event.pos):
                        print("Change mode")
                        op = player.change_mode(screen)
                        print('playerscreen: ', player.timer)
                        # print(player.mode)
                        if op == 'quit':
                            running = False
                        elif op == 'back':
                            continue
                    if pokemon_button.collidepoint(*event.pos):
                        print("pokemon")
                        op = player.shop_func(screen)
                        if op == 'quit':
                            running = False
                        elif op == 'back':
                            continue
                    if setting_button.collidepoint(*event.pos):
                        print("Setting")
                        settings_func()
                    if exit_button.collidepoint(*event.pos):
                        print("Exit")
                        player_index = -1
                        return
                        
        if running == False:
            break
        # draw
        mouse_x, mouse_y = pygame.mouse.get_pos()
        x_ratio = mouse_x / WIDTH
        y_ratio = mouse_y / HEIGHT
        bg_x = -int((bg_width - WIDTH) * x_ratio)
        bg_y = -int((bg_height - HEIGHT) * y_ratio)
        bg_x = max(min(bg_x, 0), WIDTH - bg_width)
        bg_y = max(min(bg_y, 0), HEIGHT - bg_height)
        screen.blit(background, (bg_x, bg_y))
        draw_text_center(screen, font_logo, "PIKACHU GAME", GRAY, WIDTH // 2, HEIGHT // 4)
        
        if mess_counter > 0:
            draw_text_center(screen, font_reg, mess, RED, WIDTH // 2, HEIGHT // 1.7)
            mess_counter -= 1
        # draw button
        continue_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 - button.get_height() // 2, button.get_width(), button.get_height())
        newgame_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 10 - button.get_height() // 2, button.get_width(), button.get_height())
        changemode_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 10 * 2 - button.get_height() // 2, button.get_width(), button.get_height())
        pokemon_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 10 * 3 - button.get_height() // 2, button.get_width(), button.get_height())
        setting_button = pygame.Rect(WIDTH // 4 - button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 10 * 4 - button.get_height() // 2, button.get_width(), button.get_height())
        exit_button = pygame.Rect(WIDTH // 4 - (button.get_width() - med_button.get_width()) // 2 - med_button.get_width() // 2, HEIGHT // 2.5 + HEIGHT // 10 * 5 - med_button.get_height() // 2, 150, 50)
        draw_img_center(screen, button_pressed if continue_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5)
        draw_img_center(screen, button_pressed if newgame_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 10)
        draw_img_center(screen, button_pressed if changemode_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 10 * 2)
        draw_img_center(screen, button_pressed if pokemon_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 10 * 3)
        draw_img_center(screen, button_pressed if setting_button.collidepoint(*pygame.mouse.get_pos()) else button, WIDTH // 4, HEIGHT // 2.5 + HEIGHT // 10 * 4)
        draw_img_center(screen, med_button_pressed if exit_button.collidepoint(*pygame.mouse.get_pos()) else med_button, WIDTH // 4 - (button.get_width() - med_button.get_width()) // 2, HEIGHT // 2.5 + HEIGHT // 10 * 5)
        # draw text
        if continue_button.collidepoint(*pygame.mouse.get_pos()):
            if continue_idx == -1:
                continue_idx = 0
                button_selected_sound.play()
        else:
            continue_idx = -1
        draw_text(screen, font_reg, "CONTINUE", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2, continue_idx)
        if continue_idx != -1:
            continue_idx += 1
        if newgame_button.collidepoint(*pygame.mouse.get_pos()):
            if newgame_idx == -1:
                newgame_idx = 0
                button_selected_sound.play()
        else:
            newgame_idx = -1
        draw_text(screen, font_reg, "NEW GAME", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 10, newgame_idx)
        if newgame_idx != -1:
            newgame_idx += 1
        if changemode_button.collidepoint(*pygame.mouse.get_pos()):
            if changemode_idx == -1:
                changemode_idx = 0
                button_selected_sound.play()
        else:
            changemode_idx = -1
        draw_text(screen, font_reg, "CHANGE MODE", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 10 * 2, changemode_idx)
        if changemode_idx != -1:
            changemode_idx += 1
        if pokemon_button.collidepoint(*pygame.mouse.get_pos()):
            if pokemon_idx == -1:
                pokemon_idx = 0
                button_selected_sound.play()
        else:
            pokemon_idx = -1
        draw_text(screen, font_reg, "POKEMON", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 10 * 3, pokemon_idx)
        if pokemon_idx != -1:
            pokemon_idx += 1
        if setting_button.collidepoint(*pygame.mouse.get_pos()):
            if setting_idx == -1:
                setting_idx = 0
                button_selected_sound.play()
        else:
            setting_idx = -1
        draw_text(screen, font_reg, "SETTINGS", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - button.get_height() // 2 + HEIGHT // 10 * 4, setting_idx)
        if setting_idx != -1:
            setting_idx += 1
        if exit_button.collidepoint(*pygame.mouse.get_pos()):
            if exit_idx == -1:
                exit_idx = 0
                button_selected_sound.play()
        else:
            exit_idx = -1
        draw_text(screen, font_reg, "LOG OUT", GRAY, WIDTH // 4 - button.get_width() // 2 + WIDTH // 120, HEIGHT // 2.5 - med_button.get_height() // 2 + HEIGHT // 10 * 5, exit_idx)
        if exit_idx != -1:
            exit_idx += 1
        # draw character circle
        # pygame.draw.rect(screen, RED, character_box, 3)
        draw_text_center(screen, font_reg, "CHOOSE YOUR POKEMON", GRAY, WIDTH // 4 * 3, HEIGHT // 2.7)
        pygame.draw.polygon(screen, GRAY, [(WIDTH // 4 * 3 - 30, HEIGHT // 2.7 + 20), (WIDTH // 4 * 3 + 30, HEIGHT // 2.7 + 20), (WIDTH // 4 * 3, HEIGHT // 2.7 + 20 + 20 * (3 ** 0.5))])
        min_sin, min_id = 1, 0
        for i in range(NO_CHAR):
            angle = math.pi / 2 + math.pi * 2 * i / NO_CHAR + angle_offset
            if math.sin(angle) < min_sin:
                min_sin, min_id = math.sin(angle), i
            alpha = min(240, max(40, 100 - 150 * math.sin(angle)))
            x, y = CENTER_X + RADIUS * math.cos(angle), CENTER_Y + RADIUS * math.sin(angle)
            image_copy = character_images[i].copy() if i in player.inventory else ball
            image_copy.set_alpha(alpha)
            draw_img_center(screen, image_copy, x, y)
        for i in range(NO_CHAR):
            if i == min_id:
                angle = math.pi / 2 + math.pi * 2 * i / NO_CHAR + angle_offset
                x, y = CENTER_X + RADIUS * math.cos(angle), CENTER_Y + RADIUS * math.sin(angle)
                draw_img_center(screen, frame, x, y)
        pygame.display.flip()
        pygame.time.delay(15)
    save_data()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    load_data()
    player_index = -1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if player_index == -1:
            home_screen()
        else:
            player_screen()
    
    save_data()
    pygame.quit()
    sys.exit()
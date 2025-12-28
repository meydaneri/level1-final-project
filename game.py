import pgzrun
import random

# Oyun alanı
cell = Actor('border')
cell1 = Actor('floor')
cell2 = Actor("crack")
cell3 = Actor("bones")
victory_image = Actor("victory_image")
game_over_image = Actor("game_over_image")
size_w = 9 # Alanın hücre cinsinden genişliği
size_h = 10 # Alanın hücre cinsinden yüksekliği
WIDTH = cell.width * size_w
HEIGHT = cell.height * size_h

win = 0
mode = "game"
colli = 0

TITLE = "WeCode ve Ejderhalar" # Oyunun başlığı
FPS = 30 # Saniyedeki kare sayısı
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 1, 1, 2, 1, 3, 1, 1, 0], 
          [0, 1, 1, 1, 2, 1, 1, 1, 0], 
          [0, 1, 3, 2, 1, 1, 3, 1, 0], 
          [0, 1, 1, 1, 1, 3, 1, 1, 0], 
          [0, 1, 1, 3, 1, 1, 2, 1, 0], 
          [0, 1, 1, 1, 1, 1, 1, 1, 0], 
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]] # Sağlık ve saldırı değerlerini belirtmek için kullanılan satır

# Ana karakter
char = Actor('stand')
char.top = cell.height
char.left = cell.width
char.health = 100
char.attack = 5

# Düşmanları oluşturma
enemies = []

for i in range(5):
    x = random.randint(1, 7) * cell.width
    y = random.randint(1, 7) * cell.height
    my_enemy = Actor("my_enemy", topleft = (x, y))
    my_enemy.health = random.randint(10, 20)
    my_enemy.attack = random.randint(5, 10)
    my_enemy.bonus = random.randint(0, 2)
    enemies.append(my_enemy)
   


# Bonuslar
hearts = []
swords = []   

# Haritayı çizme
def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width*j
                cell.top = cell.height*i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width*j
                cell1.top = cell.height*i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width*j
                cell2.top = cell.height*i
                cell2.draw()  
            elif my_map[i][j] == 3:
                cell3.left = cell.width*j
                cell3.top = cell.height*i
                cell3.draw() 

# Grafikleri çizme
def draw():
    if mode == 'game' or  mode=="level_2":
        screen.fill("#2f3542")
        map_draw()
        char.draw()
        screen.draw.text("HP:", center=(25, 475), color = 'white', fontsize = 20)
        screen.draw.text(str(char.health), center=(75, 475), color = 'white', fontsize = 20)
        screen.draw.text("AP:", center=(375, 475), color = 'white', fontsize = 20)
        screen.draw.text(str(char.attack), center=(425, 475), color = 'white', fontsize = 20)
        for i in range(len(enemies)):
            enemies[i].draw()
            # Düşman sağlığını çizdirme
            screen.draw.text(str(enemies[i].health), topleft=(enemies[i].x + 5, enemies[i].y - 30), color='white' ,
fontsize=18)
                             
        # Bonusları çizme
        for i in range(len(hearts)):
            hearts[i].draw()
        for i in range(len(swords)):
            swords[i].draw()
        
    # Zafer/Yenilgi penceresi
    elif mode == "end":  
        if win == 2:
            victory_image.draw()
        else:
            game_over_image.draw()


# Kontroller
def on_key_down(key):
    global colli
    old_x = char.x
    old_y = char.y
    if keyboard.right and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'stand'
    elif keyboard.left and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'left'
    elif keyboard.down and char.y + cell.height < HEIGHT - cell.height*2:
        char.y += cell.height
    elif keyboard.up and char.y - cell.height > cell.height:
        char.y -= cell.height
        
    # Düşmanlar ile çarpışma
    enemy_index = char.collidelist(enemies)
    if enemy_index != -1:
        char.x = old_x
        char.y = old_y
        colli = 1
        enemy = enemies[enemy_index]
        enemy.health -= char.attack
        char.health -= enemy.attack
        if enemy.health <= 0:
            # Bonusları ekleme
            if enemy.bonus == 1:
                heart = Actor('heart')
                heart.pos = enemy.pos
                hearts.append(heart)
            elif enemy.bonus == 2:
                sword = Actor('sword')
                sword.pos = enemy.pos
                swords.append(sword)
            enemies.pop(enemy_index)

# Zafer ve yenilgi mantığı
def victory():
    global mode, win
    if enemies == [] and char.health > 0:
        mode = "level_2"
        win += 1
        char.health = 100
        for i in range(5):
            x = random.randint(1, 7) * cell.width
            y = random.randint(1, 7) * cell.height
            enemy = Actor("enemy", topleft = (x, y))
            enemy.health = random.randint(15, 25)
            enemy.attack = random.randint(5, 10)
            enemy.bonus = random.randint(0, 2)
            enemies.append(enemy)
        if win == 2:
            mode = "end"
    elif char.health <= 0:
        mode = "end"
        win = -1
    


# Bonusların mantığı
def update(dt):
    victory()
    for i in range(len(hearts)):
        if char.colliderect(hearts[i]):
            char.health += 5
            hearts.pop(i)
            break
        
    for i in range(len(swords)):
        if char.colliderect(swords[i]):
            char.attack += 5
            swords.pop(i)
            break




def restart_game():
    global mode, win, enemies, hearts, swords

    mode = "game"
    win = 0

    # karakteri sıfırla
    char.topleft = (cell.width, cell.height)
    char.image = "stand"
    char.health = 100
    char.attack = 5

    # bonusları temizle
    hearts.clear()
    swords.clear()

    # düşmanları sıfırla
    enemies.clear()
    for i in range(5):
        x = random.randint(1, 7) * cell.width
        y = random.randint(1, 7) * cell.height
        e = Actor("my_enemy", topleft=(x, y))
        e.health = random.randint(10, 20)
        e.attack = random.randint(5, 10)
        e.bonus = random.randint(0, 2)
        enemies.append(e)

# Kazanma ekranı    
PLAY_X = 120
PLAY_Y = 310
PLAY_W = 210
PLAY_H = 62

# Game Over ekranı
GO_X = 115
GO_Y = 390
GO_W = 220
GO_H = 62

def on_mouse_down(pos, button):
    if mode == "end":
        # Victory ekranında
        if win == 2:
            if PLAY_X <= pos[0] <= PLAY_X + PLAY_W and PLAY_Y <= pos[1] <= PLAY_Y + PLAY_H:
                restart_game()

        # Game Over ekranında
        else:  # win -1 veya başka bir değer
            if GO_X <= pos[0] <= GO_X + GO_W and GO_Y <= pos[1] <= GO_Y + GO_H:
                restart_game()

        
    

pgzrun.go()

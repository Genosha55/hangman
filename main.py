import pygame
import math
import random


# set display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# menu variables
class Menu_Var:
    def __init__(self):
        self.MENU_RADIUS = 60
        self.MENU_GAP = 30

        self.menu_x = WIDTH//2
        self.menu_y = self.MENU_RADIUS + (HEIGHT - 60 - 4 * self.MENU_RADIUS - self.MENU_GAP)
        self.menu_pos1 = [self.menu_x, self.menu_y, "Start", True]
        self.menu_pos2 = [self.menu_x, self.menu_y + self.MENU_GAP + 2 * self.MENU_RADIUS, "Quit", True]

# button variables 
class Button_Var:
    def __init__(self):
        self.RADIUS = 20
        self.GAP = 15
    
    def init_letters(self):
        letters = [] # record position of all the buttons created
        startx = round((WIDTH- 4 * self.GAP - 2 * self.RADIUS - (self.RADIUS * 2 + self.GAP) * 12 ) / 2)
        starty = 400
        A = 65 # cap A is 65 in number so B is 66, letter i is A+i
        for i in range(26):
            x = startx + self.GAP * 2 + self.RADIUS + ((2 * self.RADIUS + self.GAP) * (i % 13))
            y = starty + ((i // 13) * (self.GAP + self.RADIUS * 2))
            letters.append([x, y, chr(A + i), True]) # append a list [a,b,c,d] to store features
        return letters

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
MENU_FONT = pygame.font.SysFont('comicsans', 60)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
class Game_Var:
    def __init__(self):
        self.hangman_status = 0
        self.words = ["IDE", "REPLIT", "PYTHON", "PYGAME", "DEVELOPER"]
        # self.word = random.choice(self.words) 
        # self.guessed = [] # usue a list to keep track of words guessed (might use a set)
    
    def choose_word(self):
        return random.choice(self.words) 


# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)

# # setup game loop
# FPS = 60
# clock = pygame.time.Clock()
# run = True

def draw_prep():
    win.fill(WHITE)
    #draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    #draw menu
    mv = Menu_Var()
    x1, y1, menu_info1, visible1 = mv.menu_pos1
    x2, y2, menu_info2, visible2 = mv.menu_pos2
    if visible1:
        pygame.draw.circle(win, BLUE, (x1,y1), mv.MENU_RADIUS, 5)
        text = MENU_FONT.render(menu_info1, 1, RED)
        win.blit(text, (x1 - text.get_width()/2, y1 - text.get_height()/2))
    if visible2:
        pygame.draw.circle(win, BLUE, (x2,y2), mv.MENU_RADIUS, 5)
        text = MENU_FONT.render(menu_info2, 1, RED)
        win.blit(text, (x2 - text.get_width()/2, y2 - text.get_height()/2))
    pygame.display.update()

def draw(word, guessed, hangman_status, letters):
    win.fill(WHITE)
    button_var = Button_Var()
    #draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x,y), button_var.RADIUS, 3) # 3 thick
            text = LETTER_FONT.render(ltr, 1, BLACK) # 1 as the antialias
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status],(150,100))
    pygame.display.update()

def display_message(message):
    pygame.time.delay(1000) # 1000 ms = 1 sec
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    keep_running = True
    gv = Game_Var()
    button_var = Button_Var()
    hangman_status = gv.hangman_status    
    guessed = []
    letters = button_var.init_letters()

    FPS = 60
    clock = pygame.time.Clock()
    run = True
    current_word = gv.choose_word()
    print(current_word)

    while run:
        clock.tick(FPS) # set the clock to tick at this speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y ,ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < button_var.RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in current_word:
                                hangman_status += 1 
        
        draw(current_word, guessed, hangman_status, letters)
        
        # display endgame result
        won = True
        for letter in current_word:
            if letter not in guessed:
                won = False
                break
        
        if won:                
            display_message("You Won!")
            break
        
        if hangman_status == 6:        
            display_message("You Lose...")
            break
    return keep_running

def prep_page():
    start_game = False 
    keep_running = True
    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS) # set the clock to tick at this speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_running = False
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                
                mv = Menu_Var()  
                x1, y1, menu_info1, visible1 = mv.menu_pos1
                x2, y2, menu_info2, visible2 = mv.menu_pos2
                if visible1:
                    dis1 = math.sqrt((x1 - m_x)**2 + (y1 - m_y)**2)
                    if dis1 < mv.MENU_RADIUS:
                        mv.menu_pos1[3] = False
                        start_game = True
                        run = False
                if visible2:
                    dis2 = math.sqrt((x2 - m_x)**2 + (y2 - m_y)**2)
                    if dis2 < mv.MENU_RADIUS:
                        mv.menu_pos2[3] = False
                        keep_running = False
                        run = False         
        draw_prep()
    return keep_running, start_game

class Control:
    def __init__(self):
        self.keep_running = True
        self.run = True
        self.start_game = False


control = Control()
while control.keep_running: # added a menu for restart
    # add a menu display to start the game
    control.keep_running, control.start_game = prep_page()
    if control.start_game:
        control.keep_running = main()
pygame.quit()
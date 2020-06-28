import pygame
import os
import math

# set display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables 
RADIUS = 20
GAP = 15
letters = [] # record position of all the buttons created
startx = round((WIDTH- 4 * GAP - 2 * RADIUS - (RADIUS * 2 + GAP) * 12 ) / 2)
starty = 400
A = 65 # cap A is 65 in number so B is 66, letter i is A+i
for i in range(26):
    x = startx + GAP * 2 + RADIUS + ((2 * RADIUS + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True]) # append a list [a,b,c,d] to store features

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)

# load images
images = []
for i in range(6):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)



# game variables
hangman_status = 0
word = "DEVELOPER" 
guessed = [] # usue a list to keep track of words guessed (might use a set)

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True

def draw():
    win.fill(WHITE)

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
            pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3) # 3 thick
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


while run:
    clock.tick(FPS) # set the clock to tick at this speed

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y ,ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1 
    
    # display endgame result
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    
    if won:        
        display_message("You Won!")
        break
    
    if hangman_status == 6:        
        display_message("You Lose...")
        break

pygame.quit()
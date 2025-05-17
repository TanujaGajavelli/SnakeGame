import pygame
import random
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # For PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # For normal execution
    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init()

#Colors
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

screen_width=900
screen_height=600
gameWindow=pygame.display.set_mode((screen_width,screen_height))
#background image
bgimg = pygame.image.load(resource_path("static/back.jpg"))
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()


pygame.display.set_caption("Snake Game!!")
pygame.display.update()

clock=pygame.time.Clock()

font = pygame.font.SysFont("comicsansms", 40)  # None=default font 55=size of font

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for snake_x,snake_y in snk_list:
        pygame.draw.rect(gameWindow,color,[snake_x,snake_y,snake_size,snake_size])  #x y width height

#welcome screen
def welcome():
    fps = 30  # frame per second
    exit_game=False
    while(not exit_game):
        gameWindow.fill(white)
        gameWindow.blit(bgimg, (0, 0))
        text_screen("Welcome to Snakes!!",(80,90,200),220,220)
        text_screen("Press Space Bar to play!!",(80,90,200),200,250)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                exit_game=True
            elif(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_SPACE):
                    pygame.mixer.music.load(resource_path("static/calm_music.mp3"))  # loading
                    pygame.mixer.music.play()
                    gameloop()
            pygame.display.update()
            clock.tick(fps)


#Game loop
def gameloop():
    # If user quits then it will be true
    exit_game = False
    # if game is over-True
    game_over = False
    # Game specific
    snake_x = 45
    snake_y = 75  # initial position of snake
    snake_size = 10
    fps = 30  # frame per second
    init_velocity = 2
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(70, screen_width // 2)
    food_y = random.randint(70, screen_height // 2)
    score = 0
    if(not os.path.exists(resource_path("static/HighScore.txt"))):
        with open(resource_path("static/HighScore.txt"),"w") as f:
            f.write("0")
    with open(resource_path("static/HighScore.txt"), "r") as f:
        highscore = f.read()
        if (highscore == ""):
            highscore = 0
        else:
            highscore = int(highscore)
    count = 0

    while(not exit_game):
        if(game_over):
            with open(resource_path("static/HighScore.txt"), "w") as f:
                f.write(str(highscore))
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Game Over!! Press enter to continue!!",(80,90,200),120,240)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):  # if user quits
                    exit_game = True
                if(event.type==pygame.KEYDOWN):
                    if(event.key==pygame.K_RETURN): #Return-enter key
                        gameloop()

        else:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):  # if user quits
                    exit_game = True
                    pygame.quit()
                if(event.type==pygame.KEYDOWN):
                    if(event.key==pygame.K_RIGHT):
                        velocity_x=init_velocity
                        velocity_y=0
                    if (event.key == pygame.K_LEFT):
                        velocity_x=-init_velocity
                        velocity_y=0
                    if (event.key == pygame.K_UP):
                        velocity_y=-init_velocity
                        velocity_x=0
                    if (event.key == pygame.K_DOWN):
                        velocity_y=init_velocity
                        velocity_x=0

            snake_x+=velocity_x
            snake_y+=velocity_y

            if(abs(snake_x-food_x)<6 and abs(snake_y-food_y)<6):
                score+=10
                count+=1
                food_x = random.randint(70, screen_width // 2)
                food_y = random.randint(70, screen_height // 2)
                snk_length+=5
                if(score>highscore):
                    highscore=score
            if(count==10):
                init_velocity+=1
                count=0

            gameWindow.fill(white)
            pygame.draw.rect(gameWindow, (0,100,180), [0, 0, screen_width,70])
            text_screen("Score: " + str(score)+" High Score: "+str(highscore), (165,0,0), 5, 5)
            # pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])  #x y width height

            #snake head
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if(len(snk_list)>snk_length):
                del snk_list[0]

            #if snake collides with itself
            if(head in snk_list[:-1]):
                pygame.mixer.music.load(resource_path('static/Big Explosion Cut Off.mp3'))  # loading
                pygame.mixer.music.play()

                game_over=True
            if(snake_x<0):
                snake_x=screen_width-snake_x
            elif (snake_x > screen_width):
                snake_x =snake_x-screen_width
            elif (snake_y < 70):
                snake_y = screen_height - snake_y+70
            elif (snake_y > screen_height):
                snake_y = snake_y - screen_height+70
            # if(snake_x<0 or snake_x>screen_width or snake_y<70 or snake_y>screen_height):
            #     pygame.mixer.music.load('Big Explosion Cut Off.mp3')  # loading
            #     pygame.mixer.music.play()
            #     game_over=True

            pygame.draw.rect(gameWindow, (0,0,0), [0, 70, screen_width, screen_height-50])
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            plot_snake(gameWindow,(0,255,0),snk_list,snake_size)
        pygame.display.update()  #It should be run every time after update
        clock.tick(fps)
    pygame.quit()
welcome()
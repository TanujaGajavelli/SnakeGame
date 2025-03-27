import pygame
x=pygame.init()  #initialize pygame modules
# print(x)  #testing
gameWindow=pygame.display.set_mode((1200,500))  #1200-width,500-height

#game title
pygame.display.set_caption("My First Game!!")

#If user quits then it will be true
exit_game=False
#if game is over-True
game_over=False

#Creating a game loop-handles all events in game
while(not exit_game):
    for event in pygame.event.get(): #all events user does
        if(event.type==pygame.QUIT):  #if user quits
            exit_game=True
        if(event.type==pygame.KEYDOWN): #if any key is pressed
            if(event.key==pygame.K_RIGHT):  #if right key is pressed
                print("You have pressed arrow right key!")
pygame.quit()  #game ends
quit()  #python program ends
import pygame
from classes import*
import pygame
import math
import random
from pygame.locals import*

def main():
    pygame.init()
    
    display = pygame.display.set_mode((1920, 1080))

    clock = pygame.time.Clock()
    timeKeeper = Timer('digital-7.ttf', 60)

    player1Score = Scores('digital-7.ttf', 70, 0) 
    player2Score = Scores('digital-7.ttf', 70, 0) 

    
    puck = Puck(random.uniform(0, 2 * math.pi), 0)
    puck_group = pygame.sprite.RenderPlain(puck)

    # Instantiate the player sprite objects and keep references to both the
    # actual object and the sprite group containing it.  The code originally
    # stored only the group which made it difficult to access attributes of the
    # underlying sprite such as ``rect`` or custom methods like ``mouseMove``.
    # Keeping the object references allows us to update the sprite while still
    # using the group for drawing and collision detection.
    player1_obj = Player1()
    player1 = pygame.sprite.RenderPlain(player1_obj)
    player2_obj = Player2()
    player2 = pygame.sprite.RenderPlain(player2_obj)

    background = pygame.image.load('models/background.png')
    display.blit(background,(0,0))

    # final message
    message = pygame.font.Font('TESLA.ttf', 50)

    mouseX, mouseY = 0, 0
    coord = []
    gameOver = False 
    running = True

    while running:
        '''
        for event in pygame.event.get():
    
            # Close if the user quits the 
            # game
            if event.type == exit:
                running = False
    
            # Making the image move
            elif event.type == pygame.MOUSEMOTION:
                (mouseX, mouseY) = pygame.mouse.get_pos()  
    

        display.blit(background, (0,0))
        display.blit(red_paddle, (mouseX-red_paddle_offset[0], mouseY-red_paddle_offset[1]))
    

        # Update the GUI pygame
        pygame.display.update()
'''
        ###################################################
        ###################COPIED CODE#####################
        ###################################################
 
        '''if mainM:
            #blits the main menu on the screen 
            display.blit(mainMenu.image, (0,0))
            pygame.display.flip()
            #checks for the common events in the game 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif isClicked(120, 290, 130, 70):
                    mainM = False
                elif isClicked(540, 290, 130, 70):
                    pygame.quit() '''
                    
    
            
            
        '''elif gameOver:
            #returns you to the main menu if the game is over. i.e 3 minutes have passed            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif isClicked(120, 290, 130, 70):
                    print('its working')
                    #resetting all variables for another game 
                    mainM = False
                    gameOver = False 
                    puck.compScore = 0
                    puck.playerScore = 0
                    timeKeeper.min = 2
                    timeKeeper.seconds = 60
                    puck.rect.center = puck.area.center
                    
                #check to see if the user pressed the quit button    
                elif isClicked(540, 290, 130, 70):
                    pygame.quit()
                #check to see if player wins or computer wins or if it is a draw 
                if puck.compScore > puck.playerScore:
                    msg = message.render('Computer Wins', False, (0,0,0))
                elif puck.compScore == puck.playerScore:
                    msg = message.render('It is a draw!', False, (0,0,0))
                else:
                    msg = message.render('Player wins', False, (0,0,0))
                print(msg)
                display.blit(mainMenu.image, (0,0))
                display.blit(msg, (150, 200))
        else:'''

        #check to if game is over i.e 3 minutes have passed 
        if timeKeeper.min == -1:
            gameOver = True 
            
                
        # check to see if user has pressed the main menu button
        if isClicked(340, 0, 90, 50):
            mainM = True

        #updating the scores 
        player1Text = player1Score.render(str(puck.player1Score), False, (0,0,0))
        player2Text = player2Score.render(str(puck.player2Score), False, (0,0,0))

        #checking the updating the clock 
        timeElapsed = clock.tick(60)
        timeKeeper.update(timeElapsed)
        timeText= timeKeeper.displayTime() 
        
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == MOUSEMOTION:
                # ``mouseMove`` is defined on the sprite object, not the group
                # wrapper, so call it on ``player1_obj``.
                player1_obj.mouseMove()
            
        #checks for the collision between puck and player sprite, handles its collision
        if pygame.sprite.groupcollide(puck_group, player1, False, False, pygame.sprite.collide_circle):

            (dx, dy) = pygame.mouse.get_rel()
            
            puck.angle = math.atan2(dy, dx)
            puck.speed = 30

        if pygame.sprite.groupcollide(puck_group, player2, False, False, pygame.sprite.collide_circle):

            (dx, dy) = pygame.mouse.get_rel()
            
            puck.angle = math.atan2(dy, dx)
            puck.speed = 30
    
        #places the puck back in the 
        if puck.goal:
            puck.goal = False
            puck.rect.center = puck.area.center

        

        #blits all the objects on to the display every frame
        display.blit(background, puck.rect, puck.rect)
        # ``player1`` and ``player2`` are sprite groups. For clearing the
        # background from the previous frame we need the rects of the actual
        # sprite objects.
        display.blit(background, player1_obj.rect, player1_obj.rect)
        display.blit(background, player2_obj.rect, player2_obj.rect)
        display.blit(player1Text, (550, 175))
        display.blit(player2Text, (220, 175))
        display.blit(timeText, (340, 180))
        
        
        #updates the sprites 
        player1.update()
        player2.update()
        puck_group.update()
    
        
        player1.draw(display)
        player2.draw(display)
        puck_group.draw(display)
        
    
        pygame.display.flip()
main()

# Quit the GUI game
pygame.quit()
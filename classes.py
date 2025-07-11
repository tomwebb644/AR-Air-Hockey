#com 110
#authors: Benjamin Calcote and Abhijeet Pradhan
#game: intro air hockey

import pygame
import math
from pygame.locals import *
import random
import time


def load_img(name):
    '''
    this a helper function used to load images into the variable image. returns a
    image surface and image rect
    source: https://www.pygame.org/docs/tut/ChimpLineByLine.html
    '''
    try:
        image = pygame.image.load(name)
    except pygame.error as e:
        raise SystemExit(str(e))
    return image, image.get_rect()

class Background(pygame.sprite.Sprite):
    '''
    This class instantiates a background for the display. Here the back
    ground is the image of an air hockey table. 
    '''
    def __init__(self, image):
        self.image, self.rect = load_img(image)
        
class Scores(pygame.font.Font):
    '''
    This class is designed to display scores during the game 
    
    '''
    def __init__(self, fontType, size, score):
        pygame.font.Font.__init__(self, fontType, size)
        self.score = score
    def scoreUpdate(self, newScore):
        #this methods updates the time on the display
        self.score = newScore 

class Timer(pygame.font.Font):
    '''
    This class keeps track of the time during the game. Each game lasts for three
    minutes
    '''
    def __init__(self, fontType, size):
        #instanctiating the relevant variables
        pygame.font.Font.__init__(self, fontType, size)
        self.min = 2
        self.seconds = 60
     
        #accumulates the total time in milliseconds 
        self.milliseconds = 0
        
    def update(self, delTime):
        #updates the time. the logic for the timer 
        self.milliseconds += delTime
        if self.milliseconds > 1000:
            self.seconds -= 1
            self.milliseconds = 0
        if self.seconds == 0:
            self.seconds = 60
            self.min -= 1
            
    def displayTime(self):
        #this methods displays the time on the table 
        if self.seconds == 60:
            label = self.render('{:0>2}:{:0>2}'.format(self.min+1, 0), False, (0,0,0))
        else: 
            label = self.render('{:0>2}:{:0>2}'.format(self.min, self.seconds), False, (0,0,0))
        return label 

class Puck(pygame.sprite.Sprite):
    '''
    This class deals with the interaction of the puck in the game. It has all relevant
    variables like angles, speeds scores instantiated.
    ''' 
    def __init__(self, angle, speed):
        #variable instantiation
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('models/puck.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.angle = angle
        self.speed = speed
        self.player1Score = 0
        self.player2Score = 0 
        self.goal = False 
        self.rect.center = self.area.center 
        
    def calcNewPos(self, rect, angle, speed):
        #caclcutes new postion for the puck every frame of the game. uses basic trigonometry
        dx, dy = speed*math.cos(angle), speed*math.sin(angle)
        return rect.move(dx, dy)
    
    def update(self):
        #updates the postion of the puck from the position in the last frame 
        newpos = self.calcNewPos(self.rect, self.angle, self.speed)
        #implementing friction for the puck 
        if self.speed > 0:
            self.speed -= 0.5 
        self.rect = newpos

        #the logic below checks for collisions in the edges of the display and
        #implements proper collisions 
        if not self.area.contains(newpos) and not self.goal:
       
            xl = self.rect.left
            xr = self.rect.right
            yt = self.rect.top
            yb = self.rect.bottom

            if xl < self.area.left:
                if  225 > self.rect.midleft[1] > 175:
                    self.player2Score += 1
                    print('player 2 scores', self.player2Score)
##                    self.rect.center = self.area.center
                    self.goal = True
                    self.speed = 50
                     
    
                else: 
                    self.rect.midleft = (self.area.left, self.rect.centery) 
                    self.angle = math.pi - self.angle
                    
            elif xr > self.area.right:
                if  225> self.rect.midright[1] > 175 :
                    self.player1Score += 1
                    self.speed = 50
##                    self.rect.center = self.area.center
                    self.goal = True 
                    print('player 1 scores', self.player1Score)
                     
                else:     
                    self.rect.midright = (self.area.right, self.rect.centery)
                    self.angle = math.pi - self.angle
            elif yt < self.area.top:
                self.rect.midtop = (self.rect.centerx, self.area.top) 
                self.angle = -self.angle
            elif yb > self.area.bottom:
                self.rect.midbottom = (self.rect.centerx, self.area.bottom) 
                self.angle = -self.angle

                
                
    def courtHalf(self):
        #this method check which half the puck is on 
        if self.rect.midright[0] < self.area.centerx:
            return 'left'
        else:
            return 'right' 

class Player1(pygame.sprite.Sprite):
    '''
    This class deals with the interaction of the player in the game. It allows the
    player to move his striker with the aid of the mouse controller. It also handles
    collisions with the puck
    '''
    def __init__(self):
        #instantiates variables 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('models/blue_paddle.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() 
        self.newpos = (0,0)  
        self.start()
        
    def start(self):
        #start position of the player 
      
        self.rect.midleft = self.area.midleft
       


    def mouseMove(self):
        #this method check the mouse position for the player striker to follow 
        self.newpos = pygame.mouse.get_pos()
##        print(self.newpos)
    
        
    def update(self):
        #this method updates the position of the puck in the game 
        self.rect.center = self.newpos 
##        print(pygame.mouse.get_pos())
        if not self.area.contains(self.rect):

            tl = not self.area.collidepoint(self.rect.topleft)
            tr = not self.area.collidepoint(self.rect.topright)
            bl = not self.area.collidepoint(self.rect.bottomleft)
            br = not self.area.collidepoint(self.rect.bottomright)

            if tr and tl:
                self.rect.midtop = (self.rect.centerx, self.area.top) 
            if br and bl:
                self.rect.midbottom = (self.rect.centerx, self.area.bottom) 

            elif tl and bl:
                self.rect.midleft = (self.area.left, self.rect.centery) 
        elif self.rect.centerx > self.area.centerx:
            self.rect.midright = (self.area.centerx, self.rect.centery)
        
        pygame.event.pump()
        

class Player2(pygame.sprite.Sprite):
    '''
    This class deals with the interaction of the player in the game. It allows the
    player to move his striker with the aid of the mouse controller. It also handles
    collisions with the puck
    '''
    def __init__(self):
        #instantiates variables 
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_img('models/red_paddle.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect() 
        self.newpos = (0,0)  
        self.start()
        
    def start(self):
        #start position of the player 
      
        self.rect.midleft = self.area.midleft
       


    def mouseMove(self):
        #this method check the mouse position for the player striker to follow 
        self.newpos = pygame.mouse.get_pos()
##        print(self.newpos)
    
        
    def update(self):
        #this method updates the position of the puck in the game 
        self.rect.center = self.newpos 
##        print(pygame.mouse.get_pos())
        if not self.area.contains(self.rect):

            tl = not self.area.collidepoint(self.rect.topleft)
            tr = not self.area.collidepoint(self.rect.topright)
            bl = not self.area.collidepoint(self.rect.bottomleft)
            br = not self.area.collidepoint(self.rect.bottomright)

            if tr and tl:
                self.rect.midtop = (self.rect.centerx, self.area.top) 
            if br and bl:
                self.rect.midbottom = (self.rect.centerx, self.area.bottom) 

            elif tl and bl:
                self.rect.midleft = (self.area.left, self.rect.centery) 
        elif self.rect.centerx > self.area.centerx:
            self.rect.midright = (self.area.centerx, self.rect.centery)
        
        pygame.event.pump()

    
 
def isClicked(x, y, w, h):
    '''
    this is another helper function useful in the main function to detect user clicks
    on the buttons of the menu.
    '''
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed() 

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0]: 
            return True 

        

        
        

        
            
        
    

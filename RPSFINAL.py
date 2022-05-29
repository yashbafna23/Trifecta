import pygame, sys, os, random
from pygame.locals import *

originalpath = os.getcwd()
pathtoResourcefolder = os.path.abspath(r'RPS Resources')

#Put ur path to the resource folder over here
os.chdir(pathtoResourcefolder)


FPS = 50  # frames per second, the general speed of the program

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

fontsize = 15  # Font for printing he score for the players

#            R    G    B
GRAY = (100, 100, 100)
DARKGRAY = (77, 77, 51)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LEAFGREEN = (0, 51, 0)
OLIVEGREEN = (134, 179, 0)
TURQUOISE = (0, 102, 102)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 128, 128)
OCHRE = (179, 143, 0)
DEEPBLUE = (19, 38, 58)
DARKPURPLE = (51, 51, 77)
BRIGHTGREEN = (136, 255, 77)
BROWN = (128, 64, 0)
BLACK = (0, 0, 0)
MAROON = (51, 20, 0)
BABYPINK = (255, 128, 223)
LEMONYELLOW = (255, 255, 26)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
DARKORANGE = (204, 82, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
DARKGREEN = (45, 134, 45)
DARKBLUE = (15, 15, 62)

BGCOLOR = DARKGREEN

BOXHEIGHT = 250
BOXWIDTH = 250

LeftBoxX, LeftBoxY = 70, 130
RightBoxX, RightBoxY = DISPLAY_WIDTH - LeftBoxX - BOXWIDTH, LeftBoxY

# Move Representations
HUMANMOVE = 0  # MOVE THE HUMAN PLAYER MAKES
CPUMOVE = 0  # Move the CPU HAS CHOSEN

#The position of the images
HumanX,HumanY = LeftBoxX + 50,LeftBoxY+50
CpuX,CpuY     = RightBoxX+50 , RightBoxY+50

wasScoreChanged = False

# Score variables for cpu and human
HUMANCOUNT = 0
CPUCOUNT = 0


def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 50)
    global FPS, wasScoreChanged,DISPLAYSURF, HUMANCOUNT, CPUCOUNT, HUMANMOVE, CPUMOVE,DISPLAYSURF,RockImg,ScissorsImg,PaperImg
    global RockMirrorImg,ScissorsMirrorImg,PaperMirrorImg,FPSCLOCK,FPS,ScissorsSound,PaperSound,RockSound
    global QMarkImg ,InstructionImg,wasScoreChanged,winner


    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('ROCK PAPER SCISSOR GAME')

    # These are the image files
    RockImg = pygame.image.load('Rock.png')
    RockImg = pygame.transform.scale(RockImg, (150, 150))

    ScissorsImg = pygame.image.load('Scissors.png')
    ScissorsImg = pygame.transform.scale(ScissorsImg, (150, 150))

    PaperImg = pygame.image.load('Paper.png')
    PaperImg = pygame.transform.scale(PaperImg, (150, 150))

    RockMirrorImg = pygame.image.load('RockMirror.png')
    RockMirrorImg = pygame.transform.scale(RockMirrorImg, (150, 150))

    ScissorsMirrorImg = pygame.image.load('ScissorsMirror.png')
    ScissorsMirrorImg = pygame.transform.scale(ScissorsMirrorImg, (150, 150))

    PaperMirrorImg = pygame.image.load('PaperMirror.png')
    PaperMirrorImg = pygame.transform.scale(PaperMirrorImg, (150, 150))

    QMarkImg = pygame.image.load('QMark.png')
    QMarkImg = pygame.transform.scale(QMarkImg,(150, 150))

    InstructionImg = pygame.image.load('Instructions.png')
    InstructionImg = pygame.transform.scale(InstructionImg ,(400,50) )

    #LOAD BACKGROUND MUSIC
    pygame.mixer.music.load("MainMusic.mp3")

    #LOAD MUSIC FOR MOVES
    ScissorsSound = pygame.mixer.Sound("Scissors.wav")
    RockSound = pygame.mixer.Sound("Rock.wav")
    PaperSound = pygame.mixer.Sound("Paper.wav")

    startGameAnimation()
    pygame.mixer.music.play(-1,0.0)      #Play sound

    # MAIN LOOP
    while True:
        winner = None
        for event in pygame.event.get():
             if event.type == QUIT: #QUIT CONDITION
                 os.chdir(originalpath)
                 pygame.quit()
                 os.system('python MAINMENU.py')
                 sys.exit()

             elif event.type == pygame.KEYDOWN:
                 #Check if a key was pressed
                if event.key == pygame.K_LEFT:
                    HUMANMOVE = 1
                elif event.key == pygame.K_UP:
                    HUMANMOVE = 2
                elif event.key == pygame.K_RIGHT:
                    HUMANMOVE = 3

             if event.type == pygame.KEYUP:
                 if event.key == pygame.K_SPACE:
                     if HUMANMOVE == 0:  # Case when no move was made by human and pressed space
                         continue        #Don't do anything
                     CPUMOVE = random.randint(1, 3)     #Select a move
                     if (HUMANMOVE == CPUMOVE):
                         PlayWinnerSound(HUMANMOVE)                  #Play sound only!!
                     elif (HUMANMOVE == 1 and CPUMOVE== 2) or (HUMANMOVE == 2 and CPUMOVE == 3) or (HUMANMOVE== 3 and CPUMOVE == 1):
                        PlayWinnerSound(CPUMOVE)
                        winner = 'CPU'
                        CPUCOUNT += 1              #CPU WON
                     elif (HUMANMOVE == 2 and CPUMOVE == 1) or (HUMANMOVE == 3 and CPUMOVE == 2) or (HUMANMOVE == 1 and CPUMOVE == 3):
                         PlayWinnerSound(HUMANMOVE)
                         winner = 'HUMAN'
                         HUMANCOUNT += 1            # Player won
                     wasScoreChanged=True        #TO SHOW THAT A MOVE WAS MADE BY BOTH CPU AND HUMAN

        DISPLAYSURF.fill(BGCOLOR)

        drawRectangles()                                # Draw the yellow boxes on the screen
        drawInstructionImg()
        drawCPUMove(selectCpuImg(CPUMOVE))              #IF CPU made a move draw image
        drawHumanMove(selectHumanImg(HUMANMOVE))        #If human made a move draw image
        drawFont()                                      #draw all the text elements

        pygame.display.update()

        #If a successful move was made by both players change CPUMOVE AND HUMANMOVE TO 0 and wait
        if wasScoreChanged:
            # pygame.draw.rect(DISPLAYSURF,,,)
            pygame.time.wait(1600)
            HUMANMOVE = CPUMOVE = 0
            wasScoreChanged = False

        endGameAnimation()  #PLAY ENDGAME ANIMATION IF REQUIRED

        FPSCLOCK.tick(FPS)



def PlayWinnerSound(Movemade):
    '''It plays the winner object's sound'''
    if Movemade==1:
        RockSound.play()
    elif Movemade==2:
        PaperSound.play()
    elif Movemade==3:
        ScissorsSound.play()




def selectHumanImg(MoveMade):
    ''''Returns the image of the human move selected'''
    if MoveMade==0:
        return QMarkImg
    elif MoveMade == 1:
        return RockImg
    elif MoveMade==2:
        return PaperImg
    elif MoveMade==3:
       return ScissorsImg
    else:
        return None


def drawInstructionImg():
    ''' Draw Instruction Image'''
    global DISPLAYSURF , InstructionImg
    DISPLAYSURF.blit( InstructionImg , (DISPLAY_WIDTH//2-180,DISPLAY_HEIGHT-100) )



def selectCpuImg(MoveMade):
    ''''Returns the image of the cpu move selected'''
    if MoveMade==0:
        return QMarkImg
    elif MoveMade == 1:
        return RockMirrorImg
    elif MoveMade==2:
        return PaperMirrorImg
    elif MoveMade==3:
       return ScissorsMirrorImg
    else:
        return None


def drawHumanMove(Img):
    '''This function puts the Human image on the screen'''
    global DISPLAYSURF
    if Img!=None:
        DISPLAYSURF.blit(Img,(HumanX,HumanY))

def drawCPUMove(Img):
    '''This function puts the CPU image on the screen'''
    global DISPLAYSURF
    if Img != None:
        DISPLAYSURF.blit(Img,(CpuX,CpuY))

def drawRectangles():
    ''''This function draws rectangular boxes on to the screen'''
    global wasScoreChanged ,winner
    pygame.draw.rect(DISPLAYSURF, OCHRE, (LeftBoxX, LeftBoxY, BOXWIDTH, BOXHEIGHT))
    pygame.draw.rect(DISPLAYSURF, OCHRE, (RightBoxX, RightBoxY, BOXWIDTH, BOXHEIGHT))
    pygame.draw.rect(DISPLAYSURF,  BLACK , (LeftBoxX-2, LeftBoxY-2, BOXWIDTH+4, BOXHEIGHT+4),4)
    pygame.draw.rect(DISPLAYSURF,  BLACK , (RightBoxX-2, RightBoxY-2, BOXWIDTH+4, BOXHEIGHT+4),4)
    if wasScoreChanged:
        if winner == 'HUMAN':
            pygame.draw.rect(DISPLAYSURF, BLACK , ( 10, 10, 120, 45),2)
        elif winner == 'CPU':
            pygame.draw.rect(DISPLAYSURF, BLACK, (DISPLAY_WIDTH - 140, 10, 120, 45), 2)

def startGameAnimation():
    DISPLAYSURF.fill(BLACK)
    pygame.time.wait(2000)
    fontObj = pygame.font.Font('freesansbold.ttf', 40)
    textSurfaceObj1 = fontObj.render('Welcome To Rock Paper and Scissors', True, YELLOW)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
    pygame.display.update()
    pygame.time.wait(2000)
    textSurfaceObj2 = fontObj.render('Prepare to Test Your Luck!', True, YELLOW)
    textRectObj2 = textSurfaceObj1.get_rect()
    textRectObj2.center = (DISPLAY_WIDTH / 2 + 80, DISPLAY_HEIGHT / 2 + 50)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    pygame.time.wait(2200)



def endGameAnimation():
    '''This function performs the endgame animation'''
    global DISPLAYSURF,HUMANCOUNT,CPUCOUNT
    DISPLAYSURF.fill(BLACK)
    fontObj = pygame.font.Font('freesansbold.ttf', 50)

    if(HUMANCOUNT==5):
        pygame.time.wait(500)
        textSurfaceObj1 = fontObj.render('CONGRATULATIONS!!!', True, YELLOW)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (DISPLAY_WIDTH/ 2, DISPLAY_HEIGHT/2)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)

        textSurfaceObj2 = fontObj.render('You Won! :)', True, YELLOW)
        textRectObj2 = textSurfaceObj1.get_rect()
        textRectObj2.center = (DISPLAY_WIDTH/ 2+60, DISPLAY_HEIGHT/2+60)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        pygame.time.wait(2500)
        os.chdir(originalpath)
        pygame.quit()
        os.system('python MAINMENU.py')
        sys.exit()


    elif CPUCOUNT==5:
        pygame.time.wait(500)
        textSurfaceObj1 = fontObj.render('HARD LUCK!!!', True, YELLOW)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        textSurfaceObj2 = fontObj.render('You Lost! :(', True, YELLOW)
        textRectObj2 = textSurfaceObj1.get_rect()
        textRectObj2.center = (DISPLAY_WIDTH /2+20, DISPLAY_HEIGHT / 2 + 50)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
        pygame.display.update()
        pygame.time.wait(2800)
        os.chdir(originalpath)
        pygame.quit()
        os.system('python MAINMENU.py')
        sys.exit()








def drawFont():
    '''A function to draw all the text elements on to the screen directly'''
    global CPUCOUNT,HUMANCOUNT,wasScoreChanged
    fontObj = pygame.font.Font('freesansbold.ttf', 30)
    fontObj1 = pygame.font.Font('freesansbold.ttf', 45)
    fontObj2 = pygame.font.Font('freesansbold.ttf', 25)


    textSurfaceObj1 = fontObj.render('HUMAN', True, YELLOW)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (LeftBoxX + BOXWIDTH / 2, LeftBoxY + BOXHEIGHT + 40)
    DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)

    textSurfaceObj2 = fontObj.render('CPU', True, YELLOW)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (RightBoxX + BOXWIDTH / 2, RightBoxY + BOXHEIGHT + 40)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)

    textSurfaceObj3 = fontObj1.render('VS', True, YELLOW)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = (LeftBoxX + BOXWIDTH + 80, RightBoxY + BOXHEIGHT / 2)
    DISPLAYSURF.blit(textSurfaceObj3, textRectObj3)

    textSurfaceObj4 = fontObj2.render('Score: ' + str(HUMANCOUNT), True, YELLOW)
    textRectObj4 = textSurfaceObj4.get_rect()
    textRectObj4.center = (70, 30)
    DISPLAYSURF.blit(textSurfaceObj4, textRectObj4)

    textSurfaceObj5 = fontObj2.render('Score: ' + str(CPUCOUNT), True, YELLOW)
    textRectObj5 = textSurfaceObj5.get_rect()
    textRectObj5.center = (DISPLAY_WIDTH - 80, 30)
    DISPLAYSURF.blit(textSurfaceObj5, textRectObj5)


if __name__ == '__main__':
    main()


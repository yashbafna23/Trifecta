import os,sys,pygame,random
from pygame.locals import *

orignalpath = os.getcwd()
pathtoResourcefolder = os.path.abspath(r'WAM Resources')
os.chdir(pathtoResourcefolder)

#TODO : ADD SOUNDS EFFECTS- MOLE POP SOUND , MOLE KILLED SOUND  , BACKGROUND MUSIC ,etc
#TODO : WRITE A startgameanimation() function just like the endgameanimation function for intro
#TODO : CREATE A FUNCTION TO HIGHTLIGHT THE SCORES(MISSES AND SCORE COUNT) WHEN IT IS CHANGED>
#TODO : CREATE A MUSIC TURN AND OFF BUTTON IF POSSIBLE
#TODO : FIND A WAY TO REPLACE THE MOUSE POINTER WITH SOME KIND OF A HAMMER OR SMASHING OBJECT
#TODO : MAITAIN A HIGHSORE COUNT and display it ,(USE SHELVE FILE TO MAITAIN HIGHSCORE)

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

misses = 0     #NUMBER OF MOLES WHO ESCAPED
score = 0      # TO KEEP A TRACK OF THE SCORE OF THE PLAYER


mousex , mousey = 0 , 0
isMolekilled = False
wasMouseclicked = False

YELLOW = (255, 255, 0)
BLACK = (0,0,0)
OCHRE = (179, 143, 0)
GREEN = (45, 134, 45)
BROWN = (128, 60, 0)

listOfHoles = [(i,j)for j in range(80,400,100) for i in range(150,600,100)]  #LIST OF HOLES
#print(listOfHoles)

FPS = 100

BACKGROUNCOLOR  = GREEN
currentMoleCoordinates = random.choice(listOfHoles) # SELECT A COORDINATES FOR A MOLE


molePopTime = 150                #TIME FOR WHICH THE MOLE WILL POP UP AND STAY UP.THIS TIME WILL EVENTUALLY GO ON DECREASING!!
waitTime  =   25                 #TIME BETWEEN ONE MOLE GOING IN AND ANOTHER COMING UP
timeRemaining = molePopTime      #TIMEREMAINING TO KILL THE MOLE


def main():
    global DISPLAYSURF , MoleImg ,FPS ,FPSCLOCK , molePopTime,waitTime,timeRemaining,currentMoleCoordinates
    global mousex,mousey,isMolekilled,score,misses,wasMouseclicked,moleSound

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 50)
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    FPSCLOCK = pygame.time.Clock()

    pygame.display.set_caption('WHACK A MOLE GAME')
    pygame.mixer.music.load("WAMmusic.mp3")
    pygame.mixer.music.play(-1,0.0)      #Play sound

    moleSound = pygame.mixer.Sound("S1.wav")


    #SETUP THE IMAGE
    MoleImg = pygame.image.load('mole1.png')
    MoleImg = pygame.transform.scale(MoleImg, (70, 50))
    startGameAnimation()

    while True and misses <=4 :  #MAX 5 misses allowed
        isMolekilled = False
        for event in pygame.event.get():
            if event.type == QUIT: #QUIT CONDITION
                os.chdir(orignalpath)
                pygame.quit()
                os.system('python  MAINMENU.py')
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mousex, mousey = event.pos
                isMolekilled = detectMolekill(currentMoleCoordinates,mousex,mousey)


        DISPLAYSURF.fill(BACKGROUNCOLOR)

        if isMolekilled and timeRemaining>0:
            score=score+1
            currentMoleCoordinates = random.choice(listOfHoles)
            waitFor(40)
            molePopTime -= 2                  #Molepoptime will go on decreasing!!
            timeRemaining = molePopTime

        elif timeRemaining<=0:
            misses +=1
            currentMoleCoordinates = random.choice(listOfHoles)
            waitFor(40)
            molePopTime -= 2           #Molepoptime will go on decreasing!!
            timeRemaining = molePopTime
        else:
            timeRemaining-=1

        drawMoleHoles()

        missesDisplay(misses)
        scoreDisplay(score)
        displayMoleImg(currentMoleCoordinates)

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    #End of main loop
    endGameAnimation()

    #OPEN UP MENU AGAIN
    os.chdir(orignalpath)
    pygame.quit()
    os.system('python MAINMENU.py')
    sys.exit()

def scoreDisplay(currentscore):
    '''Draws the mole holes to the screen'''
    global DISPLAYSURF
    pygame.font.init()
    myfont = pygame.font.SysFont('Free Sans Bold', 40)
    textSurface = myfont.render('SCORE:' + str(currentscore), False, (0, 0, 0))
    DISPLAYSURF.blit(textSurface, (15, 5))


def missesDisplay(currentmisses):
    '''Draws the mole holes to the screen'''
    global DISPLAYSURF
    pygame.font.init()
    myfont = pygame.font.SysFont('Free Sans Bold', 40)
    textSurface = myfont.render('MISSES:' + str(currentmisses), False, (0, 0, 0))
    DISPLAYSURF.blit(textSurface, (DISPLAY_WIDTH-160, 5))


def displayMoleImg(Coordinates):
    '''Co-ordinates is a tuple of Moles.Draws the mole on the screen. '''
    DISPLAYSURF.blit(MoleImg,Coordinates )


def drawMoleHoles():
    '''DRAWS OUT ALL MOLE HOLES TO THE SCREEN'''
    global DISPLAYSURF
    pygame.draw.rect(DISPLAYSURF, OCHRE, (50, 50, 700, 500), 3)
    for point in listOfHoles:
        pygame.draw.ellipse(DISPLAYSURF, BROWN, (point[0], point[1]+20 ,70, 35))


def waitFor(timeInmilliSecs):
    '''Makes the window wait for those many miliseconds'''
    global DISPLAUSURF,FPSCLOCK,FPS,misses
    while timeInmilliSecs>=0:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT CONDITION
                pygame.quit()
                sys.exit()
        DISPLAYSURF.fill(BACKGROUNCOLOR)
        drawMoleHoles()
        missesDisplay(misses)
        scoreDisplay(score)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        timeInmilliSecs = timeInmilliSecs-1

def waitwithCurrentScreen(timeInmilliSecs):
    '''A WAIT FUNCTION'''
    while timeInmilliSecs>=0:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT CONDITION
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        timeInmilliSecs = timeInmilliSecs-1


def detectMolekill(Coordinates,mousex,mousey):
    '''CHECK IF THE MOLE HAS BEEN KILLED.RETURNS TRUE IF THE MOLE WAS KILLED'''
    moleRect1 = pygame.Rect(Coordinates[0]+14, Coordinates[1]+2, 40, 18)
    moleRect2 = pygame.Rect(Coordinates[0], Coordinates[1]+20, 70, 33)
    if moleRect1.collidepoint(mousex, mousey) or moleRect2.collidepoint(mousex,mousey):
        return True
    else:
        return False
def startGameAnimation():
    DISPLAYSURF.fill(BLACK)
    waitwithCurrentScreen(200)
    fontObj = pygame.font.Font('freesansbold.ttf', 40)
    textSurfaceObj1 = fontObj.render('Welcome To Whack A Mole Game', True, YELLOW)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
    DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
    pygame.display.update()
    waitwithCurrentScreen(200)
    textSurfaceObj2 = fontObj.render('You have got 5 misses!', True, YELLOW)
    textRectObj2 = textSurfaceObj1.get_rect()
    textRectObj2.center = (DISPLAY_WIDTH / 2 + 80, DISPLAY_HEIGHT / 2 + 50)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    pygame.display.update()
    waitwithCurrentScreen(220)

def endGameAnimation():
    '''PLAYS THE ENDGAME ANIMATION'''
    DISPLAYSURF.fill(BLACK)
    pygame.display.update()
    waitwithCurrentScreen(100)

    DISPLAYSURF.fill(BLACK)
    fontObj = pygame.font.Font('freesansbold.ttf', 50)

    moleSound.play()

    textSurfaceObj1 = fontObj.render('HARD LUCK!!!', True, YELLOW)
    textRectObj1 = textSurfaceObj1.get_rect()
    textRectObj1.center = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2-60)
    DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
    waitwithCurrentScreen(100)


    textSurfaceObj2 = fontObj.render('Game Over :(', True, YELLOW)
    textRectObj2 = textSurfaceObj1.get_rect()
    textRectObj2.center = (DISPLAY_WIDTH / 2 , DISPLAY_HEIGHT / 2 + 20)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    waitwithCurrentScreen(100)

    textSurfaceObj2 = fontObj.render('Your score :'+str(score), True, YELLOW)
    textRectObj2 = textSurfaceObj1.get_rect()
    textRectObj2.center = (DISPLAY_WIDTH / 2 , DISPLAY_HEIGHT / 2 + 90)
    DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
    waitwithCurrentScreen(400)

    DISPLAYSURF.fill(BLACK)
    pygame.display.update()


if __name__ == '__main__':
    main()

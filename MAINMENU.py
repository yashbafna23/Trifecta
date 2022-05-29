import os,sys,pygame,random
from pygame.locals import *

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

mousex , mousey = 0 , 0
FPS = 100

BLACK   = (  0,   0,   0)

TIMEFORINTRO = 200

def main():
    global DISPLAYSURF ,mousex , mousey ,FPS,FPSCLOCK,FirstImg,SecondImg,boxRect1,boxRect2,boxRect3,boxQuit
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (300, 50)
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    FPSCLOCK = pygame.time.Clock()

    pygame.display.set_caption('Trifecta')
    pygame.mixer.music.load("BackGround.mp3")
    pygame.mixer.music.play(-1,0.0)

    #SETUP THE IMAGE
    FirstImg = pygame.image.load('Trifecta1.png')
    SecondImg = pygame.image.load('Trifecta2.png')

    #DISPLAYING FIRST IMAGE
    drawImg(FirstImg)
    waitwithCurrentScreen(500)

    #BLACKSCREEN PAUSE
    DISPLAYSURF.fill(BLACK)
    waitwithCurrentScreen(100)


    #DISPLAY BOX RECT OBJECTS FOR ALL THE OBJECTS
    boxRect1 = pygame.Rect(245,160,270,76)
    boxRect2 = pygame.Rect(245,263,270,72)
    boxRect3 = pygame.Rect(245,365,270,75)
    boxQuit = pygame.Rect(620,535,157,45)

    #print(boxRect1.topleft)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT CONDITION
                pygame.quit()
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            if event.type == MOUSEBUTTONUP and event.button == 1:
                mousex, mousey = event.pos

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mousex, mousey = event.pos
                action = detectMouseposition(mousex,mousey)
                if action==4:
                    pygame.quit()
                    sys.exit()
                if action!=0:
                    runGames(action)


        #print(mousex,mousey)
        drawImg(SecondImg)
        detectMouseposition(mousex,mousey)

        pygame.display.update()
        FPSCLOCK.tick(FPS)



def drawImg(Img):
    DISPLAYSURF.blit(Img , (0,0) )


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


def detectMouseposition(mousex,mousey):
    global boxRect1,boxRect2,boxRect3,DISPLAYSURF,boxQuit
    if boxRect1.collidepoint(mousex, mousey):
        x,y = boxRect1.topleft
        pygame.draw.rect(DISPLAYSURF,BLACK,(x-3,y-3,279,84),3)
        return 1
    elif boxRect2.collidepoint(mousex, mousey):
        x,y = boxRect2.topleft
        pygame.draw.rect(DISPLAYSURF,BLACK,(x-2,y-4,279,84),3)
        return 2
    elif boxRect3.collidepoint(mousex,mousey):
        x,y = boxRect3.topleft
        pygame.draw.rect(DISPLAYSURF,BLACK,(x-3,y-5,280,84),3)
        return 3
    elif boxQuit.collidepoint(mousex,mousey):
        x,y = boxQuit.topleft
        pygame.draw.rect(DISPLAYSURF,BLACK,(x-4,y-5,165,54),3)
        return 4
    else:
        return 0


def runGames(gameno):
    if gameno==1:
        pygame.quit()
        os.system('python CHESS4.py')
        sys.exit()

    elif gameno==2:
        pygame.quit()
        os.system('python RPSFINAL.py')
        sys.exit()

    elif gameno==3:
        pygame.quit()
        os.system('python WAM1.1.py')
        sys.exit()


if __name__ == '__main__':
    main()
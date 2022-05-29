'''
This is a chess game..Code without rotation....
'''

import pygame , sys , os ,chess,time,pyperclip,Pieceselection,Savingpgn
from pygame.locals import *

# Path to detect the folder where all the PGN files are stored
currentPath = os.getcwd()
pathtoPgnFolder = os.path.abspath(r'ChessResources\PGN')
pathtoResourcefolder = os.path.abspath(r'ChessResources')

os.chdir(pathtoResourcefolder )

# TODO: Allow the user to enter their player name in the beginning of the game and display them on board
# TODO: Provide help option
# TODO: Provide colors option on the main menu
# TODO : Create a setup file to install the games

FPS = 50                                # frames per second, the general speed of the program

BOXSIZE = 65                             #Specify the box-size of each square
MARGIN  = 80                             #ALL THE SIDE MAGRINS AROUND THE CHESSBOARD
EXTRAWIDTH = 230                         #EXTRAWIDTH TO BE DISPLAYED ON THE RIGHT HAND SID

TOTAL_SIZE = BOXSIZE * 8 + 2*MARGIN      #Calculate the total size of the screen required

fontsize = 15                            #Font for printing the chess co-ordiantes on the side of board

mousex , mousey = 0 ,0                   #keeps current x and y co-ordinates of mouse
#            R    G    B
GRAY     = (100, 100, 100)
DARKGRAY = ( 77,  77,  51)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
LEAFGREEN= (  0,  51,   0)
OLIVEGREEN=(134, 179,   0)
TURQUOISE =(  0, 102, 102)
BLUE     = (  0,   0, 255)
LIGHTBLUE =(  0, 128, 128)
OCHRE    = (179, 143,   0)
DEEPBLUE = ( 19,  38,  58)
DARKPURPLE=( 51,  51,  77)
BRIGHTGREEN=(136,255,  77)
BROWN    = (128,  64,   0)
BLACK    = (  0,   0,   0)
MAROON   = ( 51,  20,   0)
BABYPINK = ( 255,128, 223)
LEMONYELLOW=(255, 255, 26)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
DARKORANGE=(204,  82,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
DARKGREEN= ( 45, 134,  45)
DARKBLUE = ( 15,  15,  62)

BGCOLOR = DEEPBLUE

board =chess.Board()                  #Create and initialize the virtual board

pyperclip.copy(board.fen(promoted=chess.QUEEN))
#chess.WHITE = True
#chess.BLACK = False



currentBoard = []              #Saves the current position of the board
listOfMoves = []

firstClickedSquareName, destinationSquareName = None, None
firstSquareNo , destinationSquareNo = None, None
isMouseClicked = False                #Has the mouse been clicked?
isUndoButtonClicked = False
xIndex, yIndex = -1, -1               #Saves the x-y indices of the first selected piece on the board
xdest ,ydest =-1 ,-1                  #Saves the x-y indices of the destination square of the selected piece on
promoteTo=None                        #Saves the promoted piece type
wasMoveMade = False                   #Tells if a move was made in the previous iteration of the game loop


wantMusic =True                       #Tells if user wants backgrond music
iconx = TOTAL_SIZE + EXTRAWIDTH - 70  #x-cordinate of music Icon
icony = 20                            #y-coodinate of music Icon


listOfFiles  = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
listOfRanks  = ('1','2','3','4','5','6','7','8')
listOfPieces = ('King','Knight','Pawn','Rook','Queen')
listOfColors = ('Black','White')

dictofPieces={'r':'BlackRook'   ,    'R':'WhiteRook',
              'p':'BlackPawn'   ,    'P':'WhitePawn',
              'n':'BlackKnight' ,    'N':'WhiteKnight',
              'b':'BlackBishop' ,    'B':'WhiteBishop',
              'k':'BlackKing'   ,    'K':'WhiteKing',
              'q':'BlackQueen'  ,    'Q':'WhiteQueen'
              }

def main():
    global DISPLAYSURF ,FPSCLOCK ,mousex ,mousey ,isMouseClicked ,xIndex ,yIndex ,firstClickedSquareName
    global firstSquareNo,destinationSquareName,promoteTo ,wasMoveMade,wantMusic,xdest,ydest,destinationSquareNo
    global  isUndoButtonClicked,board
    x1 = 200
    y1 = 30
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x1, y1)
    pygame.init()

    DISPLAYSURF = pygame.display.set_mode((TOTAL_SIZE+EXTRAWIDTH, TOTAL_SIZE))


    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('CHESS GAME')
    startGameAnimation()

    pygame.mixer.music.load("BackSound1.mp3")
    pygame.mixer.music.play(-1,0.0)
    pieceSound = pygame.mixer.Sound("pieceSound.wav")

    while True:                                 # Main loop
        if wasMoveMade:                         #If a move was maade in the previous instruction
            pieceSound.play()
            wasMoveMade = False
            pygame.time.wait(500)

        endGameAnimation()
        updatecurrentboard()

        drawEverything()

        for event in pygame.event.get():                           #Event Handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                os.chdir(currentPath)
                pygame.quit()
                os.system('python MAINMENU.py')
                sys.exit()
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            if event.type == MOUSEBUTTONUP:
                mousex , mousey = event.pos
                isMouseClicked=False


                if isUndoButtonClicked:
                    try:
                        board.pop()
                        if listOfMoves:
                            listOfMoves.pop()
                    except:
                        pass
                    isUndoButtonClicked=False

                #If a piece was selected and a destination square was chosen
                if firstClickedSquareName !=None and isMouseOnSquare(mousex,mousey):
                    xdest,ydest,destinationSquareNo,destinationSquareName =getBoxInfo(mousex,mousey)

                    #Handling promotion case!!!
                    if board.turn and currentBoard[7 - yIndex][xIndex] == 'P' and yIndex==6 and ydest == 7:
                        promoteTo = Pieceselection.choosepiece()
                    elif not board.turn and currentBoard[7-yIndex][xIndex] == 'p' and yIndex==1 and ydest == 0:
                        promoteTo =  Pieceselection.choosepiece()

                    #Generate the Move here
                    movestring = str(firstClickedSquareName)+str(destinationSquareName)
                    move = chess.Move(firstSquareNo, destinationSquareNo,promotion=promoteTo)

                    #Check if the move is legal
                    if move in board.legal_moves:
                        #Create illusion of piece going to destination Square
                        updatecurrentboard()
                        drawEverything()
                        wasMoveMade = True
                        listOfMoves.append( chess.Move.from_uci(movestring) )
                        board.push_san(board.san(move) )          #Make the move!!!

                xIndex, yIndex, firstSquareNo, firstClickedSquareName = -1, -1, None, None
                xdest, ydest, destinationSquareNo, destinationSquareName = -1,-1,None,None
                promoteTo=None

            if event.type == MOUSEBUTTONDOWN:
                mousex , mousey = event.pos
                isMouseClicked=True
                if isMouseOnSquare(mousex,mousey) and firstClickedSquareName==None:
                    xIndex,yIndex,firstSquareNo,firstClickedSquareName = getBoxInfo(mousex,mousey)
                elif (iconx<=mousex<=iconx+60 and icony<=mousey<=icony+60 ): #If mouse is on Music Option
                    wantMusic = not wantMusic

        pygame.display.update()
        FPSCLOCK.tick(FPS)
#End of main function

#Drawing Fucntions
def drawCoordinates():
    #Functions which will draw the co-ordiates to the screen from current  perspective
    fontObj = pygame.font.Font('freesansbold.ttf', fontsize)

    # For printing out ranks.. 1,2,3.
    X = int(MARGIN / 2) + int(MARGIN/3)

    for i in range(8):

        index = 8 - i - 1

        textSurfaceObj = fontObj.render(listOfRanks[index], True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        Y = (i) * BOXSIZE + MARGIN + int(BOXSIZE / 2)
        textRectObj.center = (X, Y)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

    # For printing out filenames
    Y = TOTAL_SIZE - int(MARGIN / 2)-int(MARGIN/3)
    for i in range(8):
        index=i
        textSurfaceObj = fontObj.render(listOfFiles[index], True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        X = i * BOXSIZE + MARGIN + int(BOXSIZE / 2)
        textRectObj.center = (X, Y)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
def drawboard():

    #Draws out the entire board to the window depending upon what is the current turn(board.turn)
    DISPLAYSURF.fill(BGCOLOR)          #BACKGROUND COLOR
    color = DARKGREEN


    for row in range(8):
        X = MARGIN + row * BOXSIZE
        for column in range(8):
            if color == DARKGREEN:
                color = WHITE
            else:
                color = DARKGREEN

            Y = MARGIN + column * BOXSIZE
            boardSqrObj = pygame.Rect(X, Y, BOXSIZE, BOXSIZE)     # (X,Y) is the topleft corner of the board do be drawn
            pygame.draw.rect(DISPLAYSURF, color, boardSqrObj)
        if color == DARKGREEN:
            color = WHITE
        else:
            color = DARKGREEN
def showMouseCoordinates(x,y):
    #Displays the mouse co-ordinates onto the screen.
    fontObj = pygame.font.Font('freesansbold.ttf',20)
    textSurfaceObj = fontObj.render('MouseC:'+str(x)+' , '+str(y) , True ,YELLOW)

    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (720,50)
    DISPLAYSURF.blit(textSurfaceObj,textRectObj)
def showBoxCoordinates(x,y):
    #Displays the chesss Square co-ordinates
        xindex , yindex = boxIndices(x,y)
        currentSqrNumber=chess.square(xindex,yindex)
        nameOfSqr=chess.SQUARE_NAMES[currentSqrNumber]
        indexText = '('+str(xindex)+' '+str(yindex)+')'
        text1='ChessSquare:' + str(currentSqrNumber) + '  ' +  nameOfSqr+'  '+indexText
        fontObj2 = pygame.font.Font('freesansbold.ttf', 20)
        textSurfaceObj2 = fontObj2.render(text1, True, YELLOW)
        textRectObj2 = textSurfaceObj2.get_rect()
        textRectObj2.center = (740, 150)
        DISPLAYSURF.blit(textSurfaceObj2, textRectObj2)
def drawpieces():
    #Draws the pieces in the currentBoard list to the board
    global DISPLAYSURF,destinationSquareNo,xdest,ydest
    selectedpiecei,selectedpiecek=None,None
    for i in range(8):
        for k in range(8):
            if ( (7-i)!=yIndex or k!=xIndex) and currentBoard[i][k] != '.':

                x = k*BOXSIZE + MARGIN
                y = i *BOXSIZE+MARGIN
                imgname = dictofPieces[currentBoard[i][k]] + '.png'
                imgSurfObj = pygame.image.load(imgname)
                DISPLAYSURF.blit(imgSurfObj, (x, y))
            elif (currentBoard[i][k] != '.') : #Drawing the selected piece near the mouse pointer
                selectedpiecei=i
                selectedpiecek=k
                continue

    if selectedpiecei!=None and xdest==-1:
        imgx = int(mousex - 30)
        imgy = int(mousey - 30)
        imgname1 = dictofPieces[currentBoard[selectedpiecei][selectedpiecek]] + '.png'
        imgSurfObj = pygame.image.load(imgname1)
        DISPLAYSURF.blit(imgSurfObj, (imgx, imgy))


    elif selectedpiecei!=None and xdest!=-1:
        # if board.turn:
        imgx=MARGIN+xdest*BOXSIZE
        imgy = MARGIN + (7 - ydest) * BOXSIZE
        # else:
        #
        #     imgx = MARGIN + (7-xdest) * BOXSIZE
        #     imgy = MARGIN + ydest * BOXSIZE
        imgname1 = dictofPieces[currentBoard[selectedpiecei][selectedpiecek]] + '.png'
        imgSurfObj = pygame.image.load(imgname1)
        DISPLAYSURF.blit(imgSurfObj, (imgx, imgy))
def drawwhosemove():
    #Displays whose move it is at the top
    if board.turn:
        text = 'White'  #White to move
    else:
        text = 'Black'
    text = text + ' to move'
    fontObj = pygame.font.Font('freesansbold.ttf', 20)
    textSurfaceObj = fontObj.render(text, True, YELLOW)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (340,30)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
def drawMusicIcon():
    #Draws the Music Icon on the Screen
    global wantMusic
    if wantMusic:
        musicIcon = pygame.image.load('MusicOff.png')
        pygame.mixer.music.unpause()
    else:
        musicIcon = pygame.image.load('MusicOn.png')
        pygame.mixer.music.pause()

    musicIcon=pygame.transform.scale(musicIcon,(60,60))
    DISPLAYSURF.blit(musicIcon, (iconx, icony))
    if(iconx<=mousex<=iconx+60 and icony<=mousey<=icony+60 ):    # if mouse is on music icon
        boxRect = pygame.Rect(iconx - 5, icony - 5, 65, 65)
        pygame.draw.rect(DISPLAYSURF, WHITE, boxRect, 1)         #Draw the Outer Rectangle
def drawUndoButton():
    global DISPLAYSURF , isUndoButtonClicked,firstClickedSquareName,listOfMoves
    if isMouseClicked and isMouseOnUndoButton() and firstClickedSquareName==None:
        pygame.draw.rect(DISPLAYSURF,BRIGHTGREEN , (TOTAL_SIZE + 45, 495, 160, 60),2)
        buttoncolor = LIGHTBLUE
        isUndoButtonClicked =True
    elif isMouseOnUndoButton():
        buttoncolor = LIGHTBLUE
    else:
        buttoncolor = TURQUOISE
    text='UNDO'
    fontObj = pygame.font.Font('freesansbold.ttf', 30)
    textSurfaceObj = fontObj.render(text, True, OCHRE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (TOTAL_SIZE+125,525)
    pygame.draw.rect(DISPLAYSURF,buttoncolor,(TOTAL_SIZE+50,500,150,50))
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)

def drawEverything():
    drawboard()
    drawpieces()
    drawUndoButton()
    drawCoordinates()
    drawwhosemove()
    drawMusicIcon()
    '''showMouseCoordinates(mousex, mousey)  # To be removed later on
    if isMouseOnSquare(mousex, mousey):  # Just for displaying board square coordinates
        showBoxCoordinates(mousex, mousey)'''


#Utility Functions
def isMouseOnSquare(x,y):
    #Returns False if mouse is not present in chessboard else returns True
    if x > MARGIN and x < (MARGIN+8*BOXSIZE):
        if(y>MARGIN and y< (MARGIN+8*BOXSIZE)):
            return True
    return False

def updatecurrentboard():
    #Updates the current state of the currentBoard list
    global currentBoard
    listOfBoard = list(str(board).split('\n'))
    for i in range(len(listOfBoard)):
        listOfBoard[i] = listOfBoard[i].split(' ')
    currentBoard = listOfBoard
    pyperclip.copy(board.fen(promoted=chess.QUEEN))

def getBoxInfo(x,y):
    #returns BoardIndices , currentSquareNo and nameOfSqr
    xindex, yindex = boxIndices(x, y)
    currentSqrNumber = chess.square(xindex, yindex)
    nameOfSqr = chess.SQUARE_NAMES[currentSqrNumber]
    return xindex,yindex,currentSqrNumber,nameOfSqr

def boxIndices(x,y):
    #Convert Mouse co-ordinates to chesssquare indices depending on the players' turn
    xindex = int((x - MARGIN) / BOXSIZE)
    yindex = 7 - int((y - MARGIN) / BOXSIZE)
    return xindex, yindex

def isMouseOnUndoButton():
    if (TOTAL_SIZE+50)<=mousex<=(TOTAL_SIZE+200) and 500<=mousey<=550:
        return True
    else:
        return False



#Start and EndGame animations
def startGameAnimation():
    global DISPLAYSURF

    img1=pygame.image.load('backgroundimg1.png')
    img2=pygame.image.load('Chess2.png')
    img3 = pygame.image.load('Chess4.png')

    img1 = pygame.transform.scale(img1, (TOTAL_SIZE+EXTRAWIDTH-30, TOTAL_SIZE-30) )
    img2 = pygame.transform.scale(img2, (TOTAL_SIZE+EXTRAWIDTH-30, TOTAL_SIZE-30) )
    img3 = pygame.transform.scale(img3, (TOTAL_SIZE + EXTRAWIDTH - 30, TOTAL_SIZE - 30))

    DISPLAYSURF.fill(GRAY)
    DISPLAYSURF.blit(img1,(15,15))
    pygame.display.flip()
    waitwithCurrentScreen(400)

    DISPLAYSURF.fill(BLACK)
    pygame.display.flip()
    waitwithCurrentScreen(200)

    DISPLAYSURF.fill(GRAY)
    DISPLAYSURF.blit(img2,(15,15))
    pygame.display.flip()
    waitwithCurrentScreen(400)

    DISPLAYSURF.fill(BLACK)
    pygame.display.flip()
    waitwithCurrentScreen(200)

    DISPLAYSURF.fill(GRAY)
    DISPLAYSURF.blit(img3, (15, 15))
    pygame.display.flip()
    waitwithCurrentScreen(400)

    DISPLAYSURF.fill(BLACK)
    pygame.display.flip()
    waitwithCurrentScreen(200)

def endGameAnimation():
    if board.is_checkmate():
        pygame.mixer.music.pause()
        if board.turn:
            text1='Black Wins!'
        else:
            text1='White Wins!'

        text2 = 'Checkmate!!'
        waitwithCurrentScreen(150)
        midx = (TOTAL_SIZE + EXTRAWIDTH) // 2
        midy = TOTAL_SIZE // 2 - 50
        DISPLAYSURF.fill(DARKPURPLE)
        fontObj = pygame.font.Font('freesansbold.ttf', 80)

        textSurfaceObj = fontObj.render(text1, True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (midx, midy+50)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

        fontObj1 = pygame.font.Font('freesansbold.ttf', 50)
        textSurfaceObj1 = fontObj1.render(text2, True, YELLOW)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (midx, midy - 100)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)

        pygame.display.flip()
        waitwithCurrentScreen(300)
        displayThankforplaying()

    elif board.is_stalemate():
        pygame.mixer.music.pause()
        DISPLAYSURF.fill(DARKPURPLE)
        midx = (TOTAL_SIZE + EXTRAWIDTH) // 2
        midy = TOTAL_SIZE // 2 - 50
        waitwithCurrentScreen(50)
        text = 'It is a Draw!!'
        text2 = 'Stalemate!!'
        fontObj = pygame.font.Font('freesansbold.ttf', 70)
        textSurfaceObj = fontObj.render(text, True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (midx, midy + 50)

        fontObj1 = pygame.font.Font('freesansbold.ttf', 50)
        textSurfaceObj1 = fontObj1.render(text2, True, YELLOW)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (midx, midy - 100)

        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        pygame.display.flip()
        waitwithCurrentScreen(300)
        displayThankforplaying()

    elif board.is_insufficient_material():
        pygame.mixer.music.pause()
        DISPLAYSURF.fill(DARKPURPLE)
        midx = (TOTAL_SIZE + EXTRAWIDTH) // 2
        midy = TOTAL_SIZE // 2 - 50
        waitwithCurrentScreen(150)
        text = 'It is a Draw!!'
        text2 = 'Insufficent material!!'
        fontObj = pygame.font.Font('freesansbold.ttf', 70)
        textSurfaceObj = fontObj.render(text, True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (midx, midy + 50)

        fontObj1 = pygame.font.Font('freesansbold.ttf', 50)
        textSurfaceObj1 = fontObj1.render(text2, True, YELLOW)
        textRectObj1 = textSurfaceObj1.get_rect()
        textRectObj1.center = (midx, midy - 100)

        DISPLAYSURF.blit(textSurfaceObj, textRectObj)
        DISPLAYSURF.blit(textSurfaceObj1, textRectObj1)
        pygame.display.flip()
        waitwithCurrentScreen(300)
        displayThankforplaying()

def displayThankforplaying():
    DISPLAYSURF.fill(BLACK)
    pygame.display.flip()
    waitwithCurrentScreen(200)

    DISPLAYSURF.fill(DARKPURPLE)
    midx = (TOTAL_SIZE + EXTRAWIDTH) // 2
    midy = TOTAL_SIZE // 2 - 50
    text = 'Thanks For Playing!!'
    fontObj = pygame.font.Font('freesansbold.ttf', 70)
    textSurfaceObj = fontObj.render(text, True, YELLOW)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (midx, midy)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)
    pygame.display.flip()
    waitwithCurrentScreen(300)
    savePGN()

    os.chdir(currentPath)
    pygame.quit()
    os.system('python MAINMENU.py')
    sys.exit()


#Func for saving the pgn file
def savePGN():
    '''Saves the pgn to the PGN folder in ur resource folder'''
    board2 = chess.Board()
    pgntext = str(board2.variation_san([m for m in listOfMoves]) )
    Savingpgn.backupTo(pathtoPgnFolder , pgntext)

def waitwithCurrentScreen(timeInmilliSecs):
    '''A WAIT FUNCTION'''
    while timeInmilliSecs>=0:
        for event in pygame.event.get():
            if event.type == QUIT:  # QUIT CONDITION
                pygame.quit()
                sys.exit()
        pygame.display.update()
        FPSCLOCK.tick(100)
        timeInmilliSecs = timeInmilliSecs-1


if __name__ == '__main__' or __name__=='CHESS3':         #Eventually transfers the execution to the main() funciton..
    main()


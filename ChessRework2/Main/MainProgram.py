import BoardsetUp
import turtle 
import FileHandler
from inspect import currentframe, getframeinfo
import sys
cf = currentframe()
filename = getframeinfo(cf).filename
GameOver = False
Board, wn, Kl, Pieces,SquareSize,BoardSize = BoardsetUp.Run() 
if Kl[0] ==[0,0,"white"] or [0,0,"black"] == Kl[1]:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("One of the Kings could not be located in the config file. Please place the king on a square")))

AnimatedSquares = []
PPM =[]
Selected = [0,0]
Turn = "white"

WhiteKingMove = False
WhiteRookLongMove = False
WhiteRookShortMove = False

BlackKingMove = False
BlackRookLongMove = False
BlackRookShortMove = False

Castle = False

def changeTurn():
    global Turn
    if Turn == "white":
        Turn = "black"
    else:
        Turn = "white"
"""
=======================


=======================
Check and check mate
=======================
"""
def checkCheckMate():
    global Turn
    if Turn == "white":
        KingLocation = [Kl[0][0],Kl[0][1]]
    else: 
        KingLocation = [Kl[1][0],Kl[1][1]]
    KingMove = PossibleMoves(Board[Kl[0][0]][Kl[0][1]][1],KingLocation[0],KingLocation[1], "Mate")
    ePM = enemyPossibleMoves()
    toPop = []
    PiecesTakingKing = []
    for i in range(len(ePM)):
        for x in range(len(ePM[i][1])):
            if KingLocation == ePM[i][1][x]:
                PiecesTakingKing.append(ePM[i])
            for y in range(len(KingMove)):
                if ePM[i][1][x] == KingMove[y]:
                    toPop.append(KingMove[y])
    for i in range(len(toPop)):
        if toPop[i] in KingMove:
            KingMove.remove(toPop[i])
    toPop = []
    fPM = friendlyPossibleMoves()
    if len(KingMove) == 0 and len(PiecesTakingKing) >1:
        return True
    elif len(PiecesTakingKing) == 1:
        PTKCOORDS = PiecesTakingKing[0][0].getCoords()
        xx = -(PTKCOORDS[0]- KingLocation[0])
        yy = -(PTKCOORDS[1]- KingLocation[1]) 
        for x in range(len(PiecesTakingKing[0][1])):
            if (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] < 0 and not (xx < 0)) or (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] < 0 and not (yy < 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
            elif (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] == 0 and not (xx == 0)) or (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] == 0 and not (yy == 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
            elif (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] > 0 and not (xx > 0)) or (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] > 0 and not (yy > 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
        for i in range(len(toPop)):
            if toPop[i] in PiecesTakingKing[0][1]:
                PiecesTakingKing[0][1].remove(toPop[i])
        toPop = []
        PiecesTakingKing[0][1].pop(len(PiecesTakingKing[0][1])-1)
        LengthPieceTakingKing = len(PiecesTakingKing[0][1])
        for x in range(len(PiecesTakingKing[0][1])):
            for y in range(len(fPM)):
                for p in range(len(fPM[y][1])):
                    if fPM[y][1][p] == PiecesTakingKing[0][1][x] and fPM[y][0].getType() !="King":
                        toPop.append(PiecesTakingKing[0][1][x])
        for i in range(len(toPop)):
            if toPop[i] in PiecesTakingKing[0][1]:
                PiecesTakingKing[0][1].remove(toPop[i])
        if LengthPieceTakingKing != len(PiecesTakingKing[0][1]):
            PiecesTakingKing = []
        if len(KingMove) == 0 and len(PiecesTakingKing) > 0:
            return True
        else:
            return False
    else:
        return False
def checkCheck():
    global Turn
    check = False
    if Turn == "white":
        KingLocation = [Kl[0][0],Kl[0][1]]
    else: 
        KingLocation = [Kl[1][0],Kl[1][1]]
    PiecesTakingKing = []
    ePM = enemyPossibleMoves()
    for i in range(len(ePM)):
        for x in range(len(ePM[i][1])):
            if KingLocation == ePM[i][1][x]:
                PiecesTakingKing.append(ePM[i][1][x])
    if len(PiecesTakingKing) > 0:
        check = True
    return check
def enemyPossibleMoves():
    ePM = []
    for i in range(len(Pieces)):
        if Pieces[i].getColour() != Turn:
            Coords = Pieces[i].getCoords()
            ePM.append([Pieces[i], PossibleMoves(Pieces[i], Coords[0], Coords[1], False)])
    return ePM
def friendlyPossibleMoves():
    fPM = []
    for i in range(len(Pieces)):
        if Pieces[i].getColour() == Turn:
            Coords = Pieces[i].getCoords()
            fPM.append([Pieces[i], PossibleMoves(Pieces[i], Coords[0], Coords[1], "None")])
    return fPM  
"""
=======================


=======================
Moves the pieces
=======================
"""
def MovePiece(From,Too, InputBoard):
    global phantomPiece
    global WhiteKingMove
    global BlackKingMove
    global WhiteRookShortMove
    global WhiteRookLongMove
    global BlackRookLongMove
    global BlackRookShortMove
    global GameOver
    global blackPieces
    global whitePieces
    pawnPassPawn = False
    if Too == phantomPiece:
        pawnPassPawn = True
    phantomPiece = [-1,-1]
    if InputBoard[From[0]][From[1]][1] != "PPH":
        if InputBoard[From[0]][From[1]][1].getType() == "King":
            if InputBoard[From[0]][From[1]][1].getColour() == "white":
                Kl[0][0] = Too[0]
                Kl[0][1] = Too[1]
                WhiteKingMove = True
            else:
                Kl[1][0] = Too[0]
                Kl[1][1] = Too[1]
                BlackKingMove = True
        elif InputBoard[From[0]][From[1]][1].getType() == "Pawn" and abs(From[1]-Too[1]) == 2:
            if InputBoard[From[0]][From[1]][1].getColour() == "white":
                phantomPiece = [From[0],Too[1]-1]
            else:
                phantomPiece = [From[0],Too[1]+1] 
        elif InputBoard[From[0]][From[1]][1].getType() == "Rook":
            if InputBoard[From[0]][From[1]][1].getCoords() == [0,0]:
                WhiteRookShortMove = True
            elif InputBoard[From[0]][From[1]][1].getCoords() == [7,0]:
                WhiteRookLongMove = True
            elif InputBoard[From[0]][From[1]][1].getCoords() == [0,7]:         
                BlackRookShortMove = True
            elif InputBoard[From[0]][From[1]][1].getCoords() == [7,7]:
                BlackRookLongMove = True  
        toAdd = 0
        if pawnPassPawn == True:
            if InputBoard[From[0]][From[1]][1].getColour() == "white":
                toAdd = -1
            else:
                toAdd = 1
        PieceTaken = False
        TempPieceTaken = 'A'
        if InputBoard[Too[0]][Too[1]][1] == "PPH" and pawnPassPawn == False:
            InputBoard[From[0]][From[1]][1].getTurtle().goto((((Too[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))        
            InputBoard[From[0]][From[1]][1].setCoords(Too)
            InputBoard[Too[0]][Too[1]][1] = InputBoard[From[0]][From[1]][1]
            InputBoard[From[0]][From[1]][1] = "PPH"
        else:
            PieceTaken = True
            Pieces.remove(InputBoard[Too[0]][Too[1]+toAdd][1])
            InputBoard[From[0]][From[1]][1].setCoords(Too)
            TempPieceTaken = InputBoard[Too[0]][Too[1]+toAdd][1]
            InputBoard[Too[0]][Too[1]+toAdd][1].getTurtle().goto(-400,0)
            InputBoard[From[0]][From[1]][1].getTurtle().goto((((Too[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))   
            InputBoard[Too[0]][Too[1]+toAdd][1] = "PPH"   
            InputBoard[Too[0]][Too[1]][1] = InputBoard[From[0]][From[1]][1]
            InputBoard[From[0]][From[1]][1] = "PPH"
        wn.update()
        check = checkCheck() 
        if check == True:
            phantomPiece = Too
            penWrite("Attempted to move " + InputBoard[Too[0]][Too[1]][1].getName() + ": From: " + str(From) + ", Too: " + str(Too) + " However King is in check. Returning Pieces...","normal",penNormal) 
            phantomPiece = [-1,-1]
            if InputBoard[Too[0]][Too[1]][1].getType() == "King":
                if InputBoard[Too[0]][Too[1]][1].getColour() == "white":
                    Kl[0][0] = From[0]
                    Kl[0][1] = From[1]
                else:
                    Kl[1][0] = From[0]
                    Kl[1][1] = From[1]
            elif InputBoard[Too[0]][Too[1]][1].getType() == "Rook":
                if From == [0,0]:
                    WhiteRookShortMove = False
                elif From == [7,0]:
                    WhiteRookLongMove =  False
                elif From == [0,7]:         
                    BlackRookShortMove = False
                elif From == [7,7]:
                    BlackRookLongMove = False
            InputBoard[Too[0]][Too[1]][1].setCoords(From)
            InputBoard[Too[0]][Too[1]][1].getTurtle().goto((((From[0])*(SquareSize*2))-(SquareSize*6),(SquareSize*8)-(From[1]*(SquareSize*2))))        
            InputBoard[From[0]][From[1]][1] = InputBoard[Too[0]][Too[1]][1]
            InputBoard[Too[0]][Too[1]][1] = "PPH"
            if PieceTaken != False:
                Pieces.append(TempPieceTaken)
                Coords =TempPieceTaken.getCoords()
                TempPieceTaken.getTurtle().goto((((Coords[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Coords[1]*(SquareSize*2))))        
                InputBoard[Too[0]][Too[1]+toAdd][1] = TempPieceTaken
            wn.update()  
        else:
                    piece = InputBoard[Too[0]][Too[1]][1]
                    if piece.getType() == "Pawn":
                        if (piece.getColour() == "white" and Too[1] == 7) or (piece.getColour() == "black" and Too[1] == 0):
                            piece.setType("Queen", [[1.0, 0.0, 1.0],[0.0, 1.0, 1.0],[-1.0, 0.0, 1.0],[0.0, -1.0, 1.0],[1.0, 1.0, 1.0],[1.0, -1.0, 1.0],[-1.0, 1.0, 1.0],[-1.0, -1.0, 1.0]])
                            wn.update()
                    elif piece.getType() == "King" and abs(From[0]-Too[0]) == 2:
                        if From[0]-Too[0] == 2:
                            InputBoard[0][Too[1]][1].getTurtle().goto((((3)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))
                            InputBoard[0][Too[1]][1].setCoords([2,Too[1]])
                            InputBoard[2][Too[1]][1] = InputBoard[0][From[1]][1]
                            InputBoard[From[0]][From[1]][1] = "PPH"
                        else:
                            InputBoard[7][Too[1]][1].getTurtle().goto((((5)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))
                            InputBoard[7][Too[1]][1].setCoords([2,Too[1]])
                            InputBoard[4][Too[1]][1] = InputBoard[7][From[1]][1]
                            InputBoard[From[0]][From[1]][1] = "PPH"
                    if TempPieceTaken == "A":
                        penWrite(piece.getName() + ": From: " + str(From) + ", Too: " + str(Too),"normal",penNormal) 
                    else:
                        penWrite(piece.getName() + ": From: " + str(From) + ", Too: " + str(Too) + ", And took the piece " +TempPieceTaken.getName(),"normal",penNormal)                     
                    changeTurn()
                    if Turn == "black":
                        wn.bgcolor("darkgray")
                    else:
                        wn.bgcolor("lightgray")
                    penWrite("Turn: " + Turn,"Head",penHead) 
                    checkMate = checkCheckMate()
                    if checkMate == True:
                        penWrite("Check Mate","Head",penHead) 
                    wn.update()   


"""
=======================


=======================
Controls Animation of Squares
=======================
"""
def Animate(x,y, color):
    AnimatedSquares.append(Board[x][y][0])
    Board[x][y][0].getTurtle().color(color)
    wn.update()
def DeAnimate():
    for i in range(len(AnimatedSquares)):
        AnimatedSquares[i].setColour()
    wn.update()
"""
=======================


=======================
Works out possible Moves
=======================
"""
phantomPiece = [-1,-1]

def friendlyOnSquare(x,y):
    global Turn
    if Board[x][y][1] != "PPH":
        if Board[x][y][1].getColour() == Turn:
            return True
        else:
            return False
    else:
        return False
def enemyOnSquare(x,y):
    global Turn
    if Board[x][y][1] != "PPH":
        if Board[x][y][1].getColour() != Turn:
            return True
        else:
            return False
    else:
        return False
def PossibleMoves(piece,x,y, type):
    global phantomPiece
    global Turn
    pieceType = piece.getType()
    moves = piece.getMove()
    startingCoords = piece.getStartCoords()
    PM = []
    for i in range(len(moves)):
        xN = int(x +  moves[i][0])
        yN = int(y + moves[i][1])
        c = moves[i][2]
        if xN <= 7 and yN <= 7 and xN >= 0 and yN >=0:
            if Board[xN][yN][1] != "PPH":
                fOS = friendlyOnSquare(xN,yN)
                eOS = enemyOnSquare(xN,yN)
                nOS = False
            else:
                nOS = True
                fOS = False
                eOS = False
            if c == 0 and (fOS == False or type == False):
                if pieceType == "Knight" or pieceType == "King":
                    PM.append([xN,yN])
                    if pieceType == "King" and type != False and type != "Mate":
                        Short = False
                        Long = False
                        coords = piece.getCoords()
                        ePM = enemyPossibleMoves()
                        for p in range(len(ePM)):
                            for l in range(len(ePM[p][1])):
                                if [coords[0]-1,coords[1]] == ePM[p][1][l] or [coords[0]-2,coords[1]] == ePM[p][1][l]:
                                    Short = True
                                elif [coords[0]+1,coords[1]] == ePM[p][1][l] or [coords[0]+2,coords[1]] == ePM[p][1][l]:
                                    Long = True
                                elif  [coords[0],coords[1]] == ePM[p][1][l]:
                                    Long = True
                                    Short = True
                        if Turn == "white":
                            if WhiteRookLongMove == True:
                                Long = True
                            if WhiteRookShortMove == True:
                                Short = True
                        else:
                            if BlackRookLongMove == True:
                                Long = True
                            if BlackRookShortMove == True:
                                Short = True
                        if (WhiteKingMove == False and Turn == "white") or (BlackKingMove == False and Turn == "black"):
                            if Board[coords[0]-1][coords[1]][1] == "PPH" and Board[coords[0]-2][coords[1]][1] == "PPH" and Short == False:
                                PM.append([coords[0]-2,coords[1]])
                            if Board[coords[0]+1][coords[1]][1] == "PPH" and Board[coords[0]+2][coords[1]][1] == "PPH" and Board[coords[0]+3][coords[1]][1] == "PPH" and Long == False:
                                PM.append([coords[0]+2,coords[1]])

                elif type != "ePM" and eOS == False and type != False:
                    PM.append([xN,yN])
            elif c == 1:
                Blocked = False
                while xN <= 7 and yN <= 7 and xN >= 0 and yN >=0 and Blocked == False:
                    if Board[xN][yN][1] != "PPH":
                        fOS = friendlyOnSquare(xN,yN)
                        eOS = enemyOnSquare(xN,yN)
                        nOS = False
                    else:
                        nOS = True
                        fOS = False
                        eOS = False
                    if nOS == True:
                        PM.append([xN,yN])
                    elif fOS == True and type != False:
                        Blocked = True
                    elif eOS == True or type == False:
                        PM.append([xN,yN])
                        Blocked = True
                    xN = int(xN +  moves[i][0])
                    yN = int(yN +  moves[i][1])
            elif c == 2:
                if eOS == True or type == False:
                    PM.append([xN,yN])
                elif type == "ePM":
                    PM.append([xN,yN])
                elif phantomPiece != [-1,-1]:
                    if phantomPiece == [xN,yN]:
                        PM.append([xN,yN])
            elif c == 3:
                if pieceType == "Pawn":
                    if type != "ePM":  
                        if piece.getColour() == "white":
                            if nOS == True and y == 1 and enemyOnSquare(xN,yN-int(moves[i][1]/2)) == False and friendlyOnSquare(xN,yN -int(moves[i][1]/2)) == False and type != False:
                                PM.append([xN,yN])
                        else:
                            if nOS == True and y == 6 and enemyOnSquare(xN,yN-int(moves[i][1]/2)) == False and friendlyOnSquare(xN,yN -int(moves[i][1]/2)) == False and type != False:
                                PM.append([xN,yN]) 
                        
    return PM
"""
=======================


=======================
Save the current board
=======================
"""
def SaveBoard():
    saved = []
    for i in range(len(Pieces)):
        name  =  Pieces[i].getName() + ">"
        shape = Pieces[i].getType()
        colour = Pieces[i].getColour()
        coords = Pieces[i].getCoords()
        coords = str(coords[0]) + str(coords[1])
        moves = str(Pieces[i].getMove())
        moves = moves.replace("[[", "{[")
        moves = moves.replace("]]", "]}")
        moves = moves.replace("], [", "],[")
        saved.append([name,shape,colour,coords,moves])
    BoardsetUp.Save(saved)
"""
=======================


=======================
Runs When the board is clicked 
=======================
"""
penNormal = turtle.Turtle()
penHead = turtle.Turtle()
penNormal.penup()
penHead.penup()
penNormal.hideturtle()
penHead.hideturtle()
penNormal.hideturtle()
penHead.hideturtle()
saveButton = turtle.Turtle()
saveButton.penup()
saveButton.shape("square")
try:
    saveButton.shapesize((SquareSize)/40.0, (SquareSize)/40.0, SquareSize/32.0)
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root SqaureSize> was invalid. Please correct the error")))
    sys.exit()
saveButton.goto(SquareSize*11.6, SquareSize*0.8)
saveButton.write("Save", font=("Courier New", 15,"bold"))
saveButton.goto(SquareSize*12, 0)
saveButton.color("green")
wn.update()
FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Save Button has been created.")))
def ClearPen(pen):
    pen.undo()
def penWrite(Message, type, pen):
    ClearPen(pen)
    size = 15
    font = "normal"
    if type == "Head":
        size = 30
        font = "bold"
        pen.goto(-600, 250)
    elif type == "normal":
        pen.goto(-700, 200)
        if len(Message) > 40:
            for i in range(40):
                if Message[40-i] == " ":
                    Message = Message[:40-i] + "\n" +Message[41-i:]
                    break;
        if len(Message) > 80:
            for i in range(40):
                if Message[80-i] == " ":
                    Message = Message[:80-i] + "\n" +Message[81-i:]
                    break;
    pen.write(Message, font=("Courier New", size,font))
penWrite("Turn: white","Head",penHead) 
def BoardClicked(x,y): 
    global Turn
    global PPM
    global Selected
    global phantomPiece
    x = (int(x) + (SquareSize*15))// (SquareSize*2) - 4
    y = (-int((y-(SquareSize*2))) + (SquareSize*15)) // (SquareSize*2) -4
    if x == 9 and y == 4:
        penWrite("The Board Was saved.","normal",penNormal) 
        FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] The Board was saved.")))
        SaveBoard()
    if len(PPM) == 0:
        if x <= 7 and y <= 7 and x >= 0 and y >=0:
            if Board[x][y][1] != "PPH":
                if Board[x][y][1].getColour() == Turn:
                    FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked Piece %s was found, of the correct colour.") % (str([x,y]),Board[x][y][1].getName())))
                    penWrite("The Piece, " + Board[x][y][1].getName() + ", was selected.","normal",penNormal) 
                    PPM = PossibleMoves(Board[x][y][1],x,y,"None")
                    Board[x][y][1].getTurtle().shapesize(1.2,1.2,1.2)
                    Animate(x, y, "gray")
                    for i in range(len(PPM)):
                        Animate(PPM[i][0],PPM[i][1],"green")
                    Selected = [x,y]
                else:
                    FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked Piece %s was found of the incorrect colour.") % (str([x,y]),Board[x][y][1].getName())))
                    penWrite("The Piece on this square is not of the correct colour. Pick a piece of the turn colour: " + Turn + ".","normal",penNormal) 
            else:
                FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked, No piece was found") % (str([x,y]))))
                penWrite("There is no Piece on this square.","normal",penNormal) 
        wn.update()
    else:
        DeAnimate()
        move = False
        Board[Selected[0]][Selected[1]][1].getTurtle().shapesize(1,1,1)
        if x <= 7 and y <= 7 and x >= 0 and y >=0:
            for i in range(len(PPM)):
                if PPM[i] == [x,y]:
                    move = True
                    pieceToMove = PPM[i]
        if move == True:
            FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (found square) The Square %s was clicked, The piece %s @ %s will be moved") % (str([x,y]), Board[Selected[0]][Selected[1]][1].getName(),Selected)))           
            MovePiece(Selected,pieceToMove, Board)
        else:
            penWrite("Piece was unselected as this was an invalid move.","normal",penNormal) 
            FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (found square) The Square %s was clicked, No piece was found") % (str([x,y]))))
        PPM = []
        Selected =[]
wn.tracer(0) #Reduces the lag seen on screen
wn.onclick(BoardClicked)


                
turtle.mainloop() 
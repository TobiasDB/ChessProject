import BoardsetUp
import turtle 
import FileHandler
import sys
cf <- currentframe()
GameOver <- False
Board, wn, Kl, Pieces,SquareSize,BoardSize <- BoardsetUp.Run() 
IF Kl[0] ==[0,0,"white"] OR [0,0,"black"] == Kl[1]:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("One of the Kings could not be located in the config file. Please place the king on a square")))
ENDIF
AnimatedSquares <- []
PPM =[]
Selected <- [0,0]
Turn <- "white"
WhiteKingMove <- False
WhiteRookLongMove <- False
WhiteRookShortMove <- False
BlackKingMove <- False
BlackRookLongMove <- False
BlackRookShortMove <- False
Castle <- False
FUNCTION changeTurn():
    global Turn
    IF Turn = "white":
        Turn <- "black"
    ELSE:
        Turn <- "white"
    ENDIF
ENDFUNCTION

"""
=======================
=======================
Check and check mate
=======================
"""
FUNCTION checkCheckMate():
    global Turn
    IF Turn = "white":
        KingLocation <- [Kl[0][0],Kl[0][1]]
    ELSE: 
        KingLocation <- [Kl[1][0],Kl[1][1]]
    ENDIF
    KingMove <- PossibleMoves(Board[Kl[0][0]][Kl[0][1]][1],KingLocation[0],KingLocation[1], "Mate")
    ePM <- enemyPossibleMoves()
    toPop <- []
    PiecesTakingKing <- []
    for i in range(len(ePM)):
        for x in range(len(ePM[i][1])):
            IF KingLocation = ePM[i][1][x]:
                PiecesTakingKing.append(ePM[i])
            ENDIF
            for y in range(len(KingMove)):
                IF ePM[i][1][x] = KingMove[y]:
                    toPop.append(KingMove[y])
                ENDIF
    ENDFOR
        ENDFOR
            ENDFOR
    for i in range(len(toPop)):
        IF toPop[i] in KingMove:
            KingMove.remove(toPop[i])
        ENDIF
    ENDFOR
    toPop <- []
    fPM <- friendlyPossibleMoves()
    IF len(KingMove) = 0 AND len(PiecesTakingKing) >1:
        RETURN True
    ELSEIF len(PiecesTakingKing) = 1:
        PTKCOORDS <- PiecesTakingKing[0][0].getCoords()
        xx <- -(PTKCOORDS[0]- KingLocation[0])
        yy <- -(PTKCOORDS[1]- KingLocation[1]) 
        for x in range(len(PiecesTakingKing[0][1])):
            IF (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] < 0 AND not (xx < 0)) OR (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] < 0 AND not (yy < 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
            ELSEIF (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] = 0 AND not (xx = 0)) OR (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] = 0 AND not (yy = 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
            ELSEIF (PiecesTakingKing[0][1][x][0] - PTKCOORDS[0] > 0 AND not (xx > 0)) OR (PiecesTakingKing[0][1][x][1] - PTKCOORDS[1] > 0 AND not (yy > 0)) :
                toPop.append(PiecesTakingKing[0][1][x])
            ENDIF
        ENDFOR
        for i in range(len(toPop)):
            IF toPop[i] in PiecesTakingKing[0][1]:
                PiecesTakingKing[0][1].remove(toPop[i])
            ENDIF
        ENDFOR
        toPop <- []
        PiecesTakingKing[0][1].pop(len(PiecesTakingKing[0][1])-1)
        LengthPieceTakingKing <- len(PiecesTakingKing[0][1])
        for x in range(len(PiecesTakingKing[0][1])):
            for y in range(len(fPM)):
                for p in range(len(fPM[y][1])):
                    IF fPM[y][1][p] = PiecesTakingKing[0][1][x] AND fPM[y][0].getType() !="King":
                        toPop.append(PiecesTakingKing[0][1][x])
                    ENDIF
        ENDFOR
            ENDFOR
                ENDFOR
        for i in range(len(toPop)):
            IF toPop[i] in PiecesTakingKing[0][1]:
                PiecesTakingKing[0][1].remove(toPop[i])
            ENDIF
        ENDFOR
        IF LengthPieceTakingKing != len(PiecesTakingKing[0][1]):
            PiecesTakingKing <- []
        ENDIF
        IF len(KingMove) = 0 AND len(PiecesTakingKing) > 0:
            RETURN True
        ELSE:
            RETURN False
        ENDIF
    ELSE:
        RETURN False
    ENDIF
ENDFUNCTION

FUNCTION checkCheck():
    global Turn
    check <- False
    IF Turn = "white":
        KingLocation <- [Kl[0][0],Kl[0][1]]
    ELSE: 
        KingLocation <- [Kl[1][0],Kl[1][1]]
    ENDIF
    PiecesTakingKing <- []
    ePM <- enemyPossibleMoves()
    for i in range(len(ePM)):
        for x in range(len(ePM[i][1])):
            IF KingLocation = ePM[i][1][x]:
                PiecesTakingKing.append(ePM[i][1][x])
            ENDIF
    ENDFOR
        ENDFOR
    IF len(PiecesTakingKing) > 0:
        check <- True
    ENDIF
    RETURN check
ENDFUNCTION

FUNCTION enemyPossibleMoves():
    ePM <- []
    for i in range(len(Pieces)):
        IF Pieces[i].getColour() != Turn:
            Coords <- Pieces[i].getCoords()
            ePM.append([Pieces[i], PossibleMoves(Pieces[i], Coords[0], Coords[1], False)])
        ENDIF
    ENDFOR
    RETURN ePM
ENDFUNCTION

FUNCTION friendlyPossibleMoves():
    fPM <- []
    for i in range(len(Pieces)):
        IF Pieces[i].getColour() = Turn:
            Coords <- Pieces[i].getCoords()
            fPM.append([Pieces[i], PossibleMoves(Pieces[i], Coords[0], Coords[1], "None")])
        ENDIF
    ENDFOR
    RETURN fPM  
ENDFUNCTION

"""
=======================
=======================
Moves the pieces
=======================
"""
FUNCTION MovePiece(From,Too, InputBoard):
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
    pawnPassPawn <- False
    IF Too = phantomPiece:
        pawnPassPawn <- True
    ENDIF
    phantomPiece <- [-1,-1]
    IF InputBoard[From[0]][From[1]][1] != "PPH":
        IF InputBoard[From[0]][From[1]][1].getType() = "King":
            IF InputBoard[From[0]][From[1]][1].getColour() = "white":
                Kl[0][0] <- Too[0]
                Kl[0][1] <- Too[1]
                WhiteKingMove <- True
            ELSE:
                Kl[1][0] <- Too[0]
                Kl[1][1] <- Too[1]
                BlackKingMove <- True
            ENDIF
        ELSEIF InputBoard[From[0]][From[1]][1].getType() = "Pawn" AND abs(From[1]-Too[1]) = 2:
            IF InputBoard[From[0]][From[1]][1].getColour() = "white":
                phantomPiece <- [From[0],Too[1]-1]
            ELSE:
                phantomPiece <- [From[0],Too[1]+1] 
            ENDIF
        ELSEIF InputBoard[From[0]][From[1]][1].getType() = "Rook":
            IF InputBoard[From[0]][From[1]][1].getCoords() = [0,0]:
                WhiteRookShortMove <- True
            ELSEIF InputBoard[From[0]][From[1]][1].getCoords() = [7,0]:
                WhiteRookLongMove <- True
            ELSEIF InputBoard[From[0]][From[1]][1].getCoords() = [0,7]:         
                BlackRookShortMove <- True
            ELSEIF InputBoard[From[0]][From[1]][1].getCoords() = [7,7]:
                BlackRookLongMove <- True  
        ENDIF
            ENDIF
        toAdd <- 0
        IF pawnPassPawn = True:
            IF InputBoard[From[0]][From[1]][1].getColour() = "white":
                toAdd <- -1
            ELSE:
                toAdd <- 1
        ENDIF
            ENDIF
        PieceTaken <- False
        TempPieceTaken <- 'A'
        IF InputBoard[Too[0]][Too[1]][1] = "PPH" AND pawnPassPawn = False:
            InputBoard[From[0]][From[1]][1].getTurtle().goto((((Too[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))        
            InputBoard[From[0]][From[1]][1].setCoords(Too)
            InputBoard[Too[0]][Too[1]][1] <- InputBoard[From[0]][From[1]][1]
            InputBoard[From[0]][From[1]][1] <- "PPH"
        ELSE:
            PieceTaken <- True
            Pieces.remove(InputBoard[Too[0]][Too[1]][1])
            InputBoard[From[0]][From[1]][1].setCoords(Too)
            TempPieceTaken <- InputBoard[Too[0]][Too[1]+toAdd][1]
            InputBoard[Too[0]][Too[1]+toAdd][1].getTurtle().goto(-400,0)
            InputBoard[From[0]][From[1]][1].getTurtle().goto((((Too[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))   
            InputBoard[Too[0]][Too[1]+toAdd][1] <- "PPH"   
            InputBoard[Too[0]][Too[1]][1] <- InputBoard[From[0]][From[1]][1]
            InputBoard[From[0]][From[1]][1] <- "PPH"
        ENDIF
        wn.update()
        check <- checkCheck() 
        IF check = True:
            penWrite("Attempted to move " + InputBoard[Too[0]][Too[1]][1].getName() + ": From: " + str(From) + ", Too: " + str(Too) + " However King is in check. Returning Pieces...","normal",penNormal) 
            phantomPiece <- [-1,-1]
            IF InputBoard[Too[0]][Too[1]][1].getType() = "King":
                IF InputBoard[Too[0]][Too[1]][1].getColour() = "white":
                    Kl[0][0] <- From[0]
                    Kl[0][1] <- From[1]
                ELSE:
                    Kl[1][0] <- From[0]
                    Kl[1][1] <- From[1]
                ENDIF
            ELSEIF InputBoard[Too[0]][Too[1]][1].getType() = "Rook":
                IF From = [0,0]:
                    WhiteRookShortMove <- False
                ELSEIF From = [7,0]:
                    WhiteRookLongMove <-  False
                ELSEIF From = [0,7]:         
                    BlackRookShortMove <- False
                ELSEIF From = [7,7]:
                    BlackRookLongMove <- False
            ENDIF
                ENDIF
            InputBoard[Too[0]][Too[1]][1].setCoords(From)
            InputBoard[Too[0]][Too[1]][1].getTurtle().goto((((From[0])*(SquareSize*2))-(SquareSize*6),(SquareSize*8)-(From[1]*(SquareSize*2))))        
            InputBoard[From[0]][From[1]][1] <- InputBoard[Too[0]][Too[1]][1]
            InputBoard[Too[0]][Too[1]][1] <- "PPH"
            IF PieceTaken != False:
                Pieces.append(TempPieceTaken)
                Coords =TempPieceTaken.getCoords()
                TempPieceTaken.getTurtle().goto((((Coords[0]+1)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Coords[1]*(SquareSize*2))))        
                InputBoard[Too[0]][Too[1]+toAdd][1] <- TempPieceTaken
            ENDIF
            wn.update()  
        ELSE:
                    piece <- InputBoard[Too[0]][Too[1]][1]
                    IF piece.getType() = "Pawn":
                        IF (piece.getColour() = "white" AND Too[1] = 7) OR (piece.getColour() = "black" AND Too[1] = 0):
                            piece.setType("Queen", [[1.0, 0.0, 1.0],[0.0, 1.0, 1.0],[-1.0, 0.0, 1.0],[0.0, -1.0, 1.0],[1.0, 1.0, 1.0],[1.0, -1.0, 1.0],[-1.0, 1.0, 1.0],[-1.0, -1.0, 1.0]])
                            wn.update()
                        ENDIF
                    ELSEIF piece.getType() = "King" AND abs(From[0]-Too[0]) = 2:
                        IF From[0]-Too[0] = 2:
                            InputBoard[0][Too[1]][1].getTurtle().goto((((3)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))
                            InputBoard[0][Too[1]][1].setCoords([2,Too[1]])
                            InputBoard[2][Too[1]][1] <- InputBoard[0][From[1]][1]
                            InputBoard[From[0]][From[1]][1] <- "PPH"
                        ELSE:
                            InputBoard[7][Too[1]][1].getTurtle().goto((((5)*(SquareSize*2))-(SquareSize*8),(SquareSize*8)-(Too[1]*(SquareSize*2))))
                            InputBoard[7][Too[1]][1].setCoords([2,Too[1]])
                            InputBoard[4][Too[1]][1] <- InputBoard[7][From[1]][1]
                            InputBoard[From[0]][From[1]][1] <- "PPH"
                    ENDIF
                        ENDIF
                    IF TempPieceTaken = "A":
                        penWrite(piece.getName() + ": From: " + str(From) + ", Too: " + str(Too),"normal",penNormal) 
                    ELSE:
                        penWrite(piece.getName() + ": From: " + str(From) + ", Too: " + str(Too) + ", And took the piece " +TempPieceTaken.getName(),"normal",penNormal)                     
                    ENDIF
                    changeTurn()
                    IF Turn = "black":
                        wn.bgcolor("darkgray")
                    ELSE:
                        wn.bgcolor("lightgray")
                    ENDIF
                    penWrite("Turn: " + Turn,"Head",penHead) 
                    checkMate <- checkCheckMate()
                    IF checkMate = True:
                        penWrite("Check Mate","Head",penHead) 
                    ENDIF
                    wn.update()   
    ENDIF
        ENDIF
ENDFUNCTION

"""
=======================
=======================
Controls Animation of Squares
=======================
"""
FUNCTION Animate(x,y, color):
    AnimatedSquares.append(Board[x][y][0])
    Board[x][y][0].getTurtle().color(color)
    wn.update()
ENDFUNCTION

FUNCTION DeAnimate():
    for i in range(len(AnimatedSquares)):
        AnimatedSquares[i].setColour()
    ENDFOR
    wn.update()
ENDFUNCTION

"""
=======================
=======================
Works out possible Moves
=======================
"""
phantomPiece <- [-1,-1]
FUNCTION friendlyOnSquare(x,y):
    global Turn
    IF Board[x][y][1] != "PPH":
        IF Board[x][y][1].getColour() = Turn:
            RETURN True
        ELSE:
            RETURN False
        ENDIF
    ELSE:
        RETURN False
    ENDIF
ENDFUNCTION

FUNCTION enemyOnSquare(x,y):
    global Turn
    IF Board[x][y][1] != "PPH":
        IF Board[x][y][1].getColour() != Turn:
            RETURN True
        ELSE:
            RETURN False
        ENDIF
    ELSE:
        RETURN False
    ENDIF
ENDFUNCTION

FUNCTION PossibleMoves(piece,x,y, type):
    global phantomPiece
    global Turn
    pieceType <- piece.getType()
    moves <- piece.getMove()
    startingCoords <- piece.getStartCoords()
    PM <- []
    for i in range(len(moves)):
        xN <- int(x +  moves[i][0])
        yN <- int(y + moves[i][1])
        c <- moves[i][2]
        IF xN <= 7 AND yN <= 7 AND xN >= 0 AND yN >=0:
            IF Board[xN][yN][1] != "PPH":
                fOS <- friendlyOnSquare(xN,yN)
                eOS <- enemyOnSquare(xN,yN)
                nOS <- False
            ELSE:
                nOS <- True
                fOS <- False
                eOS <- False
            ENDIF
            IF c = 0 AND (fOS = False OR type = False):
                IF pieceType = "Knight" OR pieceType = "King":
                    PM.append([xN,yN])
                    IF pieceType = "King" AND type != False AND type != "Mate":
                        Short <- False
                        Long <- False
                        coords <- piece.getCoords()
                        ePM <- enemyPossibleMoves()
                        for p in range(len(ePM)):
                            for l in range(len(ePM[p][1])):
                                IF [coords[0]-1,coords[1]] = ePM[p][1][l] or [coords[0]-2,coords[1]] = ePM[p][1][l]:
                                    Short <- True
                                ELSEIF [coords[0]+1,coords[1]] = ePM[p][1][l] or [coords[0]+2,coords[1]] = ePM[p][1][l]:
                                    Long <- True
                                ELSEIF  [coords[0],coords[1]] = ePM[p][1][l]:
                                    Long <- True
                                    Short <- True
                                ENDIF
                        ENDFOR
                            ENDFOR
                        IF Turn = "white":
                            IF WhiteRookLongMove = True:
                                Long <- True
                            ENDIF
                            IF WhiteRookShortMove = True:
                                Short <- True
                            ENDIF
                        ELSE:
                            IF BlackRookLongMove = True:
                                Long <- True
                            ENDIF
                            IF BlackRookShortMove = True:
                                Short <- True
                        ENDIF
                            ENDIF
                        IF (WhiteKingMove = False AND Turn = "white") OR (BlackKingMove = False AND Turn = "black"):
                            IF Board[coords[0]-1][coords[1]][1] = "PPH" AND Board[coords[0]-2][coords[1]][1] = "PPH" AND Short = False:
                                PM.append([coords[0]-2,coords[1]])
                            ENDIF
                            IF Board[coords[0]+1][coords[1]][1] = "PPH" AND Board[coords[0]+2][coords[1]][1] = "PPH" AND Board[coords[0]+3][coords[1]][1] = "PPH" AND Long = False:
                                PM.append([coords[0]+2,coords[1]])
                    ENDIF
                        ENDIF
                            ENDIF
                ELSEIF type != "ePM" AND eOS = False AND type != False:
                    PM.append([xN,yN])
                ENDIF
            ELSEIF c = 1:
                Blocked <- False
                while xN <= 7 AND yN <= 7 AND xN >= 0 AND yN >=0 AND Blocked = False:
                    IF Board[xN][yN][1] != "PPH":
                        fOS <- friendlyOnSquare(xN,yN)
                        eOS <- enemyOnSquare(xN,yN)
                        nOS <- False
                    ELSE:
                        nOS <- True
                        fOS <- False
                        eOS <- False
                    ENDIF
                    IF nOS = True:
                        PM.append([xN,yN])
                    ELSEIF fOS = True AND type != False:
                        Blocked <- True
                    ELSEIF eOS = True OR type = False:
                        PM.append([xN,yN])
                        Blocked <- True
                    ENDIF
                    xN <- int(xN +  moves[i][0])
                    yN <- int(yN +  moves[i][1])
                ENDWHILE
            ELSEIF c = 2:
                IF eOS = True OR type = False:
                    PM.append([xN,yN])
                ELSEIF type = "ePM":
                    PM.append([xN,yN])
                ELSEIF phantomPiece != [-1,-1]:
                    IF phantomPiece = [xN,yN]:
                        PM.append([xN,yN])
                ENDIF
                    ENDIF
            ELSEIF c = 3:
                IF pieceType = "Pawn":
                    IF type != "ePM":  
                        IF piece.getColour() = "white":
                            IF nOS = True AND y = 1 AND enemyOnSquare(xN,yN-int(moves[i][1]/2)) = False AND friendlyOnSquare(xN,yN -int(moves[i][1]/2)) = False AND type != False:
                                PM.append([xN,yN])
                            ENDIF
                        ELSE:
                            IF nOS = True AND y = 6 AND enemyOnSquare(xN,yN-int(moves[i][1]/2)) = False AND friendlyOnSquare(xN,yN -int(moves[i][1]/2)) = False AND type != False:
                                PM.append([xN,yN]) 
        ENDIF
            ENDIF
                ENDIF
                    ENDIF
                        ENDIF
                            ENDIF
    ENDFOR
    RETURN PM
ENDFUNCTION

"""
=======================
=======================
Save the current board
=======================
"""
FUNCTION SaveBoard():
    saved <- []
    for i in range(len(Pieces)):
        name  <-  Pieces[i].getName() + ">"
        shape <- Pieces[i].getType()
        colour <- Pieces[i].getColour()
        coords <- Pieces[i].getCoords()
        coords <- str(coords[0]) + str(coords[1])
        moves <- str(Pieces[i].getMove())
        moves <- moves.replace("[[", "{[")
        moves <- moves.replace("]]", "]}")
        moves <- moves.replace("], [", "],[")
        saved.append([name,shape,colour,coords,moves])
    ENDFOR
    BoardsetUp.Save(saved)
ENDFUNCTION

"""
=======================
=======================
Runs When the board is clicked 
=======================
"""
penNormal <- turtle.Turtle()
penHead <- turtle.Turtle()
penNormal.penup()
penHead.penup()
penNormal.hideturtle()
penHead.hideturtle()
penNormal.hideturtle()
penHead.hideturtle()
saveButton <- turtle.Turtle()
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
FUNCTION ClearPen(pen):
    pen.undo()
ENDFUNCTION

FUNCTION penWrite(Message, type, pen):
    ClearPen(pen)
    size <- 15
    font <- "normal"
    IF type = "Head":
        size <- 30
        font <- "bold"
        pen.goto(-600, 250)
    ELSEIF type = "normal":
        pen.goto(-700, 200)
        IF len(Message) > 40:
            for i in range(40):
                IF Message[40-i] = " ":
                    Message <- Message[:40-i] + "\n" +Message[41-i:]
                    break;
        ENDIF
                ENDIF
            ENDFOR
        IF len(Message) > 80:
            for i in range(40):
                IF Message[80-i] = " ":
                    Message <- Message[:80-i] + "\n" +Message[81-i:]
                    break;
    ENDIF
        ENDIF
                ENDIF
            ENDFOR
    pen.write(Message, font=("Courier New", size,font))
ENDFUNCTION

penWrite("Turn: white","Head",penHead) 
FUNCTION BoardClicked(x,y): 
    global Turn
    global PPM
    global Selected
    global phantomPiece
    x <- (int(x) + (SquareSize*15))// (SquareSize*2) - 4
    y <- (-int((y-(SquareSize*2))) + (SquareSize*15)) // (SquareSize*2) -4
    IF x = 9 AND y = 4:
        penWrite("The Board Was saved.","normal",penNormal) 
        FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] The Board was saved.")))
        SaveBoard()
    ENDIF
    IF len(PPM) = 0:
        IF x <= 7 AND y <= 7 AND x >= 0 AND y >=0:
            IF Board[x][y][1] != "PPH":
                IF Board[x][y][1].getColour() = Turn:
                    FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked Piece %s was found, of the correct colour.") % (str([x,y]),Board[x][y][1].getName())))
                    penWrite("The Piece, " + Board[x][y][1].getName() + ", was selected.","normal",penNormal) 
                    PPM <- PossibleMoves(Board[x][y][1],x,y,"None")
                    Board[x][y][1].getTurtle().shapesize(1.2,1.2,1.2)
                    Animate(x, y, "gray")
                    for i in range(len(PPM)):
                        Animate(PPM[i][0],PPM[i][1],"green")
                    ENDFOR
                    Selected <- [x,y]
                ELSE:
                    FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked Piece %s was found of the incorrect colour.") % (str([x,y]),Board[x][y][1].getName())))
                    penWrite("The Piece on this square is not of the correct colour. Pick a piece of the turn colour: " + Turn + ".","normal",penNormal) 
                ENDIF
            ELSE:
                FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (finding square) Square %s was clicked, No piece was found") % (str([x,y]))))
                penWrite("There is no Piece on this square.","normal",penNormal) 
        ENDIF
            ENDIF
        wn.update()
    ELSE:
        DeAnimate()
        move <- False
        Board[Selected[0]][Selected[1]][1].getTurtle().shapesize(1,1,1)
        IF x <= 7 AND y <= 7 AND x >= 0 AND y >=0:
            for i in range(len(PPM)):
                IF PPM[i] = [x,y]:
                    move <- True
                    pieceToMove <- PPM[i]
        ENDIF
                ENDIF
            ENDFOR
        IF move = True:
            FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (found square) The Square %s was clicked, The piece %s @ %s will be moved") % (str([x,y]), Board[Selected[0]][Selected[1]][1].getName(),Selected)))           
            MovePiece(Selected,pieceToMove, Board)
        ELSE:
            penWrite("Piece was unselected as this was an invalid move.","normal",penNormal) 
            FileHandler.Logs.append(FileHandler.Log("General", filename + "/" + str(cf.f_lineno),("[Player] (found square) The Square %s was clicked, No piece was found") % (str([x,y]))))
        ENDIF
        PPM <- []
        Selected =[]
    ENDIF
ENDFUNCTION

wn.tracer(0) #Reduces the lag seen on screen
wn.onclick(BoardClicked)
turtle.mainloop()

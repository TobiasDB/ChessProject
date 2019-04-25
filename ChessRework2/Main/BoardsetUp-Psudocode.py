'''
Created on 23 Aug 2018
@author: tobiasdunlopbrown
'''
cf <- currentframe()
import turtle
import FileHandler
import sys
"""
===========================
Setting Up Global varialbes
"""
Shapes <- []
Kl <- [[0,0,"white"],[0,0,"black"]]
Board <- []
Pieces <- []
"""
===========================
"""
ROOTCompoundShapes <- FileHandler.RootClass("<CompoundShapes>")
SUBROOTCompoundShapes <- ROOTCompoundShapes.GetSubRootsList()
ROOTPieces <- FileHandler.RootClass("<Pieces>")
SUBROOTPieces <- ROOTPieces.GetSubRootsList()
ROOTGeneral <- FileHandler.RootClass("<General>")
SUBROOTGeneral <- ROOTGeneral.GetSubRootsList()
"""
===========================
Getting the setup variables from the files
"""
Moves <- [["Queen"]]
IF len(SUBROOTCompoundShapes) = 0:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <CompoundShapes> Could not be found. Please create this root.")))
    sys.exit()
ENDIF
IF len(SUBROOTPieces) = 0:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <Pieces> could not be found, it is recommended that you place pieces on the board.")))
ENDIF
IF len(SUBROOTGeneral) != 0:
    for i in range(len(SUBROOTGeneral)):
        IF "ColourBg" in SUBROOTGeneral[i]:
            colourBg <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
        ELSEIF "ColourSquares" in SUBROOTGeneral[i]:
            colours <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            whiteS <- colours[0]
            blackS <- colours[1]
        ELSEIF "ColourPieces" in SUBROOTGeneral[i]:
            colours <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            whiteP <- colours[0]
            blackP <- colours[1]
        ELSEIF "ColourSubShape" in SUBROOTGeneral[i]:
            colours <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            subShapeColour <- colours[0]
        ELSEIF "ScreenSize" in SUBROOTGeneral[i]:
            sizes <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            screenX <- float(sizes[0])
            screenY <- float(sizes[1])
        ELSEIF "BoardGap" in SUBROOTGeneral[i]:
            BoardSize <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            BoardSize <- float(BoardSize[0])
        ELSEIF "BoardSize" in SUBROOTGeneral[i]:
            SquareSize <- ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            SquareSize <- int(SquareSize[0])
        ENDIF
    ENDFOR
ELSE:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <General> could not be found, restoring normal settings.")))
    colourBg <- ["gray"]
    whiteS <- "white"
    blackS <- "black"
    whiteP <- "white"
    blackP <- "black"
    SquareSize <- 40
    BoardSize <- 0.8
    subShapeColour <- "orange"
    screenX <- 1.0
    screenY <- 1.0
ENDIF
wn <- turtle.Screen()
wn.title("Chess [-1]")
wn.screensize(2000,1500)
try:
    wn.bgcolor(colourBg[0])
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root colourBg> could not be found restoring default.")))
                                                                                                                                              ENDFUNCTION

    wn.bgcolor("gray")
try:
    wn.setup(width <- screenX, height <- screenY)
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ScreenSize> could not be found restoring default.")))
                                                                                                                                                ENDFUNCTION

    screenX <- 1.0
    screenY <- 1.0
    wn.setup(width <- screenX, height <- screenY)
try:
    Coords <- SquareSize*BoardSize
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root SqaureSize> or BoardSize> could not be found restoring default.")))
                                                                                                                                                              ENDFUNCTION

    SquareSize <- 40
    BoardSize <- 0.8
    Coords <- SquareSize*BoardSize
try:
    testVar <- whiteS
    testVar <- blackS
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ColourSquare> could not be found restoring default.")))
                                                                                                                                                  ENDFUNCTION

    whiteS <- "white"
    blackS <- "black"
try:
    testVar <- whiteP
    testVar <- blackP
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ColourPieces> could not be found restoring default.")))
                                                                                                                                                  ENDFUNCTION

    whiteP <- "white"
    blackP <- "black"
try:
    testVar <- subShapeColour
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root subShapeColour> could not be found restoring default.")))
                                                                                                                                                    ENDFUNCTION

    subShapeColour <- "orange"
wn.bgpic("nopic")
wn.tracer(0)
wn.register_shape("square",((Coords,Coords),(Coords,-Coords),(-Coords,-Coords),(-Coords,Coords)))
CLASS CreateShape():
    FUNCTION __init__(self, polys, name):
         __shapeW <- turtle.Shape("compound")
         __shapeB <- turtle.Shape("compound")
         __name <- name[:-1]
         __polys <- polys
        for i in range(len(polys)):
            for x in range(len(polys[i][0])):
                polys[i][0][x][0] <- polys[i][0][x][0] * SquareSize * BoardSize
                polys[i][0][x][1] <- polys[i][0][x][1] * SquareSize * BoardSize
            ENDFOR
            IF polys[i][1] = "Sub":
                 __shapeB.addcomponent(polys[i][0], subShapeColour, "black")
                 __shapeW.addcomponent(polys[i][0], subShapeColour, "black")
            ELSE:
                 __shapeB.addcomponent(polys[i][0], blackP, "darkgreen")
                 __shapeW.addcomponent(polys[i][0], whiteP, "darkgreen")
            ENDIF
        ENDFOR
        wn.register_shape( __name + "B", __shapeB)
        wn.register_shape( __name +"W", __shapeW)
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Shape \'%s\', has been registered.") %  __name))
    ENDFUNCTION

    FUNCTION getName(self):
        RETURN  __name
    ENDFUNCTION

ENDCLASS

CLASS Square():
    FUNCTION __init__(self,Coords):
         __turtle <- turtle.Turtle()
         __turtle.penup()
         __turtle.shape("square")
         __turtle.shapesize(1, 1, 5)
         __Coords <- Coords
        IF ( __Coords[0] +  __Coords[1]) % 2 != 0:
             __colour <- "black"
             __turtle.color(blackS)
        ELSE:
             __colour <- "white"
             __turtle.color(whiteS)
        ENDIF
         __turtle.goto((( __Coords[0]*(SquareSize*2)-(SquareSize*6)),(SquareSize*8)-( __Coords[1]*(SquareSize*2))))        
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Square \'%s\', has been created.") %  __Coords))
    ENDFUNCTION

    FUNCTION getTurtle(self):
        RETURN  __turtle
    ENDFUNCTION

    FUNCTION getColor(self):
        RETURN  __colour
    ENDFUNCTION

    FUNCTION getCoords(self):
        RETURN  __Coords
    ENDFUNCTION

    FUNCTION setColour(self):
        IF  __colour = "black":
             __turtle.color(blackS)
        ELSE:
             __turtle.color(whiteS)
        ENDIF
    ENDFUNCTION

ENDCLASS

CLASS Piece():
    FUNCTION __init__(self, properties, name):
         __turtle <- turtle.Turtle()
         __turtle.penup()
         __type <- properties[0][1]
         __name <- name[:-1]
         __colour <- properties[1][1]
        IF  __type = "King":
            IF  __colour = "white":
                Kl[0][0] <- int(properties[2][1][0])
                Kl[0][1] <- int(properties[2][1][1])
            ELSE:
                Kl[1][0] <- int(properties[2][1][0])
                Kl[1][1] <- int(properties[2][1][1])
        ENDIF
            ENDIF
        try:
             __StartCoords <- [int(properties[2][1][0]),int(properties[2][1][1])]
        except:
             __StartCoords <- [0,0]
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("Invalid starting square for piece %s") %  __name))
                                                                                                                          ENDFOR
         __Coords <-  __StartCoords
        moves <- properties[3][0]
         __moves <- moves
        IF "black" = properties[1][1]:
            shape <- (properties[0][1] + "B")
        ELSE:
            shape <- (properties[0][1] + "W")
        ENDIF
        try:
             __turtle.shape(shape)
        except:
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),(("The piece %s could not be assigned the shape %s, as it does not exist") % ( __name, shape))))
         __turtle.goto((( __Coords[0]*(SquareSize*2)-(SquareSize*6)),(SquareSize*8)-( __Coords[1]*(SquareSize*2))))        
        IF Board[ __StartCoords[0]][ __StartCoords[1]][1] = "PPH":
            Board[ __StartCoords[0]][ __StartCoords[1]][1] <- self
        ELSE:
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Square \"%s\" already had a piece on it (%s). Replacing it with %s") % (properties[2][1],Board[int(properties[2][1][0])][int(properties[2][1][1])][1].getName(), __name)))
        ENDIF
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Piece \'%s\', has been created.") %  __name))
    ENDFUNCTION

    FUNCTION getTurtle(self):
        RETURN  __turtle
    ENDFUNCTION

    FUNCTION getName(self):
        RETURN  __name
    ENDFUNCTION

    FUNCTION getType(self):
        RETURN  __type
    ENDFUNCTION

    FUNCTION getColour(self):
        RETURN  __colour
    ENDFUNCTION

    FUNCTION getMove(self):
        RETURN  __moves
    ENDFUNCTION

    FUNCTION getStartCoords(self):
        RETURN  __StartCoords
    ENDFUNCTION

    FUNCTION getCoords(self):
        RETURN  __Coords
    ENDFUNCTION

    FUNCTION setCoords(self, Coords):
         __Coords <- Coords
    ENDFUNCTION

    FUNCTION setType(self,Type, Moves):
         __moves <- Moves
         __type <- Type
        IF  __colour = "black":
             __turtle.shape((Type + "B"))
        ELSE:
             __turtle.shape((Type + "W"))
        ENDIF
    ENDFUNCTION

ENDCLASS

"""
===========================
Board SetUp
"""
"""
===========================
Run class function to return variables
"""
for i in range(len(SUBROOTCompoundShapes)):
    Shapes.append(CreateShape(ROOTCompoundShapes.GetSubRootsInfo(SUBROOTCompoundShapes[i], False), SUBROOTCompoundShapes[i])) 
ENDFOR
FUNCTION Run(): 
    global Shapes
    global Kl
    global Board
    global Pieces
    global wn
    wn.title("Chess")
    for x in range(8):
        Board.append([])
        for y in range(8):
            Board[x].append([Square([x,y]), "PPH"])    
            wn.update()      
    ENDFOR
        ENDFOR
    for i in range(len(SUBROOTPieces)):
        Pieces.append(Piece(ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], False),SUBROOTPieces[i]))
    ENDFOR
    wn.update()
    RETURN Board, wn, Kl, Pieces,SquareSize,BoardSize       
ENDFUNCTION

"""
===========================
Run class function to save board to files
"""
FUNCTION Save(Saved):     
    SaveSubRoot <- []     
    for i in range(len(SUBROOTPieces)):
        for x in range(len(Saved)):
            IF SUBROOTPieces[i] = Saved[x][0]:
                subRoot <- ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], True)
                subRoot.SetRootInfo(Saved[x])
                SaveSubRoot.append(i)
            ENDIF
    ENDFOR
        ENDFOR
    for i in range(len(SUBROOTPieces)):
        Found <- False
        for x in range(len(SaveSubRoot)):
            IF i = SaveSubRoot[x]:
                Found <- True
            ENDIF
        ENDFOR
        IF Found = False:
            subRoot <- ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], True)
            subRoot.SetRootInfo("remove")

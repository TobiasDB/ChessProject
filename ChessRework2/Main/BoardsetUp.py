'''
Created on 23 Aug 2018

@author: tobiasdunlopbrown
'''
from inspect import currentframe, getframeinfo
cf = currentframe()
filename = getframeinfo(cf).filename
import turtle
import FileHandler
import sys
"""
===========================
Setting Up Global varialbes
"""
Shapes = []
Kl = [[0,0,"white"],[0,0,"black"]]
Board = []
Pieces = []
"""
===========================
Setting Up Root infomation
"""
ROOTCompoundShapes = FileHandler.RootClass("<CompoundShapes>")
SUBROOTCompoundShapes = ROOTCompoundShapes.GetSubRootsList()
ROOTPieces = FileHandler.RootClass("<Pieces>")
SUBROOTPieces = ROOTPieces.GetSubRootsList()
ROOTGeneral = FileHandler.RootClass("<General>")
SUBROOTGeneral = ROOTGeneral.GetSubRootsList()
"""
===========================
Getting the setup variables from the files
"""
Moves = [["Queen"]]
if len(SUBROOTCompoundShapes) == 0:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <CompoundShapes> Could not be found. Please create this root.")))
    sys.exit()
if len(SUBROOTPieces) == 0:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <Pieces> could not be found, it is recommended that you place pieces on the board.")))
if len(SUBROOTGeneral) != 0:
    for i in range(len(SUBROOTGeneral)):
        if "ColourBg" in SUBROOTGeneral[i]:
            colourBg = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
        elif "ColourSquares" in SUBROOTGeneral[i]:
            colours = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            whiteS = colours[0]
            blackS = colours[1]
        elif "ColourPieces" in SUBROOTGeneral[i]:
            colours = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            whiteP = colours[0]
            blackP = colours[1]
        elif "ColourSubShape" in SUBROOTGeneral[i]:
            colours = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            subShapeColour = colours[0]
        elif "ScreenSize" in SUBROOTGeneral[i]:
            sizes = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            screenX = float(sizes[0])
            screenY = float(sizes[1])
        elif "BoardGap" in SUBROOTGeneral[i]:
            BoardSize = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            BoardSize = float(BoardSize[0])
        elif "BoardSize" in SUBROOTGeneral[i]:
            SquareSize = ROOTGeneral.GetSubRootsInfo(SUBROOTGeneral[i], False)
            SquareSize = int(SquareSize[0])
else:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Root <General> could not be found, restoring normal settings.")))
    colourBg = ["gray"]
    whiteS = "white"
    blackS = "black"
    whiteP = "white"
    blackP = "black"
    SquareSize = 40
    BoardSize = 0.8
    subShapeColour = "orange"
    screenX = 1.0
    screenY = 1.0
wn = turtle.Screen()
wn.title("Chess [-1]")
wn.screensize(2000,1500)
try:
    wn.bgcolor(colourBg[0])
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root colourBg> could not be found restoring default.")))
    wn.bgcolor("gray")
try:
    wn.setup(width = screenX, height = screenY)
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ScreenSize> could not be found restoring default.")))
    screenX = 1.0
    screenY = 1.0
    wn.setup(width = screenX, height = screenY)
try:
    Coords = SquareSize*BoardSize
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root SqaureSize> or BoardSize> could not be found restoring default.")))
    SquareSize = 40
    BoardSize = 0.8
    Coords = SquareSize*BoardSize
try:
    testVar = whiteS
    testVar = blackS
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ColourSquare> could not be found restoring default.")))
    whiteS = "white"
    blackS = "black"
try:
    testVar = whiteP
    testVar = blackP
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root ColourPieces> could not be found restoring default.")))
    whiteP = "white"
    blackP = "black"
try:
    testVar = subShapeColour
except:
    FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The sub-root subShapeColour> could not be found restoring default.")))
    subShapeColour = "orange"
    
wn.bgpic("nopic")

wn.tracer(0)
wn.register_shape("square",((Coords,Coords),(Coords,-Coords),(-Coords,-Coords),(-Coords,Coords)))
class CreateShape():
    def __init__(self, polys, name):
        self.__shapeW = turtle.Shape("compound")
        self.__shapeB = turtle.Shape("compound")
        self.__name = name[:-1]
        self.__polys = polys
        for i in range(len(polys)):
            for x in range(len(polys[i][0])):
                polys[i][0][x][0] = polys[i][0][x][0] * SquareSize * BoardSize
                polys[i][0][x][1] = polys[i][0][x][1] * SquareSize * BoardSize
            if polys[i][1] == "Sub":
                self.__shapeB.addcomponent(polys[i][0], subShapeColour, "black")
                self.__shapeW.addcomponent(polys[i][0], subShapeColour, "black")
            else:
                self.__shapeB.addcomponent(polys[i][0], blackP, "darkgreen")
                self.__shapeW.addcomponent(polys[i][0], whiteP, "darkgreen")
        wn.register_shape(self.__name + "B",self.__shapeB)
        wn.register_shape(self.__name +"W",self.__shapeW)
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Shape \'%s\', has been registered.") % self.__name))
    def getName(self):
        return self.__name
class Square():
    def __init__(self,Coords):
        self.__turtle = turtle.Turtle()
        self.__turtle.penup()
        self.__turtle.shape("square")
        self.__turtle.shapesize(1, 1, 5)
        self.__Coords = Coords
        if (self.__Coords[0] + self.__Coords[1]) % 2 != 0:
            self.__colour = "black"
            self.__turtle.color(blackS)
        else:
            self.__colour = "white"
            self.__turtle.color(whiteS)
        self.__turtle.goto(((self.__Coords[0]*(SquareSize*2)-(SquareSize*6)),(SquareSize*8)-(self.__Coords[1]*(SquareSize*2))))        
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Square \'%s\', has been created.") % self.__Coords))

    def getTurtle(self):
        return self.__turtle
    def getColor(self):
        return self.__colour
    def getCoords(self):
        return self.__Coords
    def setColour(self):
        if self.__colour == "black":
            self.__turtle.color(blackS)
        else:
            self.__turtle.color(whiteS)
class Piece():
    def __init__(self, properties, name):
        self.__turtle = turtle.Turtle()
        self.__turtle.penup()
        self.__type = properties[0][1]
        self.__name = name[:-1]
        self.__colour = properties[1][1]
        if self.__type == "King":
            if self.__colour == "white":
                Kl[0][0] = int(properties[2][1][0])
                Kl[0][1] = int(properties[2][1][1])
            else:
                Kl[1][0] = int(properties[2][1][0])
                Kl[1][1] = int(properties[2][1][1])
        try:
            self.__StartCoords = [int(properties[2][1][0]),int(properties[2][1][1])]
        except:
            self.__StartCoords = [0,0]
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("Invalid starting square for piece %s") % self.__name))
        self.__Coords = self.__StartCoords
        moves = properties[3][0]
        self.__moves = moves
        if "black" == properties[1][1]:
            shape = (properties[0][1] + "B")
        else:
            shape = (properties[0][1] + "W")
        try:
            self.__turtle.shape(shape)
        except:
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),(("The piece %s could not be assigned the shape %s, as it does not exist") % (self.__name, shape))))
        self.__turtle.goto(((self.__Coords[0]*(SquareSize*2)-(SquareSize*6)),(SquareSize*8)-(self.__Coords[1]*(SquareSize*2))))        
        if Board[self.__StartCoords[0]][self.__StartCoords[1]][1] == "PPH":
            Board[self.__StartCoords[0]][self.__StartCoords[1]][1] = self
        else:
            FileHandler.Logs.append(FileHandler.Log("Errors", filename + "/" + str(cf.f_lineno),("The Square \"%s\" already had a piece on it (%s). Replacing it with %s") % (properties[2][1],Board[int(properties[2][1][0])][int(properties[2][1][1])][1].getName(),self.__name)))
        FileHandler.Logs.append(FileHandler.Log("SetUp", filename + "/" + str(cf.f_lineno),("The Piece \'%s\', has been created.") % self.__name))

    def getTurtle(self):
        return self.__turtle
    def getName(self):
        return self.__name
    def getType(self):
        return self.__type
    def getColour(self):
        return self.__colour
    def getMove(self):
        return self.__moves
    def getStartCoords(self):
        return self.__StartCoords
    def getCoords(self):
        return self.__Coords
    def setCoords(self, Coords):
        self.__Coords = Coords
    def setType(self,Type, Moves):
        self.__moves = Moves
        self.__type = Type
        if self.__colour == "black":
            self.__turtle.shape((Type + "B"))
        else:
            self.__turtle.shape((Type + "W"))

   


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
def Run(): 
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
    for i in range(len(SUBROOTPieces)):
        Pieces.append(Piece(ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], False),SUBROOTPieces[i]))
    wn.update()
    return Board, wn, Kl, Pieces,SquareSize,BoardSize       
"""
===========================
Run class function to save board to files
"""
def Save(Saved):     
    SaveSubRoot = []     
    for i in range(len(SUBROOTPieces)):
        for x in range(len(Saved)):
            if SUBROOTPieces[i] == Saved[x][0]:
                subRoot = ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], True)
                subRoot.SetRootInfo(Saved[x])
                SaveSubRoot.append(i)
    for i in range(len(SUBROOTPieces)):
        Found = False
        for x in range(len(SaveSubRoot)):
            if i == SaveSubRoot[x]:
                Found = True
        if Found == False:
            subRoot = ROOTPieces.GetSubRootsInfo(SUBROOTPieces[i], True)
            subRoot.SetRootInfo("remove")
            
            
'''
Created on 7 Oct 2018

@author: tobiasdunlopbrown
'''
import sys
from inspect import currentframe, getframeinfo
import random
cf = currentframe()
filename = getframeinfo(cf).filename
Logs = []
Roots = []
def resetFile():
    reset = open("Log", "w")
    reset.write("General:\nSetUp:\nErrors:")
    reset.close()
resetFile()
class RootClass(): #[6.0.0] Extracts info from the config file
    def __init__(self, Root):
        try:#[6.1.0] If the config file does not exist and will cause an error, Therefore a try and except clause is used
            self.__config = open("Config") #[6.1.1] Opening the config file
        except:
            Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("The Config File could not be located. Please create a Config file."))) #[6.1.2] Calling the error message to be writen in the log
            sys.exit() #[6.1.3] Ending the program
        self.__root = Root #[6.2.0]
        self.__TextFromRoot = [] #[6.2.1]
        self.__SubRoots = [] #[6.2.2]
        self.__lines = self.__config.read().split("\n")  #[6.2.3] splits the config file into its component lines
        self.__config.close() #Close the config as it is no longer needed
        self.RootInfo(self.__root, self.__lines)  #Gets text from root
        SubRootsList = self.GetSubRootsList()
        for i in range(len(SubRootsList)):#[6.13.0]
            self.__SubRoots.append(RootClass(SubRootsList[i]))
        Logs.append(Log("SetUp", filename + "/" + str(cf.f_lineno),("The Root \'%s\', has been Found.") % self.__root))
    def RootInfo(self, root, lines):
        InfoFromRoot = []#[6.3.0] local version of self.__TextFromRoot
        lineNum = 0 #[6.3.1] Store the line number that is currently being looked at
        NumOfTabs = -0 #[6.3.2] Count the number of indentaions before the text in a line
        toPop = [] #[6.3.3] A list Containing index number of items needing to be popped
        for i,line in enumerate(lines): #[6.4.0]
            TabDepth = 0 #[6.5.0]
            checker = False
            while checker == False: 
                if ("\t" * TabDepth) in line: 
                    TabDepth +=1 
                else: 
                    checker = True 
            if TabDepth <= NumOfTabs: #[6.6.0]
                break;
            if "\t" in lines[i] and lineNum != 0: #[6.7.0]
                toAdd = line
                toAdd = toAdd[NumOfTabs:] #[6.8.0]
                InfoFromRoot.append(toAdd)
            if root in line and lineNum == 0: #[6.9.0]
                lineNum = i+1
                NumOfTabs = TabDepth
        for i in range(len(InfoFromRoot)): #[6.10.0] Formatting InfoFrom Root
            if not (">" in InfoFromRoot[i]) and not ("\t" in InfoFromRoot[i]):
                self.__TextFromRoot.append([0,InfoFromRoot[i]])
            if ">" in InfoFromRoot[i] and not "\t" in InfoFromRoot[i]:
                self.__TextFromRoot.append([1, InfoFromRoot[i]]) 
            if ">" in InfoFromRoot[i] or "\t" in InfoFromRoot[i]:
                toPop.append(i)
        for i in range(len(toPop)): #[6.11.0] Removing information
            InfoFromRoot.pop(toPop[i]-i)
        toPop = []
        return InfoFromRoot
    def GetRoot(self):
        return self.__root
    def GetSubRootsList(self):
        SubRoots = []
        for i in range(len(self.__TextFromRoot)): 
            if self.__TextFromRoot[i][0] == 1: #[6.13.1]
                SubRoots.append(self.__TextFromRoot[i][1])#[6.13.2]
        return SubRoots
    def GetSubRootsInfo(self, subRoot, Raw):
        if Raw == False: #[6.16.0]
            for i in range(len(self.__SubRoots)):
                if self.__SubRoots[i].GetRoot() == subRoot:
                    return self.__SubRoots[i].GetRootInfo()
            RootList = str(self.GetSubRootsList())
            Root = str(self.GetRoot())
            Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("""The SubRoot \"%s\" could not be found in the root \"%s\". The Following SubRoots are under this root:
        %s
            """) % (subRoot, Root, RootList)))
        else: #[6.15.0]
            for i in range(len(self.__SubRoots)):
                if self.__SubRoots[i].GetRoot() == subRoot:
                    return self.__SubRoots[i]
    
    def SetRootInfo(self, info):
        config = open("Config")
        lines = config.read().split("\n")#[6.16.0] splitting up the config file into lines
        config.close()
        for i,line in enumerate(lines):
            if self.__root in line:
                if info != "remove":#[6.17.0] checking to see if the info needs to be removed or changed
                    for x in range(len(self.__TextFromRoot)):
                        infoA = self.__TextFromRoot[x][1]#[6.18.0] Updates the info
                        infoA = "\t\t" +infoA[:8] + info[x+1]
                        lines[i+x+1] = infoA
                else:
                    counter = 0
                    for x in range(i,i+len(self.__TextFromRoot)+1): #[6.19.0] Removes the info
                        lines.pop(x-counter)
                        counter +=1
        lines = str(lines)
        lines = lines.replace("[\'", "") #[6.20.0] Format the info
        lines = lines.replace("\']", "")
        lines = lines.replace("\', \'", "\n")
        lines = lines.replace("\\t", "\t")
        config = open("Config", "w")
        config.write(lines)
        config.close()
    def GetRootInfo(self):
        toFormat = []
        Polys = [] #[6.21.0]
        Info = []
        pieceInfo = []
        for i in range(len(self.__TextFromRoot)):#[6.22.0]
            if self.__TextFromRoot[i][0] == 0:
                toFormat.append(self.__TextFromRoot[i][1])
        for i in range(len(toFormat)):
            string = toFormat[i]
            if string[:4] == "poly":#[6.23.0]
                Polys.append(self.FormatPoly(toFormat[i]))
            elif string[:4] == "info":
                Info.append(self.FormatInfo(toFormat[i]))
            elif string[:5] == "shape":
                pieceInfo.append(self.FormatPieceInfo(toFormat[i]))
                pieceInfo.append(self.FormatPieceInfo(toFormat[i+1]))
                pieceInfo.append(self.FormatPieceInfo(toFormat[i+2]))
                pieceInfo.append(self.FormatPoly(toFormat[i+3]))
        if len(Polys) > 0:
            return Polys
        elif len(Info) > 0:#[6.24.0]
            return Info
        elif len(pieceInfo) > 0:
            return pieceInfo
    def FormatPieceInfo(self, toFormat):
        return [toFormat[:8],toFormat[8:]]
    def FormatPoly(self, toFormat):
        numbers = [0,0]
        type = ""
        for x in range(len(toFormat)):
            if toFormat[x] == "{": 
                numbers[0] = x+2
            elif toFormat[x] == "}":
                numbers[1] = x-1
            elif toFormat[x] == ":":
                type = toFormat[-(len(toFormat)-x-1):]
        string = toFormat[numbers[0]:numbers[1]].split("],[",) 
        for o in range(len(string)):
            string[o] =string[o].split(",") 
            try:
                for i in range(len(string[o])):
                    string[o][i] = float(string[o][i])
            except:
                Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("Error when formatting a poly in the config file, please fix the error.")))
                sys.exit() #[6.29.0]
        return (string, type)#[6.30.0]
    def FormatInfo(self, toFormat):
        return toFormat[6:]
class Log(): #[7.0.0]
    def __init__(self, Type, Path, Message):
        self.__type = Type + ":"
        self.__path = Path #[7.1.0]
        self.__message = Message
        try:
            self.__Log = open("Log", "r")
        except:
            resetFile()
        self.__lines = self.__Log.read().split("\n")
        self.__Log.close()
        self.__Code = self.generateCode() #[7.2.0]
        self.writeToFile()
    def generateCode(self):
        return "["+self.__type[:-1] + "] " + ''.join(random.choice("123456789abcdefghijklmnopqrstuvwxyxABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(6))
    def writeToFile(self):
        try:
            self.__Log = open("Log", "w")
        except:
            resetFile()
        toWrite = ""
        LineStart = 0
        for i,line in enumerate(self.__lines): 
            if self.__type in line:
               LineStart = i+1
        if self.__type == "Errors:":
            self.__toWrite =("\tCode: %s\n\tPath: %s\n\tInfo: %s") % (self.__Code,self.__path, self.__message)
        elif self.__type == "SetUp:":
            self.__toWrite =("\t%s: %s") % (self.__Code, self.__message)    
        elif self.__type == "General:":
            self.__toWrite =("\t%s: %s") % (self.__Code, self.__message)          
        self.__lines.insert(LineStart, self.__toWrite)
        for i in range(len(self.__lines)):
            toWrite += str(self.__lines[i] + "\n")
        self.__Log.write(toWrite)
        self.__Log.close()        
    def getMessage(self):
        return self.__toWrite
    def getType(self):
        return self.__type
    
    

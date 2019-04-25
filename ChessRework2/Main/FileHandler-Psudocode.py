'''
Created on 7 Oct 2018
@author: tobiasdunlopbrown
'''
import sys
import random
cf <- currentframe()
Logs <- []
Roots <- []
FUNCTION resetFile():
    reset <- open("Log", "w")
    reset.write("General:\nSetUp:\nErrors:")
    reset.close()
ENDFUNCTION

resetFile()
    FUNCTION __init__(self, Root):
        try:#[6.1.0] If the config file does not exist AND will cause an error, Therefore a try AND except clause is used
                                                                                     ENDFOR
             __config <- open("Config") #[6.1.1] Opening the config file
        except:
            Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("The Config File could not be located. Please create a Config file."))) #[6.1.2] Calling the error message to be writen in the log
            sys.exit() #[6.1.3] Ending the program
         __root <- Root #[6.2.0]
         __TextFromRoot <- [] #[6.2.1]
         __SubRoots <- [] #[6.2.2]
         __lines <-  __config.read().split("\n")  #[6.2.3] splits the config file into its component lines
         __config.close() #Close the config as it is no longer needed
         RootInfo( __root,  __lines)  #Gets text from root
        SubRootsList <-  GetSubRootsList()
        for i in range(len(SubRootsList)):#[6.13.0]
             __SubRoots.append(RootClass(SubRootsList[i]))
        ENDFOR
        Logs.append(Log("SetUp", filename + "/" + str(cf.f_lineno),("The Root \'%s\', has been Found.") %  __root))
    ENDFUNCTION

    FUNCTION RootInfo(self, root, lines):
        InfoFromRoot <- []#[6.3.0] local version of  __TextFromRoot
        lineNum <- 0 #[6.3.1] Store the line number that is currently being looked at
        NumOfTabs <- -0 #[6.3.2] Count the number of indentaions before the text in a line
                                                                  ENDFOR
        toPop <- [] #[6.3.3] A list Containing index number of items needing to be popped
        for i,line in enumerate(lines): #[6.4.0]
            TabDepth <- 0 #[6.5.0]
            checker <- False
            while checker = False: 
                IF ("\t" * TabDepth) in line: 
                    TabDepth +=1 
                ELSE: 
                    checker <- True 
                ENDIF
            ENDWHILE
            IF TabDepth <= NumOfTabs: #[6.6.0]
                break;
            ENDIF
            IF "\t" in lines[i] AND lineNum != 0: #[6.7.0]
                toAdd <- line
                toAdd <- toAdd[NumOfTabs:] #[6.8.0]
                InfoFromRoot.append(toAdd)
            ENDIF
            IF root in line AND lineNum = 0: #[6.9.0]
                lineNum <- i+1
                NumOfTabs <- TabDepth
            ENDIF
        ENDFOR
        for i in range(len(InfoFromRoot)): #[6.10.0] Formatting InfoFrom Root
            IF not (">" in InfoFromRoot[i]) AND not ("\t" in InfoFromRoot[i]):
                 __TextFromRoot.append([0,InfoFromRoot[i]])
            ENDIF
            IF ">" in InfoFromRoot[i] AND not "\t" in InfoFromRoot[i]:
                 __TextFromRoot.append([1, InfoFromRoot[i]]) 
            ENDIF
            IF ">" in InfoFromRoot[i] OR "\t" in InfoFromRoot[i]:
                toPop.append(i)
            ENDIF
        ENDFOR
            InfoFromRoot.pop(toPop[i]-i)
        ENDFOR
        toPop <- []
        RETURN InfoFromRoot
    ENDFUNCTION

    FUNCTION GetRoot(self):
        RETURN  __root
    ENDFUNCTION

    FUNCTION GetSubRootsList(self):
        SubRoots <- []
        for i in range(len( __TextFromRoot)): 
            IF  __TextFromRoot[i][0] = 1: #[6.13.1]
                SubRoots.append( __TextFromRoot[i][1])#[6.13.2]
            ENDIF
        ENDFOR
        RETURN SubRoots
    ENDFUNCTION

    FUNCTION GetSubRootsInfo(self, subRoot, Raw):
        IF Raw = False: #[6.16.0]
            for i in range(len( __SubRoots)):
                IF  __SubRoots[i].GetRoot() = subRoot:
                    RETURN  __SubRoots[i].GetRootInfo()
                ENDIF
            ENDFOR
            RootList <- str( GetSubRootsList())
            Root <- str( GetRoot())
            Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("""The SubRoot \"%s\" could not be found in the root \"%s\". The Following SubRoots are under this root:
        ENDIF
        %s
            """) % (subRoot, Root, RootList)))
        ELSE: #[6.15.0]
            for i in range(len( __SubRoots)):
                IF  __SubRoots[i].GetRoot() = subRoot:
                    RETURN  __SubRoots[i]
                ENDIF
    ENDFUNCTION

            ENDFOR
        config <- open("Config")
        lines <- config.read().split("\n")#[6.16.0] splitting up the config file into lines
        config.close()
        for i,line in enumerate(lines):
            IF  __root in line:
                    for x in range(len( __TextFromRoot)):
                    ENDFOR
                ELSE:
                    counter <- 0
                        lines.pop(x-counter)
                        counter +=1
            ENDIF
                ENDIF
        ENDFOR
                    ENDFOR
        lines <- str(lines)
        lines <- lines.replace("\']", "")
        lines <- lines.replace("\', \'", "\n")
        lines <- lines.replace("\\t", "\t")
        config <- open("Config", "w")
        config.write(lines)
        config.close()
    ENDFUNCTION

    FUNCTION GetRootInfo(self):
        toFormat <- []
        Polys <- [] #[6.21.0]
        Info <- []
        pieceInfo <- []
        for i in range(len( __TextFromRoot)):#[6.22.0]
            IF  __TextFromRoot[i][0] = 0:
                toFormat.append( __TextFromRoot[i][1])
            ENDIF
        ENDFOR
        for i in range(len(toFormat)):
            string <- toFormat[i]
            IF string[:4] = "poly":#[6.23.0]
                Polys.append( FormatPoly(toFormat[i]))
                Info.append( FormatInfo(toFormat[i]))
            ELSEIF string[:5] = "shape":
                pieceInfo.append( FormatPieceInfo(toFormat[i]))
                pieceInfo.append( FormatPieceInfo(toFormat[i+1]))
                pieceInfo.append( FormatPieceInfo(toFormat[i+2]))
                pieceInfo.append( FormatPoly(toFormat[i+3]))
            ENDIF
        ENDFOR
        IF len(Polys) > 0:
            RETURN Polys
        ELSEIF len(Info) > 0:#[6.24.0]
            RETURN Info
        ELSEIF len(pieceInfo) > 0:
            RETURN pieceInfo
        ENDIF
    ENDFUNCTION

    FUNCTION FormatPieceInfo(self, toFormat):
        RETURN [toFormat[:8],toFormat[8:]]
    ENDFUNCTION

    FUNCTION FormatPoly(self, toFormat):
        numbers <- [0,0]
        type <- ""#[6.25.0]
        for x in range(len(toFormat)):
            IF toFormat[x] = "{": #[6.26.0]
                numbers[0] <- x+2
            ENDIF
            IF toFormat[x] = "}":
                numbers[1] <- x-1
            ENDIF
            IF toFormat[x] = ":":
                type <- toFormat[-(len(toFormat)-x-1):]
            ENDIF
        ENDFOR
        string <- toFormat[numbers[0]:numbers[1]].split("],[",) #[6.27.0]
        for o in range(len(string)):
            string[o] =string[o].split(",") #[6.28.0]
            try:
                for i in range(len(string[o])):
                    string[o][i] <- float(string[o][i])
                ENDFOR
            except:
                Logs.append(Log("Errors", filename + "/" + str(cf.f_lineno),("Error when formatting a poly in the config file, please fix the error.")))
                                                                                         ENDFOR
                sys.exit() #[6.29.0]
        ENDFOR
        RETURN (string, type)#[6.30.0]
    ENDFUNCTION

    FUNCTION FormatInfo(self, toFormat):
        RETURN toFormat[6:]
    ENDFUNCTION

ENDCLASS

CLASS Log(): #[7.0.0]
    FUNCTION __init__(self, Type, Path, Message):
         __type <- Type + ":"
         __path <- Path #[7.1.0]
         __message <- Message
        try:
             __Log <- open("Log", "r")
        except:
            resetFile()
         __lines <-  __Log.read().split("\n")
         __Log.close()
         __Code <-  generateCode() #[7.2.0]
         writeToFile()
    ENDFUNCTION

    FUNCTION generateCode(self):
        RETURN "["+ __type[:-1] + "] " + ''.join(random.choice("123456789abcdefghijklmnopqrstuvwxyxABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(6))
    ENDFUNCTION

                                                                                ENDFUNCTION

                                                                                                                                    ENDFOR
    FUNCTION writeToFile(self):
        try:
             __Log <- open("Log", "w")
        except:
            resetFile()
        toWrite <- ""
        LineStart <- 0
        for i,line in enumerate( __lines): 
            IF  __type in line:
               LineStart <- i+1
            ENDIF
        ENDFOR
        IF  __type = "Errors:":
             __toWrite <-("\tCode: %s\n\tPath: %s\n\tInfo: %s") % ( __Code, __path,  __message)
        ELSEIF  __type = "SetUp:":
             __toWrite <-("\t%s: %s") % ( __Code,  __message)    
        ELSEIF  __type = "General:":
             __toWrite <-("\t%s: %s") % ( __Code,  __message)          
        ENDIF
         __lines.insert(LineStart,  __toWrite)
        for i in range(len( __lines)):
            toWrite += str( __lines[i] + "\n")
        ENDFOR
         __Log.write(toWrite)
         __Log.close()        
    ENDFUNCTION

    FUNCTION getMessage(self):
        RETURN  __toWrite
    ENDFUNCTION

    FUNCTION getType(self):
        RETURN  __type

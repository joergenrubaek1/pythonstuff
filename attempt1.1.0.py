#!usr/bin/python3
import os
# ISO-8859-1
class prepareTxtFiles():
    
    def __init__(self):
   
        self.UdFil = ''      
        self.countLine = 0
        self.work = []
        self.filType= "ASCII"
        self.fileIsAscii = True
        
    def arbpath(self):
        return '/mnt/mindisk3/data/'
        
    def arbFilSti(self, workFile):
        return os.path.join(self.arbpath, workFile)
    
    def arbpathSave(self):
        return '/mnt/mindisk3/tilpassetdata/'
        
    def arbFilStiSave(self, workFile):
         return os.path.join(self.arbpathSave(), workFile)
    
    def loadTheFile(self, filnavn):
        try:
            self.UdFil = open(self.arbFilSti(filnavn), "r")
            if self.UdFil.mode == 'r':
                allLines = self.Udfil.readlines()
        except:
            allLines = []
            
        self.UdFil.close()
        return allLines
        
    def saveTheFile(self, LinesToBeSaved,filnavn):
        
        if self.fileIsAscii :
            try:
                self.UdFil = open(self.arbFilSti(filnavn), "w")
                if self.UdFil.mode == 'w' :
                    self.UdFil.writelines(LinesToBeSaved)
            except:
                pass
        self.UdFil.close()



    def CutLines(self, a, b):
        del self.work[a:b]
        
    def sorterFiltype(self):
        if self.filType.beginswith("ASCII"):
            self.fileIsAscii = True
        else: # self.filType.beginswith("ISO-8859-1"):
            self.fileIsAscII = False
        
            
     
            
    def findLanguageOftxt(self, IsEnglishLine, lineNumber):
        if IsEnglishLine.beginswith("Language: English"):
            self.CutLines(0, lineNumber)
            self.countLine = 0
    
    def findCharacterSetEncoding(self, IsEnglishLine, lineNumber):
        if IsEnglishLine.beginswith("Character set encoding: "):
            IsEnglishLine = IsEnglishLine[0:20]
            self.sorterFiltype()
            
    def findBeginOftxt(self, IsEnglishLine, lineNumber):    
        if IsEnglishLine.beginswith("CHAPTER I", lineNumber):
            self.CutLines(0, lineNumber)
            self.countLine = 0

    def findTheEndOfPaper(self, IsEnglishLine, lineNumber, toLastLine):
        if IsEnglishLine.beginswith("THE END"):
            self.CutLines(lineNumber, toLastLine)
            
    def findTheEndOfPlaintxt(self, IsEnglishLine, lineNumber, toLastLine):
        if IsEnglishLine.beginswith("*** END OF THIS PROJECT GUTENBERG EBOOK"):
            self.CutLines(lineNumber, toLastLine)
    
    def browseTheFiles(self):
        for _, _, filenames in os.walk(self.arbpath):
            for file in filenames :
                fileLines = self.loadTheFile(file)
                lengthOfFile = len(fileLines)
                self.work = fileLines
                for line in reversed(fileLines):
                    
                    self.countLine +=1
                    self.findLangaugeOftxt(line, self.countLine)
                    self.findBeginOftxt(line, self.countLine)
                    self.findTheEndOfPlaintxt(line, self.countLine, lengthOfFile)
            
                self.SaveTheFile(self.work)

    state = 'Soeg sprog'

    
    with open('minFil', 'r') as inFil:
        with open('minFil_out', 'w') as udFil:
            for line in inFil :
                if state == 'Soeg sprog' :
                    if line.beginsWith('Language: ')
                        if 'English' in line :
                            state = 'begynd'
                        else :
                            log(f'Droppet fil.... pga. {line}')
                            break

                if state == 'begynd' :
                    if '*** START' in line :
                        state = 'kopier'
                
                if state == 'kopier' :
                    if '*** END' in line :
                        break
                    else :
                        udFil.write(line)
                
        print('ved magi er udfile nu lukket')                
    print('ved magi er infile nu lukket')                
        
        
   
if __name__ == "__main__" :
    system1 = prepareTxtFiles()
    system1.browseTheFiles()









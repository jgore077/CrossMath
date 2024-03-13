from ReplaceLaTeXEquations import LaTeXReplacer
from ReplaceDelimiterStrings import DelimterReplacer

class LaTeXMasker():
    def __init__(self) -> None:
        self.latex = LaTeXReplacer()
        self.replacer = DelimterReplacer()
    
    def Mask(self,incomingString : str):
        return self.latex.ReplaceEquations(incomingString)
    
    def Unmask(self,incomingString : str, EquationSet : dict):
        return self.replacer.ReplaceDelimiters(incomingString,EquationSet)

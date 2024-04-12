from .ReplaceLaTeXEquations import LaTeXReplacer
from .ReplaceDelimiterStrings import DelimterReplacer


class LaTeXMasker():
    def __init__(self,delimiter) -> None:
        self.latex = LaTeXReplacer()
        self.replacer = DelimterReplacer()
        self.delimiter=delimiter
    
    def mask(self,incomingString : str):
        return self.latex.replaceEquations(incomingString,self.delimiter)
    
    def unmask(self,incomingString : str, EquationSet : dict):
        return self.replacer.replaceDelimiters(incomingString,EquationSet)

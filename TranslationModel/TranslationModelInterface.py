
class TranslationModelInterface:
    def translate(self,text)->str:
        # Any model class implemented with this
        raise NotImplementedError

class LanguageNotSupported(Exception):
    
     def __init__(self, Message):
        self.Message = Message
        return
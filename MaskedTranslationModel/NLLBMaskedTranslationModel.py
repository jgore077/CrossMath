import re
from LaTeXMasker import LaTeXMasker
from TranslationModel import NLLBModel


class NLLBMaskedTranslationModel:

    def __init__(self, delimiter: str) -> None:
        self.masker = LaTeXMasker(delimiter)
        self.translator = NLLBModel.NLLBModel()
        self.maskerRegexString = r'[¿\?\.,!0-9 ' + self.masker.delimiter + r']*'

    def translate(self, text: str, flores_from: str = None, flores_to: str = 'eng_Latn'):
        finalText = ""
        for excerpt in re.split(r"[.!?] ", text):
            maskedString, maskedDict = self.masker.mask(excerpt)
            match = re.match(self.maskerRegexString, maskedString)
            if match.group() == "" or match.group() == "¿":
                translatedString = self.translator.translate(maskedString, flores_from, flores_to)
                finalText = finalText + str(self.masker.unmask(translatedString, maskedDict)) + " "
            else:
                finalText = finalText + str(excerpt) + " "
        return finalText


if __name__ == "__main__":
    model = NLLBMaskedTranslationModel()
    print(model.translate("论欧拉马斯切罗尼常数的非理性", "zho_Hans"))
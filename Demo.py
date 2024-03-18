from langdetect import detect
from LaTeXMasker import LaTeXMasker
from TranslationModel import MBartModel

mbart = MBartModel()
masker = LaTeXMasker()

parentLanguageDict = {"ca":"es"}

def GetParentLanguage(language : str):
    if language in parentLanguageDict.keys():
        return parentLanguageDict[language]
    else:
        return language


beginningStrings = [
"Transformada de Fourier de función $1/ \\vert x \\vert$",
"تبدیل فوریه تابع $1/ \\vert x \\vert$",
"كيف يمكنني تقييم $\\sum_{n=0}^{\\infty}{\\frac{x^{kn}}{(kn)!}}$ حيث  $k$ عدد طبيعي؟",
"Comment puis-je évaluer $\\sum_{n=0}^{\\infty}{\\frac{x^{kn}}{(kn)!}}$ où $k$  est un nombre naturel ?",
"Поиск положительных целочисленных решений уравнения $\\frac{4}{x}+\\frac{10}{y}=1$",
"Die Suche nach positiven ganzzahligen Lösungen für $\\frac{4}{x}+\\frac{10}{y}=1$",
"Trovare soluzioni intere positive per $\\frac{4}{x}+\\frac{10}{y}=1$",
"求 $\\frac{4}{x}+\\frac{10}{y}=1$ 的正整数解",
"论欧拉马斯切罗尼常数的非理性",
"Sur l'irrationalité de la constante d'Euler Mascheroni",
"Ho il seguente problema: Sia $|x_{n+1} - x_n| < 1/3^n$. Mostra che $(x_n)$ è una successione di Cauchy.",
"Ich habe folgendes Problem: Sei $|x_{n+1} - x_n| < 1/3^n$. Zeige, dass $(x_n)$ eine Cauchy-Folge ist."
]

for sentence in beginningStrings:
    maskedSentence, unmaskDictionary = masker.Mask(sentence)
    print("initial:")
    print(sentence)
    print("masked:")
    print(maskedSentence)
    language = detect(maskedSentence)
    language = GetParentLanguage(language)
    language = language[:2]
    maskedTranslatedSentence = mbart.translate(maskedSentence, language, "en")
    translatedSentence = masker.Unmask(maskedTranslatedSentence[0], unmaskDictionary)
    print("translated and unmasked:")
    print(translatedSentence)
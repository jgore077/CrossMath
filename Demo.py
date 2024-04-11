from langdetect import detect
from LaTeXMasker import LaTeXMasker
from TranslationModel import MBartModel

mbart = MBartModel()
masker = LaTeXMasker()

result=mbart.translate(r"می‌خواهم مقدار عبارت زیر را پیدا کنم: $$ 5^{133} \mod 8. $$. متوجه شدم که   هنگامی که $n$ فرد است و در غیر اینصورت برابر 1 است، که من را به این نتیجه می‌رساند که $5^{133} \mod 8 = 5$ اما نمی‌دانم چگونه این را اثبات کنم. چگونه می‌توانم اثبات کنم که این اتفاق می‌افتد (یا اگر این اتفاق نمی‌افتد، راه‌حل دیگری را پیدا کنم)؟")
# We have languages that are not supported that are regional dialects or descend from supported languages, so we covert
# them to the parent language to attempt to translate.
parentLanguageDict = {"ca":"es", "kn":"hi", "pa":"hi", "sk":"cz"}

# Method to covert from child language to parent language
def GetParentLanguage(language : str):
    if language in parentLanguageDict.keys():
        return parentLanguageDict[language]
    else:
        return language

# Our test strings for this demo
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

# Iterate over our test strings
for sentence in beginningStrings:

    # Mask out the LaTeX equations
    maskedSentence, unmaskDictionary = masker.mask(sentence)

    # Show the initial sentence and its masked version, will be removed in production.
    print("initial:")
    print(sentence)
    print("masked:")
    print(maskedSentence)

    # We detect the language of the masked sentence, see if it is one of our child languages, and then truncate the
    # language code to pass to mBart for translation.
    language = detect(maskedSentence)
    language = GetParentLanguage(language)
    language = language[:2]

    # Translate the masked sentence to English and unmask
    maskedTranslatedSentence = mbart.translate(maskedSentence, language, "en")
    translatedSentence = masker.unmask(maskedTranslatedSentence[0], unmaskDictionary)

    # This is a current issue we are working on diagnosing, as when certain strings are masked, the translation instead
    # outputs this phrase, but translates correctly when translating the unmasked version, so until the issue is solved
    # we output the raw translated sentence (which is usually accurate) so there is a chance of it being correct.
    if translatedSentence == "The Committee recommends that the State party take all necessary measures to ensure the " \
                             "full enjoyment of all human rights and fundamental freedoms by women, including the right" \
                             " to education, the right to health, the right to food, the right to adequate housing " \
                             "and the right to adequate housing.":
        translatedSentence = mbart.translate(sentence, language, "en")[0]

    # Show the unmasked and translated string, will be removed in production.
    print("translated and unmasked:")
    print(translatedSentence)

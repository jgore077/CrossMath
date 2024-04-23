# coding=utf-8
from MaskedTranslationModel import MaskedTranslationModel, NLLBMaskedTranslationModel

# Declaration of our combined masking and translation model
translator = MaskedTranslationModel('QZ',20)
NLLBtranslator =NLLBMaskedTranslationModel('QZ')

# Our test strings for this demo
beginningStrings = [
"Transformada de Fourier de función $1/ \\vert x \\vert$",
"تبدیل فوریه تابع $1/ \\vert x \\vert$",
"كيف يمكنني تقييم $\\sum_{n=0}^{\\infty}{\\frac{x^{kn}}{(kn)!}}$ حيث  $k$ عدد طبيعي؟",
"Comment puis-je évaluer $\\sum_{n=0}^{\\infty}{\\frac{x^{kn}}{(kn)!}}$ où $k$ est un nombre naturel ?",
"Поиск положительных целочисленных решений уравнения $\\frac{4}{x}+\\frac{10}{y}=1$",
"Die Suche nach positiven ganzzahligen Lösungen für $\\frac{4}{x}+\\frac{10}{y}=1$",
"Trovare soluzioni intere positive per $\\frac{4}{x}+\\frac{10}{y}=1$",
"求 $\\frac{4}{x}+\\frac{10}{y}=1$ 的正整数解",
"论欧拉马斯切罗尼常数的非理性",
"Sur l'irrationalité de la constante d'Euler Mascheroni",
"Ho il seguente problema: Sia $|x_{n+1} - x_n| < 1/3^n$. Mostra che $(x_n)$ è una successione di Cauchy.",
"Ich habe folgendes Problem: Sei $|x_{n+1} - x_n| < 1/3^n$. Zeige, dass $(x_n)$ eine Cauchy-Folge ist.",
"می‌خواهم مقدار عبارت زیر را پیدا کنم: $$ 5^{133} \mod 8. $$. متوجه شدم که   هنگامی که $n$ فرد است و در غیر اینصورت برابر 1 است، که من را به این نتیجه می‌رساند که $5^{133} \mod 8 = 5$ اما نمی‌دانم چگونه این را اثبات کنم. چگونه می‌توانم اثبات کنم که این اتفاق می‌افتد (یا اگر این اتفاق نمی‌افتد، راه‌حل دیگری را پیدا کنم)؟",
"$\\frac{1}{\sqrt{-1}}=\\sqrt{-1}$?",
"¿La $\\frac{1}{\sqrt{-1}}=\\sqrt{-1}$?",
"什么是$\\frac{1}{\sqrt{-1}}=\\sqrt{-1}$?"
]

lang_code = [
    "spa_Latn",
    "pes_Arab",
    "arb_Arab",
    "fra_Latn",
    "rus_Cyrl",
    "deu_Latn",
    "ita_Latn",
    "zho_Hans",
    "zho_Hans",
    "fra_Latn",
    "ita_Latn",
    "deu_Latn",
    "pes_Arab",
    "eng_Latn",
    "spa_Latn",
    "zho_Hans"
]

# Iterate over our test strings
i=0
for sentence in beginningStrings:    
    translatedSentence = translator.translate(sentence)
    print("BART\n" + str(translatedSentence))
    print("\nNLLB" )
    translatedSentence = NLLBtranslator.translate(sentence, flores_from=lang_code[i])
    print(str(translatedSentence) + "\n")
    i = i+1

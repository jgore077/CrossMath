from LaTeXMasker import LaTeXMasker
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import csv

masker = LaTeXMasker('XX')
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")


def translate(input, translator):
    output = translator(input)
    return output[0]['translation_text']


codes = ['zho_Hans', 'hin_Deva', 'npi_Deva', 'pes_Arab', 'ces_Latn', 'hrv_Latn', 'spa_Latn']

with open("Math_Questions.tsv", encoding='utf-8') as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for code in codes:
        fd.seek(0)
        rows = [row for row in rd]
        translator = pipeline('translation', model=model, tokenizer=tokenizer, src_lang='eng_Latn', tgt_lang=code,
                              max_length=1000, device=0)
        with open(f"datasets/{code}.tsv", 'w', encoding='utf-8') as translated_set:
            for row in rows:
                translatedRow = [row[0]]
                maskedSentence, unmaskDictionary = masker.mask(row[1])
                translatedRow.append(masker.unmask(translate(maskedSentence, translator), unmaskDictionary))
                maskedSentence, unmaskDictionary = masker.mask(row[2])
                translatedRow.append(masker.unmask(translate(maskedSentence, translator), unmaskDictionary))
                translatedRow.append(row[3])
                for i in range(1, len(row)):
                    row[i] = '\t' + row[i]
                row[3] += '\n'
                for i in range(1, len(translatedRow)):
                    translatedRow[i] = '\t' + translatedRow[i]
                translatedRow[3] += '\n'
                translated_set.writelines(row)
                translated_set.writelines(translatedRow)


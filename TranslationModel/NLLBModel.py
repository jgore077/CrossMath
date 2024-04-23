from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langdetect import detect
from .TranslationModelInterface import TranslationModelInterface

class NLLBModel(TranslationModelInterface):

    def __init__(self) -> None:
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        self.twoLetterToFlores = {
            "af": "afr_Latn",
            "ar": "arb_Arab",
            "bg": "bul_Cyrl",
            "bn": "ben_Beng",
            "ca": "cat_Latn",
            "cs": "ces_Latn",
            "cy": "cym_Latn",
            "da": "dan_Latn",
            "de": "deu_Latn",
            "el": "ell_Grek",
            "en": "eng_Latn",
            "es": "spa_Latn",
            "et": "est_Latn",
            "fa": "pes_Arab",
            "fi": "fin_Latn",
            "fr": "fra_Latn",
            "gu": "guj_Gujr",
            "he": "heb_Hebr",
            "hi": "hin_Deva",
            "hr": "hrv_Latn",
            "hu": "hun_Latn",
            "id": "ind_Latn",
            "it": "ita_Latn",
            "ja": "jpn_Jpan",
            "kn": "kan_Knda",
            "ko": "kor_Hang",
            "lt": "lit_Latn",
            "lv": "lvs_Latn",
            "mk": "mkd_Cyrl",
            "ml": "mal_Mlym",
            "mr": "mar_Deva",
            "ne": "npi_Deva",
            "nl": "nld_Latn",
            "no": "nob_Latn",
            "pa": "pan_Guru",
            "pl": "pol_Latn",
            "pt": "por_Latn",
            "ro": "ron_Latn",
            "ru": "rus_Cyrl",
            "sk": "slk_Latn",
            "sl": "slv_Latn",
            "so": "som_Latn",
            "sq": "als_Latn",
            "sv": "swe_Latn",
            "sw": "swh_Latn",
            "ta": "tam_Taml",
            "te": "tel_Telu",
            "th": "tha_Thai",
            "tl": "tgl_Latn",
            "tr": "tur_Latn",
            "uk": "ukr_Cyrl",
            "ur": "urd_Arab",
            "vi": "vie_Latn",
            "zh": "zho_Hans"
        }

    def translate(self, text: str, flores_from: str = None, iso639_1_from: str = None, flores_to: str = 'eng_Latn') -> str:

        if iso639_1_from is not None:
            src_lang = self.twoLetterToFlores.get(iso639_1_from[:2])
        else:
            if flores_from is None:
                detected_lang = detect(text)
                src_lang = self.twoLetterToFlores.get(detected_lang[:2])
            else:
                src_lang = flores_from

        translator = pipeline('translation', model=self.model, tokenizer=self.tokenizer, src_lang=src_lang,
                              tgt_lang=flores_to, max_length=1000, device=0)

        output = translator(text)

        return output[0]['translation_text']
from .TranslationModelInterface import TranslationModelInterface,LanguageNotSupported
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

class MBartModel(TranslationModelInterface):
    def __init__(self):
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
        self.supported_languages=[
        "ar_AR",
        "cs_CZ",
        "de_DE",
        "en_XX",
        "es_XX",
        "et_EE",
        "fi_FI",
        "fr_XX",
        "gu_IN",
        "hi_IN",
        "it_IT",
        "kk_KZ",
        "ko_KR",
        "ja_XX",
        "lt_LT",
        "lv_LV",
        "my_MM",
        "ne_NP",
        "nl_XX",
        "ro_RO",
        "ru_RU",
        "si_LK",
        "tr_TR",
        "vi_VN",
        "zh_CN",
        "af_ZA",
        "az_AZ",
        "bn_IN",
        "fa_IR",
        "he_IL",
        "sl_SI",
        "gl_ES",
        "xh_ZA",
        "ur_PK",
        "uk_UA",
        "tl_XX",
        "th_TH",
        "te_IN",
        "ta_IN",
        "sw_KE",
        "sv_SE",
        "pt_XX",
        "ps_AF",
        "pl_PL",
        "mr_IN",
        "mn_MN",
        "ml_IN",
        "mk_MK",
        "km_KH",
        "ka_GE",
        "id_ID",
        "hr_HR",]
            
    def translate(self,text:str,iso639_1_from:str,iso639_1_to:str)->str:
        # Shortening the MBART language codes to iso639 codes
        abbreviated_lang_codes=[lang_code[:2] for lang_code in self.supported_languages]
        
        
        if len(iso639_1_from)>2:
            raise ValueError("Source Language Code Cannot Be More Than 2 Characters")
        
        if iso639_1_from not in abbreviated_lang_codes:
            raise LanguageNotSupported("Source Language Not Supported Or Language Code Does Not Exist")
        
        if len(iso639_1_to)>2:
            raise ValueError("Translation Language Code Cannot Be More Than 2 Characters")
        
        if iso639_1_to not in abbreviated_lang_codes:
            raise LanguageNotSupported("Translation Language Not Supported Or Language Code Does Not Exist")
        
        # Getting MBART code from iso639 code
        self.tokenizer.src_lang=self.supported_languages[abbreviated_lang_codes.index(iso639_1_from)]
        
        
        encoded_ar = self.tokenizer(text, return_tensors="pt")
        
        generated_tokens = self.model.generate(
            **encoded_ar,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[self.supported_languages[abbreviated_lang_codes.index(iso639_1_to)]]
        )
        
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        

    
if __name__=="__main__":
    mbart = MBartModel()
    result=mbart.translate("Im testing the language model!","en","id")
    print(result)
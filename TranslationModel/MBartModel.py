from .TranslationModelInterface import TranslationModelInterface,LanguageNotSupported
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from langdetect import detect

class MBartModel(TranslationModelInterface):
    def __init__(self):
        self.model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt",device_map='cuda')
        self.tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt",device_map='cuda')
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
        self.abbreviated_lang_codes=[lang_code[:2] for lang_code in self.supported_languages]
        self.parentLanguageDict = {"ca":"es", "kn":"hi", "pa":"hi", "sk":"cs"}
        self.parentLanguageDictKeys=self.parentLanguageDict.keys()
        
    def translate(self,text:str,iso639_1_from:str = None,iso639_1_to:str = 'en')->str:
        # Shortening the MBART language codes to iso639 codes
       
        if iso639_1_from==None:
            iso639_1_from=detect(text)
            if len(iso639_1_from)>2:
                iso639_1_from=iso639_1_from[:2]
         
        if iso639_1_from in self.parentLanguageDictKeys:
            iso639_1_from=self.parentLanguageDict[iso639_1_from]
            
        if iso639_1_to in self.parentLanguageDictKeys:
            iso639_1_to=self.parentLanguageDict[iso639_1_to]
     
        if len(iso639_1_from)>2:
            raise ValueError("Source Language Code Cannot Be More Than 2 Characters")
        
        if iso639_1_from not in self.abbreviated_lang_codes:
            raise LanguageNotSupported("Source Language Not Supported Or Language Code Does Not Exist")
        
        if len(iso639_1_to)>2:
            raise ValueError("Translation Language Code Cannot Be More Than 2 Characters")
        
        if iso639_1_to not in self.abbreviated_lang_codes:
            raise LanguageNotSupported("Translation Language Not Supported Or Language Code Does Not Exist")
        
        # Getting MBART code from iso639 code
        self.tokenizer.src_lang=self.supported_languages[self.abbreviated_lang_codes.index(iso639_1_from)]
        
        
        encoded_ar = self.tokenizer(text, return_tensors="pt").to('cuda')
        
        generated_tokens = self.model.generate(
            **encoded_ar,
            forced_bos_token_id=self.tokenizer.lang_code_to_id[self.supported_languages[self.abbreviated_lang_codes.index(iso639_1_to)]]
        )
        
        return self.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        

    
if __name__=="__main__":
    mbart = MBartModel()
    result=mbart.translate(r"می‌خواهم مقدار عبارت زیر را پیدا کنم: $$ 5^{133} \mod 8. $$. متوجه شدم که   هنگامی که $n$ فرد است و در غیر اینصورت برابر 1 است، که من را به این نتیجه می‌رساند که $5^{133} \mod 8 = 5$ اما نمی‌دانم چگونه این را اثبات کنم. چگونه می‌توانم اثبات کنم که این اتفاق می‌افتد (یا اگر این اتفاق نمی‌افتد، راه‌حل دیگری را پیدا کنم)؟")
    print(result)
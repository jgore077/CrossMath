from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

class NLLBModel:

    def __init__(self) -> None:
        self.model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
        self.tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

    def translate(self, text: str, flores_from: str = None, flores_to: str = 'eng_Latn') -> str:

        translator = pipeline('translation', model=self.model, tokenizer=self.tokenizer, src_lang=flores_from,
                              tgt_lang=flores_to, max_length=1000, device=0)

        output = translator(text)

        return output[0]['translation_text']
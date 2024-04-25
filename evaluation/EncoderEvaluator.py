import csv
import sys
from pathlib import Path
import os
# Gain access to modules in parent directory
sys.path.append(str(Path(f"{__file__}").parent.parent))
from TranslationModel import TranslationModelInterface
from MaskedTranslationModel import MaskedTranslationModel,NLLBMaskedTranslationModel
import random
import string
from typing import re
import bs4
from sentence_transformers.cross_encoder.evaluation import CECorrelationEvaluator
from torch.utils.data import DataLoader
from sentence_transformers.cross_encoder import CrossEncoder
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses, util, models, evaluation
from post_parser_record import PostParserRecord
from sentence_transformers import InputExample, SentenceTransformer, losses, SentencesDataset
from topic_file_reader import TopicReader

class EncoderEvaluator():
    def __init__(self,translationModel:TranslationModelInterface,encoder:str,resultsPath,name):
        self.name=name
        self.resultsPath=resultsPath
        self.post_reader = PostParserRecord("evaluation/Posts.V1.3.xml")
        self.model=translationModel
        self.encoderString=encoder
        self.encoder = SentenceTransformer(encoder) if self.encoderString=='sentence-transformers/all-mpnet-base-v2' else CrossEncoder(encoder)
        self.globalLanguageCodeDictionary={
            "datasets/ces_Latn.tsv":"cs",
            "datasets/hin_Deva.tsv":"hi",
            "datasets/hrv_Latn.tsv":"hr",
            "datasets/npi_Deva.tsv":"ne",
            "datasets/pes_Arab.tsv":"fa",
            "datasets/spa_Latn.tsv":"es",
            "datasets/zho_Hans.tsv":"zh"
        }

    def read_topic_files(self,sample_file_path):
        result = {}
        print("Filepath: " + sample_file_path)
        lang_code=self.globalLanguageCodeDictionary.get(sample_file_path)
        print("Lang code: " + lang_code)
        with open(sample_file_path,'r',encoding='utf-8') as tsv:
            for line in tsv.readlines():
                fields=line.split('\t')
                print(fields[0])
                title=self.model.translate(fields[1], iso639_1_from=lang_code)
                body=self.model.translate(fields[2], iso639_1_from=lang_code)
                title = title.strip()
                body = body.strip()
                result[fields[0]] = title + " " + body  # (title, body)
        return result
    
    def read_qrel_files(self,candidate_answer_file):
        map_formulas = {}
        with open(candidate_answer_file, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                topic_id = row[0]
                answer_id = int(row[2])
                if topic_id in map_formulas:
                    map_formulas[topic_id].append(answer_id)
                else:
                    map_formulas[topic_id] = [answer_id]
        return map_formulas

    def read_corpus(self,topic_tsv_path):
        candidates = {}
        queries = self.read_topic_files(topic_tsv_path)
        candidate_answer_file = "evaluation/qrel_task1_2020.tsv"
        dic_candidates = self.read_qrel_files(candidate_answer_file)
        candidate_answer_file = "evaluation/qrel_task1_2021.tsv"
        dic_candidates.update(self.read_qrel_files(candidate_answer_file))
        candidate_answer_file = "evaluation/qrel_task1_2022.tsv"
        dic_candidates.update(self.read_qrel_files(candidate_answer_file))

        for topic in dic_candidates:
            temp = {}
            lst_answers = dic_candidates[topic]
            for answer_id in lst_answers:
                if answer_id not in self.post_reader.map_just_answers:
                    continue
                answer_body = self.post_reader.map_just_answers[answer_id].body
                temp[answer_id] = answer_body
            candidates[topic] = temp
        return queries, candidates
    
    def retrieval(self,topics_tsv_path):
        embedder = self.encoder
        final_result = {}
        print("model loaded")

        "This is an important part"
        queries, candidates = self.read_corpus(topics_tsv_path)
        print("corpus read")
        print("corpus encoded")
        for topic_id in queries:
            if topic_id not in candidates:
                continue
            query = queries[topic_id]
            query_embedding= embedder.encode(query) if self.encoderString=='sentence-transformers/all-mpnet-base-v2' else None
            result = {}
            for answer_id in candidates[topic_id]:
                answer = candidates[topic_id][answer_id]
                score= util.dot_score(query_embedding, embedder.encode([answer]))[0][0].item() if self.encoderString=='sentence-transformers/all-mpnet-base-v2' else  embedder.predict([(query, answer)])[0]
                result[answer_id] = score
            final_result[topic_id] = result
        return final_result

    
    
    def main(self):
        if not os.path.exists(self.resultsPath):
            os.mkdir(self.resultsPath)
   

        for file in os.listdir('datasets'):
            name=file.split('.')[0]
            print(f'Generating results for {name}')
            final_result = self.retrieval(f'datasets/{file}')
            cfile1 = open(f"{self.resultsPath}/{name}_retrieval_result_{self.encoderString.split('/')[1]}_a1.tsv", mode='w', newline='')
            cfile2 = open(f"{self.resultsPath}/{name}_retrieval_result_{self.encoderString.split('/')[1]}_a2.tsv", mode='w', newline='')
            cfile3 = open(f"{self.resultsPath}/{name}_retrieval_result_{self.encoderString.split('/')[1]}_a3.tsv", mode='w', newline='')

            csv_writer1 = csv.writer(cfile1, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer2 = csv.writer(cfile2, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer3 = csv.writer(cfile3, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for topic_id in final_result:
                topic_c = int(topic_id.split(".")[1])
                if topic_c <=100:
                    csv_writer = csv_writer1
                elif topic_c<=300:
                    csv_writer = csv_writer2
                else:
                    csv_writer = csv_writer3
                result_map = final_result[topic_id]
                result_map = dict(sorted(result_map.items(), key=lambda item: item[1], reverse=True))
                rank = 1
                for post_id in result_map:
                    score = result_map[post_id]
                    csv_writer.writerow([topic_id, "0", post_id, str(rank), str(score), f'{self.name}-{self.encoderString.split('/')[1]}'])
                    rank += 1
                    if rank > 1000:
                        break
            cfile1.close()
            cfile2.close()
            cfile3.close()
        
    
if __name__=="__main__":
    mbartcross=EncoderEvaluator(MaskedTranslationModel('QZ',50),'cross-encoder/qnli-distilroberta-base','evaluation/mbartcross','mbart')
    mbartcross.main()
    
    mbartbi=EncoderEvaluator(MaskedTranslationModel('QZ',50),'sentence-transformers/all-mpnet-base-v2','evaluation/mbartbi','mbart')
    mbartbi.main()
    
    nllbcross=EncoderEvaluator(NLLBMaskedTranslationModel('QZ'),'cross-encoder/qnli-distilroberta-base','evaluation/nllbcross','nllb')
    nllbcross.main()
    
    nllbbi=EncoderEvaluator(NLLBMaskedTranslationModel('QZ'),'sentence-transformers/all-mpnet-base-v2','evaluation/nllbbi','nllb')
    nllbbi.main()
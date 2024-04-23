"""
The codes for this crossencoder are from this page:  https://www.sbert.net/examples/training/cross-encoder/README.html

To train the CrossEncoder, I will be using qrel for task 1. I consider the pairs to be Question and Answer; from qrel
file.
"""
import csv
import sys
from pathlib import Path
import os
# Ensure evaluation code has access to loacl module `MaskedTranslationModel` in its parent directory
sys.path.append(str(Path(f"{__file__}").parent.parent))
from MaskedTranslationModel import MaskedTranslationModel, NLLBMaskedTranslationModel
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

globalLanguageCodeDictionaryBART={
    "datasets/ces_Latn.tsv":"cs",
    "datasets/hin_Deva.tsv":"hi",
    "datasets/hrv_Latn.tsv":"hr",
    "datasets/npi_Deva.tsv":"ne",
    "datasets/pes_Arab.tsv":"fa",
    "datasets/spa_Latn.tsv":"es",
    "datasets/zho_Hans.tsv":"zh"
}

globalLanguageCodeDictionaryNLLB={
    "datasets/ces_Latn.tsv":"ces_Latn",
    "datasets/hin_Deva.tsv":"hin_Deva",
    "datasets/hrv_Latn.tsv":"hrv_Latn",
    "datasets/npi_Deva.tsv":"npi_Deva",
    "datasets/pes_Arab.tsv":"pes_Arab",
    "datasets/spa_Latn.tsv":"spa_Latn",
    "datasets/zho_Hans.tsv":"zho_Hans"
}

os.environ["PYTORCH_USE_CUDA_DSA"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
csv_writer_Epochs = None
# Script is intended to be ran from parent directory
post_reader = PostParserRecord("evaluation/Posts.V1.3.xml")
BARTModel=MaskedTranslationModel('QZ',20)
NLLBModel=NLLBMaskedTranslationModel('QZ')
resultsPath='evaluation/results/'

def read_topic_files_BART(sample_file_path):
    result = {}
    lang_code=globalLanguageCodeDictionaryBART.get(sample_file_path)
    with open(sample_file_path,'r',encoding='utf-8') as tsv:
        for line in tsv.readlines():
            fields=line.split('\t')
            print(fields[0])
            title=BARTModel.translate(fields[1], iso639_1_from=lang_code)
            body=BARTModel.translate(fields[2], iso639_1_from=lang_code)
            title = title.strip()
            body = body.strip()
            result[fields[0]] = title + " " + body  # (title, body)
    return result


def read_topic_files_NLLB(sample_file_path):
    result = {}
    lang_code=globalLanguageCodeDictionaryNLLB.get(sample_file_path)
    with open(sample_file_path,'r',encoding='utf-8') as tsv:
        for line in tsv.readlines():
            fields=line.split('\t')
            print(fields[0])
            title=NLLBModel.translate(fields[1], flores_from=lang_code)
            body=NLLBModel.translate(fields[2], flores_from=lang_code)
            title = title.strip()
            body = body.strip()
            result[fields[0]] = title + " " + body  # (title, body)
    return result


def read_qrel_files(candidate_answer_file):
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


def read_corpus(topic_tsv_path, model):
    candidates = {}
    if model == "BART":
        queries = read_topic_files_BART(topic_tsv_path)
    if model == "NLLB":
        queries = read_topic_files_NLLB(topic_tsv_path)
    candidate_answer_file = "evaluation/qrels/qrel_task1_2020.tsv"
    dic_candidates = read_qrel_files(candidate_answer_file)
    candidate_answer_file = "evaluation/qrels/qrel_task1_2021.tsv"
    dic_candidates.update(read_qrel_files(candidate_answer_file))
    candidate_answer_file = "evaluation/qrels/qrel_task1_2022.tsv"
    dic_candidates.update(read_qrel_files(candidate_answer_file))

    for topic in dic_candidates:
        temp = {}
        lst_answers = dic_candidates[topic]
        for answer_id in lst_answers:
            if answer_id not in post_reader.map_just_answers:
                continue
            answer_body = post_reader.map_just_answers[answer_id].body
            temp[answer_id] = answer_body
        candidates[topic] = temp
    return queries, candidates


def retrieval(topics_tsv_path, model):
    embedder = CrossEncoder('cross-encoder/qnli-distilroberta-base')
    final_result = {}
    print("model loaded")

    "This is an important part"
    queries, candidates = read_corpus(topics_tsv_path, model)
    print("corpus read")
    print("corpus encoded")
    for topic_id in queries:
        if topic_id not in candidates:
            continue
        query = queries[topic_id]
        result = {}
        for answer_id in candidates[topic_id]:
            answer = candidates[topic_id][answer_id]
            scores = embedder.predict([(query, answer)])
            score = scores[0]
            result[answer_id] = score
        final_result[topic_id] = result
    return final_result


def main():
    if not os.path.exists(resultsPath):
        os.mkdir(resultsPath)
    for file in os.listdir('datasets'):
        name=file.split('.')[0]
        print(f'Generating results for {name}')

        # BART Model Translation
        final_result = retrieval(f'datasets/{file}', "BART")
        cfile1 = open(f"{resultsPath}/{name}_BART_retrieval_result_distilroberta_a1.tsv", mode='w', newline='')
        cfile2 = open(f"{resultsPath}/{name}_BART_retrieval_result_distilroberta_a2.tsv", mode='w', newline='')
        cfile3 = open(f"{resultsPath}/{name}_BART_retrieval_result_distilroberta_a3.tsv", mode='w', newline='')

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
                csv_writer.writerow([topic_id, "0", post_id, str(rank), str(score), "distilroberta_base"])
                rank += 1
                if rank > 1000:
                    break
        cfile1.close()
        cfile2.close()
        cfile3.close()

        # NLLB Model Translation
        final_result = retrieval(f'datasets/{file}', "NLLB")
        cfile1 = open(f"{resultsPath}/{name}_NLLB_retrieval_result_distilroberta_a1.tsv", mode='w', newline='')
        cfile2 = open(f"{resultsPath}/{name}_NLLB_retrieval_result_distilroberta_a2.tsv", mode='w', newline='')
        cfile3 = open(f"{resultsPath}/{name}_NLLB_retrieval_result_distilroberta_a3.tsv", mode='w', newline='')

        csv_writer1 = csv.writer(cfile1, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer2 = csv.writer(cfile2, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer3 = csv.writer(cfile3, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for topic_id in final_result:
            topic_c = int(topic_id.split(".")[1])
            if topic_c <= 100:
                csv_writer = csv_writer1
            elif topic_c <= 300:
                csv_writer = csv_writer2
            else:
                csv_writer = csv_writer3
            result_map = final_result[topic_id]
            result_map = dict(sorted(result_map.items(), key=lambda item: item[1], reverse=True))
            rank = 1
            for post_id in result_map:
                score = result_map[post_id]
                csv_writer.writerow([topic_id, "0", post_id, str(rank), str(score), "distilroberta_base"])
                rank += 1
                if rank > 1000:
                    break
        cfile1.close()
        cfile2.close()
        cfile3.close()


if __name__ == '__main__':
    main()
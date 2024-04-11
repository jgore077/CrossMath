"""
The codes for this crossencoder are from this page:  https://www.sbert.net/examples/training/cross-encoder/README.html

To train the CrossEncoder, I will be using qrel for task 1. I consider the pairs to be Question and Answer; from qrel
file.
"""
import csv
import random
import string
from typing import re
import os
import bs4
from sentence_transformers.cross_encoder.evaluation import CECorrelationEvaluator
from torch.utils.data import DataLoader
from sentence_transformers.cross_encoder import CrossEncoder
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, losses, util, models, evaluation
from post_parser_record import PostParserRecord
from sentence_transformers import InputExample, SentenceTransformer, losses, SentencesDataset

from topic_file_reader import TopicReader

os.environ["CUDA_VISIBLE_DEVICES"] = "0"
MODEL = "/mnt/netstore1_home/behrooz.mansouri/MiniLM_L6"#"model_qasim_rawtext_arqmath1T_rob_128_16"#"model_qasim_rawtext_arqmath1T_tiny_128_16"#model_qasim_rawtext_arqmath1T_tiny_256_16"
FILE_Epochs = "roberta_Epoch_TSV"  # "epoch_final_diss_arqmath12_T__roberta_256_16"
csv_writer_Epochs = None
post_reader = PostParserRecord("Posts.V1.3.xml")


def read_topic_files(sample_file_path):
    topic_reader = TopicReader(sample_file_path)
    result = {}
    for topic_id in topic_reader.map_topics:
        title = str(topic_reader.map_topics[topic_id].title)
        body = str(topic_reader.map_topics[topic_id].question)
        title = title.strip()
        body = body.strip()
        result[topic_id] = title + " " + body  # (title, body)
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


def read_corpus(topic_tsv_path):
    candidates = {}
    queries = read_topic_files(topic_tsv_path)
    candidate_answer_file = "qrel_task1_2020.tsv"
    dic_candidates = read_qrel_files(candidate_answer_file)
    candidate_answer_file = "qrel_task1_2021.tsv"
    dic_candidates.update(read_qrel_files(candidate_answer_file))
    candidate_answer_file = "qrel_task1_2022.tsv"
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


def retrieval():
    embedder = CrossEncoder('cross-encoder/qnli-distilroberta-base')
    final_result = {}
    print("model loaded")

    "This is an important part"
    queries, candidates = read_corpus()
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
    final_result = retrieval()
    with open("retrieval_result_distilroberta.tsv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for topic_id in final_result:
            result_map = final_result[topic_id]
            result_map = dict(sorted(result_map.items(), key=lambda item: item[1], reverse=True))
            rank = 1
            for post_id in result_map:
                score = result_map[post_id]
                csv_writer.writerow([topic_id, "0", post_id, str(rank), str(score), "distilroberta_base"])
                rank += 1
                if rank > 1000:
                    break


if __name__ == '__main__':
    main()

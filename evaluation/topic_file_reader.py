import csv
import xml.etree.ElementTree as ET

import numpy


class Topic:
    """
    This class shows a topic for task 1. Each topic has an topic_id which is str, a title and question which
    is the question body and a list of tags.
    """

    def __init__(self, topic_id, title, question, tags):
        self.topic_id = topic_id
        self.title = title
        self.question = question
        self.lst_tags = tags


class TopicReader:
    """
    This class takes in the topic file path and read all the topics into a map. The key in this map is the topic id
    and the values are Topic which has 4 attributes: id, title, question and list of tags for each topic.

    To see each topic, use the get_topic method, which takes the topic id and return the topic in Topic object and
    you have access to the 4 attributes mentioned above.
    """

    def __init__(self, topic_file_path):
        self.map_topics = self.__read_topics(topic_file_path)

    def __read_topics(self, topic_file_path):
        map_topics = {}
        tree = ET.parse(topic_file_path)
        root = tree.getroot()
        for child in root:
            topic_id = child.attrib['number']
            title = child[0].text
            question = child[1].text
            lst_tag = child[2].text.split(",")
            map_topics[topic_id] = Topic(topic_id, title, question, lst_tag)
        return map_topics

    def get_topic(self, topic_id):
        if topic_id in self.map_topics:
            return self.map_topics[topic_id]
        return None


def read_topics(file_path):
    map_formulas = {}
    with open(file_path) as csv_file:
        csvreader = csv.reader(csv_file, delimiter='\t')
        next(csvreader)
        for row in csvreader:
            formula_id = row[0]
            topic_id = row[1]
            if topic_id in map_formulas:
                map_formulas[topic_id].append(formula_id)
            else:
                map_formulas[topic_id] = [formula_id]
    return map_formulas


def separated_duplicate_related(file_path, related_path, duplicate_path):
    related_csv = open(related_path, "w", newline='')
    duplicated_csv = open(duplicate_path, "w", newline='')

    duplicate_csv_writer = csv.writer(duplicated_csv, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    related_csv_writer = csv.writer(related_csv, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    with open(file_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for row in spamreader:
            related = int(row[3])
            if related == 2:
                duplicate_csv_writer.writerow([row[0], row[1], row[2], "1"])
            else:
                related_csv_writer.writerow([row[0], row[1], row[2], "1"])
    related_csv.close()
    duplicated_csv.close()

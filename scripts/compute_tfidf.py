from os import remove
import os.path as osp
import json
import argparse
import math
import itertools
import csv 
from nltk.corpus import stopwords

script_dir = osp.dirname(__file__)

def main():
    
    # LOAD FILE USING INPUT AND OUTPUT FLAGS, REQUIRE THE INPUT TO BE IN DATA, WRITE OUTPUT TO DATA
    parser = argparse.ArgumentParser(description = 'Compute TF-IDF from CSV of words in title of post based on topic.')
    parser.add_argument('-o', '--output_file',  help = 'JSON with word counts.', required=True)
    parser.add_argument('filtered_data', help = 'CSV with author, title, and topic as data only mentioning candidates.')
    parser.add_argument('complete_data', help = 'CSV with author, title, and topic as data for all 2000 posts.')
    
    args = parser.parse_args()
    output_file = open(f'{args.output_file}', 'w')
    filtered_data = args.filtered_data
    complete_data = args.complete_data

    num_words = 10
    stop_words = set(stopwords.words('english'))
    topics = ['Government', 'Election', 'Regional', 'External', 'Opinion', 'Society']

    result = {}; word_frequency_by_topic = {}; topic_count = {}; final = {}
    result['Government'] = {}; result['Election'] = {}; result['Regional'] = {}; result['External'] = {}; result['Opinion'] = {}; result['Society'] = {}
    word_frequency_by_topic['Government'] = {}; word_frequency_by_topic['Election'] = {}; word_frequency_by_topic['Regional'] = {}
    word_frequency_by_topic['External'] = {}; word_frequency_by_topic['Opinion'] = {}; word_frequency_by_topic['Society'] = {}
    topic_count['Government'] = {}; topic_count['Election'] = {}; topic_count['Regional'] = {}
    topic_count['External'] = {}; topic_count['Opinion'] = {}; topic_count['Society'] = {}

    # CALCULATE THE NUMBER OF TOPICS EVERY TERM IS IN
    with open(complete_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for word in word_string:
                word = word.lower()
                for topic in topics:
                    topic_count[topic][word] = 0
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for word in word_string:
                word = word.lower()
                for topic in topics:
                    if topic == row[2]:
                        topic_count[topic][word] = 1

    # CALCULATE TERM FREQUENCY BY TOPIC
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for topic in topics:
                if topic == row[2]:
                    for word in word_string:
                        word = word.lower()
                        word_frequency_by_topic[topic][word] = 0
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)       
        for row in csv_reader:
            word_string = row[1].split(" ")
            for topic in topics:
                if topic == row[2]:
                    for word in word_string:
                        word = word.lower()
                        word_frequency_by_topic[topic][word] += 1
        
    # CALCULATE TF-IDF
    for topic in word_frequency_by_topic:
        for key, value in word_frequency_by_topic[topic].items():
            if key not in stop_words:
                term_frequency = value
                total_frequency = 0
                for i in topic_count:
                    if topic_count[i][key] == 1:
                        total_frequency += 1
                result[topic][key] = term_frequency * math.log(6 / total_frequency)

    # FORMAT AND DISPLAY AS DICTIONARY
    for topic in result:
        result[topic] = {key:value for key, value in sorted(result[topic].items(), key = lambda item:item[1], reverse = True)}
        result[topic] = dict(itertools.islice(result[topic].items(), num_words))
    for topic in result:
        key_iterable = result[topic].keys()
        key_list = list(key_iterable)
        final[topic] = key_list
    output_file.write(json.dumps(final, indent = 4))
    print(json.dumps(final, indent = 4))

if __name__ == '__main__':
    main()

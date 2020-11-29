from os import remove
import os.path as osp
import json
import argparse
import math
import itertools
import csv

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

    result = {}; word_count = {}; word_frequency_by_topic = {}
    result['Government'] = {}
    result['Election'] = {}
    result['Regional'] = {}
    result['External'] = {}
    result['Opinion'] = {}
    result['Society'] = {}
    word_frequency_by_topic['Government'] = {}
    word_frequency_by_topic['Election'] = {}
    word_frequency_by_topic['Regional'] = {}
    word_frequency_by_topic['External'] = {}
    word_frequency_by_topic['Opinion'] = {}
    word_frequency_by_topic['Society'] = {}
    topics = ['Government', 'Election', 'Regional', 'External', 'Opinion', 'Society']
    total_word_count = 0

    # CLEAN THE TWO DATASETS OF NON ALPHANUMERIC CHARACTERS
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            for word in row:
                for character in word:
                        if not character.isalnum() or character == ' ':
                            character = ''
    with open(complete_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            for word in row:
                for character in word:
                        if not character.isalnum() or character == ' ':
                            character = ''

    # CALCULATE THE TOTAL WORD COUNT AND TERM FREQUENCY OF ALL 2000 POSTS FOR INVERSE DOCUMENT FREQUENCY
    with open(complete_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for word in word_string:
                total_word_count += 1
    with open(complete_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for word in word_string:
                word_count[word] = 0
    with open(complete_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for word in word_string:
                word_count[word] += 1

    # CALCULATE TERM FREQUENCY BY TOPIC
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)
        for row in csv_reader:
            word_string = row[1].split(" ")
            for topic in topics:
                if topic == row[2]:
                    for word in word_string:
                        word_frequency_by_topic[topic][word] = 0
    with open(filtered_data, mode = 'r') as csvFile:
        csv_reader = csv.reader(csvFile)
        next(csv_reader)                    
        for row in csv_reader:
            word_string = row[1].split(" ")
            for topic in topics:
                if topic == row[2]:
                    for word in word_string:
                        word_frequency_by_topic[topic][word] += 1
        
    # CALCULATE TF_IDF
    for topic in word_frequency_by_topic:
        for key, value in word_frequency_by_topic[topic].items():
            term_frequency = value
            total_frequency = word_count[key]
            tfidf_score = term_frequency * (math.log(total_word_count / total_frequency))
            result[topic][key] = tfidf_score

    # FORMAT AND DISPLAY AS DICTIONARY
    for topic in result:
        result[topic] = {key:value for key, value in sorted(result[topic].items(), key = lambda item:item[1], reverse = True)}
        result[topic] = dict(itertools.islice(result[topic].items(), num_words))
    output_file.write(json.dumps(result, indent = 4))
    print(json.dumps(result, indent = 4))


if __name__ == '__main__':
    main()

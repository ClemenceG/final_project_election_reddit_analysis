from os import remove
import requests
import os.path as osp
import json
import sys
import argparse

script_dir = osp.dirname(__file__)

def main():

    # LOAD FILE USING INPUT AND OUTPUT FLAGS, REQUIRE THE INPUT TO BE IN DATA, WRITE OUTPUT TO DATA
    parser = argparse.ArgumentParser(description = 'Collect hottest posts in provided subreddit.')
    parser.add_argument('subreddit_source',  help = 'subreddit to collect data from.')
    parser.add_argument('-o', '--output_file',  help = 'JSON file to output to', required=True)

    args = parser.parse_args()
    input_file = args.subreddit_source
    output_file = open(f'{args.output_file}', 'w')

    # FETCH THE REDDIT DATA
    result = []
    headers = {'User-Agent': 'mac:requests (by /u/thomas)'}
    url = f"https://reddit.com/r/{input_file}/hot.json?show=all&t=all&limit=100&count=100&after="
    after = "none"

    # FUNCTION TO GET THE 'HOT' POSTS, 100 AT A TIME, 4 TOTAL REQUESTS CALLS
    for i in range(4):
        response = requests.get(url + after, headers=headers)
        data = response.json()
        after = data["data"]["after"]
        result.append(data)

    # FUNCTION TO GET THE DATA FROM THE REQUEST ARRAY INTO DESIRED FORMAT
    for line in result:
        for i in range(100):        
            json.dump(line['data']['children'][i], output_file)
            output_file.write("\n")

if __name__ == '__main__':
    main()
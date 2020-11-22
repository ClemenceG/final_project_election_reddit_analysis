import json
import argparse

def filter_wout_trump_biden(data):
    for post_info in data:
        post = post_info['data']
        if not(('trump' in post['selftext'].lower()) | ('biden' in post['selftext'].lower())
        | ('trump' in post['title'].lower()) | ('biden' in post['selftext'].lower())):
            data.remove(post_info)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input json formatted posts')
    parser.add_argument('-o', '--output_file', help='JSON file to output to', required=True)

    args = parser.parse_args()
    input_file = args.subreddit_source
    output_file = open(f'{args.output_file}', 'w')

    # load json file containing a post on each line
    with open(input_file) as f:
        data = [json.loads(line) for line in f]

    # filter out post without biden or trump mentionned in the title or the post
    result = filter_wout_trump_biden(data)
    


    for line in result:
        json.dump(line, output_file)
        output_file.write("\n")



if __name__ == '__main__':
    main()

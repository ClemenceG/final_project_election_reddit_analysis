import json
import argparse
import pandas as pd

def filter_wout_trump_biden(data):
    result = []
    for post_info in data:
        post = post_info['data']
        if ('trump' in post['selftext'].lower()) | ('biden' in post['title'].lower()) | \
                ('trump' in post['title'].lower()) | ('biden' in post['selftext'].lower()):
            result.append(post)
    return result


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='input json formatted posts')
    parser.add_argument('-o', '--output_file', help='JSON file to output to', required=True)

    args = parser.parse_args()
    input_fn = args.subreddit_source
    output_fn = args.output_file

    # load json file containing a post on each line
    with open(input_fn) as f:
        data = [json.loads(line) for line in f]

    # filter out post without biden or trump mentionned in the title or the post
    result = filter_wout_trump_biden(data)

    df_result = pd.DataFrame.from_records(result)
    df_result = df_result[['author', 'title', 'selftext']]

    df_result.to_csv(output_fn, index=False)


if __name__ == '__main__':
    main()

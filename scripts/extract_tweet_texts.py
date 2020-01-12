#!/usr/bin/env python
from argparse import ArgumentParser
import csv
from pathlib import Path
import re
from sys import stderr, stdout


def cleantext(text):
    """
    text is a string

    Returns: a string, sans newlines and consecutive+trailing whitespaces, and stripped of
        entities like usernames and urls
    """
    t = re.sub(r'\s+', ' ', text) # normalize whitespace
    t = strip_retweet_meta(t)
    t = strip_urls(t)
    t = strip_leading_usernames(t)
    t = strip_trailing_hashtags(t)
    return re.sub(r'\s+', ' ', t).strip()  # and normalize whitespace one more time for fun



def extract_tweet_texts(tweets):
    """
    Given a list of tweets with full attributes, yields only the cleaned-up normalized tweet texts

    `tweets`: a list of dicts, with attribute `text`

    Yields: a list of strings
    """
    for t in tweets:
        yield cleantext(t['text'])


def filter_by_tweet_types(tweets, remove_retweets=True, remove_replies=False):
    """
    From a list of all tweets, removes retweets and replies if desired. Quote tweets are considered "original".

    `tweets`: a list of dicts, with attribute `tweet_type` that has key values of: 'original', 'retweet', 'reply', 'quote'

    Returns: a list of dicts
    """
    fweets = []
    for t in tweets:
        if (t['tweet_type'] in ['original', 'quote'] or
            (t['tweet_type'] == 'retweet' and remove_retweets != True) or
            (t['tweet_type'] == 'reply' and remove_replies != True)):

            fweets.append(t)
    return fweets


def strip_urls(text):
    """
    `text` is a single-line string, 'check out https://t.co/123456 http://t.co/123456 and also https://example.com'

    Returns: a string, 'check out   and also '
    """
    return re.sub(r'https?:\S+', '', text)


def strip_leading_usernames(text):
    """
    Removes username of user replied to; does not remove .@username addressing, e.g. '.@jack knows my name'


    `text` is a single-line string, '@jack @jill cool idea, I wonder if @humpty agrees'

    Returns: a string, sans leading @usernames, 'cool idea, I wonder if @humpty agrees'
    """
    return re.sub(r'^(?:@\w+\s+)+', '', text)

def strip_retweet_meta(text):
    """
    `text` is a single-line string, 'RT @jack: hello people'

    Returns: a string, 'hello people'
    """

    return re.sub(r'^RT @\w+: +', '', text)

def strip_trailing_hashtags(text):
    """
    `text` is a single-line string, 'Hey #bitcoin lovers, whats up? #bored #bitcoin'

    Returns: a string, sans trailing hashtags: 'Hey #bitcoin lovers, whats up? '
    """
    return re.sub(r'(?:#\w+\s*)+$', '', text)




def process_file(srcfile, remove_retweets, remove_replies):
    """
    `srcfile` is a CSV filename

    Returns: a list of strings; removes blank lines
    """
    stderr.write(f"\nReading {srcfile}\n")
    with open(srcfile) as src:
        tweets = list(csv.DictReader(src))
        stderr.write(f"\t{len(tweets)} tweets found\n")

    fweets = filter_by_tweet_types(tweets, remove_retweets=remove_retweets, remove_replies=remove_replies)
    stderr.write(f"\t{len(fweets)} filtered tweets (remove_retweets: {remove_retweets} remove_replies: {remove_replies})\n")

    texts = [text for text in extract_tweet_texts(fweets) if text]
    stderr.write(f"\t{len(texts)} non-blank tweet texts\n")
    stderr.write("\t---\n")
    return texts




def main():
    parser = ArgumentParser(description="Given an input CSV of tweets, filter and extract just the tweet texts (to stdout)")
    parser.add_argument('input_file', help='''Input path; can be filename or directory full of CSVs''')
    parser.add_argument('--destdir', action="store", default="", help='''If input path is a directory of CSVs, supply the destination directory for resulting extracts''')
    parser.add_argument('--remove-retweets', action="store_true", default=True)
    parser.add_argument('--remove-replies', action="store_true", default=False)
    args = parser.parse_args()

    input_path = Path(args.input_file)
    # process single file and print to stdout
    if input_path.is_file():
        srcfiles = [input_path]
    # process directory of files, and write to files in destdir
    elif input_path.is_dir():
        srcfiles = sorted(input_path.glob("*.csv"))
        stdout.write(f"\nFound {len(srcfiles)} CSV files in: {input_path}\n")

        # if not args.destdir:
        #     raise ValueError(f"Since {input_path} is a directory, you must supply --destdir parameter\n")
    else:
        raise ValueError(f"{input_path} is not a valid filename or directory")


    if args.destdir:
        destdir = Path(args.destdir)
        destdir.mkdir(parents=True, exist_ok=True)
    else:
        destdir = False

    for srcpath in srcfiles:
        if destdir:
            destpath = destdir.joinpath(f"{srcpath.stem}.txt")
            outs = open(destpath, 'w')
        else:
            destpath = False
            outs = stdout

        # write to file
        for text in process_file(srcpath, remove_retweets=args.remove_retweets, remove_replies=args.remove_replies):
            outs.write(f"{text}\n")

        # close if not stdout
        if destpath:
            stdout.write(f"\tWrote to: {destpath}\n")
            outs.close()



if __name__ == '__main__':
    main()

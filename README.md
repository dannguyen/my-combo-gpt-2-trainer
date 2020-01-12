# simple combo-gpt2-bot


## Thanks/Credits

https://github.com/minimaxir/gpt-2-simple


## Collection

Use **twarc**

```sh
$ mkdir -p data/collected/tweets/
$ twarc timeline pontifex --format csv > data/collected/tweets/pontifex-tweets.csv

```


## Extraction

```sh
$ ./scripts/extract_tweet_texts.py data/collected/tweets --destdir data/extracted/tweets
```

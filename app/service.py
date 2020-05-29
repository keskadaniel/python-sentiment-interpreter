import logging
import re
from bs4 import BeautifulSoup
import interpreter
import sentiment_entity as entity

logger = logging.getLogger(__name__)


def calculate(data):
    id = data['id']
    if id is not None:
        entity.Sentiment.id = id
    else:
        raise ValueError("There is no Id in json!")

    header = data['header']
    summary = data['summary']
    body = data['body']
    content = join_content(header, summary, body)
    cleaned_content = clean_content(content)
    result = interpreter.analyze_sentiment(cleaned_content, id)

    if result == 1:
        entity.Sentiment.result = 'POSITIVE'
    if result == 0:
        entity.Sentiment.result = 'NEUTRAL'
    if result == 2:
        entity.Sentiment.result = 'NEGATIVE'
    return entity.Sentiment


def join_content(header, summary, body):
    content = ''
    try:
        content = header + ' ' + summary + ' ' + body
    except ValueError as e:
        logging.exception("Wrong json format!")
    return content


def remove_shorts(word):
    array = word.split(' ')
    new_array = ''
    for x in range(0, len(array)):
        if len(array[x]) < 3:
            new_array += ' '
        else:
            new_array += array[x] + ' '
    return str(new_array)


def clean_content(content):
    # remove html
    content = BeautifulSoup(content, features="html.parser").get_text()
    # remove hashes and @
    content = ' '.join(re.sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", " ", content).split())
    # remove web addressees
    content = ' '.join(re.sub("(\w+:\/\/\S+)", " ", content).split())
    # remove punctuation
    content = ' '.join(re.sub("[\.\,\!\?\:\;\-\=\()\+\'\"\/\*\_]", " ", content).split())
    # remove words with less than 3 chars
    # content = remove_shorts(content)
    # to lowercase
    content = content.lower()
    # remove digits
    content = re.sub(r"\d+", ' ', content)
    # remove single signs
    content = re.sub(r'(?:^| )\w(?:$| )', ' ', content)
    # remove many spaces
    content = re.sub(' +', ' ', content)
    # print('cleaned ', document)
    return content

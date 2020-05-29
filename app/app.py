from flask import Flask, request
import sentiment_entity, service
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def main():
    return {'go to': '/sentiment'}


@app.route('/sentiment', methods=['POST'])
def sentiment():
    data = request.get_json()
    sentiment_entity.Sentiment = service.calculate(data)
    return {'id': sentiment_entity.Sentiment.id,
            'sentiment': sentiment_entity.Sentiment.result
            }


if __name__ == '__main__':
    app.run(host='0.0.0.0')

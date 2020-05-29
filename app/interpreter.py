import json
import numpy as np
import tensorflow
from tensorflow.python import keras
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import load_model
import logging

logger = logging.getLogger(__name__)

logger.info('Keras version %s', keras.__version__)

MODEL_PATH = 'assets/enriched_model_03_04.h5'
model = load_model(MODEL_PATH)
logger.info('*** Model loaded ***')

TOKENIZER_PATH = 'assets/enriched_tokenizer_03_04.json'
with open(TOKENIZER_PATH) as f:
    data = json.load(f)
    tokenizer = tokenizer_from_json(data)
    logger.info('*** Tokenizer loaded ***')


def analyze_sentiment(value_to_predict, document_id):
    logger.debug('Predicting sentiment for sentence: %s', value_to_predict)
    dt = [value_to_predict]
    data_array = np.array(dt)

    logger.debug('Transforming words array into Vectors')
    sequences_test = tokenizer.texts_to_sequences(data_array)
    x_val = sequence.pad_sequences(sequences_test, maxlen=50)

    prediction = model.predict(x_val, batch_size=1)
    sentiment_value = np.argmax(prediction)
    logger.info('documentId: %s; predicted array: %s; calculated sentiment: %s'
                , document_id, prediction, sentiment_value)
    return sentiment_value

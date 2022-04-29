import os
import psutil
from datetime import datetime
from typing import Union

from flask import Flask, request

from post import Post

# define Flask web app
app = Flask(__name__)


def run_chatterbox(post):
    """
    Given the incoming POST request, construct the chatterbox command to be executed and execute it.
    :param post: the incoming POST request to process
    :return:
    """

    if post.operation == 'SYNC':
        response = post.process_sync()
        return response

    elif post.operation == 'ASYNC':
        response = post.process_async()
        return response

    return post.BAD_POST_REQUEST


def parse_post_request(post_request):
    print('POST request body:\n', post_request)

    # instantiate Post object
    post = Post(post_request, datetime.now())

    response = {}

    if post.request_is_valid():
        # todo post.add_to_queue()
        # execute chatterbox using POST request body
        response = run_chatterbox(post)

    return response


def process_get_request(get_request):
    pass


def process_delete_request(delete_request):
    pass


def is_valid_json():
    return request.get_json() is not None


@app.route('/text', methods=['GET', 'POST'])
def process_text_request() -> Union[int, dict]:
    if request.get_json() is None:
        return 400  # if the request is NOT valid json then return error code 400

    # if we get here we definitely received valid json
    if request.method == 'POST':
        response = parse_post_request(request.get_json())

    elif request.method == 'GET':
        # response = parse_get_request(request)
        pass

    return response


@app.route('/model', methods=['GET'])
def process_model_request():
    response = """['tts_models.en.ek1.tacotron2',
                'tts_models.en.ljspeech.tacotron2-DDC',
                'tts_models.en.ljspeech.glow-tts',
                'tts_models.en.ljspeech.fast_pitch']"""

    return response


@app.route('/model/<id>', methods=['GET'])
def process_model_id_request():
    pass
    # return response


@app.route('/health', methods=['GET'])
def process_health_request():

    process = psutil.Process(os.getpid())
    response = {'healthy': 'true',
                'memoryUsage': process.memory_info().rss}  # in bytes

    return response


# todo - how to handle dynamic request e.g. /model/{id}


app.run(debug=True)  # threaded=True

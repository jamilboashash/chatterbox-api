from datetime import datetime
from typing import Union

from flask import Flask, request, make_response, Response
from post import Post
from postRequest import PostRequest, process_sync, process_async
import subprocess

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

    return 400


def parse_post_request(post_request):
    print('POST request body:\n', post_request)

    # instantiate Post object
    post = Post(post_request, datetime.now())

    response = {}

    if post.request_is_valid():
        # todo post.add_to_queue()
        # execute chatterbox using POST request body
        response = run_chatterbox(post)

    # if operation == 'SYNC':
    #     process_sync()
    #
    # elif operation == 'ASYNC':
    #     process_async()
    # else:
    #     # todo - clarify with tutor how to handle this case - exit_with_code(Exit.BAD_OPERATION) ?
    #     pass

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
    pass


@app.route('/health', methods=['GET'])
def process_health_request():
    pass


# todo - how to handle dynamic request e.g. /model/{id}


app.run(debug=True)  # threaded=True

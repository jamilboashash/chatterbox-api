from typing import Union

from flask import Flask, request, make_response
from postRequest import PostRequest, process_sync, process_async
from postResponse import PostResponse
import subprocess
import requests
import json

# define Flask web app
app = Flask(__name__)


def construct_command(post_request) -> list[str]:
    """
    Given the /text POST request, construct the chatterbox command to be executed
    :param post_request: the incoming POST request to process
    :return:
    """

    command = ['chatterbox', 'run']

    # extract json data from request object

    # --model
    if 'model' in post_request:
        model = post_request['model'].replace('.', '/')
        command.extend(['--model', model])

    # --input-file
    # create new file and write 'message' contents into it, then give the filename to 'command'
    filename = 'chatterbox-testing/test.in'
    with open(filename, 'x') as file:
        file.write(post_request['message'])
    command.extend(['--input-file', filename])

    # --out-path (leaving blank for default)
    # --run-id todo - confirm details with tutors and implement!

    return command


def run_chatterbox(post_request):
    """
    Given the incoming POST request, construct the chatterbox command to be executed and execute it.
    :param post_request: the incoming POST request to process
    :return:
    """
    command = construct_command(post_request)
    print('command: ', command)

    subprocess.run(command)

    print('subprocess finished...', flush=True)


def post_request_is_valid(post_request) -> bool:

    # make sure the request body is valid
    print('Request arg:\n', post_request['message'])

    if (1 <= len(post_request['message']) <= 280) and (post_request['operation'] == 'SYNC'):
        print('This must be a SYNC operation')
        return True
    elif (len(post_request['message']) > 280) and (post_request['operation'] == 'ASYNC'):
        print('This must be an ASYNC operation')
        return True
    else:
        return False

    # request is valid - assign values to postRequest class
    # post_req = PostRequest(message, operation)


def parse_post_request(post_request):

    print('POST request body:\n', post_request)

    if post_request_is_valid(post_request):
        # execute chatterbox using POST request body
        run_chatterbox(post_request)

    # instantiate Text object and PostResponse object
    # text = Text(message, operation, model)

    # response = PostResponse(1, text, 'COMPLETED', './out/*.wav', os.path.getmtime('./out/*.wav'))

    # if operation == 'SYNC':
    #     process_sync()
    #
    # elif operation == 'ASYNC':
    #     process_async()
    # else:
    #     # todo - clarify with tutor how to handle this case - exit_with_code(Exit.BAD_OPERATION) ?
    #     pass

    return "Generic Test Response! "  # response


def process_get_request(get_request):
    pass


def process_delete_request(delete_request):
    pass


def is_valid_json():
    return request.get_json() is not None


@app.route('/text', methods=['GET', 'POST'])
def process_text_request() -> Union[int, str]:

    if request.get_json() is None:
        return 400  # if the request is NOT valid json then return error code 400

    response = None

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

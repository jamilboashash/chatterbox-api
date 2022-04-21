from flask import Flask
from flask import request
from text import Text, process_sync, process_async
from response import PostResponse
import subprocess

# define Flask web app
app = Flask(__name__)


def construct_command(post_request) -> list[str]:
    """
    Given the /text POST request, construct the chatterbox command to be executed
    :param post_request: the incoming POST request to process
    :return:
    """

    # extract json data from request object
    message = post_request['message']
    # operation = post_request['operation']
    # model = post_request['model']

    # create new file and write 'message' contents into it, then give the filename to 'command'
    filename = 'chatterbox-testing/test.in'
    with open(filename, 'x') as file:
        file.write(message)

    command = ['chatterbox', 'run', '--input-file', filename]

    # command = ['chatterbox', 'run',
    #            '--input-file', filename,
    #            '--output-path', 'chatterbox-testing/out/',
    #            '--run-id', '001']

    return command


def run_chatterbox(post_request):
    """
    Given the incoming POST request, construct the chatterbox command to be executed and execute it.
    :param post_request: the incoming POST request to process
    :return:
    """
    command = construct_command(post_request)
    print('command: ', command)
    print('command type: ', type(command))

    subprocess.run(command)

    print('subprocess finished...', flush=True)



def process_post_request(post_request):

    print('POST request body:\n', post_request)

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


@app.route('/text', methods=['GET', 'POST'])
def parse_request():

    if request.method == 'POST':
        response = process_post_request(request.json)

    elif request.method == 'GET':
        # response = process_get_request(request.json)
        pass

    elif request.method == 'DELETE':
        # response = process_delete_request(request.json)
        pass

    else:
        # todo - check with tutor how to handle this case
        pass

    return response


app.run(debug=True)  # threaded=True

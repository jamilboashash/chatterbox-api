from flask import Flask
from flask import request
from text import Text, process_sync, process_async
from response import PostResponse
import os

# define Flask web app
app = Flask(__name__)


def process_post_request(post_request):

    print(post_request)

    # extract json data from request object
    message = post_request['message']
    operation = post_request['operation']
    model = post_request['model']

    # instantiate Text object and PostResponse object
    text = Text(message, operation, model)

    # write message to file
    with open("test.msg", "x") as file:
        file.write(message)

    exec(f'chatterbox run --input-file test.msg')

    print('chatterbox finished running...')

    response = PostResponse(1, text, 'COMPLETED', './out/*.wav', os.path.getmtime('./out/*.wav'))

    # if operation == 'SYNC':
    #     process_sync()
    #
    # elif operation == 'ASYNC':
    #     process_async()
    # else:
    #     # todo - clarify with tutor how to handle this case - exit_with_code(Exit.BAD_OPERATION) ?
    #     pass

    return "Response: That worked!!! ", response


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


app.run(debug=True)

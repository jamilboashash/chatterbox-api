from flask import Flask
from flask import request
from text import Text, process_sync, process_async
# from exit import Exit

# define Flask web app
app = Flask(__name__)


def process_post_request(post_request):

    print(post_request)

    # extract json data from request object
    message = post_request['message']
    operation = post_request['operation']
    model = post_request['model']

    # define text object
    text = Text(message, operation, model)

    if operation == 'SYNC':
        process_sync()
    elif operation == 'ASYNC':
        process_async()
    else:
        # todo - clarify with tutor how to handle this case
        #  exit_with_code(Exit.BAD_OPERATION)
        pass

    return "Response: That worked!!!"


@app.route('/text', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        response = process_post_request(request.json)

    return response


app.run(debug=True)

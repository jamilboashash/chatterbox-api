import glob
import itertools
import json
import os
import subprocess


class Post:
    id_iter = itertools.count()
    BAD_POST_REQUEST = 400

    def __init__(self, post_request, created_at):
        self.request_id = self.id_iter
        self.message = post_request['message']
        self.operation = post_request['operation']
        if 'model' in post_request:
            self.model = post_request['model']
        else:
            self.model = 'tts_models/en/ljspeech/glow-tts'  # chatterbox default model
        self.status = None
        self.resource = None
        self.created_at = created_at
        self.processed_at = None
        self.error = None

    def generate_response(self, message, operation, model, status, resource, created_at, processed_at, error):
        response = {"id": str(next(self.id_iter)),
                    "message": message,
                    "operation": operation,
                    "model": model,
                    "status": status,
                    "resource": resource,
                    "created_at": created_at,
                    "processed_at": processed_at,
                    "error": error}
        return response

    def construct_command(self) -> list[str]:
        """
        Construct the chatterbox command to be executed
        :return:
        """
        command = ['chatterbox', 'run']

        # --model argument
        model = self.model.replace('.', '/')
        command.extend(['--model', model])

        print(command)

        # --input-file argument
        # create new file and write 'message' contents into it, then give the filename to 'command'
        filename = './message.in'
        with open(filename, 'w') as file:
            file.write(self.message)
        command.extend(['--input-file', filename])

        # --out-path argument (leaving blank for default)
        # --run-id argument todo - confirm details with tutors and implement!

        print('command: ', command)

        return command

    def construct_response(self):

        # read json file
        files = glob.glob('out/*.json')
        latest = max(files, key=os.path.getctime)
        print('Latest file:\n', latest)
        with open(latest, 'r') as file:
            json_file = json.load(file)

        print('json file:\n', json_file)
        # process_json_file(json_file)

        self.status = 'COMPLETED'  # todo - implement properly
        if 'result' in json_file:
            self.resource = json_file['result']['wav']
            print('Resource:\n', json_file['result']['wav'])
        self.processed_at = os.path.getctime(latest)

        if 'error' in json_file:
            self.error = json_file['result']['error']
            print('Error:\n', self.error)

        # example = {"id": "2bf02bea-c0fd-43ee-b5f0-77e7117b2261",
        #            "message": "Hello, CSSE6400!",
        #            "operation": "SYNC",
        #            "model": "tts_models.en.ljspeech.glow-tts",
        #            "status": "COMPLETED",
        #            "resource": "http://storage:4566/chatterbox-texts/2bf02bea-c0fd-43ee-b5f0-77e7117b2261.wav",
        #            "created_at": "2022-04-26T07:22:10.467Z",
        #            "processed_at": "2022-04-26T07:22:19.171Z",
        #            "error": 'null'}

        response = self.generate_response(self.message, self.operation, self.model, self.status,
                                          self.resource, self.created_at, self.processed_at, self.error)

        return str(response)

    def request_is_valid(self) -> bool:
        """
        Make sure the request body is valid.
        :return:
        """

        print('Length of message:\n\t', len(self.message))

        if (0 < len(self.message) <= 280) and (self.operation == 'SYNC'):
            print('SYNC POST /text request is valid...', flush=True)
            return True

        elif (len(self.message) > 280) and (self.operation == 'ASYNC'):
            print('ASYNC POST /text request is valid...', flush=True)
            return True

        # todo - validate the model field

        return False

    def process_sync(self):

        command = self.construct_command()
        subprocess.run(command)
        print('subprocess finished...', flush=True)
        self.clean_up()
        response = self.construct_response()
        return response

    def process_async(self):
        # todo - process asynchronously
        pass

    def clean_up(self):
        # todo - delete temp/message.in file
        pass

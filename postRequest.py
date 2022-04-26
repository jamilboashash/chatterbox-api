def process_sync():
    print('Received a SYNC operation \nExecuting chatterbox')

    exec('chatterbox')


def process_async():
    print('Received a SYNC operation')


class PostRequest:

    valid_operations = ['SYNC', 'ASYNC']
    valid_models = ['', 'tacotron', 'tacotron2', 'glow-tts', 'speedy-speech',
                    'align-tts', 'fastpitch', 'fastspeech', 'vits']

    def __init__(self, message: str, operation: str):
        self.id = 1  # todo - needs to be dynamically generated
        self.message = message
        self.operation = operation
        self.model = None

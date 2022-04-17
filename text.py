def process_sync():
    print('Received a SYNC operation \nExecuting chatterbox')

    exec('chatterbox')


def process_async():
    print('Received a SYNC operation')


class Text:

    def __init__(self, message, operation, model):
        self.message = message
        self.operation = operation
        self.model = model



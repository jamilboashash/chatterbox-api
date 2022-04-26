import itertools


class PostResponse:

    id_iter = itertools.count()

    def __init__(self, text, status, resource, created_at, processed_at):
        self.request_id = next(self.id_iter),
        self.text = text,
        self.status = status,
        self.resource = resource,
        self.created_at = None,
        self.processed_at = None
        self.error = None




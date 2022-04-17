import sys
from enum import Enum


class Exit(Enum):
    BAD_OPERATION = 1
    SOMETHING_ELSE = 2

    def __init__(self):
        pass

def exit_with_code(exit_code: Enum) -> None:
    """
    todo - doco
    todo - test these exit codes
    :return:
    """
    exit_msg = ['Bad Operation in POST request. Must be either SYNc or ASYNC',
                'Over 280 characters and not ASYNC message']

    print(exit_msg[exit_code], file=sys.stderr)
    exit(exit_code)

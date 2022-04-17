
class ExitStatus:

    def __init__(self):
        pass

    def exit_with_code(exit_code: int) -> None:
        exit_msg = ['Over 280 characters and not ASYNC message']

        print(exit_msg[exit_code])

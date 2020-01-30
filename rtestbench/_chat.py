"""A message shaper for communication between app and user.

Defines private functions that create the messages.
Defines classes for interactions with user on a specific channel.
"""


def _create_welcome_message() -> str:
    message = ("\n\n\n"
               "============================\n"
               "   Welcome to R-testbench   \n"
               "============================\n\n")
    return message

def _create_goodbye_message() -> str:
    message = ("\n\n"
               "============================\n"
               "            Bye!            \n"
               "============================\n")
    return message

def _create_ready_message() -> str:
    return "R-testbench is ready for use!\n'"


class TerminalChat(object):
    """A class for sending messages to the user through the terminal."""

    def say_welcome(self):
        welcome_message = _create_welcome_message()
        print(welcome_message)
    
    def say_goodbye(self):
        goodbye_message = _create_goodbye_message()
        print(goodbye_message)
    
    def say_ready(self):
        ready_message = _create_ready_message()
        print(ready_message)

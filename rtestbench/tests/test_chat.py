"""Unit tests for the _chat module."""


import pytest

import rtestbench._chat as chat


@pytest.fixture
def terminal_chat():
    """Returns a TerminalChat object."""

    return chat.TerminalChat()


def test_create_welcome_message():
    """Tests that the welcome message is not empty."""

    assert chat._create_welcome_message()

def test_create_goodbye_message():
    """Tests that the goodbye message is not empty."""

    assert chat._create_goodbye_message()

def test_create_ready_message():
    """Tests that the ready message is not empty."""

    assert chat._create_ready_message()

def test_say_welcome(capsys, terminal_chat):
    terminal_chat.say_welcome()
    assert capsys.readouterr().out == chat._create_welcome_message() + '\n'

def test_say_goodbye(capsys, terminal_chat):
    terminal_chat.say_goodbye()
    assert capsys.readouterr().out == chat._create_goodbye_message() + '\n'

def test_say_ready(capsys, terminal_chat):
    terminal_chat.say_ready()
    assert capsys.readouterr().out == chat._create_ready_message() + '\n'

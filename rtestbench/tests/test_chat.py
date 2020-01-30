"""Unit tests for the _chat module."""


import pytest

import rtestbench._chat as chat


def test_create_welcome_message():
    """Tests that the welcome message is not empty."""

    assert chat._create_welcome_message()

def test_create_goodbye_message():
    """Tests that the goodbye message is not empty."""

    assert chat._create_goodbye_message()

def test_create_ready_message():
    """Tests that the ready message is not empty."""

    assert chat._create_ready_message()

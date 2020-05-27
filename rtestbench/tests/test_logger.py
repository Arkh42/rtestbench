"""Unit tests for the _logger module."""


import pytest
from logging import DEBUG, INFO, WARNING

import rtestbench._logger as log


def test_make_logger_default():

    logger = log.make_logger()

    assert logger.name == "rtestbench._logger"
    assert logger.level == DEBUG

    assert logger.handlers[0].level == INFO
    assert logger.handlers[1].level == DEBUG


def test_make_logger_verbose():
    """Tests that the verbose logger has the correct name and levels."""

    logger = log.make_logger('toto_verb', verbose=True)

    assert logger.name == 'toto_verb'
    assert logger.level == DEBUG

    assert logger.handlers[0].level == INFO
    assert logger.handlers[1].level == DEBUG

def test_make_logger_nonverbose():
    """Tests that the non-verbose logger has the correct name and levels."""

    logger = log.make_logger('toto_nverb', verbose=False)

    assert logger.name == 'toto_nverb'
    assert logger.level == DEBUG

    assert logger.handlers[0].level == WARNING
    assert logger.handlers[1].level == DEBUG

"""Test for the _meta module."""


import pytest
import json

import rtestbench._meta as meta


# json datasets
JSON_DATA_1_ELEM = {"Tester": "A. Quenon"}
JSON_DATA_MULTI_ELEM = {
    "Tester": "A. Quenon",
    "Values": [1.0, 2.0]
}
RUN_LABEL = "A test run"
TIMESTAMP_LABEL = "Timestamp: test started"


@pytest.fixture
def meta_man(tmp_path):
    """Returns a MetaDataManager."""

    d = tmp_path / "json"
    d.mkdir()

    f = d / "meta_file"
    man = meta.MetaDataManager(f)

    return man


def test_initialize(meta_man):
    """Checks that the json file is created at initialization."""

    fpath = meta_man._file_path
    del meta_man

    assert fpath.exists()


def test_get_timestamp():
    #TODO


@pytest.mark.parametrize("json_data", [JSON_DATA_1_ELEM, JSON_DATA_MULTI_ELEM])
def test_dump_meta(meta_man, json_data):
    """Checks that data are correctly dumped into file and can be loaded as is after 
        closing the file and reopening it for read."""
    
    meta_man.dump_meta(json_data)
    meta_man._file_stream.close()

    with open(meta_man._file_path) as f:
        assert json.load(f) == json_data


def test_dump_timestamp(meta_man):
    meta_man.dump_timestamp(TIMESTAMP_LABEL)
    meta_man._file_stream.close()

    with open(meta_man._file_path) as f:
        read_data = json.load(f)
        assert TIMESTAMP_LABEL in read_data.keys()
        for timestamp in read_data.values():
            assert timestamp.count('-') == 2
            assert timestamp.count('T') == 1
            assert timestamp.count(':') >= 2


def test_dump_run_info(meta_man):
    meta_man.dump_run_info(number=42, description=RUN_LABEL)
    meta_man._file_stream.close()

    with open(meta_man._file_path) as f:
        read_data = json.load(f)
        assert "Run" in read_data.keys()
        assert "Number" in read_data["Run"].keys()
        assert "Timestamp" in read_data["Run"].keys()
        assert "Info" in read_data["Run"].keys()
        assert read_data["Run"]["Number"] == 42
        assert read_data["Run"]["Info"] == RUN_LABEL

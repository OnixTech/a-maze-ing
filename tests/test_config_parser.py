import os
import tempfile
from pathlib import Path

import pytest

from src.config_parser import ConfigParser, ParserError


# Utility: write a config to a temp file
def write_config(content: str) -> str:
    tf = tempfile.NamedTemporaryFile("w+", delete=False)
    tf.write(content)
    tf.flush()
    return tf.name


# --- TESTS ---


def test_valid_config(tmp_path: Path) -> None:
    config_text = """
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=7,8
OUTPUT_FILE={}
PERFECT=True
""".format(tmp_path / "maze_out.txt")
    fname = write_config(config_text)
    try:
        parser = ConfigParser(fname)
        config = parser.load()
        assert parser.width == 15
        assert parser.height == 12
        assert parser.entry == (0, 0)
        assert parser.exit == (7, 8)
        assert not parser.perfect or config["PERFECT"] == "True"
    finally:
        os.unlink(fname)


def test_missing_key() -> None:
    config_text = """
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=7,8
OUTPUT_FILE=maze.txt
"""
    fname = write_config(config_text)
    try:
        parser = ConfigParser(fname)
        with pytest.raises(ParserError) as exc:
            parser.load()
        assert "Missing key" in str(exc.value)
    finally:
        os.unlink(fname)


def test_unknown_key() -> None:
    config_text = """
WIDTH=15
HEIGHT=12
ENTRY=0,0
EXIT=7,8
OUTPUT_FILE=maze.txt
PERFECT=True
ALIEN=42
"""
    fname = write_config(config_text)
    try:
        parser = ConfigParser(fname)
        with pytest.raises(ParserError) as exc:
            parser.load()
        assert "Unknown key" in str(exc.value)
    finally:
        os.unlink(fname)


def test_non_integer_width() -> None:
    config_text = """
WIDTH=foo
HEIGHT=12
ENTRY=0,0
EXIT=7,8
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    fname = write_config(config_text)
    try:
        parser = ConfigParser(fname)
        with pytest.raises(ParserError) as exc:
            parser.load()
        assert "WIDTH must be integer" in str(exc.value)
    finally:
        os.unlink(fname)


def test_extraneous_value_line() -> None:
    config_text = """
WIDTH=10
HEIGHT=10
ENTRY=0,0,1
EXIT=5,5
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    fname = write_config(config_text)
    try:
        parser = ConfigParser(fname)
        with pytest.raises(ParserError) as exc:
            parser.load()
        assert "Extraneous value" in str(
            exc.value
        ) or "ENTRY must have fomat" in str(exc.value)
    finally:
        os.unlink(fname)

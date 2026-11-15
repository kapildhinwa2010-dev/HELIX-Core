"""Tests for HELIX-Core: record storage, parity detection, honest repair."""

import pytest

from helix_core import HelixMemory, spiral_coordinates


def test_write_read_roundtrip():
    memory = HelixMemory(size=8, record_size=4)
    memory.write("alpha", b"\x01\x02\x03\x04")
    assert memory.read("alpha") == b"\x01\x02\x03\x04"


def test_record_flip_detected_not_repairable():
    memory = HelixMemory(size=8, record_size=4)
    memory.write("alpha", b"\x01\x02\x03\x04")
    memory.corrupt("alpha")
    assert memory.verify() is False
    memory.repair()
    assert memory.verify() is True
    # documented limitation: repair restored the parity byte, the
    # record byte is still flipped - read_checked() must refuse it
    with pytest.raises(ValueError):
        memory.read_checked("alpha")


def test_parity_flip_detected_and_repaired():
    memory = HelixMemory(size=8, record_size=4)
    memory.write("alpha", b"\x01\x02\x03\x04")
    memory.corrupt_parity("alpha")
    assert memory.verify() is False
    assert memory.repair() == 1
    assert memory.verify() is True
    assert memory.read_checked("alpha") == b"\x01\x02\x03\x04"


def test_read_checked_clean_row():
    memory = HelixMemory(size=8, record_size=4)
    memory.write("alpha", b"\x01\x02\x03\x04")
    assert memory.read_checked("alpha") == b"\x01\x02\x03\x04"


def test_unknown_key_raises():
    memory = HelixMemory(size=8, record_size=4)
    with pytest.raises(KeyError):
        memory.read("nope")


def test_arena_full_raises():
    memory = HelixMemory(size=4, record_size=2)
    for i in range(4):
        memory.write("k{}".format(i), b"\x01\x02")
    with pytest.raises(MemoryError):
        memory.write("overflow", b"\x01\x02")


def test_spiral_covers_grid_once():
    coords = spiral_coordinates(5)
    assert len(coords) == 25 and len(set(coords)) == 25

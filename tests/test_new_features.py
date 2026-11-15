"""Tests for full-record storage, collision probing and repair."""

import pytest

from helix_core import HelixMemory


def test_full_record_roundtrip():
    mem = HelixMemory(size=8, record_size=4)
    mem.write("k", b"\x01\x02\x03\x04")
    assert mem.read("k") == b"\x01\x02\x03\x04"


def test_anagram_keys_do_not_collide():
    mem = HelixMemory(size=8, record_size=4)
    mem.write("ab", b"\x01\x02\x03\x04")
    mem.write("ba", b"\x05\x06\x07\x08")
    assert mem.read("ab") == b"\x01\x02\x03\x04"
    assert mem.read("ba") == b"\x05\x06\x07\x08"

def test_read_unknown_key_raises():
    mem = HelixMemory(size=8, record_size=4)
    with pytest.raises(KeyError):
        mem.read("missing")


def test_overwrite_keeps_slot():
    mem = HelixMemory(size=8, record_size=4)
    mem.write("k", b"\x01\x02\x03\x04")
    mem.write("k", b"\x09\x09\x09\x09")
    assert mem.read("k") == b"\x09\x09\x09\x09"
    assert len(mem) == 1


def test_arena_full_raises():
    mem = HelixMemory(size=5, record_size=4)
    for i in range(5):
        mem.write(f"k{i}", bytes([i]) * 4)
    with pytest.raises(MemoryError):
        mem.write("overflow", b"\x00" * 4)

def test_repair_restores_parity_byte():
    mem = HelixMemory(size=8, record_size=4)
    mem.write("k", b"\x01\x02\x03\x04")
    row = mem._slots["k"]
    mem.arena[row, 4] ^= 0xFF  # flip the parity byte only
    assert mem.verify() is False
    assert mem.repair() == 1
    assert mem.verify() is True
    assert mem.read("k") == b"\x01\x02\x03\x04"


def test_record_plus_parity_size_validation():
    with pytest.raises(ValueError):
        HelixMemory(size=3, record_size=4)

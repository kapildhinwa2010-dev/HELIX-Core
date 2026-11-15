# HELIX-Core

[![CI](https://github.com/kapildhinwa2010-dev/HELIX-Core/actions/workflows/ci.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/HELIX-Core/actions/workflows/ci.yml)
[![CodeQL](https://github.com/kapildhinwa2010-dev/HELIX-Core/actions/workflows/codeql.yml/badge.svg)](https://github.com/kapildhinwa2010-dev/HELIX-Core/actions/workflows/codeql.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Core spiral-addressed record arena: one record per row, XOR parity detection, blake2b-keyed slots.

**Part of the [Kapildhinwa2010-dev Toolkit](https://github.com/kapildhinwa2010-dev/Kapildhinwa2010-dev).**

## What it does

Each key owns one row of a spiral-walked square arena. write() stores
the full record plus an XOR parity byte; verify() detects any odd
number of flipped bytes per row; read_checked() refuses corrupted rows
instead of returning silent corruption. This is the canonical base of
the spiral-memory family (SpiralDB, ECC-Memory, HELIX-Lib/Pro extend
it).

## Install

    pip install -r requirements.txt

## Quick start

    from helix_core import HelixMemory

    mem = HelixMemory(size=8, record_size=4)
    mem.write("alpha", b"\x01\x02\x03\x04")
    print(mem.read_checked("alpha"))

## API

- write / read / read_checked / read_cell / verify / repair / corrupt /
  corrupt_parity / usage
- spiral_coordinates(size)

## Honest results and limitations

- One XOR parity byte per row DETECTS corruption but cannot locate it.
  repair() restores the parity byte assuming the record is intact; a
  flipped record byte is detected but NOT repairable. Earlier
  revisions claimed "repaired exactly" - that was wrong and is fixed.
- Capacity is one record per row: a 8x8 arena holds 8 records.
- Two flipped bytes in one row cancel out and pass verify().
- Research toy for the spiral-addressing idea, not trustworthy storage.
  For single-cell correction see ECC-Memory (row+column parity).

## License

MIT - see [LICENSE](LICENSE).

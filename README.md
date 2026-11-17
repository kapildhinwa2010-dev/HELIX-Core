# HELIX-Core

HELIX-Core is a small Python prototype for storing fixed-size byte records in a bounded, in-memory two-dimensional arena. It assigns keys to rows using a deterministic BLAKE2b-derived spiral starting position, stores one record per row, and provides XOR-parity and content-hash checks for detecting some forms of corruption.

## Status

This repository contains an implemented Python module and unit tests. It is an experimental, process-local data structure—not a persistent database or production storage system. No benchmark results are provided.

## Implemented features

- `spiral_coordinates(size)` returns a clockwise spiral traversal of a square grid, starting at its center.
- `HelixMemory` stores fixed-length byte records in a NumPy `uint8` array. A key is assigned a row based on a BLAKE2b-derived spiral start and probing for an unoccupied row; rewriting a key keeps its existing row.
- Each record row includes an XOR parity byte. `verify()` checks parity for used rows, and `repair()` rewrites mismatching row parity bytes; it does not recover damaged record data.
- `read_checked()` checks row parity and compares the record with a SHA-256 digest retained in memory when it was written. It raises `ValueError` when a check detects corruption.
- Additional methods include `read()`, `read_cell()`, `corrupt()`, `corrupt_parity()`, and `usage()`.

## Requirements and installation

Python 3.9 or newer is declared in the project metadata. NumPy is the runtime dependency. From the repository root, install the declared requirements with:

```sh
python -m pip install -r requirements.txt
```

The requirements file also includes pytest for running the tests. The module can be imported directly from the repository root; this project does not provide a command-line interface.

## Example

Run from the repository root after installing requirements:

```sh
python - <<'PY'
from helix_core import HelixMemory

memory = HelixMemory(size=8, record_size=4)
memory.write("alpha", b"abcd")
print(memory.read_checked("alpha"))
PY
```

The arena requires `size >= record_size + 1`, and its row-based allocation allows at most `size` keys. Records must be exactly `record_size` bytes.

## Tests

Run the test suite from the repository root:

```sh
python -m pytest -q
```

On the cloned repository commit `f5573ed`, this command completed locally with **14 passed**. The module and test files also compiled successfully with `python -m compileall -q helix_core.py tests`. The GitHub Actions workflow defines pytest and compile/smoke checks for Python 3.10, 3.11, and 3.12; this statement describes the workflow configuration, not a separately verified Actions run.

## Limitations

- Data and the SHA-256 reference digests exist only in the `HelixMemory` instance. There is no file format, persistence, recovery across process restarts, or database interface.
- Capacity is one record per row (at most `size` records), with a fixed record length for each instance. There is no deletion or variable-length record support.
- XOR parity can fail to detect an even number of byte changes in a row. `read_checked()` adds comparison to the in-memory content digest, but this is not persistent or tamper-proof integrity protection.
- `repair()` only rewrites parity metadata based on the current record bytes; it cannot restore a corrupted record. After a record corruption it may make `verify()` pass, while `read_checked()` still rejects the changed record using its retained digest.
- No performance measurements or claims of concurrency safety are provided.

## License

The `LICENSE` file contains the MIT License. See [LICENSE](LICENSE) for its terms.

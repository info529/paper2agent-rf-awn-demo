"""Normalize RadioML serialization keys only; verify all array content after writing."""
import argparse
import hashlib
import json
import pathlib
import pickle
import struct
import numpy as np


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            digest.update(block)
    return digest.hexdigest()


def normalized(data):
    if type(data) is not dict:
        raise TypeError("Expected dictionary")
    result = {}
    converted = 0
    for key, value in data.items():
        if type(key) is not tuple or len(key) != 2:
            raise TypeError("Expected (modulation, SNR) tuple")
        modulation, snr = key
        if type(modulation) is str:
            modulation = modulation.encode("ascii")
            converted += 1
        elif type(modulation) is bytes:
            modulation.decode("ascii")
        else:
            raise TypeError("Unexpected modulation type")
        if type(snr) is not int:
            raise TypeError("Expected integer SNR")
        if type(value) is not np.ndarray:
            raise TypeError("Expected NumPy array")
        if value.shape != (1000, 2, 128) or value.dtype != np.dtype("float32"):
            raise ValueError("Unexpected array shape or dtype")
        new_key = (modulation, snr)
        if new_key in result:
            raise ValueError("Normalization key collision")
        result[new_key] = value

    expected = {
        b"QAM16", b"QAM64", b"8PSK", b"WBFM", b"BPSK", b"CPFSK",
        b"AM-DSB", b"GFSK", b"PAM4", b"QPSK", b"AM-SSB"
    }
    mods = {k[0] for k in result}
    snrs = {k[1] for k in result}
    if len(result) != 220 or mods != expected or snrs != set(range(-20, 20, 2)):
        raise ValueError("Unexpected class/SNR inventory")
    if set(result) != {(m, s) for m in mods for s in snrs}:
        raise ValueError("Incomplete class/SNR product")
    if sum(v.shape[0] for v in result.values()) != 220000:
        raise ValueError("Unexpected total examples")
    return result, converted


def semantic_hash(data):
    """Sorted normalized keys; framed names, signed SNR, dtype, shape, C-order bytes."""
    values, _ = normalized(data)
    digest = hashlib.sha256(b"RML2016.10a-semantic-v1\x00")
    for (mod, snr), array in sorted(values.items()):
        dtype = array.dtype.str.encode("ascii")
        digest.update(struct.pack(">I", len(mod)) + mod)
        digest.update(struct.pack(">q", snr))
        digest.update(struct.pack(">I", len(dtype)) + dtype)
        digest.update(struct.pack(">I", array.ndim))
        digest.update(struct.pack(">" + "Q" * array.ndim, *array.shape))
        raw = array.tobytes(order="C")
        digest.update(struct.pack(">Q", len(raw)))
        digest.update(raw)
    return digest.hexdigest()


def load(path):
    with path.open("rb") as stream:
        return pickle.load(stream, encoding="bytes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--evidence", type=pathlib.Path, required=True)
    args = parser.parse_args()

    before_file_hash = file_hash(args.source)
    original = load(args.source)
    derived, count = normalized(original)
    before = semantic_hash(original)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as stream:
        pickle.dump(derived, stream, protocol=4)

    source_reload, _ = normalized(load(args.source))
    output_reload, _ = normalized(load(args.output))
    assert source_reload.keys() == output_reload.keys()
    for key in source_reload:
        left, right = source_reload[key], output_reload[key]
        assert left.shape == right.shape
        assert left.dtype == right.dtype
        assert np.array_equal(left, right), "Array mismatch: " + repr(key)
        assert left.tobytes(order="C") == right.tobytes(order="C"), "Bit mismatch"

    after = semantic_hash(output_reload)
    assert before == after, "Semantic hash mismatch"
    assert file_hash(args.source) == before_file_hash, "Source file changed"

    record = {
        "source": str(args.source),
        "output": str(args.output),
        "source_sha256": before_file_hash,
        "output_sha256": file_hash(args.output),
        "source_size_bytes": args.source.stat().st_size,
        "output_size_bytes": args.output.stat().st_size,
        "converted_keys": count,
        "verified_groups": len(source_reload),
        "semantic_before_sha256": before,
        "semantic_after_sha256": after,
        "all_shapes_dtypes_array_equal_and_bytes_equal": True,
        "source_unchanged": True,
    }
    args.evidence.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()

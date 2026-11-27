"""Unit tests for the Python firmware tools and index builder.

Run with:
    python3 -m unittest discover -s tests
"""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from icom_rza1_decode import autokey_decode, autokey_reverse, lzss_decompress
from ic_rza1_repack import autokey_encode, lzss_compress
from icom_patch import apply_ops


class CodecTests(unittest.TestCase):
    def test_autokey_roundtrip(self):
        data = bytes((i * 37 + 13) & 255 for i in range(4096))
        for base, key, iv in ((0x64, 0x19, 0x9B), (0x38, 0x2B, 0x00), (0x88, 0x7F, 0xFF)):
            enc = autokey_encode(data, base, key, iv)
            dec, _ = autokey_decode(enc, base, key, iv)
            self.assertEqual(dec, data)

    def test_autokey_reverse_recovers_ff_anchor(self):
        plain = bytes(range(250)) + b"\xff" * 64
        base, key, iv = 0x64, 0x19, 0xAA
        enc = autokey_encode(plain, base, key, iv)
        rec, rec_iv = autokey_reverse(enc, base, key, last=0xFF)
        self.assertEqual(rec, plain)
        self.assertEqual(rec_iv, iv)

    def test_lzss_roundtrip(self):
        samples = [
            b"X",
            b"ABCABCABCABC",
            b"A" * 128,
            b"hello hello hello world world! " * 20,
            bytes(((i * 17) ^ (i >> 3)) & 255 for i in range(8192)),
        ]
        for sample in samples:
            comp = lzss_compress(sample)
            decomp, _ = lzss_decompress(comp, len(sample))
            self.assertEqual(decomp, sample)

    def test_apply_ops_hex_and_copy(self):
        stock = bytes(range(64))
        patch = {
            "load_address": 0x1000,
            "image_size": 64,
            "ops": [
                {"at": "0x1004", "hex": "deadbeef"},
                {"at": "0x1010", "copy_from": "0x1020", "len": 8},
            ],
        }
        out = apply_ops(stock, patch)
        self.assertEqual(out[4:8], bytes.fromhex("deadbeef"))
        self.assertEqual(out[16:24], stock[32:40])

    def test_apply_ops_rejects_out_of_bounds(self):
        stock = b"\x00" * 16
        bad_write = {"load_address": 0, "image_size": 16, "ops": [{"at": "0x0e", "hex": "01020304"}]}
        with self.assertRaises(ValueError):
            apply_ops(stock, bad_write)

        bad_copy = {"load_address": 0, "image_size": 16, "ops": [{"at": "0x00", "copy_from": "0x0c", "len": 8}]}
        with self.assertRaises(ValueError):
            apply_ops(stock, bad_copy)


class IndexIntegrityTests(unittest.TestCase):
    def test_releases_and_index_match(self):
        rel = json.loads((ROOT / "releases.json").read_text())
        idx = json.loads((ROOT / "docs" / "patches" / "index.json").read_text())
        active = [r for r in rel["releases"] if r.get("status", "active") == "active"]
        self.assertEqual(len(idx["releases"]), len(active))

        for entry in idx["releases"]:
            patch_path = ROOT / "docs" / "patches" / entry["release"]["patch_file"]
            self.assertTrue(patch_path.is_file(), f"missing patch {patch_path}")
            self.assertEqual(
                hashlib.sha256(patch_path.read_bytes()).hexdigest(),
                entry["release"]["patch_sha256"],
            )
            bundle = entry["release"].get("apps_bundle")
            if bundle:
                bundle_path = ROOT / "docs" / bundle["path"]
                self.assertTrue(bundle_path.is_file(), f"missing bundle {bundle_path}")
                self.assertEqual(
                    hashlib.sha256(bundle_path.read_bytes()).hexdigest(),
                    bundle["sha256"],
                )


if __name__ == "__main__":
    unittest.main()

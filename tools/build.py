#!/usr/bin/env python3
"""Rebuild the list from its four sources and compare with the published files.
Python 3.8+, standard library only.

  python3 tools/build.py                 # downloads BIP39 + EFF lists from their official URLs
  python3 tools/build.py --bip39 english.txt --eff eff_large_wordlist.txt   # offline, local copies
  python3 tools/build.py --write         # (re)write wordlist.txt and wordlist-index-order.txt

Composition, in this exact order (this order defines the word index 0..9999):
  1. BIP39 English list, all 2,048 words, official order
  2. EFF large wordlist (7,776 words), official order, minus the 870 words already in step 1 -> 6,906
  3. sources/custom.txt  (946 words, none in BIP39 or EFF)
  4. sources/extra.txt   (100 words, none in BIP39 or EFF)
"""
import argparse
import hashlib
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIP39_URL = "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt"
EFF_URL = "https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt"
# SHA-256 of the upstream files as downloaded for v1.0.0
BIP39_SHA256 = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"
EFF_SHA256 = "addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e"


def fetch(path, url):
    if path:
        with open(path, "rb") as f:
            return f.read()
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read()


def read_words(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return [w for w in f.read().split("\n") if w]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bip39", help="local copy of BIP39 english.txt")
    ap.add_argument("--eff", help="local copy of eff_large_wordlist.txt")
    ap.add_argument("--write", action="store_true", help="write the output files")
    a = ap.parse_args()

    b_raw = fetch(a.bip39, BIP39_URL)
    e_raw = fetch(a.eff, EFF_URL)
    for label, raw, want in (("BIP39", b_raw, BIP39_SHA256), ("EFF", e_raw, EFF_SHA256)):
        got = hashlib.sha256(raw).hexdigest()
        print("%-5s upstream SHA-256 %s %s" % (label, got, "(matches v1.0.0)" if got == want else "(DIFFERENT from v1.0.0!)"))

    bip39 = b_raw.decode("utf-8").split()
    eff = [line.split("\t")[1] for line in e_raw.decode("utf-8").splitlines() if "\t" in line]
    assert len(bip39) == 2048 and len(eff) == 7776, "unexpected upstream sizes"
    in_bip = set(bip39)
    eff_rest = [w for w in eff if w not in in_bip]
    custom = read_words("sources/custom.txt")
    extra = read_words("sources/extra.txt")
    index_order = bip39 + eff_rest + custom + extra
    print("parts: BIP39 %d + EFF-only %d + custom %d + extra %d = %d (unique %d)" % (
        len(bip39), len(eff_rest), len(custom), len(extra), len(index_order), len(set(index_order))))
    assert len(set(index_order)) == len(index_order), "duplicates across sources"

    idx_text = "\n".join(index_order) + "\n"
    srt_text = "\n".join(sorted(index_order)) + "\n"
    if a.write:
        for name, text in (("wordlist-index-order.txt", idx_text), ("wordlist.txt", srt_text)):
            with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("wrote " + name)
        return 0
    ok = True
    for name, text in (("wordlist-index-order.txt", idx_text), ("wordlist.txt", srt_text)):
        with open(os.path.join(ROOT, name), encoding="utf-8", newline="") as f:
            same = f.read() == text
        print("%-26s %s" % (name, "IDENTICAL to rebuild" if same else "DIFFERS from rebuild"))
        ok = ok and same
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

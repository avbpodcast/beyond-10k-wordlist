#!/usr/bin/env python3
"""Verify the beyond-10k-wordlist files. Python 3.8+, standard library only.

Run from the repository root:   python3 tools/verify.py
Exit code 0 = every check passed, 1 = at least one check failed.
"""
import hashlib
import json
import math
import os
import re
import sys

EXPECTED_COUNT = 10000
WORD_RE = re.compile(r"^[a-z]+(-[a-z]+)*$")   # lowercase ASCII letters, optional inner hyphens
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = 0


def check(ok, label, detail=""):
    global failures
    print(("PASS  " if ok else "FAIL  ") + label + ((" (" + detail + ")") if detail else ""))
    if not ok:
        failures += 1
    return ok


def load_lines(name):
    path = os.path.join(ROOT, name)
    with open(path, "rb") as f:
        raw = f.read()
    check(b"\r" not in raw, name + ": LF line endings only, no CR")
    check(raw.endswith(b"\n") and not raw.endswith(b"\n\n"), name + ": ends with exactly one newline")
    try:
        text = raw.decode("utf-8")
        check(True, name + ": valid UTF-8")
    except UnicodeDecodeError as e:
        check(False, name + ": valid UTF-8", str(e))
        text = raw.decode("utf-8", "replace")
    words = text.split("\n")[:-1] if text.endswith("\n") else text.split("\n")
    return raw, words


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    raw, words = load_lines("wordlist.txt")
    check(len(words) == EXPECTED_COUNT, "wordlist.txt: word count", "%d, expected %d" % (len(words), EXPECTED_COUNT))
    check(all(w for w in words), "wordlist.txt: no empty lines")
    check(len(set(words)) == len(words), "wordlist.txt: all words unique",
          "%d duplicates" % (len(words) - len(set(words))))
    check(words == sorted(words), "wordlist.txt: sorted (plain byte order, like LC_ALL=C sort)")
    bad = [w for w in words if not WORD_RE.match(w)]
    check(not bad, "wordlist.txt: only a-z and inner '-'", ", ".join(bad[:5]))
    check(all(w == w.strip() for w in words), "wordlist.txt: no leading/trailing spaces")

    idx_path = os.path.join(ROOT, "wordlist-index-order.txt")
    if os.path.exists(idx_path):
        iraw, iwords = load_lines("wordlist-index-order.txt")
        check(sorted(iwords) == words, "wordlist-index-order.txt: same words as wordlist.txt")
    js_path = os.path.join(ROOT, "wordlist.json")
    if os.path.exists(js_path):
        with open(js_path, encoding="utf-8") as f:
            data = json.load(f)
        check(data.get("words") == words, "wordlist.json: 'words' equals wordlist.txt")
        check(data.get("count") == len(words), "wordlist.json: 'count' matches")

    sums = os.path.join(ROOT, "SHA256SUMS.txt")
    if os.path.exists(sums):
        with open(sums, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                want, name = line.split(None, 1)
                name = name.lstrip("*")
                p = os.path.join(ROOT, name)
                if not os.path.exists(p):
                    check(False, "SHA256SUMS.txt: " + name, "file missing")
                    continue
                with open(p, "rb") as g:
                    check(sha256(g.read()) == want, "SHA256SUMS.txt: " + name)

    n = len(set(words))
    print()
    print("words:          %d" % len(words))
    print("bits per word:  %.4f  (log2 of %d)" % (math.log2(n), n) if n else "bits per word:  n/a")
    print("SHA-256 wordlist.txt: " + sha256(raw))
    if os.path.exists(idx_path):
        print("SHA-256 wordlist-index-order.txt: " + sha256(iraw))
    print()
    print("RESULT: " + ("ALL CHECKS PASSED" if failures == 0 else "%d CHECK(S) FAILED" % failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

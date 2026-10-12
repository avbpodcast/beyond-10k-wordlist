# Changelog

This project uses [Semantic Versioning](https://semver.org). For a word list, that means:
- **MAJOR**: any word added, removed, respelled or moved (new checksums; tools must opt in).
- **MINOR**: new files or formats with the same words in the same order.
- **PATCH**: documentation and script fixes only.

## [1.0.0] - 2026-10-13

First public release.

- `wordlist.txt`: 10,000 unique lowercase words, sorted, 13.29 bits per word.
  SHA-256 `e385d00b1b16c937f19acb2a21dd6652a1d77ed8fa8e41a3d2b6dde20b6aab4e`.
- `wordlist-index-order.txt`: the same words in index order, identical to the list built into
  the Amulet Word Picker, Beyond Entropy (v1.03+), Project Age Good and Beyond Wallet The Hand / The Stick.
  SHA-256 `42d99f37a2d8ed00ee266db013fc9837c443819a7f07cc06bcf3c7f2f3a0494f`.
- `wordlist.json`, `sources/custom.txt`, `sources/extra.txt`.
- `tools/verify.py` (integrity checks) and `tools/build.py` (reproducible rebuild from the official BIP39 and EFF lists).
- README, SELECTION (method), LICENSE (CC BY 4.0 for the list, MIT for the scripts, with attributions).

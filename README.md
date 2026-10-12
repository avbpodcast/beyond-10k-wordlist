# beyond-10k-wordlist

A list of **10,000 unique English words** for making **random-word passphrases**: easy to write down and type, offline, and strong when the words are picked by a computer's secure random generator.

- One word = **log2(10,000) ≈ 13.29 bits** of entropy (if picked uniformly at random).
- 6 random words ≈ **79.7 bits**. 8 random words ≈ **106.3 bits**.
- Plain lowercase ASCII (`a`–`z`, plus a hyphen in 4 words). No accents, no capitals, no digits.
- Built from four sources: the BIP39 English list, the EFF large wordlist, 946 "custom" words and 100 "extra" words. The custom words were made with AI-assisted generation from a fixed rule set and then curated by hand. The extra words were added by hand. See [SELECTION.md](SELECTION.md).
- Compiled by Mr. 21 (Kim De Vos).

> **Not for Bitcoin seed phrases.** Bitcoin wallets use the 2,048-word **BIP39** list and its checksum. This list is for *passwords and passphrases* (for example to encrypt a file with [age](https://age-encryption.org)). Never use it to make or "improve" a seed phrase.

## Files

| File | What it is |
|---|---|
| `wordlist.txt` | The list. One word per line, UTF-8, LF line endings, sorted (plain byte order), ends with a newline. |
| `wordlist-index-order.txt` | The same 10,000 words in **index order** (line 1 = index 0 … line 10,000 = index 9,999). Use this file if your code turns numbers into words, so that number *n* always gives the same word as the tools listed below. |
| `wordlist.json` | The sorted list plus metadata (`count`, `bits_per_word`, checksums). |
| `sources/custom.txt`, `sources/extra.txt` | The 946 + 100 words that are not in BIP39 or EFF. |
| `tools/verify.py` | Checks count, sort order, uniqueness, character set, line endings and the checksums. |
| `tools/build.py` | Rebuilds both list files from the official BIP39 and EFF lists plus `sources/`, and compares. |
| `SHA256SUMS.txt` | SHA-256 checksums of every file. |

Checksums for v1.0.0:

```
e385d00b1b16c937f19acb2a21dd6652a1d77ed8fa8e41a3d2b6dde20b6aab4e  wordlist.txt
42d99f37a2d8ed00ee266db013fc9837c443819a7f07cc06bcf3c7f2f3a0494f  wordlist-index-order.txt
```

## Verify your copy

```
python3 tools/verify.py      # prints PASS/FAIL per check and the SHA-256
python3 tools/build.py       # optional: rebuild from the official upstream lists and compare
sha256sum -c SHA256SUMS.txt  # Linux/macOS alternative
```

On Windows, use `py tools\verify.py`. If you download with git on Windows, the included `.gitattributes` keeps LF line endings so the checksums still match.

## How strong is it?

Each word is one uniform choice out of 10,000. Strength depends **only** on how many words you pick and on picking them with a secure random generator.

| Words | Entropy | Possible passphrases | Average time to guess at 10¹² guesses/second |
|---:|---:|---:|---:|
| 4 | 53.2 bits | 10¹⁶ | about 1.4 hours |
| 5 | 66.4 bits | 10²⁰ | about 1.6 years |
| 6 | 79.7 bits | 10²⁴ | about 16,000 years |
| 7 | 93.0 bits | 10²⁸ | about 160 million years |
| 8 | 106.3 bits | 10³² | about 1.6 trillion years |

The last column assumes a very fast attacker against a fast hash, with the attacker knowing you used this list and how many words you picked. A deliberately slow key-derivation function, like the scrypt that age uses for passphrases, makes every guess far more expensive. That helps, but don't use it as an excuse to pick fewer words.

For comparison, the 7,776-word EFF list gives 12.92 bits per word, and BIP39's 2,048 words give 11 bits per word.

**How many words?** For a passphrase that protects something important (an encrypted backup, a password-manager vault), **6 words or more** is a sensible minimum; use **7 or 8** for long-term, high-value secrets.

## Use it safely

1. **Let a computer pick.** Use a cryptographically secure random generator (`secrets` in Python, `crypto.getRandomValues` in browsers, `/dev/urandom`, or real dice with a dice-to-number method). **Never pick words yourself.** Words you "like" are much easier to guess.
2. **Pick each word uniformly.** Avoid `random_number % 10000` with a small random number, because that makes some words more likely. Use rejection sampling (see the examples below) or a library function that already does it, like Python's `secrets.choice`.
3. **Don't throw away draws you dislike.** Re-rolling until it "looks good" lowers the strength. If you really must, re-roll the *whole* passphrase, not single words.
4. **Separate words with spaces.** Four words contain a hyphen (`drop-down`, `felt-tip`, `t-shirt`, `yo-yo`), and 555 words are the start of a longer word (for example `act` and `action`), so a hyphen or no separator at all can make two different passphrases look the same. A space avoids that. It doesn't change the entropy math above.
5. **Keep the passphrase secret, not the list.** The list is public by design. All of the security comes from the random choice.
6. **Write it down offline** if you need a backup, and store it apart from what it protects.

### Python (standard library)

```python
import secrets

with open("wordlist.txt", encoding="utf-8") as f:
    words = [w for w in f.read().split("\n") if w]
assert len(words) == 10000

n = 6
passphrase = " ".join(secrets.choice(words) for _ in range(n))  # secrets.choice is uniform
print(passphrase)
```

### JavaScript (browser or Node 19+)

```js
// words: array of the 10,000 words, e.g. from wordlist.json -> data.words
function uniformIndex(n) {
  // Rejection sampling: no modulo bias.
  const limit = Math.floor(0x100000000 / n) * n;   // largest multiple of n below 2^32
  const buf = new Uint32Array(1);
  while (true) {
    crypto.getRandomValues(buf);
    if (buf[0] < limit) return buf[0] % n;
  }
}

function passphrase(words, count = 6) {
  if (words.length !== 10000) throw new Error("unexpected list size");
  return Array.from({ length: count }, () => words[uniformIndex(words.length)]).join(" ");
}
```

## Where it is used

The list started in the **Amulet Word Picker** and is the "lock word" or passphrase list in these offline tools:

- **Beyond Entropy** (v1.03 and later): random passphrase words for `.age` encryption, picked by rejection sampling.
- **Project Age Good** (Python CLI and offline HTML): suggests random words (6 by default in the CLI) for age passphrase encryption.
- **Beyond Wallet: The Hand and The Stick**: the four "lock words" on paper B that protect the `.age` copy of the seed backup. The seed itself stays BIP39.

These tools look words up **by index**, using the order in `wordlist-index-order.txt`. Changing the list or its order would change which words those tools produce, so v1.x will not change the words or their order.

## Word list facts (v1.0.0)

| | |
|---|---|
| Words | 10,000, all unique |
| Characters | `a`–`z` and `-` (hyphen only in `drop-down`, `felt-tip`, `t-shirt`, `yo-yo`) |
| Length | 3 to 11 characters, average 6.74 |
| Case / accents | all lowercase, pure ASCII |
| From BIP39 English | 2,048 (all of them) |
| From EFF large wordlist | 7,776 (all of them, 870 of which are also in BIP39) |
| Added (`custom` 946 + `extra` 100) | 1,046, in neither BIP39 nor EFF. Compiled by the author: AI-assisted generation from a rule set (length limits, made-up and science words, names from science fiction, TV series, bands, films, ships, planets and more), then curated and merged by hand, plus 100 hand-picked extras. |
| Unique prefix | none shorter than the full word: 555 words are a prefix of a longer word (e.g. `act` / `action`). The first 5 letters identify 6,258 words uniquely. |

## License

Compiled by Mr. 21 (Kim De Vos). Individual words are not owned by anyone; the license covers the selection and arrangement of the list as a whole.

The list as a whole is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**. The BIP39 words carry an MIT notice, and the EFF words require attribution to the EFF. The scripts in `tools/` are MIT. See [LICENSE](LICENSE) for the full texts and attributions.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

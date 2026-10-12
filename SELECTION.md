# How the words were selected

This file describes how the 10,000 words were put together. The list was compiled by Mr. 21 (Kim De Vos). The composition and properties below were checked against the published files with `tools/build.py` and `tools/verify.py`.

## Goal

A list that is:

- **big**: 10,000 words gives 13.29 bits per word, more than BIP39 (11 bits) or EFF (12.92 bits), so a strong passphrase needs fewer words;
- **plain**: lowercase ASCII only, so it types the same on any keyboard and survives copy, paste and handwriting;
- **familiar**: it starts from two widely used, well-reviewed lists;
- **fixed**: the order never changes, so tools that turn numbers into words keep producing the same words.

The size of the list is round on purpose: with exactly 10,000 words, the strength of *n* words is simply 10,000ⁿ.

## The four parts, in index order

The index order (`wordlist-index-order.txt`) is the four parts concatenated:

| Index range | Part | Words | Source |
|---|---|---:|---|
| 0 – 2,047 | BIP39 English | 2,048 | [bitcoin/bips `bip-0039/english.txt`](https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt), complete, in its official order |
| 2,048 – 8,953 | EFF large wordlist | 6,906 | [EFF `eff_large_wordlist.txt`](https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt) (7,776 words) in its official order, **minus the 870 words that are already in BIP39** |
| 8,954 – 9,899 | Custom | 946 | `sources/custom.txt`, words that are in neither BIP39 nor EFF |
| 9,900 – 9,999 | Extra | 100 | `sources/extra.txt`, words that are in neither BIP39 nor EFF |

So the list contains **every** BIP39 English word and **every** EFF large-list word, plus 1,046 added words. The four parts don't overlap, and the total is exactly 10,000 unique words.

`wordlist.txt` holds the same words sorted in plain byte order (`LC_ALL=C sort`).

Upstream files used for v1.0.0 (SHA-256 as downloaded):

```
2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda  bip-0039/english.txt
addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e  eff_large_wordlist.txt
```

`tools/build.py` downloads both files, checks these hashes, rebuilds the list and confirms it is byte-for-byte identical to the published files.

## Why these two base lists

- **BIP39 English**: 2,048 common words, chosen so that the first four letters identify each word, and widely known to Bitcoin users.
- **EFF large wordlist**: 7,776 words made by the Electronic Frontier Foundation for dice-based passphrases (5 dice per word), selected for being easy to remember and type. See EFF's post ["EFF's New Wordlists for Random Passphrases"](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) (19 July 2016).

## The added words (custom and extra)

The 1,046 added words are not taken from a published list. They were compiled by the author, Mr. 21 (Kim De Vos). The compilation of the whole list is the author's own work.

### Custom (946 words): AI-assisted generation, then hand curation

The custom words were built in early 2026 in a series of steps with an AI assistant (Grok), then curated and merged by hand.

1. **A rule-based first list.** The instructions given to the assistant were:
   - words of 5 to 8 characters (some later steps allowed 4 to 10);
   - avoid words that are common in breached-password lists;
   - mix roughly 30% made-up pronounceable words, 40% uncommon science terms and 30% terms from law, literature and chemistry;
   - cover every starting letter of the alphabet;
   - exclude BIP39 words (in a later step also SLIP-39 words);
   - remove words that are hard to remember.

   Dutch and French variants were made with the same rules.
2. **Batches of names and terms**, each with a length limit (mostly 5 to 8 or 9 letters): character names from TV series and science-fiction novels (among others *The Expanse*, Peter F. Hamilton, the *Murderbot* books, *Blake's 7*, *The Boys*, *Peacemaker*), names from Tad Williams' *Otherland*, medical syndromes and effects, named chemical reactions, uncommon English words, chemical elements, band names (electronic, industrial, EBM, grunge), brand names, IKEA product names, planet and starship names from science fiction, one-word film titles, and names of foods and places.
3. **Merge.** The batches were merged, duplicates removed, entries containing " - " and BIP39 words dropped, removed entries replaced with names of characters from Quentin Tarantino films, the list padded to 1,040 entries, and everything put in lowercase.
4. **Hand curation.** The author then reworked the merged list by hand. Many generated words were dropped and others were added, so the final list differs a lot from the intermediate AI output. When the 10,000-word pool was built, 94 entries that were already in BIP39 or EFF were removed (they're in the list once, in their original part), along with two entries that weren't plain words. One word was added. That left the 946 words in `sources/custom.txt`.

These categories can be traced in the final custom list. The counts are the custom words that also appear in one of the generated batches; 194 of the 946 can be traced this way:

| Category | Custom words traced |
|---|---:|
| Character names from science-fiction novels and series (*The Expanse*, Peter F. Hamilton, *Murderbot* and others), e.g. `camina`, `ozzie`, `qatux` | 46 |
| TV-series characters (*Blake's 7*, *The Boys*, *Peacemaker*, *Banshee*, *Fallout*), e.g. `maeve`, `kimiko`, `vigilante` | 39 |
| Band names (electronic, industrial, EBM, grunge), e.g. `oomph`, `klinik`, `mudhoney` | 26 |
| Starship names, e.g. `rocinante`, `nostromo`, `serenity` | 18 |
| Food and brand names, e.g. `gianduja`, `taralli`, `quilmes` | 18 |
| One-word film titles, e.g. `inception`, `memento`, `solaris` | 17 |
| Rule-based list (made-up and science words, including the Dutch and French variants), e.g. `pabez`, `taxon`, `tanka` | 10 |
| Planet names, e.g. `hyperion`, `deneb`, `charon` | 8 |
| Chemical elements, e.g. `gallium`, `niobium`, `vanadium` | 5 |
| Tarantino characters, e.g. `ordell`, `winston` | 5 |
| Other (one chemical-reaction name, one IKEA name) | 2 |

The other 752 custom words could not be traced to a single batch. They come from the author's own curated working list, which was merged in the last step. Looking at the list, they include many star names, rivers and places, computing and security terms, mythology, and names from games, books and films. Those themes are an observation only; they weren't counted.

### Extra (100 words): added by hand

The 100 extra words were added by the author by hand. The Amulet Word Picker described them as "100 curated extras". They are mostly biology and science terms (`allele`, `chlorophyll`, `mitosis`, `xylem`), old or literary English (`forsooth`, `hither`, `wherefore`) and folklore or fantasy words (`kraken`, `valkyrie`, `wyrm`).

### What was and wasn't checked

- "Avoid common breached passwords" was an instruction to the AI assistant, not a verified check. For this release the list was compared with the public SecLists `10k-most-common.txt` password list. 122 of the 1,046 added words appear in it (e.g. `ashley`, `cooper`, `voyager`), and so do 916 BIP39 words and 794 EFF words. **This doesn't weaken random passphrases**: their strength comes entirely from the random choice of words (see README), not from the words being rare.
- The other rules (length, starting letters, the 30/40/30 mix) were instructions during generation and weren't enforced on the final list. The facts that *are* verified for the final list are in the table below.

## Properties checked for v1.0.0

| Check | Result |
|---|---|
| Count | 10,000 |
| Duplicates | 0 |
| Characters | `a`–`z`, plus `-` in 4 EFF words (`drop-down`, `felt-tip`, `t-shirt`, `yo-yo`) |
| Uppercase / non-ASCII | none |
| Length | min 3, max 11, average 6.74 |
| Length per part | BIP39 3–8 (avg 5.40) · EFF part 3–9 (avg 7.17) · custom 4–10 (avg 6.50) · extra 3–11 (avg 6.92) |
| Unique prefix | No fixed prefix length identifies every word, because 555 words are a prefix of another word (e.g. `act` / `action`). The first 4 letters identify 3,288 words uniquely, the first 5 letters 6,258, and the first 6 letters 8,407. |
| Singular/plural pairs | 30 pairs where both `w` and `ws` are in the list (e.g. `sport` / `sports`), plus 4 `w` / `wes` pairs |
| Homophones | 40 groups with identical pronunciation in the CMU Pronouncing Dictionary (e.g. `pair` / `pear`, `right` / `write`). 1,597 words, mostly proper names and invented words, have no entry there, so this count is a lower bound. |
| Profanity | Exact matches against the public LDNOOBW English list: `grope`, `hardcore`, `swinger` (all three come from the EFF list). |

None of these affect the entropy math: every word is still exactly one of 10,000 equally likely choices. They only matter if a person has to *read, hear, or retype* a passphrase. That's why the README says to separate words with spaces and to write the passphrase down exactly.

## Stability promise

Version 1.x will never add, remove, reorder or respell words. Any change to the words would be a new major version (2.0.0) with a new file name and checksum, so existing tools keep working.

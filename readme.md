
# Meitei Mayek Transliterator (Latin → Meitei Mayek)

A rule-based Python transliteration tool that converts **Latin-script Manipuri (Meiteilon)** into **Meitei Mayek** with improved phoneme handling, correct vowel placement, Lonsum (final consonants) application, and Meitei digit (Cheising) support.

This project focuses on **linguistic correctness and transparency**, avoiding machine-learning or probabilistic approaches.

---

## Overview

Meitei Mayek is the indigenous script of the Meitei language (Meiteilon).
Many users still write Meiteilon using the Latin script. This tool bridges that gap by transliterating Latin input into proper Meitei Mayek while respecting phonetic and orthographic rules.

---

## Features

* Latin → Meitei Mayek transliteration
* Multi-character consonant recognition (`kh`, `ng`, `ch`, `sh`, etc.)
* Correct vowel handling:

  * Initial vowels
  * Middle vowels (diacritics / following characters)
  * Inherent vowel `a`
* Automatic **Lonsum (final consonant)** conversion
* Meitei Cheising digit support (0–9)
* Preserves punctuation and symbols
* Optional spaced output for learning and analysis
* Interactive command-line interface
* No external dependencies

---

## File Included

meitei_mayek_transliterator_better.py

---

## Requirements

* Python 3.7 or higher
* Works on Windows, Linux, and macOS

---

## Installation

Clone the repository:

git clone [https://github.com/your-username/meitei-mayek-transliterator.git](https://github.com/pravinheiz/meitei-mayek-transliterator.git)
cd meitei-mayek-transliterator

---

## Usage

### Interactive Mode

Run the script:

python meitei_mayek_transliterator_better.py

Example session:

Latin → Meitei Mayek (Ctrl+C to quit)

> eina manipur gi mi ni
> Normal :  ꯑꯩꯅ ꯃꯅꯤꯄꯨꯔ ꯒꯤ ꯃꯤ ꯅꯤ
> Spaced :  ꯑ ꯩ ꯅ / ꯃ ꯅ ꯤ ꯄ ꯨ ꯔ / ꯒ ꯤ / ꯃ ꯤ / ꯅ ꯤ

---

## Programmatic Usage

from meitei_mayek_transliterator_better import transliterate

text = "Eina Manipur gi mi ni"

normal_output = transliterate(text)
spaced_output = transliterate(text, spaced=True)

print(normal_output)
print(spaced_output)

---

## Output Modes

### Normal Mode

Produces standard Meitei Mayek text.

### Spaced Mode

Each character is separated by a space.
Original word boundaries are marked using `/`.

Useful for:

* Learning Meitei Mayek
* Debugging transliteration rules
* Linguistic analysis

---

## Supported Script Elements

### Consonants

Native and commonly used loan phonemes:

k kh g ng ch jh t d n p b m y r l w s h f v

---

### Vowels

#### Initial Vowels

Used at the beginning of words or syllables:

a aa i ii e ee u o oo ai ei au ou

Mapped to Meitei Mayek initial vowel forms.

#### Middle Vowels

Applied after consonants as diacritics or following letters.

---

### Lonsum (Final Consonants)

Automatically applied when a word ends with:

k t p m n l ng

---

### Digits (Meitei Cheising)

0–9 → ꯰–꯹

---

## How It Works

1. Tokenizes Latin text into phoneme-like units
2. Matches multi-character patterns first
3. Converts tokens using position-aware vowel rules
4. Applies Lonsum to final consonants
5. Preserves unknown characters safely

---

## Use Cases

* Meitei Mayek learning and teaching tools
* NLP preprocessing for Meiteilon
* Academic and linguistic research
* Script digitization and preservation
* Command-line transliteration utilities

---

## Limitations

* Rule-based; does not use a dictionary
* Loanword pronunciation may vary
* Dialect-specific variations are not fully covered

---

## Future Improvements

* Syllable-aware parsing
* Dictionary-based corrections
* Reverse transliteration (Meitei Mayek → Latin)
* Web-based interface
* Android application support

---

## License

MIT License
Free to use, modify, and distribute.

---

## Contributions

Contributions are welcome.
If you improve phoneme accuracy, vowel rules, or add dialect support, feel free to open a pull request.


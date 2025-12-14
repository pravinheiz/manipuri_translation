# meitei_mayek_transliterator_better.py
# Latin (Manipuri) -> Meitei Mayek

# ---------- MAPPINGS ----------

CONSONANTS = {
    "kh": "ꯈ",
    "ng": "ꯉ",
    "ch": "ꯆ",
    "jh": "ꯖ",   # optional (loan)
    "sh": "ꯁ",

    "k":  "ꯀ",
    "g":  "ꯒ",   # loans
    "c":  "ꯆ",
    "j":  "ꯖ",   # loans
    "t":  "ꯇ",
    "d":  "ꯗ",   # loans
    "n":  "ꯅ",
    "p":  "ꯄ",
    "b":  "ꯕ",   # loans
    "m":  "ꯃ",
    "y":  "ꯌ",
    "r":  "ꯔ",
    "l":  "ꯂ",
    "w":  "ꯋ",
    "s":  "ꯁ",
    "h":  "ꯍ",
    "f":  "ꯐ",   # approximate with PH
    "v":  "ꯕ",
}

# Vowels at beginning of a word / syllable
INITIAL_VOWELS = {
    "aa": "ꯑꯥ",
    "a":  "ꯑ",
    "ii": "ꯏ",
    "ee": "ꯏ",
    "i":  "ꯏ",
    "u":  "ꯎ",
    "oo": "ꯑꯣ",
    "o":  "ꯑꯣ",
    "e":  "ꯑꯦ",
    "ou": "ꯑꯧ",   # au / ou diphthong
    "au": "ꯑꯧ",
    "ei": "ꯑꯩ",
    "ai": "ꯑꯩ",
}

# Vowels after consonants (as diacritics / following letters)
MIDDLE_VOWELS = {
    "aa": "ꯥ",
    "a":  "",      # inherent vowel
    "ii": "ꯤ",
    "ee": "ꯤ",
    "i":  "ꯤ",
    "u":  "ꯨ",
    "oo": "ꯣ",
    "o":  "ꯣ",
    "e":  "ꯦ",
    "ou": "ꯧ",
    "au": "ꯧ",
    "ei": "ꯩ",
    "ai": "ꯩ",
}

# Lonsum (final consonant letters)
LONSUM = {
    "k":  "ꯛ",
    "t":  "ꯠ",
    "p":  "ꯞ",
    "m":  "ꯝ",
    "n":  "ꯟ",
    "l":  "ꯜ",
    "ng": "ꯡ",
}

# Digits: 0-9 -> Meitei Cheising
DIGITS = {str(i): chr(0xABF0 + i) for i in range(10)}

# Multi-char patterns we want to detect first
MULTI_PATTERNS = sorted(
    set(
        list(CONSONANTS.keys())
        + list(INITIAL_VOWELS.keys())
        + list(MIDDLE_VOWELS.keys())
        + list(LONSUM.keys())
    ),
    key=len,
    reverse=True
)


def transliterate_word(word: str) -> str:
    w = word.lower()

    # 1) Tokenize Latin word into phoneme-like units
    tokens = []
    i = 0
    while i < len(w):
        ch = w[i]

        # Non-letters kept as own tokens
        if not ch.isalpha():
            tokens.append(ch)
            i += 1
            continue

        matched = False
        for pat in MULTI_PATTERNS:
            if w.startswith(pat, i):
                tokens.append(pat)
                i += len(pat)
                matched = True
                break

        if matched:
            continue

        # Fallback: single letter
        tokens.append(ch)
        i += 1

    # 2) Convert tokens to Meitei Mayek
    out = []
    start_of_word = True
    last_consonant_index = None  # index in `out` of last consonant symbol

    i = 0
    while i < len(tokens):
        t = tokens[i]

        # Punctuation / symbols
        if len(t) == 1 and not t.isalnum():
            out.append(t)
            start_of_word = True
            last_consonant_index = None
            i += 1
            continue

        # Digits
        if len(t) == 1 and t.isdigit():
            out.append(DIGITS.get(t, t))
            start_of_word = False
            last_consonant_index = None
            i += 1
            continue

        # Consonants
        if t in CONSONANTS:
            out.append(CONSONANTS[t])
            last_consonant_index = len(out) - 1
            start_of_word = False
            i += 1
            continue

        # Vowels
        if t in INITIAL_VOWELS or t in MIDDLE_VOWELS:
            if start_of_word or last_consonant_index is None:
                out.append(INITIAL_VOWELS.get(t, t))
            else:
                out.append(MIDDLE_VOWELS.get(t, t))
            start_of_word = False
            i += 1
            continue

        # Unknown alpha sequence – just copy (so we don't lose text)
        out.append(t)
        start_of_word = False
        last_consonant_index = None
        i += 1

    # 3) Apply Lonsum for final consonant of the *word*
    #    If the Latin ended on k/t/p/m/n/ng/l and there was a consonant at end
    j = len(tokens) - 1
    while j >= 0 and not tokens[j].isalpha():
        j -= 1

    if j >= 0:
        last_tok = tokens[j]
        if last_tok in LONSUM:
            # Replace the last consonant symbol in `out` with Lonsum form
            k = len(out) - 1
            while k >= 0 and not out[k].isalpha() and not ('\uABC0' <= out[k] <= '\uABFF'):
                k -= 1
            if k >= 0:
                out[k] = LONSUM[last_tok]

    return "".join(out)


def transliterate(text: str, spaced: bool = False) -> str:
    """
    Transliterate full text.

    spaced = False -> normal Meitei Mayek text
    spaced = True  -> every character separated by spaces, word gaps marked with '/'
    """
    result = " ".join(transliterate_word(w) for w in text.split(" "))

    if not spaced:
        return result

    spaced_chars = []
    for ch in result:
        if ch == " ":
            spaced_chars.append("/")   # separate original words
        else:
            spaced_chars.append(ch)
    return " ".join(spaced_chars)


if __name__ == "__main__":
    print("Latin → Meitei Mayek (Ctrl+C to quit)")
    while True:
        try:
            s = input("> ")
        except KeyboardInterrupt:
            print("\nBye!")
            break

        print("Normal : ", transliterate(s))
        print("Spaced : ", transliterate(s, spaced=True))

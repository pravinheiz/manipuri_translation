import tkinter as tk
from tkinter import ttk, messagebox

# =========================================================
# Latin (Manipuri) → Meitei Mayek (ORIGINAL LOGIC)
# =========================================================

CONSONANTS = {
    "kh": "ꯈ", "ng": "ꯉ", "ch": "ꯆ", "jh": "ꯖ", "sh": "ꯁ",
    "k": "ꯀ", "g": "ꯒ", "c": "ꯆ", "j": "ꯖ",
    "t": "ꯇ", "d": "ꯗ", "n": "ꯅ",
    "p": "ꯄ", "b": "ꯕ", "m": "ꯃ",
    "y": "ꯌ", "r": "ꯔ", "l": "ꯂ",
    "w": "ꯋ", "s": "ꯁ", "h": "ꯍ",
    "f": "ꯐ", "v": "ꯕ",
}

INITIAL_VOWELS = {
    "aa": "ꯑꯥ", "a": "ꯑ", "ii": "ꯏ", "ee": "ꯏ", "i": "ꯏ",
    "u": "ꯎ", "oo": "ꯑꯣ", "o": "ꯑꯣ",
    "e": "ꯑꯦ", "ou": "ꯑꯧ", "au": "ꯑꯧ",
    "ei": "ꯑꯩ", "ai": "ꯑꯩ",
}

MIDDLE_VOWELS = {
    "aa": "ꯥ", "a": "", "ii": "ꯤ", "ee": "ꯤ", "i": "ꯤ",
    "u": "ꯨ", "oo": "ꯣ", "o": "ꯣ",
    "e": "ꯦ", "ou": "ꯧ", "au": "ꯧ",
    "ei": "ꯩ", "ai": "ꯩ",
}

LONSUM = {
    "k": "ꯛ", "t": "ꯠ", "p": "ꯞ",
    "m": "ꯝ", "n": "ꯟ", "l": "ꯜ", "ng": "ꯡ",
}

DIGITS = {str(i): chr(0xABF0 + i) for i in range(10)}

MULTI_PATTERNS = sorted(
    set(CONSONANTS) | set(INITIAL_VOWELS) | set(MIDDLE_VOWELS) | set(LONSUM),
    key=len, reverse=True
)

def transliterate_word(word: str) -> str:
    w = word.lower()
    tokens, i = [], 0

    while i < len(w):
        if not w[i].isalpha():
            tokens.append(w[i])
            i += 1
            continue
        for p in MULTI_PATTERNS:
            if w.startswith(p, i):
                tokens.append(p)
                i += len(p)
                break
        else:
            tokens.append(w[i])
            i += 1

    out, start, last_c = [], True, None

    for t in tokens:
        if not t.isalnum():
            out.append(t)
            start, last_c = True, None
        elif t.isdigit():
            out.append(DIGITS[t])
            start, last_c = False, None
        elif t in CONSONANTS:
            out.append(CONSONANTS[t])
            last_c = len(out) - 1
            start = False
        elif t in INITIAL_VOWELS or t in MIDDLE_VOWELS:
            out.append(INITIAL_VOWELS[t] if start or last_c is None else MIDDLE_VOWELS[t])
            start = False
        else:
            out.append(t)

    j = len(tokens) - 1
    while j >= 0 and not tokens[j].isalpha():
        j -= 1
    if j >= 0 and tokens[j] in LONSUM:
        for i in range(len(out) - 1, -1, -1):
            if out[i].isalpha():
                out[i] = LONSUM[tokens[j]]
                break

    return "".join(out)

def transliterate_forward_line(line: str) -> str:
    return " ".join(transliterate_word(w) for w in line.split(" "))

# =========================================================
# Meitei Mayek → Manipuri Latin
# =========================================================

REV_CONSONANTS = {v: k for k, v in CONSONANTS.items()}
REV_LONSUM = {v: k for k, v in LONSUM.items()}

REV_VOWELS = {
    "ꯥ": "aa", "ꯤ": "i", "ꯨ": "u",
    "ꯣ": "o", "ꯦ": "e", "ꯧ": "ou", "ꯩ": "ei",
}

REV_INITIAL_VOWELS = {
    "ꯑ": "a", "ꯑꯥ": "aa", "ꯏ": "i", "ꯎ": "u",
    "ꯑꯣ": "o", "ꯑꯦ": "e", "ꯑꯧ": "ou", "ꯑꯩ": "ei",
}

def transliterate_reverse_line(line: str) -> str:
    out, chars, i = [], list(line), 0

    while i < len(chars):
        ch = chars[i]

        if ch == " ":
            out.append(" ")
            i += 1
            continue

        if i + 1 < len(chars) and ch + chars[i+1] in REV_INITIAL_VOWELS:
            out.append(REV_INITIAL_VOWELS[ch + chars[i+1]])
            i += 2
            continue

        if ch in REV_INITIAL_VOWELS:
            out.append(REV_INITIAL_VOWELS[ch])
            i += 1
            continue

        if ch in REV_LONSUM:
            out.append(REV_LONSUM[ch])
            i += 1
            continue

        if ch in REV_CONSONANTS:
            base = REV_CONSONANTS[ch]
            if i + 1 < len(chars) and chars[i+1] in REV_VOWELS:
                out.append(base + REV_VOWELS[chars[i+1]])
                i += 2
            else:
                out.append(base + "a")
                i += 1
            continue

        out.append(ch)
        i += 1

    return "".join(out)

# =========================================================
# LINE-BY-LINE AUTO DETECTION
# =========================================================

def is_meitei_line(line: str) -> bool:
    return any('\uABC0' <= ch <= '\uABFF' for ch in line)

def transliterate_text(text: str) -> str:
    output_lines = []
    for line in text.split("\n"):
        if is_meitei_line(line):
            output_lines.append(transliterate_reverse_line(line))
        else:
            output_lines.append(transliterate_forward_line(line))
    return "\n".join(output_lines)

# =========================================================
# GUI
# =========================================================

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Meitei Mayek ↔ Manipuri Latin (Line by Line)")

        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{int(sw*0.7)}x{int(sh*0.7)}")
        root.minsize(700, 400)

        self.build_ui()

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        tk.Label(
            self.root,
            text="Meitei Mayek ↔ Manipuri Latin Translator",
            font=("Segoe UI", 18, "bold")
        ).grid(row=0, column=0, pady=10)

        main = tk.Frame(self.root)
        main.grid(row=1, column=0, sticky="nsew", padx=15)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        tk.Label(main, text="Input").grid(row=0, column=0, sticky="w")
        tk.Label(main, text="Output").grid(row=0, column=1, sticky="w")

        self.input_box = tk.Text(main, wrap="word", font=("Segoe UI", 14))
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        self.input_box.bind("<KeyRelease>", self.update)

        self.output_box = tk.Text(main, wrap="word", font=("Segoe UI", 14),
                                  state="disabled")
        self.output_box.grid(row=1, column=1, sticky="nsew")

        controls = tk.Frame(self.root)
        controls.grid(row=2, column=0, pady=10)

        ttk.Button(controls, text="Copy Output", command=self.copy_output).pack(side="left", padx=8)
        ttk.Button(controls, text="Clear", command=self.clear).pack(side="left", padx=8)

    def update(self, event=None):
        text = self.input_box.get("1.0", "end-1c")
        result = transliterate_text(text)

        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", result)
        self.output_box.config(state="disabled")

    def copy_output(self):
        text = self.output_box.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Copy", "Nothing to copy.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()

    def clear(self):
        self.input_box.delete("1.0", "end")
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    TranslatorGUI(root)
    root.mainloop()

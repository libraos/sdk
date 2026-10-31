"""Mask direct identifiers before text leaves the machine; restore them in the answer.

    from veil_mask import Detector, Mapping, mask, restore

    detect = Detector()                         # downloads libraos/veil-detect from Hugging Face (about 1 GB)
    mapping = Mapping()                         # keep it for the whole conversation, and keep it to yourself
    masked = mask("Mail anna.berg@example.org", detect, mapping)   # "Mail [EMAIL_1]"
    # ... send `masked` to the outside model ...
    text, unresolved = restore("I wrote to [EMAIL_1].", mapping)   # "I wrote to anna.berg@example.org.", []

The detector is the open-weight token classifier; the regular expressions here catch what has a fixed shape. Dates,
amounts and cities are left in, because a model needs them to reason. The mapping holds the originals, so treat it as
you treat the text. Needs torch and transformers for Detector; the rest is stdlib.
"""
from __future__ import annotations

import re

REPO, REVISION = "libraos/veil-detect", "v1.0.0"


class Detector:
    """The published model over a document of any length. See the model card: huggingface.co/libraos/veil-detect."""

    def __init__(self, repo: str = REPO, revision: str = REVISION, device: str = "cpu", window: int = 384, stride: int = 64):
        import torch
        from transformers import AutoModelForTokenClassification, AutoTokenizer

        self.torch, self.device, self.window, self.stride = torch, device, window, stride
        self.tok = AutoTokenizer.from_pretrained(repo, revision=revision)
        self.model = AutoModelForTokenClassification.from_pretrained(repo, revision=revision).eval().to(device)

    def __call__(self, text: str) -> list[dict]:
        tok, id2label = self.tok, self.model.config.id2label
        enc = tok(text, add_special_tokens=False, return_offsets_mapping=True, verbose=False)
        ids, offsets = enc["input_ids"], enc["offset_mapping"]
        body, tag_at = self.window - 2, {}
        for start in range(0, max(1, len(ids) - self.stride), body - self.stride):
            x = self.torch.tensor([[tok.cls_token_id] + ids[start:start + body] + [tok.sep_token_id]]).to(self.device)
            with self.torch.no_grad():
                pred = self.model(input_ids=x).logits[0, 1:-1].argmax(-1).tolist()
            for (a, b), p in zip(offsets[start:start + body], pred):
                if a < b:
                    tag_at[(a, b)] = id2label[p]
        spans: list[dict] = []
        for (a, b), tag in sorted(tag_at.items()):
            if tag == "O":
                continue
            label = tag.split("-", 1)[1]
            prev = spans[-1] if spans else None
            if prev and prev["label"] == label and not text[prev["end"]:a].strip() and "\n" not in text[prev["end"]:a]:
                prev["end"] = b  # the same span, across a space but not a line break
            else:
                spans.append({"start": a, "end": b, "label": label})
        return spans


# ------------------------------------------------------------------ identifiers with a fixed shape
def _luhn(s: str) -> bool:
    digits = [int(c) for c in re.sub(r"\D", "", s)]
    total = sum(d if i % 2 == 0 else (d * 2 - 9 if d > 4 else d * 2) for i, d in enumerate(reversed(digits)))
    return 13 <= len(digits) <= 19 and total % 10 == 0 and len(set(digits)) > 1


def _iban(s: str) -> bool:
    s = s.replace(" ", "")
    return 15 <= len(s) <= 34 and int("".join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 == 1


def _ipv4(s: str) -> bool:
    return all(int(p) <= 255 for p in s.split("."))


_has_digit = lambda s: any(c.isdigit() for c in s)
_literal = lambda s: not re.search(r"[\[\](){}$<>%]", s)
_SERVICE_ACCOUNTS = {"root", "admin", "administrator", "user", "ubuntu", "debian", "centos", "ec2-user", "runner", "git", "deploy", "app", "node",
                     "postgres", "mysql", "service", "shared", "public", "default", "guest", "test", "www-data", "none", "null", "true", "false"}
_a_person = lambda s: s.casefold() not in _SERVICE_ACCOUNTS

# (kind, pattern, check, group). Earlier wins a tie; the longest match wins an overlap.
PATTERNS = [(kind, re.compile(rx), check, group) for kind, rx, check, group in [
    ("SECRET", r"(?<![\w+.\-])[A-Za-z][A-Za-z0-9+.\-]{1,20}://[^\s:/@\"']+:[^\s/@\"']+@[^\s<>\"']*[^\s<>\"'.,;:)]", None, 0),  # a URL with a password
    ("EMAIL", r"[\w.%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", None, 0),
    ("URL", r"(?:https?://|www\.)[^\s<>\"'()\[\]]*[^\s<>\"'()\[\].,;:]", None, 0),
    ("CONTACT", r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?!\d|\.\d)", _ipv4, 0),
    ("PHONE", r"(?<![\w])\+\d{1,3}[ -]?\(?\d{1,4}\)?(?:[ -]?\d{2,4}){2,4}(?!\d)", None, 0),
    ("PHONE", r"(?<![\w])\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}(?!\d)", None, 0),
    ("PHONE", r"(?<!\d)1[3-9]\d(?:[ -]?\d{4}){2}(?!\d)", None, 0),
    ("ACCOUNT", r"(?<![\d-])(?:\d[ -]?){12,18}\d(?![\d-])", _luhn, 0),
    ("ACCOUNT", r"(?<![A-Z0-9])[A-Z]{2}\d{2}(?: ?[A-Z0-9]{4}){2,7}(?: ?[A-Z0-9]{1,4})?(?![A-Z0-9])", _iban, 0),
    ("ACCOUNT", r"(?<![0-9A-Za-z])0x[0-9a-fA-F]{40}(?![0-9A-Za-z])", None, 0),
    ("ID", r"(?<![0-9A-Za-z])0x[0-9a-fA-F]{64}(?![0-9A-Za-z])", None, 0),
    ("ID", r"(?<![\d-])(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}(?![\d-])", None, 0),
    ("ID", r"(?<![\dXx])\d{17}[\dXx](?![\dXx])", None, 0),  # 身份证
    ("SECRET", r"(?<![\w\-])(?:sk-[\w\-]{20,}|[spr]k_(?:live|test)_[A-Za-z0-9]{16,}|(?:AKIA|ASIA)[A-Z0-9]{16}|AIza[\w\-]{35}|gh[pousr]_[A-Za-z0-9]{36,}"
               r"|github_pat_\w{22,}|glpat-[\w\-]{20,}|xox[abeoprs]-[A-Za-z0-9\-]{10,}|hf_[A-Za-z0-9]{30,}|npm_[A-Za-z0-9]{36,}|msk_(?:live|test)_[\w\-]{16,})(?![\w\-])", _has_digit, 0),
    ("SECRET", r"(?<![\w\-])eyJ[\w\-]{8,}\.eyJ[\w\-]{8,}\.[\w\-]{8,}(?![\w\-])", None, 0),  # a JWT
    ("SECRET", r"(?i:\bbearer)\s+([A-Za-z0-9._~+/=\-]{16,})", _has_digit, 1),
    ("SECRET", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----[A-Za-z0-9+/=\s\\]{16,}(?:-----END [A-Z0-9 ]*PRIVATE KEY-----)?", None, 0),
    # After a label: an unquoted value must hold more than a name (code assigns password = self.secret), a quoted one is a literal.
    ("SECRET", r"(?:(?i:\b(?:password|passphrase|passwd|pwd))|密码|口令)[\"']?\s*[:=：]\s*([^\s\"',;，。；]{5,127}[^\s\"',;，。；.!?:)])",
     lambda s: _literal(s) and bool(re.search(r"[^A-Za-z._\-]", s)), 1),
    ("SECRET", r"(?i:\b(?:password|passphrase|passwd|pwd))[\"']?\s*[:=]\s*[\"']([^\"'\n]{4,127})[\"']", _literal, 1),
    # The name in a home directory or a login. Only the name goes: the rest of a path is what a reader needs. A bare
    # "user:" is not a login, because "User: hello" is a chat turn.
    ("CONTACT", r"(?:/home/|/Users/|[A-Za-z]:\\+Users\\+)([\w.\-]{2,64})", _a_person, 1),
    ("CONTACT", r"(?<![A-Za-z])(?:(?i:user(?:[_-]?name)?|login)\s*=\s*|[\"'](?i:user(?:[_-]?name)?|login)[\"']\s*:\s*|(?i:user[_-]?name)\s*:\s*)[\"']([\w.\-]{2,64})[\"']", _a_person, 1),
    ("ADDRESS", r"(?<![A-Za-z0-9])[A-PR-UWYZ][A-HK-Y]?\d[A-Z\d]? \d[ABD-HJLNP-UW-Z]{2}(?![A-Za-z0-9])", None, 0),  # a UK postcode
]]

# ------------------------------------------------------------------ what the detector's labels mean here
KIND_OF_LABEL = {"person": "PERSON", "organization": "COMPANY", "id": "ID", "financial": "ACCOUNT", "credential": "SECRET", "date_of_birth": "DOB"}
_STREET = re.compile(r"\d|\b(?:street|st\.|avenue|ave\.?|boulevard|blvd|road|rd\.|drive|lane|way|suite|unit|apt\.?|floor|rue|chemin)\b|路|街|号|弄|室|栋|大厦", re.I)
_BIRTH = re.compile(r"(?i)(?:\bborn(?:\s+on)?|date\s+of\s+birth|\bDOB\b|birth\s*date|出生)[^.;\n]{0,25}$")
# Words a contract uses for its own parties: the detector proposes them, and they identify nobody.
_ROLES = {"employer", "employee", "company", "customer", "client", "party", "parties", "landlord", "tenant", "buyer", "seller", "vendor", "user", "甲方", "乙方", "公司", "客户"}
_CJK = re.compile(r"[\u4e00-\u9fff]")


def _is_word(c: str) -> bool:
    return c.isalnum() and not _CJK.match(c)


def _whole_words(text: str, a: int, b: int) -> tuple[int, int]:
    """A model fragment inside a number or a name would leave its other half in clear."""
    while a < b and not text[a].isalnum() and text[a] not in "+(":
        a += 1
    while b > a and not text[b - 1].isalnum() and text[b - 1] not in ".)":
        b -= 1
    while a > 0 and a < b and _is_word(text[a - 1]) and _is_word(text[a]):
        a -= 1
    while a < b < len(text) and _is_word(text[b]) and _is_word(text[b - 1]):
        b += 1
    return a, b


def _kind_of_contact(value: str) -> str:
    if "@" in value:
        return "EMAIL"
    if re.match(r"(?:https?://|www\.)", value, re.I):
        return "URL"
    return "PHONE" if sum(c.isdigit() for c in value) >= 7 and not re.fullmatch(r"[\d.]+", value) else "CONTACT"


def _model_spans(text: str, detect) -> list[tuple[int, int, str]]:
    spans: list[tuple[int, int, str]] = []
    for s in sorted(detect(text), key=lambda s: s["start"]):
        a, b = _whole_words(text, s["start"], s["end"])
        value, label = text[a:b], s["label"]
        if not value or value.casefold().removeprefix("the ") in _ROLES:
            continue
        if label == "location":
            # Pieces of one address are one span, so it gets one placeholder; the street test comes afterwards.
            if spans and spans[-1][2] == "LOCATION" and re.fullmatch(r"[\s,]{0,3}", text[spans[-1][1]:a]):
                spans[-1] = (spans[-1][0], b, "LOCATION")
            else:
                spans.append((a, b, "LOCATION"))
        elif label == "contact":
            spans.append((a, b, _kind_of_contact(value)))
        elif label == "date" and _BIRTH.search(text[max(0, a - 40):a]):
            spans.append((a, b, "DOB"))
        elif label in KIND_OF_LABEL:
            spans.append((a, b, KIND_OF_LABEL[label]))
    return [(a, b, "ADDRESS" if k == "LOCATION" else k) for a, b, k in spans if k != "LOCATION" or _STREET.search(text[a:b])]


def find_spans(text: str, detect) -> list[tuple[int, int, str]]:
    """Non-overlapping (start, end, kind). Patterns are final; a model span keeps only the parts outside them."""
    rules = []
    for kind, rx, check, group in PATTERNS:
        for m in rx.finditer(text):
            if check is None or check(m.group(group)):
                rules.append((m.start(group), m.end(group), kind))
    spans = list(rules)
    # The model can lose a name when an address next to it repeats that name (margaret.holloway@...). A second pass with
    # what the patterns already found blanked out, at the same length so offsets hold, gets those back.
    blanked = list(text)
    for a, b, _ in rules:
        blanked[a:b] = " " * (b - a)
    blanked = "".join(blanked)
    for a, b, kind in _model_spans(text, detect) + (_model_spans(blanked, detect) if rules else []):
        pieces = [(a, b)]
        for ra, rb, _ in rules:
            pieces = [p for x, y in pieces for p in ([(x, y)] if rb <= x or ra >= y else [(x, min(y, ra)), (max(x, rb), y)]) if p[0] < p[1]]
        for x, y in pieces:
            x, y = _whole_words(text, x, y)
            if sum(c.isalnum() for c in text[x:y]) >= 2:
                spans.append((x, y, kind))
    # Every mention of a name, not only the ones the model tagged.
    for name, kind in {(text[a:b], k) for a, b, k in spans if k in ("PERSON", "COMPANY") and b - a >= 2}:
        if len(name) >= 4 or _CJK.search(name):
            edge = (r"", r"") if _CJK.search(name) else (r"(?<!\w)", r"(?!\w)")
            spans += [(m.start(), m.end(), kind) for m in re.finditer(edge[0] + re.escape(name) + edge[1], text)]
        if kind == "PERSON":  # "Priya Raman" is later "Ms. Raman", which the model does not always tag
            for part in name.split()[1:] + name.split()[:1] if " " in name else []:
                if len(part) >= 3 and part[0].isupper():
                    spans += [(m.start(), m.end(), kind) for m in re.finditer(r"(?<!\w)" + re.escape(part) + r"(?!\w)", text)]
    out: list[tuple[int, int, str]] = []
    for a, b, kind in sorted(spans, key=lambda s: (s[0], s[0] - s[1])):
        if out and a < out[-1][1]:
            continue
        # One name or address the model tagged in pieces gets one placeholder.
        joins = {"PERSON": r" +", "COMPANY": r" +", "ADDRESS": r"[ ,]{1,3}"}.get(kind)
        if out and out[-1][2] == kind and joins and re.fullmatch(joins, text[out[-1][1]:a]):
            out[-1] = (out[-1][0], b, kind)
        else:
            out.append((a, b, kind))
    return out


# ------------------------------------------------------------------ the round trip
_KINDS = "PERSON|COMPANY|ADDRESS|EMAIL|PHONE|URL|CONTACT|ID|ACCOUNT|SECRET|DOB"
_PLACEHOLDER = re.compile(rf"\[\s*({_KINDS})[_ ](\d+)\s*\]|(?<![A-Za-z0-9_])({_KINDS})_(\d+)(?![A-Za-z0-9_])", re.I)


def _key(m: re.Match) -> tuple[str, int]:
    kind, n = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
    return kind.upper(), int(n)


class Mapping:
    """Which placeholder stands for what, for one conversation. It holds the originals: keep it local, never log it."""

    def __init__(self) -> None:
        self.originals: dict[tuple[str, int], str] = {}
        self._placeholder_of: dict[tuple[str, str], tuple[str, int]] = {}
        self._counts: dict[str, int] = {}
        self._already_in_text: set[tuple[str, int]] = set()

    def placeholder(self, kind: str, value: str) -> str:
        key = self._placeholder_of.get((kind, value.casefold())) or self._person_with_this_part(kind, value)
        if key is None:
            n = self._counts.get(kind, 0) + 1
            while (kind, n) in self._already_in_text:
                n += 1
            self._counts[kind] = n
            key = self._placeholder_of[(kind, value.casefold())] = (kind, n)
            self.originals[key] = value
        return f"[{key[0]}_{key[1]}]"

    def _person_with_this_part(self, kind: str, value: str) -> tuple[str, int] | None:
        """"Ms. Raman" is the same person as "Priya Raman", and the model has to know that to reason. If two people share
        the surname it stays apart. It restores as the full name, which reads correctly in an answer."""
        if kind != "PERSON" or " " in value:
            return None
        found = {key for (k, name), key in self._placeholder_of.items() if k == kind and value.casefold() in name.split()}
        return found.pop() if len(found) == 1 else None


def mask(text: str, detect, mapping: Mapping) -> str:
    """Text with placeholders in place of direct identifiers. Call it on every message of a conversation with one mapping,
    so one person keeps one placeholder across turns."""
    mapping._already_in_text |= {_key(m) for m in _PLACEHOLDER.finditer(text)}
    spans = find_spans(text, detect)
    for a, b, kind in spans:  # full names first, so a surname that comes before its full name still joins it
        if kind == "PERSON" and " " in text[a:b]:
            mapping.placeholder(kind, text[a:b])
    out, pos = [], 0
    for a, b, kind in spans:
        out += [text[pos:a], mapping.placeholder(kind, text[a:b])]
        pos = b
    return "".join(out) + text[pos:]


def restore(text: str, mapping: Mapping) -> tuple[str, list[str]]:
    """(the answer with the originals back, the placeholders the mapping does not cover). If that list is not empty, the
    model made one up or garbled one, so do not show the answer as it is."""
    unresolved: list[str] = []

    def back(m: re.Match) -> str:
        key = _key(m)
        if key in mapping.originals:
            return mapping.originals[key]
        if key not in mapping._already_in_text:
            unresolved.append(m.group(0))
        return m.group(0)

    return _PLACEHOLDER.sub(back, text), unresolved

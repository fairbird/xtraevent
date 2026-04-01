# -*- coding: utf-8 -*-

import sys
import json

PY3 = sys.version_info[0] >= 3

try:
    # Python 2
    from urllib import urlencode
    import urllib2 as request_mod
except ImportError:
    # Python 3
    from urllib.parse import urlencode
    import urllib.request as request_mod


TARGET_LANG = ""


def _to_unicode(text):
    if text is None:
        return u""
    try:
        if PY3:
            if isinstance(text, str):
                return text
            else:
                return text.decode("utf-8", "ignore")
        else:
            if isinstance(text, unicode):
                return text
            else:
                return text.decode("utf-8", "ignore")
    except Exception:
        try:
            return str(text)
        except Exception:
            return u""


def is_mostly_arabic(text):
    t = _to_unicode(text)
    if not t:
        return False

    total_letters = 0
    arabic_letters = 0

    for ch in t:
        code = ord(ch)
        if (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A) or (0x0600 <= code <= 0x06FF):
            total_letters += 1
            if 0x0600 <= code <= 0x06FF:
                arabic_letters += 1

    if total_letters == 0:
        return False

    try:
        ratio = float(arabic_letters) / float(total_letters)
    except Exception:
        return False
    return ratio >= 0.6

def is_arabic_word(word):
    w = _to_unicode(word)
    if not w:
        return False

    letters = [ch for ch in w if ch.strip()]
    if not letters:
        return False

    arabic = 0
    for ch in letters:
        code = ord(ch)
        if 0x0600 <= code <= 0x06FF:
            arabic += 1

    try:
        ratio = float(arabic) / float(len(letters))
    except Exception:
        return False

    return ratio >= 0.6


def levenshtein_distance(a, b, max_distance=2):
    a = _to_unicode(a)
    b = _to_unicode(b)

    if a == b:
        return 0

    if abs(len(a) - len(b)) > max_distance:
        return max_distance + 1

    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)

    if len(a) > len(b):
        a, b = b, a

    previous_row = list(range(len(b) + 1))

    for i, ca in enumerate(a, 1):
        current_row = [i]
        min_in_row = i
        for j, cb in enumerate(b, 1):
            insert_cost = current_row[j - 1] + 1
            delete_cost = previous_row[j] + 1
            replace_cost = previous_row[j - 1] + (0 if ca == cb else 1)
            c = min(insert_cost, delete_cost, replace_cost)
            current_row.append(c)
            if c < min_in_row:
                min_in_row = c
        if min_in_row > max_distance:
            return max_distance + 1
        previous_row = current_row

    return previous_row[-1]


def post_process_arabic_text(original, translated):
    o = _to_unicode(original)
    t = _to_unicode(translated)

    while u"  " in t:
        t = t.replace(u"  ", u" ")

    o_words = o.split()
    t_words = t.split()

    if not o_words or not t_words:
        return t.strip()

    n = min(len(o_words), len(t_words))
    new_t_words = list(t_words)

    for i in range(n):
        ow = o_words[i]
        tw = t_words[i]

        if is_arabic_word(ow) and is_arabic_word(tw):
            if len(ow) >= 3 and levenshtein_distance(ow, tw, max_distance=1) <= 1:
                new_t_words[i] = ow

    return u" ".join(new_t_words).strip()


def translate_text(text, target_lang=None):
    """
    Hybrid translation + auto-correction:
    - If text is already mostly Arabic, return it unchanged.
    - If target_lang is not provided, return empty string so caller can keep original text.
    - Otherwise translate with Google.
    """
    text = _to_unicode(text)

    if not text:
        return u""

    if not target_lang:
        return u""

    if is_mostly_arabic(text) and target_lang == "ar":
        return text

    base_url = "https://translate.googleapis.com/translate_a/single"

    params = {
        "client": "gtx",
        "sl": "auto",
        "tl": target_lang,
        "dt": "t",
        "q": text.encode("utf-8") if not PY3 else text,
    }

    try:
        query_string = urlencode(params)
        if PY3 and isinstance(query_string, bytes):
            query_string = query_string.decode("utf-8")

        url = base_url + "?" + query_string

        req = request_mod.Request(url)
        resp = request_mod.urlopen(req, timeout=10)
        raw = resp.read()

        if PY3 and isinstance(raw, bytes):
            raw = raw.decode("utf-8")

        data = json.loads(raw)

        translated_chunks = []
        if isinstance(data, list) and data:
            for item in data[0]:
                if item and isinstance(item, list) and item[0]:
                    translated_chunks.append(item[0])

        translated_text = u"".join(translated_chunks).strip()
        if not translated_text:
            return u""

        if target_lang == "ar":
            translated_text = post_process_arabic_text(text, translated_text)

        return translated_text

    except Exception as e:
        try:
            print("Error in Google Translate:", str(e))
        except Exception:
            pass
        return u""
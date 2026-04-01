# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re

REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'
    r'(: odc\.\d+)|'
    r'(\d+: odc\.\d+)|'
    r'(\d+ odc\.\d+)|'
    r'!|'
    r'/.*|'
    r'\|\s[0-9]+\+|'
    r'[0-9]+\+|'
    r'\s\d{4}\Z|'
    r'([\(\[\|].*?[\)\]\|])|'
    r'(\"|\"\.|\"\,|\.)\s.+|'
    r'\"|:|'
    r'\*|'
    r'Премьера\.\s|'
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
    r'(х|Х|м|М|т|Т|д|Д)/с\s|'
    r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
    r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
    r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
    r'\d{1,3}(-я|-й|\sс-н).+|',
    re.DOTALL
)

# Easy manual title fixes
# Exact match replacement after cleaning
TITLE_REPLACEMENTS_EXACT = {
    u"التفاح الحرام": u"التفاحة المحرمة",
}

# Partial replacement after cleaning
TITLE_REPLACEMENTS_CONTAINS = {
    # u"old text": u"new text",
}

ELCINEMA_INFO_DIR_NAME = "infoselcinema"
ELCINEMA_STAR_DIR_NAME = "infoselcinemastars"
ELCINEMA_RATED_DIR_NAME = "infoselcinemarated"
TMDB_INFO_DIR_NAME = "infos"
TMDB_STAR_DIR_NAME = "infostmdbstar"
TMDB_RATED_DIR_NAME = "infostmdbrated"
OMDB_INFO_DIR_NAME = "infosomdb"
OMDB_STAR_DIR_NAME = "infosomdbsterne"
OMDB_RATED_DIR_NAME = "infosomdbrated"

def safe_str(value):
    try:
        if value is None:
            return ""
        return str(value).strip()
    except Exception:
        return ""

def helper_log(message):
    try:
        log_fn = globals().get("logout")
        if callable(log_fn):
            log_fn("xtraTitleHelper " + safe_str(message))
    except Exception:
        pass

def smart_capitalize_title(title):
    try:
        title = safe_str(title)
        if not title:
            return ""
        if re.search(r'[\u0600-\u06FF]', title):
            return title
        small_words = {
            "a", "an", "and", "as", "at", "but", "by", "for", "from",
            "in", "into", "nor", "of", "on", "or", "over", "the", "to", "with"
        }
        result = []
        for i, word in enumerate(title.split()):
            if re.match(r'^\d+([.,]\d+)?$', word):
                result.append(word)
                continue
            if re.search(r'\d', word):
                result.append(word.upper() if word.isupper() else word)
                continue
            lower_word = word.lower()
            if i > 0 and lower_word in small_words:
                result.append(lower_word)
            else:
                result.append(lower_word[:1].upper() + lower_word[1:])
        return " ".join(result)
    except Exception:
        return safe_str(title)

def apply_title_replacements(title):
    try:
        title = safe_str(title)
        if not title:
            return ""

        # Exact match first
        if title in TITLE_REPLACEMENTS_EXACT:
            replaced = TITLE_REPLACEMENTS_EXACT[title]
            helper_log("apply_title_replacements exact {} -> {}".format(title, replaced))
            title = replaced

        # Partial contains replacements
        for old_value, new_value in TITLE_REPLACEMENTS_CONTAINS.items():
            if old_value and old_value in title:
                updated = title.replace(old_value, new_value)
                helper_log("apply_title_replacements contains {} -> {} result={}".format(old_value, new_value, updated))
                title = updated

        return title
    except Exception as err:
        helper_log("apply_title_replacements error={}".format(err))
        return safe_str(title)

def clean_search_title(title):
    try:
        if not title:
            return ""
        original_title = safe_str(title)
        title = original_title
        title = title.replace('\xc2\x86', '').replace('\xc2\x87', '')
        title = re.sub(r'^(live:\s*|LIVE:\s*|LIVE\s+|live\s+)', '', title).strip()
        title = REGEX.sub('', title).strip()
        title = title.replace(":", " ")
        title = re.sub(r'[_]+', ' _ ', title)
        title = re.sub(r'[-]+', ' - ', title)
        title = re.sub(r'\s{2,}', ' ', title).strip()

        arabic_patterns = [
            r'\s*[_\-]+\s*ج\s*\d+\s*[_\-]+\s*ح\s*\d+.*$',
            r'\s*[_\-]+\s*ح\s*\d+\s*[_\-]+\s*ج\s*\d+.*$',
            r'\s*[_\-]+\s*جزء\s*\d+\s*[_\-]+\s*حلقة\s*\d+.*$',
            r'\s*[_\-]+\s*حلقة\s*\d+\s*[_\-]+\s*جزء\s*\d+.*$',
            r'\s*[_\-]+\s*الموسم\s*\d+\s*[_\-]+\s*الحلقة\s*\d+.*$',
            r'\s*[_\-]+\s*الحلقة\s*\d+\s*[_\-]+\s*الموسم\s*\d+.*$',
            r'\s+ج\s*\d+\s+ح\s*\d+.*$',
            r'\s+ح\s*\d+\s+ج\s*\d+.*$',
            r'\s+جزء\s*\d+\s+حلقة\s*\d+.*$',
            r'\s+حلقة\s*\d+\s+جزء\s*\d+.*$',
            r'\s+الموسم\s*\d+\s+الحلقة\s*\d+.*$',
            r'\s+الحلقة\s*\d+\s+الموسم\s*\d+.*$',
            r'\s*[_\-]+\s*ج\s*\d+.*$',
            r'\s*[_\-]+\s*ح\s*\d+.*$',
            r'\s*[_\-]+\s*جزء\s*\d+.*$',
            r'\s*[_\-]+\s*حلقة\s*\d+.*$',
            r'\s*[_\-]+\s*الموسم\s*\d+.*$',
            r'\s*[_\-]+\s*الحلقة\s*\d+.*$',
            r'\s+ج\s*\d+.*$',
            r'\s+ح\s*\d+.*$',
            r'\s+جزء\s*\d+.*$',
            r'\s+حلقة\s*\d+.*$',
            r'\s+الموسم\s*\d+.*$',
            r'\s+الحلقة\s*\d+.*$',
        ]
        for pattern in arabic_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()

        english_patterns = [
            r'\s*[_\-]+\s*S\d+\s*E\d+.*$',
            r'\s+S\d+\s*E\d+.*$',
            r'\s*[_\-]+\s*Season\s*\d+\s*Episode\s*\d+.*$',
            r'\s+Season\s*\d+\s*Episode\s*\d+.*$',
            r'\s*[_\-]+\s*Episode\s*\d+.*$',
            r'\s+Episode\s*\d+.*$',
            r'\s*[_\-]+\s*Ep\.?\s*\d+.*$',
            r'\s+Ep\.?\s*\d+.*$',
        ]
        for pattern in english_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()

        title = re.sub(r'\s*[_\-:|]+\s*$', '', title).strip()
        title = re.sub(r'\s{2,}', ' ', title).strip()

        # Manual replacements
        title = apply_title_replacements(title)

        title = smart_capitalize_title(title)
        helper_log("clean_search_title original={} result={}".format(original_title, title))
        return title
    except Exception:
        return smart_capitalize_title(safe_str(title))

def contains_arabic_text(text):
    try:
        text = safe_str(text)
        result = bool(text and re.search(r'[\u0600-\u06FF]', text))
        return result
    except Exception:
        return False

def safe_filename(value):
    try:
        value = safe_str(value)
        value = re.sub(r'[^\w\-\.\u0600-\u06FF]+', '_', value, flags=re.UNICODE)
        value = re.sub(r'_+', '_', value).strip('._')
        return value or "title"
    except Exception:
        return "title"

def tmdb_provider_enabled():
    try:
        from Components.config import config
        return bool(config.plugins.xtraEvent.tmdb.value)
    except Exception:
        return True

def elcinema_provider_enabled():
    try:
        from Components.config import config
        return bool(config.plugins.xtraEvent.extra3.value)
    except Exception:
        return True

def omdb_provider_enabled():
    return True

def _join_xtra_dir(pathLoc, folder_name, clean_title):
    try:
        return "{}xtraEvent/{}/{}.json".format(pathLoc, folder_name, clean_title)
    except Exception:
        return ""

def _enabled_order(arabic, prefer_tmdb=True):
    tmdb_on = tmdb_provider_enabled()
    elcinema_on = elcinema_provider_enabled()
    omdb_on = omdb_provider_enabled()
    order = []

    if arabic:
        if elcinema_on:
            order.append("elcinema")
        if tmdb_on:
            order.append("tmdb")
        if omdb_on:
            order.append("omdb")
    else:
        if prefer_tmdb:
            if tmdb_on:
                order.append("tmdb")
            if omdb_on:
                order.append("omdb")
            if elcinema_on:
                order.append("elcinema")
        else:
            if omdb_on:
                order.append("omdb")
            if tmdb_on:
                order.append("tmdb")
            if elcinema_on:
                order.append("elcinema")

    if not order:
        order = ["omdb", "tmdb", "elcinema"]
    return order

def get_selected_provider_for_title(clean_title, prefer_tmdb=True):
    arabic = contains_arabic_text(clean_title)
    order = _enabled_order(arabic, prefer_tmdb=prefer_tmdb)
    provider = order[0] if order else "omdb"
    helper_log("selected provider title={} arabic={} prefer_tmdb={} provider={}".format(clean_title, arabic, prefer_tmdb, provider))
    return provider

def get_info_json_candidates(pathLoc, clean_title, prefer_tmdb=True):
    order = _enabled_order(contains_arabic_text(clean_title), prefer_tmdb=prefer_tmdb)
    mapping = {
        "elcinema": [ELCINEMA_INFO_DIR_NAME],
        "tmdb": [TMDB_INFO_DIR_NAME],
        "omdb": [OMDB_INFO_DIR_NAME],
    }
    folders = []
    for provider in order:
        folders.extend(mapping.get(provider, []))
    helper_log("info candidates title={} folders={}".format(clean_title, folders))
    return [_join_xtra_dir(pathLoc, folder, clean_title) for folder in folders]

def get_star_json_candidates(pathLoc, clean_title, prefer_tmdb=True):
    order = _enabled_order(contains_arabic_text(clean_title), prefer_tmdb=prefer_tmdb)
    mapping = {
        "elcinema": [ELCINEMA_STAR_DIR_NAME, ELCINEMA_INFO_DIR_NAME],
        "tmdb": [TMDB_STAR_DIR_NAME, TMDB_INFO_DIR_NAME],
        "omdb": [OMDB_STAR_DIR_NAME, OMDB_INFO_DIR_NAME],
    }
    folders = []
    for provider in order:
        folders.extend(mapping.get(provider, []))
    helper_log("star candidates title={} folders={}".format(clean_title, folders))
    return [_join_xtra_dir(pathLoc, folder, clean_title) for folder in folders]

def get_rated_json_candidates(pathLoc, clean_title, prefer_tmdb=True):
    order = _enabled_order(contains_arabic_text(clean_title), prefer_tmdb=prefer_tmdb)
    mapping = {
        "elcinema": [ELCINEMA_RATED_DIR_NAME, ELCINEMA_INFO_DIR_NAME],
        "tmdb": [TMDB_RATED_DIR_NAME, TMDB_INFO_DIR_NAME],
        "omdb": [OMDB_RATED_DIR_NAME, OMDB_INFO_DIR_NAME],
    }
    folders = []
    for provider in order:
        folders.extend(mapping.get(provider, []))
    helper_log("rated candidates title={} folders={}".format(clean_title, folders))
    return [_join_xtra_dir(pathLoc, folder, clean_title) for folder in folders]

def get_provider_target_json_path(pathLoc, clean_title, provider, json_kind="info"):
    folder = ""
    if json_kind == "info":
        folder = {
            "elcinema": ELCINEMA_INFO_DIR_NAME,
            "tmdb": TMDB_INFO_DIR_NAME,
            "omdb": OMDB_INFO_DIR_NAME,
        }.get(provider, OMDB_INFO_DIR_NAME)
    elif json_kind == "star":
        folder = {
            "elcinema": ELCINEMA_STAR_DIR_NAME,
            "tmdb": TMDB_STAR_DIR_NAME,
            "omdb": OMDB_STAR_DIR_NAME,
        }.get(provider, OMDB_STAR_DIR_NAME)
    elif json_kind == "rated":
        folder = {
            "elcinema": ELCINEMA_RATED_DIR_NAME,
            "tmdb": TMDB_RATED_DIR_NAME,
            "omdb": OMDB_RATED_DIR_NAME,
        }.get(provider, OMDB_RATED_DIR_NAME)
    return _join_xtra_dir(pathLoc, folder, clean_title)

def load_first_json(path_list):
    try:
        import json
        import os
        for json_path in path_list:
            if json_path and os.path.exists(json_path):
                with open(json_path, "r") as handle:
                    data = json.load(handle)
                helper_log("load_first_json selected={}".format(json_path))
                return data, json_path
    except Exception as err:
        helper_log("load_first_json error={}".format(err))
    return {}, None
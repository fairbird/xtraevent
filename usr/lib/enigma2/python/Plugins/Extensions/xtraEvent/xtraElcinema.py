# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import re
import json
from html import unescape

try:
    from .xtraTitleHelper import clean_search_title, safe_str, safe_filename, ELCINEMA_INFO_DIR_NAME, ELCINEMA_STAR_DIR_NAME, ELCINEMA_RATED_DIR_NAME
except Exception:
    from xtraTitleHelper import clean_search_title, safe_str, safe_filename, ELCINEMA_INFO_DIR_NAME, ELCINEMA_STAR_DIR_NAME, ELCINEMA_RATED_DIR_NAME


def _log(message):
    try:
        log_fn = globals().get("logout")
        if callable(log_fn):
            log_fn("xtraElcinema " + safe_str(message))
    except Exception:
        pass


def _strip_tags(value):
    value = safe_str(value)
    if not value:
        return ""
    value = re.sub(r'<br\s*/?>', '\n', value, flags=re.IGNORECASE)
    value = re.sub(r'<span[^>]*class=["\']hide["\'][^>]*>(.*?)</span>', r' \1', value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r'<a[^>]*id=["\']read-more["\'][^>]*>.*?</a>', '', value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r'<a[^>]*>.*?</a>', '', value, flags=re.IGNORECASE | re.DOTALL)
    value = re.sub(r'<[^>]+>', '', value)
    value = unescape(value)
    value = re.sub(r'\s+', ' ', value).strip()
    return value


def _extract_first(patterns, text, flags=re.IGNORECASE | re.DOTALL):
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(1).strip()
    return ""


def _extract_all(pattern, text, flags=re.IGNORECASE | re.DOTALL):
    return [m.strip() for m in re.findall(pattern, text, flags) if safe_str(m).strip()]


def _parse_duration_minutes(duration_text):
    try:
        m = re.search(r'(\d+)', safe_str(duration_text))
        if m:
            return int(m.group(1))
    except Exception:
        pass
    return 0


def _extract_plot(html_text):
    html_text = safe_str(html_text)
    plot_candidates = [
        # Details section: ملخص القصة
        r'<strong>\s*ملخص\s+القصة\s*:?\s*</strong>\s*<p[^>]*>(.*?)</p>',
        # Alternate details layout
        r'ملخص\s+القصة\s*:?\s*</strong>\s*<p[^>]*>(.*?)</p>',
        # Intro paragraph after the metadata block
        r'<div class="intro-box".*?<hr\s*/?>\s*(?:.*?\n)*?\s*<p[^>]*>(.*?)</p>',
        # Fallback generic intro paragraph
        r'<div class="intro-box".*?<p[^>]*>(.*?)</p>',
    ]

    for pattern in plot_candidates:
        match = re.search(pattern, html_text, re.IGNORECASE | re.DOTALL)
        if match:
            raw_plot = match.group(1).strip()
            clean_plot = _strip_tags(raw_plot)
            if clean_plot:
                _log("plot extracted pattern={} value={}".format(pattern, clean_plot[:120]))
                return clean_plot

    _log("plot not found")
    return ""


def _extract_title_ar(html_text):
    title_ar = _extract_first([
        r'<span class="left(?:\s+notranslate)?" dir="rtl">(.*?)</span>',
        r'id="title-ar"[^>]*value="([^"]+)"',
        r"id='title-ar'[^>]*value='([^']+)'",
        r'<h1[^>]*>.*?<span class="left(?:\s+notranslate)?" dir="rtl">(.*?)</span>',
    ], html_text)
    return _strip_tags(title_ar)


def _extract_title_en(html_text):
    title_en = _extract_first([
        r'<span class="right(?:\s+notranslate)?" dir="ltr">(.*?)</span>',
        r'id="title-en"[^>]*value="([^"]+)"',
        r"id='title-en'[^>]*value='([^']+)'",
    ], html_text)
    return _strip_tags(title_en)


def extract_elcinema_data(html_text):
    html_text = safe_str(html_text)
    data = {}

    work_id = _extract_first([
        r'og:url"\s+content="https?://elcinema\.com/work/(\d+)',
        r'canonical"\s+href="https?://elcinema\.com/work/(\d+)/?"',
        r'/work/(\d+)'
    ], html_text)
    data["id"] = work_id

    poster = _extract_first([
        r'<div class="intro-box".*?<img[^>]+src="(https?://[^"]+_315x420_[^"]+)"',
        r'<meta property="og:image" content="(https?://[^"]+)"'
    ], html_text)
    data["poster"] = poster

    rating = _extract_first([
        r'<div class="stars-orange-\d+">.*?<div>([\d.]+)</div>',
        r'التقييم\s*:\s*([\d.]+)'
    ], html_text)

    title_ar = _extract_title_ar(html_text)
    title_en = _extract_title_en(html_text)

    year = _extract_first([
        r'<span class="left">\s*&nbsp;\((\d{4})\)&nbsp;',
        r'\((\d{4})\)'
    ], html_text)

    media_type = _extract_first([
        r'<ul class="list-separator">\s*<li><a href="/index/work/category/\d+">(.*?)</a></li>',
        r'<li><a href="/index/work/category/\d+">(.*?)</a></li>'
    ], html_text)

    country = _extract_first([
        r'<a href="/index/work/country/[^"]+">(.*?)</a>'
    ], html_text)

    duration = _extract_first([
        r'<a href="/index/work/country/[^"]+">.*?</a></li>\s*<li>(.*?)</li>',
        r'<li>(\d+\s*دقيقة)</li>'
    ], html_text)

    genre = _extract_first([
        r'تصنيف العمل:.*?<a href="/index/work/genre/\d+">(.*?)</a>',
        r'تصنيف العمل:.*?<li><a[^>]*>(.*?)</a></li>'
    ], html_text)

    plot = _extract_plot(html_text)

    director = _extract_first([
        r'<ul class="list-separator list-title">\s*<li>ﺇﺧﺮاﺝ:</li>.*?<a href="/person/\d+/">(.*?)</a>',
        r'<li>ﺇﺧﺮاﺝ:</li>.*?<a href="/person/\d+/">(.*?)</a>',
        r'<li>إخراج:</li>.*?<a href="/person/\d+/">(.*?)</a>'
    ], html_text)

    writer = _extract_first([
        r'<ul class="list-separator list-title">\s*<li>ﺗﺄﻟﻴﻒ:</li>.*?<a href="/person/\d+/">(.*?)</a>',
        r'<li>ﺗﺄﻟﻴﻒ:</li>.*?<a href="/person/\d+/">(.*?)</a>',
        r'<li>تأليف:</li>.*?<a href="/person/\d+/">(.*?)</a>'
    ], html_text)

    cast_block = _extract_first([
        r'(<ul class="list-separator list-title">\s*<li>طاقم العمل:</li>.*?</ul>)'
    ], html_text)

    cast_names = []
    if cast_block:
        cast_names = _extract_all(r'<a href="/person/\d+/">(.*?)</a>', cast_block)

    data.update({
        "title_ar": title_ar,
        "title_en": title_en,
        "year": safe_str(year),
        "media_type": _strip_tags(media_type),
        "country": _strip_tags(country),
        "duration": _strip_tags(duration),
        "genre": _strip_tags(genre),
        "plot": safe_str(plot),
        "director": _strip_tags(director),
        "writer": _strip_tags(writer),
        "cast": [_strip_tags(x) for x in cast_names if _strip_tags(x)],
        "rating": safe_str(rating),
    })

    _log("extract id={} title_ar={} title_en={} poster={} plot_len={}".format(
        data.get("id", ""),
        data.get("title_ar", ""),
        data.get("title_en", ""),
        data.get("poster", ""),
        len(data.get("plot", ""))
    ))
    return data


def build_tmdb_like_json(data, title_override=None):
    title_value = safe_str(title_override) or safe_str(data.get("title_ar")) or safe_str(data.get("title_en"))
    original_value = safe_str(data.get("title_en")) or title_value
    year = safe_str(data.get("year"))
    rating = safe_str(data.get("rating"))
    vote_average = 0.0
    try:
        if rating:
            vote_average = round(float(rating), 1)
    except Exception:
        vote_average = 0.0

    duration_text = safe_str(data.get("duration"))
    runtime = _parse_duration_minutes(duration_text)
    media_type_text = safe_str(data.get("media_type"))
    is_series = ("مسلسل" in media_type_text) or ("series" in media_type_text.lower())

    result = {
        "provider": "elcinema",
        "id": safe_str(data.get("id")),
        "title": title_value,
        "name": title_value,
        "original_title": original_value or title_value,
        "original_name": original_value or title_value,
        "media_type": "tv" if is_series else "movie",
        "Type": "series" if is_series else "movie",
        "overview": safe_str(data.get("plot")),
        "Plot": safe_str(data.get("plot")),
        "PlotOriginal": safe_str(data.get("plot")),
        "vote_average": vote_average,
        "imdbRating": rating,
        "poster_path": safe_str(data.get("poster")),
        "poster": safe_str(data.get("poster")),
        "Genre": safe_str(data.get("genre")),
        "Country": safe_str(data.get("country")),
        "Director": safe_str(data.get("director")),
        "Writer": safe_str(data.get("writer")),
        "Actors": ", ".join(data.get("cast", [])[:10]),
        "Runtime": duration_text,
        "runtime": runtime,
        "duration_text": duration_text,
        "source_url": "https://elcinema.com/work/{}".format(safe_str(data.get("id"))) if safe_str(data.get("id")) else "",
        "elcinema_title_ar": safe_str(data.get("title_ar")),
        "elcinema_title_en": safe_str(data.get("title_en")),
        "genres": [],
        "production_countries": [],
        "spoken_languages": [],
        "credits": {"crew": [], "cast": []},
    }

    if year:
        date_value = "{}-01-01".format(year)
        result["release_date"] = date_value
        result["first_air_date"] = date_value
        result["Year"] = year

    if result["Genre"]:
        result["genres"].append({"id": 0, "name": result["Genre"]})

    if result["Country"]:
        result["production_countries"].append({"iso_3166_1": "", "name": result["Country"]})

    if result["Director"]:
        result["credits"]["crew"].append({"name": result["Director"], "job": "Director", "department": "Directing"})

    if result["Writer"]:
        result["credits"]["crew"].append({"name": result["Writer"], "job": "Writer", "department": "Writing"})

    for cast_name in data.get("cast", [])[:20]:
        result["credits"]["cast"].append({"name": cast_name})

    _log("build json title={} provider=elcinema plot_len={}".format(title_value, len(result.get("overview", ""))))
    return result


def write_elcinema_support_files(base_dir, clean_title, info_json):
    info_dir = os.path.join(base_dir, ELCINEMA_INFO_DIR_NAME)
    star_dir = os.path.join(base_dir, ELCINEMA_STAR_DIR_NAME)
    rated_dir = os.path.join(base_dir, ELCINEMA_RATED_DIR_NAME)

    for folder in (info_dir, star_dir, rated_dir):
        if not os.path.exists(folder):
            os.makedirs(folder)
            _log("created folder={}".format(folder))

    info_path = os.path.join(info_dir, "{}.json".format(clean_title))
    with open(info_path, "w") as handle:
        json.dump(info_json, handle, indent=2, ensure_ascii=False)
    _log("saved info json={}".format(info_path))

    try:
        star_path = os.path.join(star_dir, "{}.json".format(clean_title))
        with open(star_path, "w") as handle:
            json.dump({
                "title": clean_title,
                "provider": "elcinema",
                "star": safe_str(info_json.get("imdbRating", "")),
                "vote_average": info_json.get("vote_average", 0)
            }, handle, indent=2, ensure_ascii=False)
        _log("saved star json={}".format(star_path))
    except Exception as err:
        _log("save star json error={}".format(err))

    try:
        rated_path = os.path.join(rated_dir, "{}.json".format(clean_title))
        with open(rated_path, "w") as handle:
            json.dump({
                "title": clean_title,
                "provider": "elcinema",
                "parental": safe_str(info_json.get("Rated", "")) or safe_str(info_json.get("parental", "")),
                "Rated": safe_str(info_json.get("Rated", ""))
            }, handle, indent=2, ensure_ascii=False)
        _log("saved rated json={}".format(rated_path))
    except Exception as err:
        _log("save rated json error={}".format(err))

    return info_path


def save_elcinema_info_from_html(html_path, infos_base_dir, title_override=None):
    if not html_path or not os.path.exists(html_path):
        _log("html not found={}".format(html_path))
        return ""

    with open(html_path, "r", encoding="utf-8", errors="ignore") as handle:
        html_text = handle.read()

    data = extract_elcinema_data(html_text)
    clean_title = clean_search_title(title_override or data.get("title_ar") or data.get("title_en"))
    if not clean_title:
        clean_title = safe_filename(title_override or data.get("title_ar") or data.get("title_en") or "title")

    info_json = build_tmdb_like_json(data, title_override=clean_title)
    path = write_elcinema_support_files(infos_base_dir, clean_title, info_json)
    _log("save_elcinema_info_from_html title={} path={}".format(clean_title, path))
    return path


def find_elcinema_html_for_title(elcinema_dir, title):
    if not elcinema_dir or not os.path.isdir(elcinema_dir):
        _log("elcinema dir missing={}".format(elcinema_dir))
        return ""

    clean_title = clean_search_title(title)
    safe_title = safe_filename(clean_title)
    candidates = []

    for name in os.listdir(elcinema_dir):
        if not name.lower().endswith(".html"):
            continue
        path = os.path.join(elcinema_dir, name)
        lower = name.lower()
        if safe_title.lower() in lower or clean_title.lower() in lower:
            candidates.append(path)

    candidates.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    selected = candidates[0] if candidates else ""
    _log("find html title={} selected={}".format(title, selected))
    return selected
# -*- coding: utf-8 -*-
# by digiteng...07.2020 - 11.2020 - 11.2021
# FOR INFO
# <widget source="session.Event_Now" render="Label" position="50,545" size="930,400" font="Regular; 32" halign="left" transparent="1" zPosition="2" backgroundColor="background">
#    <convert type="xtraInfo">Title,Year,Description</convert>
# </widget>
#
# FOR IMDB RATING STAR...
# <ePixmap pixmap="xtra/star_b.png" position="990,278" size="200,20" alphatest="blend" zPosition="2" transparent="1" />
# <widget source="ServiceEvent" render="Progress" pixmap="xtra/star.png" position="990,278" size="200,20" alphatest="blend" transparent="1" zPosition="2" backgroundColor="background">
#    <convert type="xtraInfo">imdbRatingValue</convert>
# </widget>

from __future__ import absolute_import
# Standard library imports
import os
import sys
import re
import json
import inspect
import threading

# Internal imports
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.config import config
from Components.Converter.xtraEventGenre import getGenreStringSub
from Plugins.Extensions.xtraEvent.google_translate_api import translate_text
from Plugins.Extensions.xtraEvent.xtraTitleHelper import *
from Plugins.Extensions.xtraEvent.xtraElcinema import *

# ------- Logfile ------
from datetime import datetime
from os import remove
from os.path import isfile

try:
    if sys.version_info[0] >= 3:
        from urllib.parse import quote
    else:
        from urllib import quote
except Exception as e:
    quote = None

try:
    # Py3
    import requests
except ImportError:
    # Py2
    import urllib2

########################### Delete log file ##################################
dir_path = "/tmp/xtraevent"

try:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print("Directory has been created:", dir_path)
    else:
        print("Directory already exists:", dir_path)
except Exception as e:
    print("Error creating directory:", e)

REGEX = re.compile(
    r'([\(\[]).*?([\)\]])|'
    r'(: odc\.\d+)|'
    r'(\d+: odc\.\d+)|'
    r'(\d+ odc\.\d+)|'
    r'!|'
    r'/.*|'
    r'\|\s[0-9]+\+|'
    r'[0-9]+\+|'
    r'([\(\[\|].*?[\)\]\|])|'
    r'(\"|\"\.|\"\,|\.)\s.+|'
    r'\"|'
    r'\*|'
    r'Премьера\.\s|'
    r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
    r'(х|Х|м|М|т|Т|д|Д)/с\s',
    re.DOTALL
)


def safe_str(value):
    try:
        if value is None:
            return ""
        return str(value).strip()
    except:
        return ""


def smart_capitalize_title(title):
    """
    Normalize title case without destroying sequel numbers or dotted decimals.
    Examples:
        THE MATRIX -> The Matrix
        the matrix -> The Matrix
        M3GAN 2.0 -> M3GAN 2.0
        F1 THE MOVIE -> F1 The Movie
    """
    try:
        title = safe_str(title)
        if not title:
            return ""

        small_words = {
            "a", "an", "and", "as", "at", "but", "by", "for", "from",
            "in", "into", "nor", "of", "on", "or", "over", "the", "to", "with"
        }

        words = title.split()
        result = []

        for i, word in enumerate(words):
            original = word

            # Keep pure numbers as they are
            if re.match(r'^\d+([.,]\d+)?$', original):
                result.append(original)
                continue

            # Keep words with digits inside as uppercase-ish originals
            # Examples: M3GAN, F1
            if re.search(r'\d', original):
                result.append(original.upper() if original.isupper() else original)
                continue

            lower_word = original.lower()

            if i > 0 and lower_word in small_words:
                result.append(lower_word)
            else:
                result.append(lower_word[:1].upper() + lower_word[1:])

        return " ".join(result)

    except Exception:
        return safe_str(title)


def clean_search_title(title):
    """
    Shared title cleaner for xtraInfo / xtraParental / xtraStar / xtraLogo.

    Goals:
    - remove EPG junk
    - remove explicit episode/season suffixes
    - normalize separators
    - remove ':' so saved filenames stay consistent
    - normalize title case so duplicates do not happen because of letter case
    """
    try:
        if not title:
            return ""

        original_title = safe_str(title)
        title = original_title

        # Remove service control chars
        title = title.replace('\xc2\x86', '').replace('\xc2\x87', '')

        # Normalize common live prefixes
        title = re.sub(r'^(live:\s*|LIVE:\s*|LIVE\s+|live\s+)', '', title).strip()

        # First run generic cleanup regex
        title = REGEX.sub('', title).strip()

        # Normalize separators early
        title = title.replace(":", " ")
        title = re.sub(r'[_]+', ' _ ', title)
        title = re.sub(r'[-]+', ' - ', title)
        title = re.sub(r'\s{2,}', ' ', title).strip()

        # Arabic season / episode patterns
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

        # English TV episode patterns
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

        # Final normalization
        title = re.sub(r'\s*[_\-:|]+\s*$', '', title).strip()
        title = re.sub(r'\s{2,}', ' ', title).strip()

        # Normalize case so same title from different channels becomes one filename
        title = smart_capitalize_title(title)

        logout(data="clean_search_title original={}".format(original_title))
        logout(data="clean_search_title result={}".format(title))

        return title

    except Exception as e:
        logout(data="clean_search_title error: {}".format(str(e)))
        return smart_capitalize_title(safe_str(title))

def contains_arabic_text(text):
    try:
        text = safe_str(text)
        if not text:
            return False
        return re.search(r'[\u0600-\u06FF]', text) is not None
    except:
        return False


def clean_bidi_marks(text):
    """
    Remove bidi control characters completely.
    """
    try:
        text = safe_str(text)
        if not text:
            return ""

        for ch in [
            u"\u202A", u"\u202B", u"\u202C", u"\u202D", u"\u202E",
            u"\u2066", u"\u2067", u"\u2068", u"\u2069",
            u"\u200E", u"\u200F"
        ]:
            text = text.replace(ch, "")

        return text.strip()
    except:
        return safe_str(text)


def prepare_plot_for_display(text):
    """
    Return clean plain text only.
    No bidi markers, no prefix characters.
    """
    try:
        return clean_bidi_marks(text)
    except:
        return safe_str(text)

def strip_diacritics(text):
    """
    Convert accented characters to plain ASCII-like base characters when possible.
    Example: 'Kohë për të vrarë' -> 'Kohe per te vrare'
    """
    try:
        if not text:
            return ""

        try:
            import unicodedata
            text = unicodedata.normalize("NFKD", text)
            text = "".join([c for c in text if not unicodedata.combining(c)])
        except Exception as e:
            logout(data="strip_diacritics normalize error: {}".format(str(e)))

        return safe_str(text)
    except Exception as e:
        logout(data="strip_diacritics error: {}".format(str(e)))
        return safe_str(text)

def is_rtl_language():
    try:
        return get_plot_translate_lang() in ("ar", "fa", "ur", "he")
    except:
        return False


def contains_arabic_text(text):
    try:
        if not text:
            return False
        return re.search(r'[\u0600-\u06FF]', text) is not None
    except:
        return False


def force_rtl_multiline(text):
    """
    Force correct RTL rendering for multiline Arabic text.
    Wrap each line with RTL embedding marks.
    """
    try:
        text = safe_str(text)
        if not text:
            return ""

        if not (is_rtl_language() or contains_arabic_text(text)):
            return text

        lines = text.splitlines()
        rtl_lines = []
        for line in lines:
            line = safe_str(line)
            if line:
                rtl_lines.append(u"\u202B" + line + u"\u202C")
            else:
                rtl_lines.append("")
        return "\n".join(rtl_lines)
    except Exception as e:
        logout(data="force_rtl_multiline error: {}".format(str(e)))
        return safe_str(text)

def get_omdb_api():
    try:
        if config.plugins.xtraEvent.omdbAPI.value != "":
            return config.plugins.xtraEvent.omdbAPI.value
    except:
        pass
    return "69000e83"


def get_tmdb_api():
    try:
        if config.plugins.xtraEvent.tmdbAPI.value != "":
            return config.plugins.xtraEvent.tmdbAPI.value
    except:
        pass
    return "3c3efcf47c3577558812bb9d64019d65"


def get_info_provider():
    try:
        return config.plugins.xtraEvent.infoProvider.value
    except:
        return "omdb"


def is_tmdb_json(read_json):
    """
    Return True if this json looks like TMDB data.
    """
    try:
        if not isinstance(read_json, dict):
            return False

        # Strong TMDB indicators
        if "overview" in read_json:
            return True
        if "vote_average" in read_json:
            return True
        if "genres" in read_json and isinstance(read_json.get("genres"), list):
            return True
        if "production_countries" in read_json:
            return True
        if "spoken_languages" in read_json:
            return True

        # Search-result style TMDB indicators
        if "media_type" in read_json:
            return True
        if "first_air_date" in read_json:
            return True
        if "original_title" in read_json or "original_name" in read_json:
            return True

        return False
    except Exception as e:
        logout(data="is_tmdb_json error: {}".format(str(e)))
        return False


def is_omdb_json(read_json):
    """
    Return True if this json looks like OMDB data.
    """
    try:
        if not isinstance(read_json, dict):
            return False

        if "Title" in read_json:
            return True
        if "Plot" in read_json:
            return True
        if "imdbRating" in read_json:
            return True
        if "Response" in read_json:
            return True

        return False
    except Exception as e:
        logout(data="is_omdb_json error: {}".format(str(e)))
        return False


def get_json_provider(read_json):
    """
    Detect provider from the json content itself.
    This is better than trusting only config because fallback loading is possible.
    """
    try:
        provider = safe_str(read_json.get("provider", "")).lower() if isinstance(read_json, dict) else ""
        if provider == "elcinema":
            return "elcinema"
        if provider == "omdb":
            return "omdb"
        if provider == "tmdb":
            return "tmdb"
        if is_omdb_json(read_json):
            return "omdb"
        if is_tmdb_json(read_json):
            return "tmdb"
    except Exception as e:
        logout(data="get_json_provider error: {}".format(str(e)))

    return get_info_provider()

def join_non_empty(items, sep=", "):
    try:
        cleaned = [safe_str(x) for x in items if safe_str(x)]
        return sep.join(cleaned)
    except:
        return ""


def get_title_value(read_json):
    """
    OMDB:
      Title
    TMDB:
      title / name / original_title / original_name
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Title", ""))

        return (
            safe_str(read_json.get("title", "")) or
            safe_str(read_json.get("name", "")) or
            safe_str(read_json.get("original_title", "")) or
            safe_str(read_json.get("original_name", "")) or
            safe_str(read_json.get("Title", ""))
        )
    except Exception as e:
        logout(data="get_title_value error: {}".format(str(e)))
        return ""


def get_year_value(read_json):
    """
    OMDB:
      Year
    TMDB:
      release_date / first_air_date
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            year = safe_str(read_json.get("Year", ""))
            return year.replace("-", "").strip()

        date_value = (
            safe_str(read_json.get("release_date", "")) or
            safe_str(read_json.get("first_air_date", "")) or
            safe_str(read_json.get("Year", ""))
        )

        if len(date_value) >= 4:
            return date_value[:4]

        return ""
    except Exception as e:
        logout(data="get_year_value error: {}".format(str(e)))
        return ""


def get_released_value(read_json):
    """
    OMDB:
      Released
    TMDB:
      release_date / first_air_date
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Released", ""))

        return (
            safe_str(read_json.get("release_date", "")) or
            safe_str(read_json.get("first_air_date", "")) or
            safe_str(read_json.get("Released", ""))
        )
    except Exception as e:
        logout(data="get_released_value error: {}".format(str(e)))
        return ""


def get_runtime_value(read_json):
    """
    OMDB:
      Runtime   -> e.g. '90 min'
    TMDB:
      runtime   -> integer minutes
      episode_run_time -> list
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Runtime", ""))

        runtime_tmdb = read_json.get("runtime", 0)
        if runtime_tmdb:
            return "{} min".format(runtime_tmdb)

        episode_runtime = read_json.get("episode_run_time", [])
        if isinstance(episode_runtime, list) and len(episode_runtime) > 0 and episode_runtime[0]:
            return "{} min".format(episode_runtime[0])

        return safe_str(read_json.get("Runtime", ""))
    except Exception as e:
        logout(data="get_runtime_value error: {}".format(str(e)))
        return ""


def get_duration_value(read_json):
    """
    Same as runtime for json-based info.
    """
    try:
        return get_runtime_value(read_json)
    except Exception as e:
        logout(data="get_duration_value error: {}".format(str(e)))
        return ""


def get_genre_value(read_json):
    """
    OMDB:
      Genre -> 'Drama, Comedy'
    TMDB:
      genres -> [{'id':..,'name':'Drama'}, ...]
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Genre", ""))

        genre = safe_str(read_json.get("Genre", ""))
        if genre:
            return genre

        genres_list = read_json.get("genres", [])
        if isinstance(genres_list, list):
            return join_non_empty([g.get("name", "") for g in genres_list if isinstance(g, dict)])

        return ""
    except Exception as e:
        logout(data="get_genre_value error: {}".format(str(e)))
        return ""


def get_genre_first_value(read_json):
    """
    Return the first genre only, useful for Compact.
    """
    try:
        genre_value = get_genre_value(read_json)
        if genre_value:
            return genre_value.split(",")[0].strip()
        return ""
    except Exception as e:
        logout(data="get_genre_first_value error: {}".format(str(e)))
        return ""

def ensure_translated_plot_in_json(read_json, json_path=None):
    try:
        if not read_json:
            logout(data="ensure_translated_plot_in_json: empty json")
            return read_json, ""

        provider = get_json_provider(read_json)

        if provider == "tmdb":
            source_plot = safe_str(read_json.get("overview", "")) or safe_str(read_json.get("Plot", ""))
        else:
            source_plot = safe_str(read_json.get("Plot", ""))

        source_plot = clean_bidi_marks(source_plot)

        if not source_plot:
            logout(data="ensure_translated_plot_in_json: no source plot found")
            return read_json, ""

        if not is_plot_translate_enabled():
            logout(data="ensure_translated_plot_in_json: translation OFF")
            return read_json, prepare_plot_for_display(source_plot)

        target_lang = get_plot_translate_lang()
        stored_lang = safe_str(read_json.get("PlotTranslatedLang", ""))
        stored_plot = clean_bidi_marks(read_json.get("PlotTranslated", ""))

        if stored_plot and stored_lang == target_lang:
            logout(data="ensure_translated_plot_in_json: using cached translated plot for {}".format(target_lang))
            return read_json, prepare_plot_for_display(stored_plot)

        logout(data="ensure_translated_plot_in_json: translating plot to {}".format(target_lang))
        translated_plot = translate_text(source_plot, target_lang=target_lang)
        translated_plot = clean_bidi_marks(translated_plot)

        if translated_plot:
            read_json["PlotOriginal"] = source_plot
            read_json["PlotTranslated"] = translated_plot
            read_json["PlotTranslatedLang"] = target_lang

            if json_path:
                try:
                    with open(json_path, "w") as file:
                        json.dump(read_json, file)
                    logout(data="ensure_translated_plot_in_json: translated plot saved to json")
                except Exception as e:
                    logout(data="ensure_translated_plot_in_json: failed saving json: {}".format(str(e)))

            return read_json, prepare_plot_for_display(translated_plot)

        logout(data="ensure_translated_plot_in_json: translation returned empty")
        return read_json, prepare_plot_for_display(source_plot)

    except Exception as e:
        logout(data="ensure_translated_plot_in_json error: {}".format(str(e)))
        try:
            provider = get_json_provider(read_json)
            if provider == "tmdb":
                fallback = safe_str(read_json.get("overview", "")) or safe_str(read_json.get("Plot", ""))
            else:
                fallback = safe_str(read_json.get("Plot", ""))
            return read_json, prepare_plot_for_display(fallback)
        except:
            return read_json, ""

def get_plot_value(read_json, json_path=None):
    """
    Return plot text for display.
    If translation is ON, ensure translated plot is stored in json and return it.
    """
    try:
        updated_json, plot_value = ensure_translated_plot_in_json(read_json, json_path)
        return plot_value
    except Exception as e:
        logout(data="get_plot_value error: {}".format(str(e)))
        return ""

def get_language_value(read_json):
    """
    OMDB:
      Language -> 'English, Arabic'
    TMDB:
      spoken_languages[*].english_name
      fallback: original_language
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Language", ""))

        language_value = safe_str(read_json.get("Language", ""))
        if language_value:
            return language_value

        spoken = read_json.get("spoken_languages", [])
        if isinstance(spoken, list) and spoken:
            value = join_non_empty([x.get("english_name", "") for x in spoken if isinstance(x, dict)])
            if value:
                return value

        return safe_str(read_json.get("original_language", ""))
    except Exception as e:
        logout(data="get_language_value error: {}".format(str(e)))
        return ""


def get_country_value(read_json):
    """
    OMDB:
      Country -> 'United States'
    TMDB:
      production_countries[*].name
      fallback: origin_country list
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Country", ""))

        country_value = safe_str(read_json.get("Country", ""))
        if country_value:
            return country_value

        prod_countries = read_json.get("production_countries", [])
        if isinstance(prod_countries, list) and prod_countries:
            value = join_non_empty([x.get("name", "") for x in prod_countries if isinstance(x, dict)])
            if value:
                return value

        origin_country = read_json.get("origin_country", [])
        if isinstance(origin_country, list) and origin_country:
            return join_non_empty(origin_country)

        return ""
    except Exception as e:
        logout(data="get_country_value error: {}".format(str(e)))
        return ""


def get_country_compact_value(read_json):
    """
    Compact-friendly country string.
    """
    try:
        country_value = get_country_value(read_json)
        if country_value:
            return country_value.replace("United States", "USA").replace("United Kingdom", "UK")
        return ""
    except Exception as e:
        logout(data="get_country_compact_value error: {}".format(str(e)))
        return ""


def get_rated_value(read_json):
    """
    OMDB:
      Rated
    TMDB:
      no direct equivalent in the base details json
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Rated", ""))

        return safe_str(read_json.get("Rated", ""))
    except Exception as e:
        logout(data="get_rated_value error: {}".format(str(e)))
        return ""


def get_awards_value(read_json):
    """
    OMDB:
      Awards
    TMDB:
      no direct equivalent in the base details json
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Awards", ""))

        return safe_str(read_json.get("Awards", ""))
    except Exception as e:
        logout(data="get_awards_value error: {}".format(str(e)))
        return ""


def get_director_value(read_json):
    """
    OMDB:
      Director
    TMDB:
      not present in the sample/details json unless credits are requested
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Director", ""))

        # Optional support if you later save credits into the TMDB json
        credits = read_json.get("credits", {})
        if isinstance(credits, dict):
            crew = credits.get("crew", [])
            if isinstance(crew, list):
                directors = [p.get("name", "") for p in crew if isinstance(p, dict) and p.get("job", "") == "Director"]
                value = join_non_empty(directors)
                if value:
                    return value

        return safe_str(read_json.get("Director", ""))
    except Exception as e:
        logout(data="get_director_value error: {}".format(str(e)))
        return ""


def get_writer_value(read_json):
    """
    OMDB:
      Writer
    TMDB:
      not present in the sample/details json unless credits are requested
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Writer", ""))

        credits = read_json.get("credits", {})
        if isinstance(credits, dict):
            crew = credits.get("crew", [])
            if isinstance(crew, list):
                writers = []
                for p in crew:
                    if not isinstance(p, dict):
                        continue
                    job = p.get("job", "")
                    department = p.get("department", "")
                    if job in ("Writer", "Screenplay", "Story") or department == "Writing":
                        writers.append(p.get("name", ""))

                value = join_non_empty(list(dict.fromkeys([w for w in writers if w])))
                if value:
                    return value

        return safe_str(read_json.get("Writer", ""))
    except Exception as e:
        logout(data="get_writer_value error: {}".format(str(e)))
        return ""


def get_actors_value(read_json):
    """
    OMDB:
      Actors
    TMDB:
      not present in the sample/details json unless credits are requested
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Actors", ""))

        credits = read_json.get("credits", {})
        if isinstance(credits, dict):
            cast = credits.get("cast", [])
            if isinstance(cast, list) and cast:
                names = [p.get("name", "") for p in cast[:10] if isinstance(p, dict)]
                value = join_non_empty(names)
                if value:
                    return value

        return safe_str(read_json.get("Actors", ""))
    except Exception as e:
        logout(data="get_actors_value error: {}".format(str(e)))
        return ""


def get_imdb_rating_value(read_json):
    """
    OMDB:
      imdbRating
    TMDB:
      vote_average
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("imdbRating", ""))

        imdb_rating = safe_str(read_json.get("imdbRating", ""))
        if imdb_rating:
            return imdb_rating

        vote_average = read_json.get("vote_average", "")
        if vote_average != "" and vote_average is not None:
            try:
                return str(round(float(vote_average), 1))
            except:
                return safe_str(vote_average)

        return ""
    except Exception as e:
        logout(data="get_imdb_rating_value error: {}".format(str(e)))
        return ""


def get_imdb_rating_simple_value(read_json):
    try:
        return get_imdb_rating_value(read_json)
    except Exception as e:
        logout(data="get_imdb_rating_simple_value error: {}".format(str(e)))
        return ""


def get_imdb_votes_value(read_json):
    """
    OMDB:
      imdbVotes
    TMDB:
      vote_count
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("imdbVotes", ""))

        imdb_votes = safe_str(read_json.get("imdbVotes", ""))
        if imdb_votes:
            return imdb_votes

        vote_count = read_json.get("vote_count", "")
        if vote_count != "" and vote_count is not None:
            return safe_str(vote_count)

        return ""
    except Exception as e:
        logout(data="get_imdb_votes_value error: {}".format(str(e)))
        return ""


def get_type_value(read_json):
    """
    OMDB:
      Type
    TMDB:
      infer from content or media_type
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("Type", ""))

        type_value = safe_str(read_json.get("Type", ""))
        if type_value:
            return type_value

        media_type = safe_str(read_json.get("media_type", ""))
        if media_type:
            if media_type == "tv":
                return "series"
            if media_type == "movie":
                return "movie"
            return media_type

        if read_json.get("title", "") or read_json.get("original_title", "") or read_json.get("release_date", ""):
            return "movie"

        if read_json.get("name", "") or read_json.get("original_name", "") or read_json.get("first_air_date", ""):
            return "series"

        return ""
    except Exception as e:
        logout(data="get_type_value error: {}".format(str(e)))
        return ""


def get_total_seasons_value(read_json):
    """
    OMDB:
      totalSeasons
    TMDB:
      number_of_seasons if present in TV details json
    """
    try:
        provider = get_json_provider(read_json)

        if provider == "omdb":
            return safe_str(read_json.get("totalSeasons", ""))

        total_seasons = safe_str(read_json.get("number_of_seasons", ""))
        if total_seasons:
            return total_seasons

        return safe_str(read_json.get("totalSeasons", ""))
    except Exception as e:
        logout(data="get_total_seasons_value error: {}".format(str(e)))
        return ""


def get_imdb_rating_numeric_for_value(read_json):
    """
    Numeric 0..10 rating for Progress/value usage.
    """
    try:
        rating = get_imdb_rating_value(read_json)
        if rating:
            return float(rating)
        return 0.0
    except Exception as e:
        logout(data="get_imdb_rating_numeric_for_value error: {}".format(str(e)))
        return 0.0

def get_tmdb_parental_value(details_json):
    """
    Extract parental rating from TMDB details json with appended release data / content ratings.
    Returns a raw rating string such as 'PG-13', '16', 'TV-MA', etc.
    """
    try:
        # Movie style: release_dates.results[].release_dates[].certification
        release_dates = details_json.get("release_dates", {}).get("results", [])
        if isinstance(release_dates, list):
            preferred_countries = ["DE", "US", "GB"]
            for country in preferred_countries:
                for item in release_dates:
                    if item.get("iso_3166_1") == country:
                        for rel in item.get("release_dates", []):
                            cert = safe_str(rel.get("certification", ""))
                            if cert:
                                return cert
            for item in release_dates:
                for rel in item.get("release_dates", []):
                    cert = safe_str(rel.get("certification", ""))
                    if cert:
                        return cert

        # TV style: content_ratings.results[].rating
        content_ratings = details_json.get("content_ratings", {}).get("results", [])
        if isinstance(content_ratings, list):
            preferred_countries = ["DE", "US", "GB"]
            for country in preferred_countries:
                for item in content_ratings:
                    if item.get("iso_3166_1") == country:
                        rating = safe_str(item.get("rating", ""))
                        if rating:
                            return rating
            for item in content_ratings:
                rating = safe_str(item.get("rating", ""))
                if rating:
                    return rating

        return ""
    except Exception as e:
        logout(data="get_tmdb_parental_value error: {}".format(str(e)))
        return ""

def get_tmdb_star_value(details_json):
    """
    Return rating value for star widget from TMDB details json.
    Uses vote_average.
    """
    try:
        vote_average = details_json.get("vote_average", "")
        if vote_average != "" and vote_average is not None:
            return str(round(float(vote_average), 1))
    except Exception as e:
        logout(data="get_tmdb_star_value error: {}".format(str(e)))
        return ""


def get_compact_parts(read_json):
    """
    Build reusable compact pieces from either provider.
    """
    try:
        parts = []

        genre_first = get_genre_first_value(read_json)
        if genre_first:
            parts.append(genre_first)

        country_value = get_country_compact_value(read_json)
        if country_value:
            parts.append(country_value)

        rating_value = get_imdb_rating_value(read_json)
        if rating_value:
            parts.append("IMDB:{}".format(rating_value))

        rated_value = get_rated_value(read_json)
        if rated_value and rated_value != "Not Rated":
            parts.append("{}+".format(rated_value))

        type_value = get_type_value(read_json)
        if type_value:
            # Keep available for future use if you want to show it in Compact
            pass

        year_value = get_year_value(read_json)
        if year_value:
            parts.append(year_value)

        return parts
    except Exception as e:
        logout(data="get_compact_parts error: {}".format(str(e)))
        return []

def is_plot_translate_enabled():
    try:
        return config.plugins.xtraEvent.translatePlot.value
    except:
        return False


def get_plot_translate_lang():
    try:
        return config.plugins.xtraEvent.translatePlotLang.value
    except:
        return "ar"


def get_plot_for_display(read_json, rating_jsonomdb=None):
    """
    Return the plot that should be displayed.

    Behavior:
    - If translation is OFF: return original Plot.
    - If translation is ON and a translated plot already exists for the selected language:
      return the translated plot.
    - If translation is ON and the translated plot is missing or for another language:
      translate the existing Plot now, save it back into the OMDB json if possible,
      and return the translated plot.
    - Fallback: return the original Plot.
    """

    try:
        if not read_json:
            logout(data="get_plot_for_display: read_json is empty")
            return ""
    except Exception as e:
        logout(data="get_plot_for_display: invalid read_json: {}".format(str(e)))
        return ""

    try:
        original_plot = read_json.get("Plot", "")
    except Exception as e:
        logout(data="get_plot_for_display: failed reading original Plot: {}".format(str(e)))
        original_plot = ""

    if not original_plot:
        logout(data="get_plot_for_display: original Plot is empty")
        return ""

    try:
        translate_enabled = is_plot_translate_enabled()
    except Exception as e:
        logout(data="get_plot_for_display: failed reading translate flag: {}".format(str(e)))
        translate_enabled = False

    if not translate_enabled:
        logout(data="get_plot_for_display: translation is OFF, using original Plot")
        return original_plot

    try:
        target_lang = get_plot_translate_lang()
    except Exception as e:
        logout(data="get_plot_for_display: failed reading target language: {}".format(str(e)))
        target_lang = "ar"

    try:
        stored_translated_plot = read_json.get("PlotTranslated", "")
    except Exception as e:
        logout(data="get_plot_for_display: failed reading PlotTranslated: {}".format(str(e)))
        stored_translated_plot = ""

    try:
        stored_translated_lang = read_json.get("PlotTranslatedLang", "")
    except Exception as e:
        logout(data="get_plot_for_display: failed reading PlotTranslatedLang: {}".format(str(e)))
        stored_translated_lang = ""

    # Reuse cached translation if it matches the selected language
    if stored_translated_plot and stored_translated_lang == target_lang:
        logout(data="get_plot_for_display: using cached translated plot for lang={}".format(target_lang))
        return stored_translated_plot

    # Translate existing plot now
    try:
        logout(data="get_plot_for_display: translating existing plot to lang={}".format(target_lang))
        translated_plot = translate_text(original_plot, target_lang=target_lang)

        if translated_plot:
            read_json["PlotOriginal"] = original_plot
            read_json["PlotTranslated"] = translated_plot
            read_json["PlotTranslatedLang"] = target_lang

            # Update existing OMDB json file if available
            if rating_jsonomdb:
                try:
                    json_dir = os.path.dirname(rating_jsonomdb)
                    if json_dir and not os.path.exists(json_dir):
                        os.makedirs(json_dir)

                    with open(rating_jsonomdb, "w") as file:
                        json.dump(read_json, file)

                    logout(data="get_plot_for_display: translated plot saved into existing json")
                except Exception as e:
                    logout(data="get_plot_for_display: failed writing translated plot to json: {}".format(str(e)))

            return translated_plot

        logout(data="get_plot_for_display: translation returned empty, using original Plot")
        return original_plot

    except Exception as e:
        logout(data="get_plot_for_display: translation error: {}".format(str(e)))
        return original_plot


myfile=dir_path + "/info.log"
# # If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
# ############################# Copy file ############################################
# For py2, the int and str statements were removed, and the degree symbol was added.

# ##########################  Create log file ##################################
# kitte888 create logfile the entry in logstatus

logstatus = "on"
if config.plugins.xtraEvent.logFiles.value == True:
    logstatus = "on"
else:
    logstatus = "off"

logstatus = "on"
# ________________________________________________________________________________

def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----- This is what the command must look like to write to the file.  -----
logout(data="start")

try:
    pathLoc = config.plugins.xtraEvent.loc.value
    logout(data="start pathloc")
    logout(data=str(pathLoc))
except:
    pass


def load_preferred_info_json_for_title(evntNm):
    try:
        prefer_tmdb = get_info_provider() == "tmdb"
    except:
        prefer_tmdb = True
    candidates = get_info_json_candidates(pathLoc, evntNm, prefer_tmdb=prefer_tmdb)
    logout(data="info json candidates={}".format(candidates))
    return load_first_json(candidates)

def get_selected_info_provider_for_title(evntNm):
    try:
        prefer_tmdb = get_info_provider() == "tmdb"
    except:
        prefer_tmdb = True
    provider = get_selected_provider_for_title(evntNm, prefer_tmdb=prefer_tmdb)
    logout(data="selected provider for title {} => {}".format(evntNm, provider))
    return provider


class xtraInfo(Converter, object):
    logout(data="----- class xrtraInfo -----")
    Title = "Title"
    Year = "Year"
    Rated = "Rated"
    Released = "Released"
    Runtime = "Runtime"
    Genre = "Genre"
    Director = "Director"
    Writer = "Writer"
    Actors = "Actors"
    Plot = "Description"
    Language = "Language"
    Country = "Country"
    Awards = "Awards"
    imdbRating = "imdbRating"
    imdbRatingValue = "imdbRatingValue"
    imdbRatingSimple = "imdbRatingSimple"
    imdbVotes = "imdbVotes"
    Type = "Type"
    totalSeasons = "totalSeasons"
    SE = "SE"
    Duration = "Duration"
    Compact = "Compact"
    Shortdesc = "Shortdesc"
    Longdesc = "Longdesc"

    lastevnt = "none"
    logout(data=str(lastevnt))

    def __init__(self, type):
        logout(data="----- def init -----")
        Converter.__init__(self, type)
        self.types = str(type).split(",")
        # lastevnt = ""


    def getText(self):
        logout(data="159 ---------------------------------------------------------------------------------------------------------- start def getText")

        event = self.source.event
        logout(data=str(event))
        logout(data="event object")

        if not event:
            logout(data="no event name")
            return ""

        logout(data="event found")

        if not self.types:
            logout(data="no types configured")
            return ""

        evnt = event.getEventName()
        logout(data="raw event name")
        logout(data=str(evnt))

        logout(data="last event name")
        logout(data=str(self.lastevnt))

        if self.lastevnt == evnt:
            logout(data="same event requested again")

        self.lastevnt = evnt
        evntNm = clean_search_title(evnt)
        logout(data="clean event name")
        logout(data=str(evntNm))

        rating_json = "{}xtraEvent/infos/{}.json".format(pathLoc, evntNm)
        rating_jsonomdb = "{}xtraEvent/infosomdb/{}.json".format(pathLoc, evntNm)
        jsonomdb = "{}xtraEvent/infosomdb".format(pathLoc)
        xtrapath = "{}xtraEvent/".format(pathLoc)

        logout(data="json paths")
        logout(data=str(rating_json))
        logout(data=str(rating_jsonomdb))
        logout(data=str(jsonomdb))

        if not os.path.exists(jsonomdb):
            logout(data="creating infosomdb directory")
            os.makedirs("{}infosomdb".format(xtrapath))

        ############################################################ download omdb json ############################################################
        def download_json(rating_jsonomdb, api, evntNm):
            if os.path.exists(rating_jsonomdb):
                logout(data="OMDB json already exists")
                return

            logout(data="OMDB json does not exist yet")

            clean_title = clean_search_title(evntNm)
            if not clean_title:
                logout(data="OMDB info download: clean title is empty")
                return

            title_variants = [clean_title]

            try:
                translated_en = translate_text(clean_title, target_lang="en")
                translated_en = clean_bidi_marks(safe_str(translated_en))
                if translated_en and translated_en.lower() != clean_title.lower():
                    title_variants.append(translated_en)
                    logout(data="OMDB english fallback title={}".format(translated_en))
            except Exception as e:
                logout(data="OMDB english title translate error: {}".format(str(e)))

            title_variants = list(dict.fromkeys([t for t in title_variants if t]))

            for title in title_variants:
                url = "https://www.omdbapi.com/?apikey=%s&t=%s" % (get_omdb_api(), title.lower())
                logout(data="Trying OMDB title variant: %s" % title)
                logout(data="OMDB URL: %s" % url)

                try:
                    if sys.version_info[0] >= 3:
                        response = requests.get(url)
                        read_json = response.json()
                    else:
                        response = urllib2.urlopen(url)
                        read_json = json.load(response)

                    if read_json.get("Response") == "True":
                        original_plot = clean_bidi_marks(safe_str(read_json.get("Plot", "")))
                        read_json["PlotOriginal"] = original_plot

                        try:
                            if is_plot_translate_enabled() and original_plot:
                                target_lang = get_plot_translate_lang()
                                translated_plot = translate_text(original_plot, target_lang=target_lang)
                                translated_plot = clean_bidi_marks(translated_plot)

                                if translated_plot:
                                    read_json["PlotTranslated"] = translated_plot
                                    read_json["PlotTranslatedLang"] = target_lang
                                else:
                                    read_json["PlotTranslated"] = ""
                                    read_json["PlotTranslatedLang"] = ""
                            else:
                                read_json["PlotTranslated"] = ""
                                read_json["PlotTranslatedLang"] = ""
                        except Exception as e:
                            read_json["PlotTranslated"] = ""
                            read_json["PlotTranslatedLang"] = ""
                            logout(data="translation error during OMDB download: {}".format(str(e)))

                        with open(rating_jsonomdb, "w") as file:
                            json.dump(read_json, file)
                        return
                    else:
                        logout(data="OMDB returned no info for title: %s" % title)

                except Exception as e:
                    logout(data="OMDB download error: %s" % str(e))

            logout(data="All OMDB title variants failed")
        ###########################################################################################################################################

        ############################################################ download tmdb json ############################################################
        def download_tmdb_json(rating_json, evntNm):
            if os.path.exists(rating_json):
                logout(data="TMDB info json already exists")
                return

            logout(data="TMDB info json does not exist yet")

            if quote is None:
                logout(data="TMDB info download error: quote import failed")
                return

            try:
                configured_search_type = config.plugins.xtraEvent.searchType.value
            except:
                configured_search_type = "multi"

            search_types = [configured_search_type]
            if configured_search_type != "multi":
                search_types.append("multi")

            search_types = list(dict.fromkeys(search_types))

            clean_title = clean_search_title(evntNm)
            if not clean_title:
                logout(data="TMDB info download: clean title is empty")
                return

            title_variants = [clean_title]

            # Only one fallback: translate cleaned title to English
            translated_en = ""
            try:
                translated_en = translate_text(clean_title, target_lang="en")
                translated_en = safe_str(translated_en)
                if translated_en and translated_en.lower() != clean_title.lower():
                    title_variants.append(translated_en)
                    logout(data="TMDB english fallback title={}".format(translated_en))
            except Exception as e:
                logout(data="TMDB english title translate error: {}".format(str(e)))

            title_variants = list(dict.fromkeys([t for t in title_variants if t]))
            logout(data="TMDB search title variants={}".format(str(title_variants)))
            logout(data="TMDB search types={}".format(str(search_types)))

            lang = "en"
            try:
                if config.plugins.xtraEvent.searchLang.value:
                    from Components.Language import language
                    lang = language.getLanguage()[:2]
            except:
                try:
                    if config.plugins.xtraEvent.searchLang.value:
                        lang = config.osd.language.value[:-3]
                except:
                    lang = "en"

            for title in title_variants:
                for srch in search_types:
                    try:
                        url = "https://api.themoviedb.org/3/search/{}?api_key={}&query={}".format(
                            srch, get_tmdb_api(), quote(title)
                        )

                        try:
                            if config.plugins.xtraEvent.searchLang.value:
                                url += "&language={}".format(lang)
                        except:
                            pass

                        logout(data="TMDB search type={} title={}".format(srch, title))
                        logout(data="TMDB search url: {}".format(url))

                        search_json = requests.get(url).json()

                        try:
                            results_count = len(search_json.get("results", []))
                        except:
                            results_count = 0

                        logout(data="TMDB search response page={} results={}".format(
                            search_json.get("page", 0), results_count
                        ))

                        results = search_json.get("results", [])
                        if not results:
                            logout(data="TMDB search returned no results for title: {}".format(title))
                            continue

                        first_result = results[0]
                        tmdb_id = first_result.get("id")
                        media_type = first_result.get("media_type", srch)

                        # Search endpoint 'movie' or 'tv' may not include media_type
                        if srch in ("movie", "tv"):
                            media_type = srch

                        # If multi result has unknown media_type, infer it
                        if media_type not in ("movie", "tv"):
                            if first_result.get("title", "") or first_result.get("release_date", ""):
                                media_type = "movie"
                            else:
                                media_type = "tv"

                        logout(data="TMDB first result title={} name={} media_type={} id={}".format(
                            first_result.get("title", ""),
                            first_result.get("name", ""),
                            media_type,
                            tmdb_id
                        ))

                        if not tmdb_id:
                            logout(data="TMDB result missing id")
                            continue

                        details_url = "https://api.themoviedb.org/3/{}/{}?api_key={}&append_to_response=credits,release_dates,content_ratings".format(
                            media_type, tmdb_id, get_tmdb_api()
                        )

                        try:
                            if config.plugins.xtraEvent.searchLang.value:
                                details_url += "&language={}".format(lang)
                        except:
                            pass

                        logout(data="TMDB details url: {}".format(details_url))
                        details_json = requests.get(details_url).json()

                        if details_json.get("id"):
                            tmdb_rated_path = "{}xtraEvent/infostmdbrated/{}.json".format(pathLoc, evntNm)
                            tmdb_star_path = "{}xtraEvent/infostmdbstar/{}.json".format(pathLoc, evntNm)

                            try:
                                tmdb_parental = get_tmdb_parental_value(details_json)
                                with open(tmdb_rated_path, "w") as file:
                                    json.dump({
                                        "title": evntNm,
                                        "provider": "tmdb",
                                        "parental": tmdb_parental
                                    }, file)
                                logout(data="TMDB parental json saved")
                            except Exception as e:
                                logout(data="TMDB parental json save error: {}".format(str(e)))

                            try:
                                tmdb_star = get_tmdb_star_value(details_json)
                                with open(tmdb_star_path, "w") as file:
                                    json.dump({
                                        "title": evntNm,
                                        "provider": "tmdb",
                                        "star": tmdb_star
                                    }, file)
                                logout(data="TMDB star json saved")
                            except Exception as e:
                                logout(data="TMDB star json save error: {}".format(str(e)))

                            try:
                                source_plot = safe_str(details_json.get("overview", "")) or safe_str(details_json.get("Plot", ""))
                                details_json["PlotOriginal"] = source_plot

                                if is_plot_translate_enabled() and source_plot:
                                    target_lang = get_plot_translate_lang()
                                    translated_plot = translate_text(source_plot, target_lang=target_lang)

                                    if translated_plot:
                                        translated_plot = force_rtl_multiline(translated_plot)
                                        details_json["PlotTranslated"] = translated_plot
                                        details_json["PlotTranslatedLang"] = target_lang
                                        logout(data="translated plot saved during TMDB download")
                                    else:
                                        details_json["PlotTranslated"] = ""
                                        details_json["PlotTranslatedLang"] = ""
                                else:
                                    details_json["PlotTranslated"] = ""
                                    details_json["PlotTranslatedLang"] = ""
                            except Exception as e:
                                details_json["PlotTranslated"] = ""
                                details_json["PlotTranslatedLang"] = ""
                                logout(data="TMDB translation error during download: {}".format(str(e)))

                            with open(rating_json, "w") as file:
                                json.dump(details_json, file)

                            logout(data="TMDB info json saved")
                            return

                        logout(data="TMDB details json missing id")

                    except Exception as e:
                        logout(data="TMDB info download error: {}".format(str(e)))

            logout(data="All TMDB title variants failed")
        ###########################################################################################################################################

        provider = get_selected_info_provider_for_title(evntNm)

        try:
            if provider == "elcinema":
                target_json_path = get_provider_target_json_path(pathLoc, evntNm, "elcinema", "info")
            elif provider == "tmdb":
                target_json_path = get_provider_target_json_path(pathLoc, evntNm, "tmdb", "info")
            else:
                target_json_path = get_provider_target_json_path(pathLoc, evntNm, "omdb", "info")
        except Exception as e:
            logout(data="target json path error: {}".format(str(e)))
            target_json_path = ""

        if contains_arabic_text(evntNm):
            logout(data="Arabic title detected, elcinema has first read/download priority")
            try:
                if provider == "elcinema" and (not target_json_path or not os.path.exists(target_json_path)) and save_elcinema_info_from_html and find_elcinema_html_for_title:
                    elcinema_dir = os.path.join(dir_path, "elcinema")
                    html_path = find_elcinema_html_for_title(elcinema_dir, evntNm)
                    logout(data="elcinema html candidate={}".format(html_path))
                    if html_path:
                        created_json = save_elcinema_info_from_html(html_path, xtrapath, title_override=evntNm)
                        logout(data="elcinema json created={}".format(created_json))
                        target_json_path = created_json or target_json_path
            except Exception as e:
                logout(data="elcinema json create error: {}".format(str(e)))

        logout(data="selected info provider: {}".format(provider))
        logout(data="selected info target json: {}".format(target_json_path))

        need_download = False
        if target_json_path and os.path.exists(target_json_path):
            logout(data="selected provider json already exists")
        else:
            if provider == "elcinema":
                logout(data="selected provider is elcinema and no json was created from html")
            else:
                need_download = True

        if need_download:
            logout(data="json missing for selected provider, starting download thread")
            if provider == "tmdb":
                thread = threading.Thread(target=download_tmdb_json, args=(target_json_path, evntNm))
            else:
                thread = threading.Thread(target=download_json, args=(target_json_path, get_omdb_api(), evntNm))
            thread.start()
        else:
            logout(data="json already exists or provider is elcinema without remote fallback, skip starting download thread")

        fd = "{}\n{}\n{}".format(event.getEventName(), event.getShortDescription(), event.getExtendedDescription())

        evnt = []
        try:
            logout(data="getText main try")

            read_json, current_json_path = load_preferred_info_json_for_title(evntNm)
            provider = get_json_provider(read_json) if read_json else get_info_provider()
            if current_json_path:
                logout(data="selected info json={}".format(current_json_path))
            else:
                logout(data="no preferred info json found")

            for type in self.types:
                logout(data="requested type")
                logout(data=str(type))
                type = type.strip()

                # -----------------------------------------------------------------------------------------------------------------------
                if type == self.Title:
                    logout(data="Title")
                    try:
                        title = get_title_value(read_json)
                        if title:
                            evnt.append("Title : {}".format(title))
                        else:
                            evnt.append("Title - {}".format(event.getEventName()))
                    except Exception as e:
                        logout(data="Title error: {}".format(str(e)))
                        evnt.append("Title - {}".format(event.getEventName()))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Year:
                    logout(data="Year")
                    try:
                        year = get_year_value(read_json)
                        if year:
                            evnt.append("Year : {}".format(year))
                        else:
                            year = ''
                            fd_year = fd.replace(',', '').replace('(', '').replace(')', '')
                            fdl = [r'\d{4} [A-Z]+', r'[A-Z]+ \d{4}', r'[A-Z][a-z]+\s\d{4}', r'\+\d+\s\d{4}']
                            for i in fdl:
                                year = re.findall(i, fd_year)
                                if year:
                                    year = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year[0]).strip()
                                    evnt.append("Year : {}".format(year))
                                    break
                    except Exception as e:
                        logout(data="Year error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Rated:
                    logout(data="Rated")
                    try:
                        rated_value = get_rated_value(read_json)
                        if rated_value and rated_value != "Not Rated":
                            evnt.append("Rated : {}+".format(rated_value))
                        elif rated_value == "Not Rated":
                            parentName = ''
                            prs = [r'[aA]b ((\d+))', r'[+]((\d+))', r'Od lat: ((\d+))', r'(\d+)[+]', r'(TP)', r'[-](\d+)']
                            for i in prs:
                                prr = re.search(i, fd)
                                if prr:
                                    parentName = prr.group(1)
                                    parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                    evnt.append("Rated : {}+".format(parentName))
                                    break
                        else:
                            try:
                                age = ''
                                rating = event.getParentalData()
                                if rating:
                                    age = rating.getRating()
                                    evnt.append("Rated - {}+".format(age))
                            except:
                                pass
                    except Exception as e:
                        logout(data="Rated error: {}".format(str(e)))
                        parentName = ''
                        prs = [r'[aA]b ((\d+))', r'[+]((\d+))', r'Od lat: ((\d+))', r'(\d+)[+]', r'(TP)', r'[-](\d+)']
                        for i in prs:
                            prr = re.search(i, fd)
                            if prr:
                                parentName = prr.group(1)
                                parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                evnt.append("Rated : {}+".format(parentName))
                                break

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Released:
                    logout(data="Released")
                    try:
                        released = get_released_value(read_json)
                        if released:
                            evnt.append("Released : {}".format(released))
                    except Exception as e:
                        logout(data="Released error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Runtime:
                    logout(data="Runtime")
                    try:
                        runtime = get_runtime_value(read_json)
                        if runtime:
                            evnt.append("Runtime : {}".format(runtime))
                    except Exception as e:
                        logout(data="Runtime error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Genre:
                    logout(data="Genre")
                    try:
                        genre = get_genre_value(read_json)
                        if genre:
                            evnt.append("Genre : {}".format(genre))
                        else:
                            genres = event.getGenreDataList()
                            if genres:
                                genre = genres[0]
                                evnt.append("Genre - {}".format(getGenreStringSub(genre[0], genre[1])))
                    except Exception as e:
                        logout(data="Genre error: {}".format(str(e)))
                        try:
                            genres = event.getGenreDataList()
                            if genres:
                                genre = genres[0]
                                evnt.append("Genre - {}".format(getGenreStringSub(genre[0], genre[1])))
                        except:
                            pass

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Director:
                    logout(data="Director")
                    try:
                        director_value = get_director_value(read_json)
                        if director_value:
                            evnt.append("Director : {}".format(director_value))
                    except Exception as e:
                        logout(data="Director error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Writer:
                    logout(data="Writer")
                    try:
                        writer_value = get_writer_value(read_json)
                        if writer_value:
                            evnt.append("Writer : {}".format(writer_value))
                    except Exception as e:
                        logout(data="Writer error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Actors:
                    logout(data="Actors")
                    try:
                        actors_value = get_actors_value(read_json)
                        if actors_value:
                            evnt.append("Actors : {}".format(actors_value))
                    except Exception as e:
                        logout(data="Actors error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Plot:
                    logout(data="Plot")
                    try:
                        plot_to_show = get_plot_value(read_json, current_json_path)

                        if plot_to_show:
                            evnt.append(plot_to_show)
                        else:
                            short_desc = event.getShortDescription() or ""
                            long_desc = event.getExtendedDescription() or ""
                            fallback_plot = "\n".join([x for x in [short_desc, long_desc] if x])
                            evnt.append(fallback_plot if fallback_plot else event.getEventName())

                    except Exception as e:
                        logout(data="Plot show error: {}".format(str(e)))
                        short_desc = event.getShortDescription() or ""
                        long_desc = event.getExtendedDescription() or ""
                        fallback_plot = "\n".join([x for x in [short_desc, long_desc] if x])
                        evnt.append(fallback_plot if fallback_plot else event.getEventName())

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Language:
                    logout(data="Language")
                    try:
                        language_value = get_language_value(read_json)
                        if language_value:
                            evnt.append("Language : {}".format(language_value))
                    except Exception as e:
                        logout(data="Language error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Country:
                    logout(data="Country")
                    try:
                        country_value = get_country_value(read_json)
                        if country_value:
                            evnt.append("Country : {}".format(country_value))
                    except Exception as e:
                        logout(data="Country error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Awards:
                    logout(data="Awards")
                    try:
                        awards_value = get_awards_value(read_json)
                        if awards_value:
                            evnt.append("Awards : {}".format(awards_value))
                    except Exception as e:
                        logout(data="Awards error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.imdbRating:
                    logout(data="imdbRating")
                    try:
                        imdb_rating = get_imdb_rating_value(read_json)
                        if imdb_rating:
                            evnt.append("IMDB : {}".format(imdb_rating))
                    except Exception as e:
                        logout(data="imdbRating error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.imdbRatingSimple:
                    logout(data="imdbRatingSimple")
                    try:
                        imdb_rating_simple = get_imdb_rating_simple_value(read_json)
                        if imdb_rating_simple:
                            evnt.append("{}".format(imdb_rating_simple))
                    except Exception as e:
                        logout(data="imdbRatingSimple error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.imdbVotes:
                    logout(data="imdbVotes")
                    try:
                        imdb_votes = get_imdb_votes_value(read_json)
                        if imdb_votes:
                            evnt.append("imdbVotes : {}".format(imdb_votes))
                    except Exception as e:
                        logout(data="imdbVotes error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Type:
                    logout(data="Type")
                    try:
                        type_value = get_type_value(read_json)
                        if type_value:
                            evnt.append("Type : {}".format(type_value))
                    except Exception as e:
                        logout(data="Type error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.totalSeasons:
                    logout(data="totalSeasons")
                    try:
                        total_seasons = get_total_seasons_value(read_json)
                        if total_seasons:
                            evnt.append("TotalSeasons : {}".format(total_seasons))
                    except Exception as e:
                        logout(data="totalSeasons error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Duration:
                    logout(data="Duration")
                    try:
                        runtime_value = get_duration_value(read_json)
                        if runtime_value:
                            evnt.append("Duration : {}".format(runtime_value))
                        else:
                            raise ValueError("Empty Runtime")
                    except Exception as e:
                        logout(data="Duration primary error: {}".format(str(e)))
                        try:
                            drtn = round(event.getDuration() // 60)
                            if drtn > 0:
                                evnt.append("Duration - {}min".format(drtn))
                            else:
                                prs = re.findall(r' \d+ Min', fd)
                                if prs:
                                    minutes = re.findall(r'\d+', prs[0])
                                    if minutes:
                                        evnt.append("Duration : {}min".format(minutes[0]))
                        except Exception as e2:
                            logout(data="Failed to resolve Duration: {}".format(str(e2)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Shortdesc:
                    logout(data="Shortdesc")

                    try:
                        genre_value = get_genre_value(read_json)
                    except Exception as e:
                        logout(data="Shortdesc genre error: {}".format(str(e)))
                        genre_value = ""

                    try:
                        plot_to_show = get_plot_value(read_json, current_json_path)
                    except Exception as e:
                        logout(data="Shortdesc plot error: {}".format(str(e)))
                        plot_to_show = ""

                    if genre_value:
                        evnt.append("Genre : {}".format(genre_value))

                    if plot_to_show:
                        evnt.append("{}".format(plot_to_show))
                    else:
                        short_desc = event.getShortDescription() or ""
                        long_desc = event.getExtendedDescription() or ""
                        fallback_plot = "\n".join([x for x in [short_desc, long_desc] if x])
                        evnt.append(fallback_plot if fallback_plot else event.getEventName())

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Longdesc:
                    logout(data="Longdesc")

                    try:
                        genre_value = get_genre_value(read_json)
                    except Exception as e:
                        logout(data="Longdesc genre error: {}".format(str(e)))
                        genre_value = ""

                    try:
                        plot_to_show = get_plot_value(read_json, current_json_path)
                    except Exception as e:
                        logout(data="Longdesc plot error: {}".format(str(e)))
                        plot_to_show = ""

                    try:
                        writer_value = get_writer_value(read_json)
                    except Exception as e:
                        logout(data="Longdesc writer error: {}".format(str(e)))
                        writer_value = ""

                    try:
                        director_value = get_director_value(read_json)
                    except Exception as e:
                        logout(data="Longdesc director error: {}".format(str(e)))
                        director_value = ""

                    if genre_value:
                        evnt.append("Genre : {}".format(genre_value))

                    if plot_to_show:
                        evnt.append("{}".format(plot_to_show))
                    else:
                        short_desc = event.getShortDescription() or ""
                        long_desc = event.getExtendedDescription() or ""
                        fallback_plot = "\n".join([x for x in [short_desc, long_desc] if x])
                        evnt.append(fallback_plot if fallback_plot else event.getEventName())

                    if writer_value:
                        evnt.append("Writer : {}".format(writer_value))

                    if director_value:
                        evnt.append("Director : {}".format(director_value))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.SE:
                    logout(data="SE")
                    try:
                        prs = [r'(\d+). Staffel, Folge (\d+)', r'T(\d+) Ep.(\d+)', r'"Episodio (\d+)" T(\d+)']
                        for i in prs:
                            seg = re.search(i, fd)
                            if seg:
                                s = seg.group(1).zfill(2)
                                e = seg.group(2).zfill(2)
                                evnt.append("SE : S{}E{}".format(s, e))
                                break
                    except Exception as e:
                        logout(data="SE error: {}".format(str(e)))

                # -----------------------------------------------------------------------------------------------------------------------
                elif type == self.Compact:
                    logout(data="Compact")

                    try:
                        compact_parts = get_compact_parts(read_json)
                        for part in compact_parts:
                            evnt.append(part)
                    except Exception as e:
                        logout(data="Compact helper error: {}".format(str(e)))

                    try:
                        rated_value = get_rated_value(read_json)
                        if rated_value and rated_value != "Not Rated":
                            rated_formatted = "{}+".format(rated_value)
                            if rated_formatted not in evnt:
                                evnt.append(rated_formatted)
                        elif rated_value == "Not Rated":
                            parentName = ''
                            prs = [r'[aA]b ((\d+))', r'[+]((\d+))', r'Od lat: ((\d+))', r'(\d+)[+]', r'(TP)', r'[-](\d+)']
                            for i in prs:
                                prr = re.search(i, fd)
                                if prr:
                                    parentName = prr.group(1)
                                    parentName = parentName.replace('7', '6').replace('10', '12').replace('TP', '0')
                                    rated_formatted = "{}+".format(parentName)
                                    if rated_formatted not in evnt:
                                        evnt.append(rated_formatted)
                                    break
                        else:
                            try:
                                age = ''
                                rating = event.getParentalData()
                                if rating:
                                    age = rating.getRating()
                                    rated_formatted = "{}+".format(age)
                                    if rated_formatted not in evnt:
                                        evnt.append(rated_formatted)
                            except:
                                pass
                    except Exception as e:
                        logout(data="Compact rated error: {}".format(str(e)))

                    try:
                        prs = [r'(\d+). Staffel, Folge (\d+)', r'T(\d+) Ep.(\d+)', r'"Episodio (\d+)" T(\d+)']
                        for i in prs:
                            seg = re.search(i, fd)
                            if seg:
                                s = seg.group(1).zfill(2)
                                e = seg.group(2).zfill(2)
                                evnt.append("S{}E{}".format(s, e))
                                break
                    except Exception as e:
                        logout(data="Compact SE error: {}".format(str(e)))

                    try:
                        year_value = get_year_value(read_json)
                        if not year_value:
                            year_tmp = ''
                            fd_year = fd.replace(',', '').replace('(', '').replace(')', '')
                            fdl = [r'\d{4} [A-Z]+', r'[A-Z]+ \d{4}', r'[A-Z][a-z]+\s\d{4}', r'\+\d+\s\d{4}']
                            for i in fdl:
                                year_tmp = re.findall(i, fd_year)
                                if year_tmp:
                                    year_tmp = re.sub(r'\(.*?\)|\.|\+\d+', ' ', year_tmp[0]).strip()
                                    year_value = year_tmp
                                    break

                        if year_value and year_value not in evnt:
                            evnt.append("{}".format(year_value))
                    except Exception as e:
                        logout(data="Compact year error: {}".format(str(e)))

                if type != self.Compact:
                    tc = "\n".join(evnt)
                else:
                    current_provider = get_json_provider(read_json) if read_json else ""
                    if current_provider == "elcinema" or contains_arabic_text(evntNm):
                        tc = " • ".join([clean_bidi_marks(safe_str(x)) for x in evnt if safe_str(x)])
                    else:
                        tc = '\\c0000??00 • '
                        tc += '\\c00??????'
                        tc = tc.join(evnt)

            return tc

        except Exception as e:
            logout(data="getText main error: {}".format(str(e)))
            return ""
        else:
            logout(data="no event name")
            return ""

    text = property(getText)

    def getValue(self):
        logout(data="getValue")
        event = self.source.event
        if not event:
            return 0

        if not self.types:
            return 0

        try:
            evnt = event.getEventName()
            evntNm = clean_search_title(evnt)

            read_json, current_json_path = load_preferred_info_json_for_title(evntNm)

            for type in self.types:
                type = type.strip()
                if type == self.imdbRatingValue:
                    rating_value = get_imdb_rating_numeric_for_value(read_json)
                    return int(10 * float(rating_value)) if rating_value else 0

        except Exception as e:
            logout(data="getValue error: {}".format(str(e)))

        return 0

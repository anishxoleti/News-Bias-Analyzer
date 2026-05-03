# Analyzes text for distortion signals using rule-based logic
# This runs independently of the AI - pure Python analysis

LOADED_WORDS = [
    "radical", "extreme", "destroy", "crisis", "disaster", "catastrophe",
    "corrupt", "evil", "threat", "dangerous", "alarming", "shocking",
    "outrage", "chaos", "collapse", "attack", "slam", "blast", "crush",
    "explode", "surge", "expose", "betray", "lie", "fraud", "hoax"
]

HEDGE_WORDS = [
    "allegedly", "reportedly", "claims", "suggests", "according to",
    "some say", "many believe", "critics argue", "supporters claim"
]


def count_loaded_language(text):
    text_lower = text.lower()
    found = [w for w in LOADED_WORDS if w in text_lower]
    return found


def count_hedge_words(text):
    text_lower = text.lower()
    found = [w for w in HEDGE_WORDS if w in text_lower]
    return found


def check_exclamations(text):
    return text.count("!")


def check_caps_ratio(text):
    # High ratio of capitalized words can signal sensationalism
    words = text.split()
    if not words:
        return 0.0
    caps_words = [w for w in words if w.isupper() and len(w) > 2]
    return round(len(caps_words) / len(words), 2)


def analyze_distortion(text):
    loaded = count_loaded_language(text)
    hedges = count_hedge_words(text)
    exclamations = check_exclamations(text)
    caps_ratio = check_caps_ratio(text)

    # Simple scoring: each signal adds to distortion score
    distortion_score = 0
    distortion_score += len(loaded) * 2
    distortion_score += exclamations * 1
    distortion_score += caps_ratio * 10

    # Hedge words reduce distortion slightly (shows awareness of uncertainty)
    distortion_score -= len(hedges) * 0.5
    distortion_score = max(0, round(distortion_score, 1))

    return {
        "distortion_score": distortion_score,
        "loaded_words_found": loaded,
        "hedge_words_found": hedges,
        "exclamation_count": exclamations,
        "caps_ratio": caps_ratio,
        "flag": distortion_score >= 5
    }
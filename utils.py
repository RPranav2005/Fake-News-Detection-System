"""
utils.py
========
Helper utilities for the Fake News Detection platform:
  - URL article extraction
  - Sentiment analysis
  - Bias detection
  - Credibility scoring
  - Clickbait detection
  - Explanation generation
"""

import re
import requests
from bs4 import BeautifulSoup


# ── URL Article Extraction ───────────────────────────────────────────────────

def extract_article_from_url(url: str) -> dict:
    """
    Fetch and extract the main article content from a news URL.
    Returns a dict with keys: 'title', 'text', 'full_text', 'success', 'error'.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Extract title
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find("h1"):
            title = soup.find("h1").get_text()

        # Extract paragraphs from article body
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs if len(p.get_text()) > 40)

        if len(text) < 100:
            text = soup.get_text(separator=" ")

        text  = re.sub(r"\s+", " ", text).strip()
        title = re.sub(r"\s+", " ", title).strip()

        return {"title": title, "text": text, "full_text": f"{title} {text}", "success": True, "error": ""}
    except requests.exceptions.Timeout:
        return {"title": "", "text": "", "full_text": "", "success": False, "error": "Request timed out."}
    except requests.exceptions.ConnectionError:
        return {"title": "", "text": "", "full_text": "", "success": False, "error": "Could not connect to URL."}
    except Exception as e:
        return {"title": "", "text": "", "full_text": "", "success": False, "error": str(e)}


# ── Sentiment Analysis ────────────────────────────────────────────────────────

POSITIVE_WORDS = {
    "great","good","excellent","wonderful","amazing","fantastic","outstanding",
    "positive","success","benefit","improve","growth","hope","best","achieve",
    "progress","celebrate","support","help","trust","peace","love","joy",
    "happy","glad","win","victory","strong","healthy","safe","freedom",
    "truth","honest","fair","justice","care","proud","bright","kind",
}

NEGATIVE_WORDS = {
    "bad","terrible","awful","horrible","disaster","crisis","fail","corrupt",
    "cheat","lie","fraud","danger","attack","threat","hate","fear","war",
    "death","kill","violence","crime","scandal","illegal","evil","worst",
    "false","fake","manipulate","deceive","destroy","collapse","blame",
    "terror","panic","chaos","shock","outrage","broke","toxic","harm",
}

def analyze_sentiment(text: str) -> dict:
    """
    Rule-based sentiment analysis.
    Returns: {'label': str, 'score': float, 'positive_count': int, 'negative_count': int}
    """
    words = re.findall(r"\b[a-z]+\b", text.lower())
    pos_count = sum(1 for w in words if w in POSITIVE_WORDS)
    neg_count = sum(1 for w in words if w in NEGATIVE_WORDS)
    total     = max(pos_count + neg_count, 1)

    score = (pos_count - neg_count) / total  # range -1 to 1
    if score > 0.1:
        label = "Positive"
    elif score < -0.1:
        label = "Negative"
    else:
        label = "Neutral"

    normalised = round((score + 1) / 2, 3)  # 0–1

    return {
        "label": label,
        "score": normalised,
        "positive_count": pos_count,
        "negative_count": neg_count,
    }


# ── Bias Detection ────────────────────────────────────────────────────────────

EMOTIONAL_WORDS = {
    "shocking","outrageous","unbelievable","devastating","explosive","bombshell",
    "alarming","horrifying","disgusting","appalling","scandalous","terrifying",
    "heartbreaking","infuriating","stunning","incredible","jaw-dropping",
    "mind-blowing","absolutely","completely","totally","utterly","definitely",
    "certainly","obviously","clearly","everyone","nobody","always","never",
    "must","should","will","huge","massive","enormous","crisis",
}

FACTUAL_INDICATORS = {
    "according","report","study","research","data","statistics","evidence",
    "source","document","official","government","agency","university","science",
    "percent","million","billion","survey","analysis","findings","published",
    "journal","expert","professor","stated","confirmed","announced","revealed",
}

def detect_bias(text: str) -> dict:
    """
    Detect emotional vs factual bias in text.
    Returns: {'label': str, 'score': float, 'emotional_words': int, 'factual_indicators': int}
    """
    words = re.findall(r"\b[a-z\-]+\b", text.lower())
    emotional_count = sum(1 for w in words if w in EMOTIONAL_WORDS)
    factual_count   = sum(1 for w in words if w in FACTUAL_INDICATORS)
    total = max(emotional_count + factual_count, 1)
    bias_ratio = emotional_count / total

    if bias_ratio > 0.6:
        label = "Highly Emotional / Biased"
    elif bias_ratio > 0.35:
        label = "Moderately Biased"
    else:
        label = "Mostly Factual"

    return {
        "label": label,
        "score": round(bias_ratio, 3),
        "emotional_words": emotional_count,
        "factual_indicators": factual_count,
    }


# ── Credibility Score ─────────────────────────────────────────────────────────

def compute_credibility_score(
    confidence: float,
    sentiment_score: float,
    bias_score: float,
    is_real: bool,
) -> dict:
    """
    Compute a composite credibility score (0–100).
    Weights: model confidence 50%, low bias 30%, sentiment neutrality 20%.
    """
    low_bias_score    = 1.0 - bias_score
    sentiment_neutral = 1.0 - abs(sentiment_score - 0.5) * 2

    raw = (
        0.50 * confidence +
        0.30 * low_bias_score +
        0.20 * sentiment_neutral
    )

    if not is_real:
        raw = raw * (1 - confidence * 0.6)

    score = int(round(raw * 100))
    score = max(0, min(100, score))

    if score >= 70:
        level = "High Credibility"
    elif score >= 40:
        level = "Moderate Credibility"
    else:
        level = "Low Credibility"

    return {"score": score, "level": level}


# ── Clickbait Detection ───────────────────────────────────────────────────────

CLICKBAIT_PHRASES = [
    r"\byou won'?t believe\b", r"\bshocking\b", r"\bblown away\b",
    r"\bmust see\b", r"\bthis is why\b", r"\bwhat happens next\b",
    r"\bnumber \d+\b", r"\bsecret\b", r"\bthey don'?t want you to know\b",
    r"\bbreaking\b", r"\burgent\b", r"\bexclusive\b", r"\bwarning\b",
    r"\bjust in\b", r"\bwow\b", r"\bomg\b", r"\bcrazy\b",
]

def detect_clickbait(title: str) -> dict:
    """
    Detect clickbait patterns in article headlines.
    Returns: {'is_clickbait': bool, 'score': float, 'reasons': list}
    """
    if not title:
        return {"is_clickbait": False, "score": 0.0, "reasons": []}

    reasons = []
    t = title.strip()
    words = t.split()

    upper_words = [w for w in words if w.isupper() and len(w) > 2]
    if len(upper_words) >= 2:
        reasons.append("Multiple ALL-CAPS words")

    if t.count("!") >= 2:
        reasons.append("Excessive exclamation marks")
    if t.count("?") >= 2:
        reasons.append("Multiple question marks")

    for pattern in CLICKBAIT_PHRASES:
        if re.search(pattern, t, re.IGNORECASE):
            match_word = re.search(pattern, t, re.IGNORECASE).group(0)
            reasons.append(f'Clickbait phrase: "{match_word}"')

    score = min(len(reasons) / 4.0, 1.0)
    is_clickbait = score >= 0.25

    return {"is_clickbait": is_clickbait, "score": round(score, 2), "reasons": reasons}


# ── Explanation Generator ─────────────────────────────────────────────────────

def generate_explanation(
    label: str,
    confidence: float,
    sentiment: dict,
    bias: dict,
    clickbait: dict,
) -> str:
    """Generate a human-readable explanation for the prediction."""
    conf_pct = round(confidence * 100, 1)
    parts = []

    if label == "FAKE":
        parts.append(f"This article is likely **FAKE** (model confidence: {conf_pct}%).")
        if bias["score"] > 0.4:
            parts.append(
                f"It contains highly emotional and sensational language, "
                f"with {bias['emotional_words']} emotional words detected."
            )
        if clickbait["is_clickbait"]:
            parts.append(
                "The headline exhibits clickbait characteristics: "
                + "; ".join(clickbait["reasons"]) + "."
            )
        if sentiment["label"].startswith("Negative"):
            parts.append("The overall tone is predominantly negative, which is common in misinformation.")
        if bias["factual_indicators"] < 3:
            parts.append("There is a noticeable absence of factual citations or authoritative sources.")
        if len(parts) == 1:
            parts.append("The text patterns resemble those frequently found in fabricated news articles.")
    else:
        parts.append(f"This article appears to be **REAL** (model confidence: {conf_pct}%).")
        if bias["factual_indicators"] >= 3:
            parts.append(
                f"It references factual language and credible indicators "
                f"({bias['factual_indicators']} factual markers found)."
            )
        if bias["score"] < 0.35:
            parts.append("The language is measured and avoids excessive emotional rhetoric.")
        if not clickbait["is_clickbait"]:
            parts.append("The headline does not exhibit clickbait patterns.")
        if len(parts) == 1:
            parts.append("The writing style and language patterns are consistent with legitimate news reporting.")

    return " ".join(parts)


# ── Word frequency for word cloud ─────────────────────────────────────────────

def get_top_words(text: str, n: int = 20) -> dict:
    """Return the top-n most frequent non-stopword words in text."""
    from collections import Counter
    import nltk
    from nltk.corpus import stopwords
    nltk.download("stopwords", quiet=True)
    stop = set(stopwords.words("english"))
    words = re.findall(r"\b[a-z]{3,}\b", text.lower())
    words = [w for w in words if w not in stop]
    counter = Counter(words)
    return dict(counter.most_common(n))

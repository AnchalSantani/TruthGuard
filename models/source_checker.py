from models.trusted_sources import TRUSTED_SOURCES


def analyze_source(text):
    """
    Analyze the news text to identify trusted sources.
    Returns a dictionary containing source details.
    """

    text_lower = text.lower()

    for source_name, info in TRUSTED_SOURCES.items():

        for keyword in info["keywords"]:

            if keyword.lower() in text_lower:

                return {
                    "name": source_name,
                    "category": info["category"],
                    "credibility": info["credibility"],
                    "score": info["score"],
                    "reason": info["reason"]
                }

    return {
        "name": "Unknown Source",
        "category": "Unknown",
        "credibility": "Unknown",
        "score": 20,
        "reason": "No trusted source was detected in the provided text."
    }
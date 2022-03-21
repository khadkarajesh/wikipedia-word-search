import string

import requests

from .notifier import email_notifier

BASE_URL = "https://en.wikipedia.org/api/rest_v1"
THRESHOLD = 20.0


def clean(summary: str) -> list[str]:
    tokens = summary.split()
    table = str.maketrans('', '', string.punctuation)
    words = [w.translate(table) for w in tokens]
    words = [word for word in words if word.isalpha()]
    words = [word.lower() for word in words]
    return list(set(words))


def compute_score(words) -> float:
    if len(words) == 0: return 0.0
    vocabulary_length = len(words)
    filtered_words = [word for word in words if len(word) > 5]
    percentage = (len(filtered_words) / vocabulary_length) * 100
    return percentage


def get_summary(title: str):
    response = requests.get(url=f'{BASE_URL}/page/summary/{title}')
    data = response.json()
    if response.status_code != requests.codes.ok: return {
        'status': data.get('title'),
        'code': response.status_code,
    }
    summary = data.get('extract')
    if len(summary) > 0:
        words = clean(summary)
        score = compute_score(words)
        if score > THRESHOLD:
            email_notifier.notify()
    return {'summary': summary}

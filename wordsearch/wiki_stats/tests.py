import requests_mock

from . import services

summary_more_words = "Stack Overflow is a question and answer website for professional and enthusiast programmers. It is the flagship site of the Stack Exchange Network, created in 2008 by Jeff Atwood and Joel Spolsky. It features questions and answers on a wide range of topics in computer programming. It was created to be a more open alternative to earlier question and answer websites such as Experts-Exchange. Stack Overflow was sold to Prosus, a Netherlands-based consumer internet conglomerate, on 2 June 2021 for $1.8 billion."
summary_less_words = "This is test. It is used for less than threshold test case. It doesn't send email. it has less words which has length more than 5"


def test_clean_should_return_words_without_punctuation_and_number():
    words = services.clean(summary_more_words)
    assert '.' not in words
    assert not any([0, 1, 2, 3, 4, 5]) in words
    assert not any(['.', '&']) in words


def test_compute_score_should_return_more_than_threshold_percentage():
    words = services.clean(summary_more_words)
    score = services.compute_score(words)
    assert score > services.THRESHOLD


def test_compute_score_return_less_than_threshold_percentage():
    words = services.clean(summary_less_words)
    score = services.compute_score(words)
    assert score < services.THRESHOLD


def test_get_summary_should_return_summary():
    with requests_mock.Mocker() as m:
        title = "stackoverflow"
        m.get(f'{services.BASE_URL}/page/summary/{title}', json={"extract": summary_more_words})
        response = services.get_summary(title)
        assert response.get('summary') == summary_more_words


def test_get_summary_should_return_empty_summary():
    with requests_mock.Mocker() as m:
        title = "fsfsfsdff"
        m.get(f'{services.BASE_URL}/page/summary/{title}', json={"extract": ''})
        response = services.get_summary(title)
        assert len(response.get('summary')) == 0


def test_get_summary_should_return_not_found():
    with requests_mock.Mocker() as m:
        title = "fsfsfsdfffsfsfsdfsfs"
        m.get(f'{services.BASE_URL}/page/summary/{title}', json={'title': 'not_found', 'code': 404, 'extract': ''},
              status_code=404)
        response = services.get_summary(title)
        assert response.get('code') == 404
        assert response.get('status') == 'not_found'

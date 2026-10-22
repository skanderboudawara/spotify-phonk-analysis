import requests


def get_def(subject):
    """
    returns the definition of the topic in Wikipedia

    :param subject: (str) The name of the topic to search
    :return: (str) The definition of the topic in  Wikipedia
    """
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": subject,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }

    # Wikipedia rejects requests without a descriptive User-Agent
    headers = {"User-Agent": "spotify-phonk-analysis/1.0 (https://github.com/skanderboudawara/spotify-phonk-analysis)"}

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    page = next(iter(data["query"]["pages"].values()))
    return page["extract"]

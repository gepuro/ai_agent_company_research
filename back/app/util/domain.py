from urllib.parse import urlparse


def get_domain_from_url(url):
    if url is None:
        return None
    parsed_url = urlparse(url)
    return parsed_url.netloc

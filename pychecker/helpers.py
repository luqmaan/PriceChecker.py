class URLError(Exception):

    def __init__(self, url):
        self.value = "Invalid URL: " + url

    def __str__(self):
        return repr(self.value)


def domain_for(url):
    import re
    domain = re.findall("[www.{0,1}\.]*[a-z.0-9]+\.com", url)
    if len(domain) < 1:
        raise URLError(domain)
    return domain[0]

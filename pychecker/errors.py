class URLError(Exception):

    def __init__(self, url):
        self.value = "Invalid URL: " + url

    def __str__(self):
        return repr(self.value)

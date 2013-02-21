import sys
# I needed this, sorry :(
sys.path.insert(0, "/Library/Python/2.7/site-packages")

from pyquery import PyQuery as pq
from urlparse import urlparse

# [site: url: { attribute keys: values (dom xpaths) }
search_list = {"urbanoutfitters.com": {"/catalog/productdetail.jsp": {
    "price": ["span[itemprop=price]", "span[itemprop=sale]"]
}}}


def getProductInfo(html, url):
    d = pq(html)
    # urlparse("http://fqdn") -> scheme, netloc, path, params, query, fragment
    # urlparse(url) ?
    site = "urbanoutfitters.com"
    path = "/catalog/productdetail.jsp"
    for name, l in search_list[site][path].items():
        print name
        for xpath in l:
            print xpath
            print d(xpath).text()

# http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS
fname = "uo-koto.html"
f = open(fname, 'r')
h = f.read()
f.close()

getProductInfo(h, "http://urbanoutfitters.com/catalog/productdetail.jsp")

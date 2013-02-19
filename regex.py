from BeautifulSoup import BeautifulSoup

regexes = {
    "uo": {
        "price": ""
    }
}


def getProductInfo(html, store):
    soup = BeautifulSoup(html)
    return soup.h2


# http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS
fname = "uo-koto.html"
f = open(fname, 'r')
html = ""
for line in f:
    html += str(line)

print getProductInfo(html, "uo")

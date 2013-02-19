from bs4 import BeautifulSoup

regexes = {
    "uo": {
        "price": "",
        "sku": ""
    }
}


def getProductInfo(html, store):
    soup = BeautifulSoup(html)
    for h in soup.find_all(itemprop=True):
        print h.text


# http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS
fname = "uo-koto.html"
f = open(fname, 'r')
html = ""
for line in f:
    html += str(line)

getProductInfo(html, "uo")

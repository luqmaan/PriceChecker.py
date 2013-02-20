from bs4 import BeautifulSoup
import ast

recipes = {
    "uo": {
        "all": "itemprop",  # Breaks, <anything itemProp="anything">
        "price": "('span', {'itemprop': 'price'})",  # <span itemprop="price">
        "sku": "('p', {'itemprop': 'productID'})",
    }
}

regexes = {}


def getProductInfo(html, store):
    soup = BeautifulSoup(html)

    price_param = ast.literal_eval(recipes[store]["price"])
    print soup.find(price_param[0], price_param[1]).text

    price_param = ast.literal_eval(recipes[store]["sku"])
    print soup.find(price_param[0], price_param[1]).text

    print "\nAll Product Properties\n"
    for tag in soup.find_all():
        if 'itemprop' in tag.attrs:
            print tag

# http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id=26872101&parentid=M_NEWARRIVALS
fname = "uo-koto.html"
f = open(fname, 'r')
html = ""
for line in f:
    html += str(line)

getProductInfo(html, "uo")

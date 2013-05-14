import hashlib
import re
from helpers import URLError
from selenium import webdriver
from clint.textui import colored

# This file should not interact with the database or the flask app
# Instead it provides methods for getting the data from phantom.
# The goal is to have this file running at the same time as the server,
# so that we don't have to restart Phantom every time we get a new request.
# After the first request (~10 seconds), most requests take ~5s or less.

print colored.red("STARTING PHANTOM")
phantom = webdriver.PhantomJS()
phantom.set_window_size(1024, 768)


def product_info(url, selector):

    print colored.yellow("CALLED PRODUCT INFO")

    if not valid_url(url):
        raise URLError(url)

    img_hash = hashlib.md5(url).hexdigest()
    screenshot_path = 'static/screens/' + img_hash + '.png'
    phantom.get(url)
    if not phantom.save_screenshot('pychecker/' + screenshot_path):
        raise IOError("Unable to save screenshot to: " + 'pychecker/' + screenshot_path)

    # find the price in the string, in case there's info like 'On Sale: $2.32'
    # if there is more than one price, go with the last one
    el = phantom.find_element_by_css_selector(selector)

    # IDEA: What if we passed mutliuple selectors that were all tried until a price was find
    #       What if multiple prices are found? Is there a way to determine the best price other than the last price?

    element_text = re.findall("\$[0-9]+.{0,1}[0-9]{0,2}", el.text)[-1]
    element_text = element_text.replace('$', '').replace(',', '')
    return element_text, screenshot_path


def valid_url(url):
    domain = re.findall("[www.{0,1}\.]*[a-z.0-9]+\.com", url)
    return len(domain) > 0


def tests():
    print "Macy's #1"
    import time
    started = time.time()
    print product_info(
        "http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker" +
        "-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=" +
        "37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)",
        "DIV.standardProdPricingGroup > SPAN")
    stopped = time.time()
    print started - stopped
    print "Urban Outfitters #1"
    started = time.time()
    print product_info(
        "http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id" +
        "=26872101&parentid=M_NEWARRIVALS",
        "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    stopped = time.time()
    print "Macy's #2"
    print started - stopped
    started = time.time()
    print product_info(
        "http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker" +
        "-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=" +
        "37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)",
        "DIV.standardProdPricingGroup > SPAN")
    stopped = time.time()
    print started - stopped
    print "Urban Outfitters #2"
    started = time.time()
    print product_info(
        "http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id" +
        "=26872101&parentid=M_NEWARRIVALS",
        "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    stopped = time.time()
    print started - stopped


def main():
    tests()

if __name__ == '__main__':
    main()

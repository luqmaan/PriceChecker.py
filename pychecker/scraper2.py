import hashlib
import re
from URLError import URLError
from selenium import webdriver


phantom = webdriver.PhantomJS()
phantom.set_window_size(1024, 768)


def get_price(url, selector):

    if not valid_url(url):
        raise URLError(url)

    img_hash = hashlib.md5("url").hexdigest()
    screenshot_path = '../static/screens/' + img_hash + '.png'
    phantom.get(url)
    phantom.save_screenshot(screenshot_path)

    # find the price in the string, in case there's info like 'On Sale: $2.32'
    # if there is more than one price, go with the last one
    el = phantom.find_element_by_css_selector(selector)
    element_text = re.findall("\$[0-9]+.{0,1}[0-9]{0,2}", el.text)[-1]
    element_text = element_text.replace('$', '').replace(',', '')
    return element_text, screenshot_path


def valid_url(url):
    return True


def tests():
    print "Macy's #1"
    import time
    started = time.time()
    print get_site(
        "http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker" +
        "-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=" +
        "37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)",
        "DIV.standardProdPricingGroup > SPAN")
    stopped = time.time()
    print started - stopped
    print "Urban Outfitters #1"
    started = time.time()
    print get_site(
        "http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id" +
        "=26872101&parentid=M_NEWARRIVALS",
        "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    stopped = time.time()
    print "Macy's #2"
    print started - stopped
    started = time.time()
    print get_site(
        "http://www1.macys.com/shop/product/cuisinart-chw-12-coffee-maker" +
        "-12-cup-programmable-with-hot-water-system?ID=466900&CategoryID=" +
        "37460#fn=sp%3D1%26spc%3D189%26ruleId%3D18%26slotId%3Drec(3)",
        "DIV.standardProdPricingGroup > SPAN")
    stopped = time.time()
    print started - stopped
    print "Urban Outfitters #2"
    started = time.time()
    print get_site(
        "http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id" +
        "=26872101&parentid=M_NEWARRIVALS",
        "DIV#content > DIV#productDetail > DIV#prodOptions > H2.price > SPAN")
    stopped = time.time()
    print started - stopped


def main():
    tests()

if __name__ == '__main__':
    main()

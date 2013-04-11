'A HTML scraper using Ghost.Py'

import sys
sys.path.insert(0, "../")

from pychecker import app
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import abort
from urlparse import urlparse
import re
from pychecker.notify import notify

from pychecker import app
from pychecker.database import db_session, Base
from pychecker.models import *
from clint.textui import colored



rate_limits = {"global": {"daily": 100, "hourly": 10},
               "domain": {"daily": 10, "hourly": 10},
               "site": {"daily": 1, "hourly": 1}}


def getRateLimit(type, when):
    return rate_limits[type][when]


def valid_product(url):
    'placeholder for a function that tests if a product is valid'

    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(url_regex, url):
        return False

    # check for regexes matching url...if not, site is not supported currently
    url = getHostPart(url)

    r = db_session.query(RegEx).filter(RegEx.siteurl.like('%'+url['host']+'%'))
    if r.count() > 0:
        return True

    return False


def getHostPart(url):
    # urlparse("http://fqdn") -> scheme, netloc, path, params, query, fragment
    url = urlparse(url)
    # split(':') XXX
    return {"protocol": url[0], "host": url[1], "path": url[2], "params": url[3], "query": url[4], "fragment": url[5]}


def update(url):
    u = getHostPart(url)

    p = db_session.query(Product).filter(Product.url == url).first()
    r = db_session.query(RegEx).filter(RegEx.siteurl.like('%'+u['host']+'%')).all()

    if app.debug is False:

        limits = {"global": {"daily": 0, "hourly": 0},
                  "domain": {"daily": 0, "hourly": 0},
                  "site": {"daily": 0, "hourly": 0}}
        for row in r:
            limits["domain"]["daily"] = limits["domain"]["daily"] + row.history.filter(ScrapeHistory.created >= 60*60*24).count()
            limits["domain"]["hourly"] = limits["domain"]["hourly"] + row.history.filter(ScrapeHistory.created >= 60*24).count()

        if p is not None:
            limits["site"]["daily"] = db_session.query(ScrapeHistory).filter(
                ScrapeHistory.product_id == p.id and ScrapeHistory.created >= 60*60*24).count()
            limits["site"]["hourly"] = db_session.query(ScrapeHistory).filter(
                ScrapeHistory.product_id == p.id and ScrapeHistory.created >= 60*60).count()
        else:
            limits["site"]["daily"] = 0
            limits["site"]["hourly"] = 0

        limits["global"]["daily"] = db_session.query(ScrapeHistory).filter(ScrapeHistory.created >= 60*60*24).count()
        limits["global"]["hourly"] = db_session.query(ScrapeHistory).filter(ScrapeHistory.created >= 60*60).count()

        if limits["domain"]["daily"] >= getRateLimit("domain", "daily"):
            raise Exception("Daily rate limit for domain reached")
        if limits["domain"]["hourly"] >= getRateLimit("domain", "hourly"):
            raise Exception("Hourly rate limit for domain reached")
        if limits["site"]["daily"] >= getRateLimit("site", "daily"):
            raise Exception("Daily rate limit for url reached")
        if limits["site"]["hourly"] >= getRateLimit("site", "hourly"):
            raise Exception("Hourly rate limit for url reached")
        if limits["global"]["daily"] >= getRateLimit("global", "daily"):
            raise Exception("Daily global rate limit reached")
        if limits["global"]["hourly"] >= getRateLimit("global", "hourly"):
            raise Exception("Hourly global rate limit reached")

    import hashlib

    print colored.cyan("Starting up ghost, prepare to wait for eons")
    g = Ghost(wait_timeout=60)
    print colored.cyan("Ghost started")
    page, extra = g.open(url)
    print colored.cyan("Ghost opened page")

    img = hashlib.md5()
    img.update(url)
    img = os.getcwd() + "/pychecker/static/img/" + img.hexdigest() + ".png"
    g.capture_to(img)

    print colored.cyan("Ghost captured image")

    price = ""

    for row in r:
        result, res = g.evaluate("document.querySelector('" + row.regex + "').innerText")
        if result is None:
            continue

        price = unicode(result, errors='ignore').replace('$', '').replace(',', '')
        # XXX find best match and save it

        if p is not None:
            s = ScrapeHistory(p.id, row.id, "Success", price)
        else:
            s = ScrapeHistory(0, row.id, "Success", price)
        db_session.add(s)


    db_session.commit()
    return (price, "/static/img/" + os.path.basename(img))

# main worker


@app.route('/scraper/process/')
def process():

    # basic authentication
    # if request.remote_addr != "127.0.0.1":
    #     abort(401)

    # attempt to acquire tmpfile "lock"
    # changed to use actual os /tmp directory
    # lockfile = os.getcwd() + "/tmp/.scraper_process.lock"

    # try:
    #     with open(lockfile):
    #         return "Scraper already running " + str(e)
    # except (IOError, Exception) as e:
    #     pass

    # f = open(lockfile, "w+")
    # f.close()

    changed = 0
    same = 0
    todo = []

    p = db_session.query(Product).filter().order_by("url").all()
    for product in p:
        print colored.yellow("Checking if product " + str(product.url) + " needs to be updated")

        try:
            price, img = update(product.url)
            print colored.blue("Product " + str(product.url) + " has been checked")
            if price != product.currentPrice:
                changed += 1
                for user in product.users:
                    print colored.green("Found a change and scheduled notification")
                    todo.append((user, product, price))
            else:
                same += 1
                print colored.green("The product price has not changed")

            product.currentPrice = price
            product.image = img
            db_session.add(product)
        except Exception as e:
            print colored.red("OMG, something went wrong: " + str(e))
            s = ScrapeHistory(product.id, -1, "Failed", str(e))
            db_session.add(s)

        db_session.commit()

    print colored.green("==========================")
    print colored.green("==========================")
    print colored.green("Done checking all products")
    print colored.green("Changed: %d Same: %d" % (changed, same))
    print colored.green("==========================")
    print colored.green("==========================")

    for t in todo:
        print colored.green("About to notify: " + str(t))
        notify(t[0], t[1], t[2])

    # release tmpfile lock
    # os.remove(lockfile)

    message = "Done checking all products\n"
    message += "Changed: %d Same: %d" % (changed, same)
    return render_template("debug.html", message=message)

if __name__ == "__main__":
    process()

import os
from ghost import Ghost

# ... profit!

'icmp'

from pychecker import app
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import abort

# rate limit settings
rate_limits = {"global": {"day":100,"hour":10}, "site":{"day":10,"hour":10}}
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22",
           "Accept":"text/html", "Accept-Language":"en-US,en;q=0.8", "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3"}

def getRateLimit(type, when):
        return rate_limits[type][when]

def valid_product(url):
	'placeholder for a function that tests if a product is valid'

	# check for regexes matching url...if not, site is not supported currently
	url=getHostPart(url)

        r = db_session.query(RegEx).filter(RegEx.siteurl.like('%'+url['host']+'%'))
	if r.count() > 0: return True

	return False 

# work in progress to receive data from chrome-extension...deprecated?
@app.route('/regex/add', methods=['POST', 'GET'])
def regex_add():
        from flask import json
        import base64

        # get user session to attach this to their account also XXX
        # only store ss, html data with user session since it could contain private info
        user_id = current_user.is_authenticated() and current_user.id or 1 # XXX fail


        if request.method == 'POST' and request.form.get('data') <> None:
                d=json.loads(base64.b64decode(request.form.get("data")))

                if request.args.get('confirm', "false") == "true":
                        pass
                else:
                        return render_template("regex_add_confirm.html", data=d)

                return ""
                r = RegEx(request.form['url'], request.form['xpath'],
                                "xpath", request.form['meta'],
                                request.form['title'], request.form['text'],
                                request.form['name'])

                db_session.add(r)
                db_session.commit()
                # catch errors?

                # redirect XXX
                return "Thanks for the submission!"

        elif request.method == 'GET':
                return "no data received"



import sys
sys.path.insert(0, "../")

from pyquery import PyQuery as pq
from urlparse import urlparse
import httplib

from pychecker.database import db_session, Base
from pychecker.models import *

def getHostPart(url):
        # urlparse("http://fqdn") -> scheme, netloc, path, params, query, fragment
        url = urlparse(url)
        # split(':') XXX
        return {"protocol":url[0], "host":url[1], "path":url[2], "params":url[3], "query":url[4], "fragment":url[5]}

# product model, regexes, buffer
def update_product(product, regex, buf):
	
	# sometimes PyQuery will fail to load the DOM ... XXX

        try:
                d = pq(str(buf))
        except Exception as e:
                s = ScrapeHistory(product.id, -1, "Failed", "PyQuery: " + str(e))
                db_session.add(s)
                return False

        success = {}
        for row in regex:
                try:
                        price = d(str(row.regex)).text()
                        if price != row.regex:
                                s = ScrapeHistory(product.id, row.id, "Success", price)
                                success[row] = price
                        else: raise Exception("RegEx failed")
                except Exception as e:
                        s = ScrapeHistory(product.id, row.id, "Failed", str(e))
                db_session.add(s)

        for regex, price in enumerate(success):
                if len(price) <= 0: continue

                price = float(price.replace('$', '').replace(',',''))
                if notifyPrice > price:
                        # NOTIFY
                        pass
                product.price = price
                db_session.add(product)

		# need a way to best associate a product with the best matching regex/xpath
		# maybe with product.regex_id ?

                break # use first non-empty match ... we can probably do better

# main worker 
@app.route('/cron/process')
def process():

	# basic authentication 
	if request.remote_addr != "127.0.0.1": 
		abort(401)

	url_cache = {}

	# set big lock to prevent concurrent/overlapping runs? XXX

	p = db_session.query(Product).filter(Product.id == 12).order_by("url").all()
	for product in p:

	        url=getHostPart(product.url)
        	r = db_session.query(RegEx).filter(RegEx.siteurl.like('%'+url['host']+'%')).all()

        	# we already downloaded this url before, use cache and update
	        if product.url in url_cache:
        	        update_product(product, r, url_cache[product.url])
			db_session.commit()
                	continue

	        # check ratelimits
        	site_daily = 0
	        site_hourly = 0
        	for row in r:
	                # add history from ScrapeHistory regex_id relation
        	        site_daily = site_daily + row.history.filter(ScrapeHistory.created >= 60*60*24).count()
                	site_hourly = site_hourly + row.history.filter(ScrapeHistory.created >= 60*60).count()

	        if site_daily >= getRateLimit("global", "day") or site_daily >= getRateLimit("site", "day"): continue
        	elif site_hourly >= getRateLimit("global", "hour") or site_hourly >= getRateLimit("site", "hour"): continue

		# may need to farm this out to full linux-based servers for headless phantomjs processing

	        # make http connection for product url
	        port = url['port'] or 80 
	        body = None # Store more data in regex table if necessary XXX

	        h = httplib.HTTPConnection(url['host'], port)
        	try:
	                h.connect();

        	        # also allow different http verbs XXX
                	h.request("GET", product.url, body, headers)
	                resp = h.getresponse()
        	        # check status
                	buf = resp.read()
	                h.close()

        	        # cache response for url
	                url_cache[product.url] = buf

        	        update_product(product, r, url_cache[product.url])
	        except Exception as e:
        	        s = ScrapeHistory(product.id, row.id, "Failed", "Download: " + str(e))
                	db_session.add(s)

		db_session.commit()


if __name__ == "__main__":
	process()

# ... profit!


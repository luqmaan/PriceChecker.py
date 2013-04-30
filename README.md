PyChecker
==

http://pychecker.com

![Image](fabulous.jpg?raw=true)

It sucks to check prices on those fabulous new shoes everyday, waiting for them to be on sale.

Meet [PyChecker](http://pychecker.com), a web server + scraper that notifies you when the price changes. It's like IFTTT for products. Add a product and get notifications when the price changes.


Installation
--

- install node.js
- install phantom.js
- install [Python Imaging Library](https://developers.google.com/appengine/docs/python/images/installingPIL#mac)
- run `pip install -r requirements.txt`


Starting the application
--

- Run ./runserver.py
- If this is your first time running the server, be sure to intialize the database. This is not the correct way to do so, but for now you can do initialize the database by visiting the '/init/' route
- Schedule a cron job to execute scraper/cron.py


Design
--

[Color scheme](http://www.colourlovers.com/palette/2785786/Stronger)

Fonts are:

- [Raleway](http://www.google.com/fonts/specimen/Raleway)
- [Wisdom Script](http://www.losttype.com/font/?name=wisdom%20script)
- Arial



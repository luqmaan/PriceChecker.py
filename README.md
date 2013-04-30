PyChecker
==

Installation
--

- install node.js
- install phantom.js
- run `pip install -r requirements.txt`


Starting the application
--

- Run ./runserver.sh
- If this is your first time running the server, be sure to intialize the database. This is not the correct way to do so, but for now you can do initialize the database by visiting the '/init/' route
- Schedule a cron job to execute scraper/cron.py


Design
--

[Color scheme](http://www.colourlovers.com/palette/2785786/Stronger)

Fonts are:

- [Raleway](http://www.google.com/fonts/specimen/Raleway)
- [Wisdom Script](http://www.losttype.com/font/?name=wisdom%20script)
- Arial


Database
--

To initialize the database with some basic info, enable the `database.init()` line in __init__.py. This adds:

- A user named john who has a toothbrush and chocolate
- A user named jane who has chocolate


To view these users products:

    john = db_session.query(models.User).filter(models.User.username == "john").first()
    jane = db_session.query(models.User).filter(models.User.username == "jane").first()
    print jane.products
        -> [<Product ('Chocolate', 'http://amazon.com','77', '11', '/static/img/screenshot.jpg')>]
    print john.products
        -> [<Product ('Toothbrush', 'http://google.com','50', '23', '/static/img/screenshot.jpg')>, <Product ('Chocolate', 'http://amazon.com','77', '11', '/static/img/screenshot.jpg')>]

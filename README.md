PyChecker
==

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

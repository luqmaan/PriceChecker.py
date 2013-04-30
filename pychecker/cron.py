import database
import models
import scraper2


def notify(user, product, old_price, new_price):
    print user + " gets a notification"


def main():
    ''' Update all the products in the db, if there are changes notify '''
    notify_queue = []

    products = models.Product.query.all()
    for product in products:
        print (product.url, product.selector)
        price, img = scraper2.product_info(product.url, product.selector)
        if price is not product.price:
            notify_queue.append((product, product.price, price))
            product.price = price
        product.image = img
        database.db_session.commit()

    for i in notify_queue:
        for user in product.users:
            notify(notify_queue[i])

if __name__ == '__main__':
    main()

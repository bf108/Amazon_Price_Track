from price_tracker import PriceTrack
from createTables import ProductInfo
from mailAlert import mailAlerter
from error_notification import errorNotification
import os
import sqlite3

def main():
	try:
		#Get daily price for product and title
		price, product = PriceTrack().getPrice()

		#Make connection to db
		conn = sqlite3.connect('db.sqlite3')

		#Use Scraped Values to instantiate ProductInfo object
		prod = ProductInfo(product, price, conn)

		#Only save entries once per day
		if prod.maxDate():
			#Insert values into db
			prod.insertRow()

			#Only send email if price changes
			diff = prod.priceDiff()

			if diff != 0:
				# maxPrice = prod.checkMaxPrice()
				# minPrice = prod.checkMinPrice()

				mailAlerter(prod.price, diff)

	except Exception as e:
		errorNotification(e)


if __name__ == '__main__':
	main()
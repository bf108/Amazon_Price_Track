import sqlite3
from datetime import datetime as dt

# Model for SQLite table
class ProductInfo:

	def __init__(self,product,price,conn):
		self.date = dt.strftime(dt.today(),'%Y-%m-%d')
		self.product = product.encode('ascii','ignore').decode('ascii')
		self.price = price
		self.conn = conn

	def insertRow(self):
		'''
		Insert row in db table for product

		params
		conn: sqlite3 connection
		prodInfo: object of Class ProductInfo: date, product, price

		returns: none
		'''
		with self.conn:
			c = self.conn.cursor()
			c.execute("""INSERT INTO price_tracker 
						(date, product, price)
						VALUES (?, ?, ?)""",
						(self.date, self.product, self.price))

	def maxDate(self):
		'''
		Compares present day, to last entry in price_tracker table
		This is to only allow single entry per day.

		returns: True if last date different to current date, False if same.
		'''
		with self.conn:
			c = self.conn.cursor()
			latest = c.execute("SELECT MAX(date) FROM price_tracker").fetchone()[0]
			return latest != self.date

	def priceDiff(self):
		with self.conn:
			c = self.conn.cursor()
			diff = c.execute("""
					SELECT id, (price - LAG(price,1) OVER (ORDER BY id)) AS diff
					FROM price_tracker ORDER BY id DESC;
				""").fetchone()[1]

			return diff

	def checkMinPrice(self):
		'''
		return: boolean - True if todays price is lowest ever price
		'''
		with self.conn:
			c = self.conn.cursor()
			minPrice = c.execute("""SELECT MIN(price) FROM price_tracker
						WHERE date < ?;""",(self.date,)).fetchone()[0]

			return minPrice

	def checkMaxPrice(self):
		'''
		return: boolean - True if todays price highest ever price 
		'''
		with self.conn:
			c = self.conn.cursor()

			maxPrice = c.execute("""SELECT MAX(price) FROM price_tracker
						WHERE date < ?;""",(self.date,)).fetchone()[0]

			return maxPrice

def createTable(conn):
	with conn:
		c = conn.cursor()
		# Create Table
		c.execute("""CREATE TABLE IF NOT EXISTS price_tracker(
										id INTEGER PRIMARY KEY,
										date INTEGER NOT NULL,
										product TEXT NOT NULL,
										price REAL NOT NULL
						);""")
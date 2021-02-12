import requests
from bs4 import BeautifulSoup as bs

class PriceTrack:

	def __init__(self):
		#Headers are require to prevent Amazon assuming you are a bot
		self.url = 'https://www.amazon.co.uk/Sony-Advanced-1-0-Type-F1-8-2-8-DSC-RX100M3/dp/B00KW3BJ1Y/ref=sr_1_1?crid=3AOXWXIJO2ZVA&dchild=1&keywords=rx100+iii&qid=1612729103&sprefix=rx100%2Caps%2C162&sr=8-1'
		self.headers = 	{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}	

	def textConverter(self, text):
		'''
		Convert price in string format to float value for comparison. Price in format £ XXX.XX
		text: str
		return: float of price
		'''
		value = text.split('£')[1]
		value = value.replace(',','')

		try:
			return float(value)
		except:
			return float(value.split('.')[0])

	def getPrice(self):
		'''
		Pull price from amazon website
		'''
		response = requests.get(self.url, headers=self.headers).content

		soup = bs(response, 'html.parser')

		price = self.textConverter(soup.find('span', id='priceblock_ourprice').text)
		product = soup.find('span',id='productTitle').text.strip()

		return price, product
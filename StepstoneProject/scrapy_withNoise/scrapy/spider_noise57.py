import scrapy
from scrapy.crawler import CrawlerProcess
import sys

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	urls = ["""https://www.truyenhinhsomatdat.net""",
			"""https://www.npco.website""",
			"""https://www.foto-andes.com"""] #define the start URL you want to start your crawl from
	#urls = [sys.argv[1]]
	pages = []

	def start_requests(self):
		try:
			for url in self.urls:
		#		print(url)
				yield scrapy.Request(url=url, 
					callback=self.parse, 
					dont_filter=True, 
					meta={"proxy": "http://172.57.238.7:7777"},
					headers={"User-Agent": "My UserAgent"})
		except:
			pass

	def parse(self, response):
		print("baba")
		nextPage = None
		#print(response.xpath('//a/@href').getall())

		#get the link to the next page (if there is one)
		# for sel in response.xpath('//a[@class="portal_navigator_next common_link"]'):
		# 	next = sel.xpath('@href').extract()
		# 	if next not in self.pages:
		# 		nextPage = next

		# 	#If there are more pages in list, go to them and scrape them
		# 	if nextPage is not None:
		# 		yield scrapy.Request(nextPage[0], self.parse, dont_filter=True,
		# 			meta={"proxy": "http://172.57.238.1:3128"},
		# 			headers={"User-Agent": "My UserAgent"})

		for sel in response.xpath('//a/@href').getall():
			#print(sel)
			#print("babababa")
			#print("www." in str(sel))
			if ("www."==str(sel)[0:4]) or ("https://"==str(sel)[0:8]) or ("http://" in str(sel)[0:7]):
				nextPage=str(sel)
				#print(nextPage)
				#print("babababa2")
				yield scrapy.Request(nextPage, self.parse, dont_filter=True,
					meta={"proxy": "http://172.57.238.7:7777"},
					headers={"User-Agent": "My UserAgent"})

process = CrawlerProcess()
spider = QuotesSpider()
process.crawl(spider)
process.start() # the script will block here until the crawling is finished

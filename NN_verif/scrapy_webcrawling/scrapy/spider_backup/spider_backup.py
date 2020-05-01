import scrapy
from scrapy.crawler import CrawlerProcess
import sys

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	urls = ["""https://www.research.ed.ac.uk/portal/en/projects/search.html"""] #define the start URL you want to start your crawl from
	#urls = [sys.argv[1]]
	pages = []

	def start_requests(self):
		#print(sys.argv)
		#self.urls.append(self.start_url)
		#print(self.start_url)
		try:
			for url in self.urls:
		#		print(url)
				yield scrapy.Request(url=url, 
					callback=self.parse, 
					dont_filter=True, 
					meta={"proxy": "http://172.16.238.1:3128"},
					headers={"User-Agent": "My UserAgent"})
		except:
			pass

	def parse(self, response):
		print("baba")
		nextPage = None
		#get the link to the next page (if there is one)
		for sel in response.xpath('//a[@class="portal_navigator_next common_link"]'):
			next = sel.xpath('@href').extract()
			if next not in self.pages:
				nextPage = next

			#If there are more pages in list, go to them and scrape them
			if nextPage is not None:
				yield scrapy.Request(nextPage[0], self.parse, dont_filter=True)

process = CrawlerProcess()
spider = QuotesSpider()
process.crawl(spider)
process.start() # the script will block here until the crawling is finished

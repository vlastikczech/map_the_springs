import urllib
import requests
import csv
import json
from flask import jsonify
from geojson import Feature, FeatureCollection, Point
from bs4 import BeautifulSoup

class Scraper(object):
	def __init__(self, settings):
		self.base_url = settings['base_url']
		self.excludes = settings['excludes']
		self.gatherStateUrls(settings['states_list'])
		self.buildSpringListByState()
		self.produceCSV()

	def gatherStateUrls(self, states_list):
		url = urllib.parse.urljoin(self.base_url, states_list)
		response = requests.get(url)
		content = BeautifulSoup(response.content, "html.parser")
		divs = content.find_all("div", {"class": "wsite-section-elements"})

		for div in divs:
			a_tags = div.find_all("a")
			url_list = self.filterUrlList(a_tags)
			if len(url_list) > 0:
				self.explodeStates(url_list)

	def buildSpringListByState(self):
		for state,data in self.states_data.items():
			print("processing %s" % state)
			state_urls = self.getStateData(data['url'])
			data['springs'] = state_urls

	def getStateData(self, state_url):
		url = urllib.parse.urljoin(self.base_url, state_url)
		response = requests.get(url)
		content = BeautifulSoup(response.content, "html.parser")
		divs = content.find_all("div", {"class": "wsite-section-elements"})

		springs_urls = []
		for div in divs:
			a_tags = div.find_all("a")
			url_list = self.filterUrlList(a_tags, extra_filter=state_url)
			if len(url_list) > 0:
				springs_urls.extend(url_list)
		
		springs_data = []
		for spring_url in springs_urls:
			spring_data = self.getSpringData(spring_url)
			if spring_data is not None:
				springs_data.append(spring_data)
		return springs_data

	def getSpringData(self, spring_url):
		spring_data = {}
		spring_data['url'] = urllib.parse.urljoin(self.base_url, spring_url)
		response = requests.get(spring_data['url'])
		content = BeautifulSoup(response.content, "html.parser")
		try:
			spring_data['title'] = content.find("meta",  property="og:title").get('content')
		except AttributeError:
			# probably a bad link
			return None

		print("  -processing %s" % spring_data['title'])

		iframes = content.select(".wsite-map iframe")
		for iframe in iframes:
			src = "http:%s" % iframe.get('src')
			parsed = urllib.parse.parse_qs(src)
			spring_data['long'] = parsed['long'][0]
			spring_data['lat'] = parsed['lat'][0]
		return spring_data

	def explodeStates(self, urls):
		states = {}
		for state_url in urls:
			name = state_url.split('-')[0].strip('/').capitalize()
			states[name] = {'url':state_url}
		self.states_data = states

	def filterUrlList(self, link_list, extra_filter=None):
		url_list = []
		for a in link_list:
			url = a.get('href')
			if url not in ('','/',None, extra_filter) and url not in (self.excludes):
				url_list.append(url)
		return url_list

	def produceCSV(self):
		header_row = "Title,URL,Lat,Long\n"
		with open('./output/output.csv', 'w', encoding="utf-8") as csv:
			csv.write(header_row)
			for state, data in self.states_data.items():
				for spring in data['springs']:
					title = spring['title']
					url = spring['url']
					lat = spring['lat']
					lon = spring['long']
					line = ','.join([title,url,lat,lon])
					csv.write("%s\n" % line)

	def produceJson(self):
		reader = csv.DictReader(open('./output/output.csv'))

		dict_list = []
		for line in reader:
			dict_list.append(line)
		return jsonify({'springs': dict_list, 'success': 1})

	def produceGeoJsonFromCSV(self):
		features = []
		with open('./output/output.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=',')
			next(reader)
			for Title, Url, latitude, longitude, in reader:
				features.append(
					Feature(
						geometry = Point([float(longitude), float(latitude)]),
						properties = {
							'title': Title,
							'url': Url
						}
					)
				)
		return FeatureCollection(features)

	def produceCSVJson(self):
		with open('./output/output.csv') as csv_data:
			reader = csv.reader(csv_data)

			# eliminates blank rows if they don't exist
			rows = [row for row in reader if row]
			headings = rows[0] # get headings

			springs_data = {}
			for row in rows[1:]:
				#append the dataitem to the end of the dictionary entry
				#set the default value of [] of this key has not been seen
				for col_header, data_column in zip(headings, row):
					springs_data.setdefault(col_header, []).append(data_column)
		return springs_data

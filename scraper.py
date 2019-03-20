# for py 3.4
from bs4 import BeautifulSoup
import requests
import datetime
import re

def makeSoup(url):
	headers = {'User-Agent': 'Chrome/39.0.2171.95'}
	request = requests.get(url, headers=headers)
	soup = BeautifulSoup(request.text, "html.parser")
	return soup

def writeFile(links, num_of_articles, file_name, title):
	doc_start = '<div>'
	heading = '<h2>'+title+'</h2>'
	timestamp = '<h3>Updated ' + str(datetime.datetime.now())[:16] + ' UTC</h3>'
	list_open = '<ol class="list-group">'
	list_close = '</ol>'
	doc_end = '</div>'
	document = open(file_name, 'w', encoding='utf8')
	document.truncate()
	document.write(doc_start)
	document.write(heading)
	document.write(timestamp)
	document.write(list_open)
	for i in range(0, num_of_articles):
		print (str(links[i]).encode('utf8'))
		document.write('<li class="list-group-item">'+str(links[i].prettify(formatter="html"))+'</li>')
	document.write(list_close)
	document.write(doc_end)
	document.close()

def createHackerNewsLinks():
	url = "http://news.ycombinator.com"

	soup = makeSoup(url)

	rows = soup.findAll('tr',attrs={'class':'athing'})

	row_soup = BeautifulSoup(str(rows), "html.parser")

	titles = row_soup.findAll('td',attrs={'class':'title'})

	title_soup = BeautifulSoup(str(titles), "html.parser")

	links = title_soup.findAll('a')

	for link in links:
		href = link['href']
		if href.startswith('i'):
			link['href'] = 'https://news.ycombinator.com/' + href

	exclusion = r"from\?site"

	cleanedList = []

	for link in links:
		match = re.search(exclusion, str(link))
		if not match:
			cleanedList.append(link)

	writeFile(cleanedList, 30, 'hn.html', 'Hacker News Top 10 Articles')

def createHanselmanLinks():
	url = "http://www.hanselman.com/blog/"

	soup = makeSoup(url)

	headings = soup.findAll('h2',attrs={'class':'blogTitle'})

	heading_soup = BeautifulSoup(str(headings), "html.parser")

	links = heading_soup.findAll('a')

	writeFile(links, 5, 'sh.html',"Scott Hanselman's Last 5 Posts")

def createCodingHorrorLinks():
	url = "http://blog.codinghorror.com"

	soup = makeSoup(url)

	headings = soup.findAll('h2',attrs={'class':'post-title'})

	heading_soup = BeautifulSoup(str(headings), "html.parser")

	links = heading_soup.findAll('a')

	writeFile(links, 5, 'ch.html',"Jeff Atwood's Last 5 Posts")

	# fix local relative links
	document = open('ch.html', 'r', encoding='utf8')
	contents = document.read()
	document.close()
	contents = contents.replace('href="/', 'href="http://blog.codinghorror.com/')
	document = open('ch.html', 'w', encoding='utf8')
	document.truncate()
	document.write(contents)
	document.close()

def createSpaceXLinks():
	url = "http://www.spacex.com/news"

	soup = makeSoup(url)

	headings = soup.findAll('h2',attrs={'class':'title'})

	heading_soup = BeautifulSoup(str(headings), "html.parser")

	links = heading_soup.findAll('a')

	numLinks = len(links)

	writeFile(links, numLinks, 'spacex.html',"SpaceX News")


createHackerNewsLinks()
createHanselmanLinks()
createCodingHorrorLinks()
createSpaceXLinks()

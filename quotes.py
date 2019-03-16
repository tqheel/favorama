# for py 3.4
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def makeSoup(url):
	headers = {'User-Agent': 'Chrome/39.0.2171.95'}
	request = requests.get(url, headers=headers)
	soup = BeautifulSoup(request.text, "html.parser")
	return soup

def writeFile(links, num_of_articles, file_name, title):
	doc_start = '<div>'
	heading = '<h2>'+title+'</h2>'
	list_open = '<ol class="list-group">'
	list_close = '</ol>'
	doc_end = '</div>'
	document = open(file_name, 'w', encoding='utf8')
	document.truncate()
	document.write(doc_start)
	document.write(heading)
	document.write(list_open)
	for i in range(0, num_of_articles):
		print (str(links[i]).encode('utf8'))
		document.write('<li class="list-group-item">'+str(links[i].prettify(formatter="html"))+'</li>')
	document.write(list_close)
	document.write(doc_end)
	document.close()

def createSenecaQuotes():
	url = "https://dailystoic.com/seneca-quotes/"

	soup = makeSoup(url)

	rows = soup.findAll('tr',attrs={'class':'athing'})

	row_soup = BeautifulSoup(str(rows), "html.parser")

	titles = row_soup.findAll('td',attrs={'class':'title'})

	title_soup = BeautifulSoup(str(titles), "html.parser")

	links = title_soup.findAll('a')

	exclusion = r"from\?site"

	cleanedList = []

	for link in links:
		match = re.search(exclusion, str(link))
		if not match:
			cleanedList.append(link)

	#TODO: Need to inspect each link and prefix link with full domain name if link is an internal only link

	writeFile(cleanedList, 10, 'quotes.html', 'Hacker News Top 10 Articles')

createSenecaQuotes()
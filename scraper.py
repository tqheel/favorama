# for py 3.4
from bs4 import BeautifulSoup
import requests

def makeSoup(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text, "html.parser")
	return soup

def writeFile(links, num_of_articles, file_name, title):
	doc_start = '<div>'
	heading = '<h2>'+title+'</h2>'
	list_open = '<ol>'
	list_close = '</ol>'
	doc_end = '</div>'
	document = open(file_name, 'w', encoding='ascii')
	document.truncate()
	document.write(doc_start)
	document.write(heading)
	document.write(list_open)
	for i in range(0, num_of_articles):
		print (str(links[i]).encode('utf8'))
		document.write('<li>'+str(links[i].prettify(formatter="html"))+'</li>')
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
	#TODO: Need to inspect each link and prefix link with full domain name if link is an internal only link

	writeFile(links, 10, 'hn.html', 'Hacker News Top 10 Articles')

def createHanselmanLinks():
	url = "http://www.hanselman.com/blog/"

	soup = makeSoup(url)

	headings = soup.findAll('h2',attrs={'class':'blogTitle'})

	heading_soup = BeautifulSoup(str(headings), "html.parser")

	links = heading_soup.findAll('a')

	writeFile(links, 5, 'sh.html',"Scott Hanselman's Last 5 Posts")

def createConeryLinks():
	url = "http://rob.conery.io/"

	soup = makeSoup(url)

	post_listing = soup.findAll('section', attrs={'class':'post-listing'})

	articles = post_listing[0].findAll('article',attrs={'class':'post'})

	article_soup = BeautifulSoup(str(articles), "html.parser")

	post_contents = soup.findAll('div',attrs={'class':'post-content'})

	post_contents_soup = BeautifulSoup(str(post_contents), "html.parser")

	headings = post_contents_soup.findAll('h2')

	heading_soup = BeautifulSoup(str(headings), "html.parser")

	links = heading_soup.findAll('a')

	# for li in links:
	# 	print(str(li))

	# for heading in headings:
	# 	print(str(heading))

	# for pl in post_listing:
	# 	print(str(pl.prettify('utf8')))

	# writeFile(links, 10, 'rc.html', "Rob Conery's Last 10 Posts")


createHackerNewsLinks()
createHanselmanLinks()
# createConeryLinks()

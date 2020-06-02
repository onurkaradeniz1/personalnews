import requests
from bs4 import BeautifulSoup
import pprint		
import csv
import xml.etree.ElementTree as ET
from pymongo import MongoClient



client = MongoClient('mongodb://localhost:27017/')
db = client.pnews

def users():
	userlist = list()
	for user in db.pcustomers.find():
		userlist.append((user["username"], user["keywords"]))
	return userlist


def keywords():
	allkeywords = list()
	for user in db.pcustomers.find():
		allkeywords = allkeywords + (user["keywords"])
	return list(dict.fromkeys(allkeywords))


def scrape_data():
	res = requests.get("https://www.hurriyet.com.tr/rss/gundem")
	soup = BeautifulSoup(res.text, 'xml')
	title = soup.findAll("item")
	full_scrape_list = list()
	for item in title:
		full_scrape_list.append([item.title.text, item.description.text, item.link.text])
	return full_scrape_list


def filtered_scrape_data():
	scrape_result = scrape_data()
	allkeywords = keywords()
	filtered_list = list()
	for t in range(len(allkeywords)):
		for i in range(len(scrape_result)):
			if allkeywords[t] in scrape_result[i][0] or allkeywords[t] in scrape_result[i][1]:
				filtered_list.append([allkeywords[t], scrape_result[i][0],  scrape_result[i][1], scrape_result[i][2]])
	return filtered_list


def news_per_user():
	userList = users()
	filtered_list = filtered_scrape_data()
	alluserNews = list()
	for user in userList:
		userNews = list()
		userNews = userNews.clear()
		userNews = list()
		for user_keywords in user[1]:
			for filtered_news in filtered_list:
				if user_keywords == filtered_news[0]:
					userNews.append([user_keywords, filtered_news[1], filtered_news[2], filtered_news[3]])
		alluserNews.append([user[0], userNews])
	return alluserNews
		


pprint.pprint(news_per_user())









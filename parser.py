#!/usr/bin/python2
# -*- coding: utf-8 -*-
import urllib
import json
import datetime
from lxml.html import fromstring
from lxml.html import tostring
def getDate(day, month, year):
    months=['Января','Февраля','Марта','Апреля','Майя','Июня','Июля','Августа','Сентября','Октября','Ноября','Декабря'];
    month = int(month) - 1;
    return str(day+" ")+str(months[month]).decode('utf8').encode('cp1251')+str(" "+year);
def getData(url):
    host = "pornoboss.tv"
    html = urllib.urlopen(url).read();
    page = fromstring(html);
    UrlName = ".//*[@id='content']/div[2]/div[2]/div[1]/h1/text()";
    header = page.xpath(UrlName);
    #print unicode(header[0]);
    
    UrlCategories = ".//*[@id='content']/div[2]/div[2]/div[3]/a/text()";
    categories = page.xpath(UrlCategories);
    UrlLinkCategories = ".//*[@id='content']/div[2]/div[2]/div[3]/a/@href";
    link = page.xpath(UrlLinkCategories);
    catArr = [];
    iteration = 0;
    for item in link:
        catArr.append({"name": categories[iteration].encode("cp1251"), "link": link[iteration].encode("cp1251")});
        iteration=iteration+1;
        
    UrlDate = ".//*[@id='content']/div[2]/div[2]/div[3]/text()";
    date = page.xpath(UrlDate);
    try:
        mydate = date[0].encode("cp1251").split(str(","));
    except IndexError:
        print "Error";
    if(mydate[0]=="Сегодня".decode("utf-8").encode("cp1251")):
        dateArr = str(datetime.date.today()).split("-");
        dateVideo = getDate(dateArr[2], dateArr[1], dateArr[0]);
    else:
        if(mydate[0]=="Вчера".decode("utf-8").encode("cp1251")):
            dateArr = str(datetime.date.today() - datetime.timedelta(days=1)).split("-");
            dateVideo = getDate(dateArr[2], dateArr[1], dateArr[0]);
        else:
            dateArr = str(mydate[0]).split("-");
            dateVideo = getDate(dateArr[0], dateArr[1], dateArr[2]);
    #print date[0].encode("cp1251");
            
    UrlDescription = ".//*[@class='img']/div[1]/div[1]/text()";
    description = page.xpath(UrlDescription);
    #print description[0].encode("cp1251");
    result = {"host": host, "url":url, "header": header[0].encode("cp1251"), "categories": catArr, "date": str(dateVideo),
              "description": description[0].encode("cp1251")};
    return result;
def getResult(url):
    html = urllib.urlopen(url).read();
    page = fromstring(html)
    page.make_links_absolute(url)
    PathOnPage = ".//*[@id='content']/div/div/div/a/@href";
    UrlVideo = page.xpath(PathOnPage);
    #jsonResult = [];
    for item in UrlVideo:
        #jsonResult.append(getData(item));
        with open('data.json', 'a') as outfile:json.dump(getData(item), outfile, sort_keys = True, indent = 4, ensure_ascii = False);
        f = open('data.json', 'a');
        f.write(",");
        f.close();
def main():
    i=1;
    url = "http://pornoboss.tv";
    html = urllib.urlopen(url).read();
    page = fromstring(html);
    path = ".//*[@id='content']/div[2]/div[21]/a[10]/text()";
    last = page.xpath(path);
    while i<=int(last[0]):
        getResult("http://pornoboss.tv/page/"+str(i));
        i=i+1;
main();

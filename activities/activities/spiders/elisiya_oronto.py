
import os
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import scrapy
import json
import csv
import re
from scrapy.http import Request

from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup
import string
class ConcordiaSpider(CrawlSpider):
    name = "Elisiya"
   #allowed_domains = ["www.tripadvisor.ca"]
    start_urls = [
##        "http://www.tripadvisor.ca/Attractions-g187147-Activities-c25-Paris_Ile_de_France.html"
     #  "http://www.tripadvisor.ca/Attractions-g155032-Activities-c25-oa.*.-Montreal_Quebec.html#TtD"
    ]
    def start_requests(self):
        self.f_sv = open('BErlin.csv', 'a')
        self.f_sv2= open('items2.csv', 'a')
        for i in xrange(30,330,30):
            yield self.make_requests_from_url("http://www.tripadvisor.ca/Attractions-g187323-Activities-c25-oa%i-Berlin.html#TtD"%i)

       
    #define the rule to crawl everything from concordia websites
    rules = [Rule(SgmlLinkExtractor(allow_domains=("tripadvisor.ca")),callback="parse_item")]
    member=""
    activity=""
    count=0
    hrefcount=0
    activityre=""
    typ=""
    OwnerDescription=""
    rating =""
    review=""
    #self.f_sv = open('items'+str(ConcordiaSpider.count)+'.csv', 'wb')

    '''Crawler returns the document to this function'''
    def parse_item(self, response):
##        self.f_sv = open('LAselinuim.csv', 'a')
##        self.f_sv2= open('items2.csv', 'a')

        headers1=['name','memberCity','memberCounry','MemberGender','memberAge','CitiesVisited','Countriesvisited','memberDescription','Activitiy','Type','ownerdesc','rating','review']
        headers2=['activites']
        self.f_csv=csv.writer(self.f_sv)
        self.f_csv2=csv.writer(self.f_sv2)
##
##        if ConcordiaSpider.count==0:
##            ConcordiaSpider.count= ConcordiaSpider.count+1
##            self.f_csv2.writerow(headers2)
        
        if ConcordiaSpider.count==0:
            ConcordiaSpider.count= ConcordiaSpider.count+1
            self.f_csv.writerow(headers1)
##        

##        ConcordiaSpider.count= ConcordiaSpider.count+1
        soup = BeautifulSoup(response.body)
        for activi in soup.findAll("div",attrs={'class':'quality easyClear'}):
            for k in activi.findAll('a'):
                href=k.get('href')
                print href
                
                
            request2=scrapy.Request("http://www.tripadvisor.ca/"+href,callback=self.parse_page2, dont_filter=True)
            yield request2
            #print request2
    def parse_page2(self, response):
        typ=""
        OwnerDescription=""
        rating=""
        review=""
        print "---------------------------------------------------"
        print response.url
        
        soup2 = BeautifulSoup(response.body)
##        self.f_sv = open('items'+str(ConcordiaSpider.count)+'.csv', 'wb')
##        headers=['name','memberLocation','memberAge','CitiesVisited','memberDescription','Activitiy']
##        self.f_csv=csv.writer(self.f_sv)
##        ConcordiaSpider.count= ConcordiaSpider.count+1
##        self.f_csv.writerow(headers)
        for acti in soup2('div',attrs={'class':'slim_ranking'}):
            activitytemp=acti.find('a').text
            activityre=activitytemp.encode('ascii','ignore')
            self.f_csv2.writerows(activityre)
            if "activities" in activityre.lower():
                ConcordiaSpider.count= ConcordiaSpider.count+1
                print ConcordiaSpider.count
                print "=========="
##                driver = webdriver.Chrome()
                counter=0
                temp=[]
                for ac in soup2.findAll('div',attrs={'class':'listing_details'}):
                        for k in ac.findAll('div',attrs={'class':'detail'}):
                            if counter==0:
                                temp=k.text.encode('ascii','ignore').strip()
                                Type=temp.split(':')
                                typ=Type[1]
                                counter=counter+1
                      
##                for ac in soup2.findAll('div',attrs={'class':'listing_description'}):
##
##                    for j in ac.findAll('span',attrs={'class':'onShow'}):
##                        print "in onshow"
##                        temp2=j.text.encode('ascii','ignore')
##                        Description= temp2.split('\n')
##                        print Description[2]
##                        OwnerDescription=Description[2]
                for kk in soup2.findAll('div',attrs={'class':'attractionOverlay attractionOverlayHide'}):
                    #print "fffffffffffffffffffffffffff"
                    for jj in kk.findAll('div',attrs={'class':'listing_details'}):
                        temp2=jj.text.encode('ascii','ignore')
                        OwnerDescription=temp2
                
                for title in soup2.findAll('div',attrs={'class':'brandArea'}):
                    activity= title.find('h1').text
                    print ConcordiaSpider.activity
                    print self.activity
                    rows=[(self.activity)]
                    self.f_csv2.writerow(rows)
                    ConcordiaSpider.hrefcount=ConcordiaSpider.hrefcount+1
                    print ConcordiaSpider.hrefcount
##                    driver = webdriver.Chrome()
                    for ra in soup2.findAll('div',attrs={'class':"reviewSelector "}):
                        for k in ra.findAll('img',attrs={'class':re.compile("sprite-rating_s_fill")}):
                            temprating=k.get('alt')
                            rating=temprating.encode('ascii','ignore')
                        for j in ra.findAll("div",attrs={'class':"entry"}):
                            tempreview=j.find('p').text
                            review=tempreview.encode('ascii','ignore')
##                            driver = webdriver.Chrome()
##                            driver.get(response.url)
##                           # driver.implicitly_wait(10)
##                            revid=ra.get('id')
##                            print revid
##                            for revie in driver.find_elements_by_xpath('//div[starts-with(@id,"%s")]'%revid):
##                                try:
##                                    more = WebDriverWait(revie, 2).until(EC.presence_of_element_located((By.CLASS_NAME, 'moreLink')))
##                                    if more.is_displayed():
##                                        print "i am displayed"
##                                        more.click()
##                                        driver.implicitly_wait(2)
##                                except (NoSuchElementException, TimeoutException):
##                                    print "i am exception"
##                                    tempreview=j.find('p').text
##                                    review=tempreview.encode('ascii','ignore')
##                                    
##                                #print review
##                                try:
##                                    full_review = revie.find_element_by_class_name('dyn_full_review')
##                                    en = full_review.find_element_by_class_name('entry')
##                                    tempreview1=en.text
##                                    review=tempreview1.encode('ascii','ignore')
##                                except:
##                                    
##                                    pass
##                                #print "----"
##                            driver.close()
                                  
##                        driver.close() 
                        for mmember in ra.findAll('div',attrs={'class':'username mo'}):
                            memberName=mmember.find('span').text
                            ConcordiaSpider.member= memberName.encode('ascii','ignore')
                            items=[activity,typ,OwnerDescription,rating,review]
                            request3=scrapy.Request("http://www.tripadvisor.ca/members/"+ConcordiaSpider.member,callback=self.parse_page3, dont_filter=True,meta={'item':items})
                            yield request3
                for nextpage in soup2.findAll('link',attrs={'rel':'next'}):
                    href=nextpage.get('href')
                    print "****************************************************"
                    print href
                    request4=scrapy.Request("http://www.tripadvisor.ca/"+href,callback=self.parse_page2, dont_filter=True)
                    print "jjjj"
                    yield request4
                
                            
##                    for mmember in soup2('div',attrs={'class':'username mo'}):
##                        memberName=mmember.find('span').text
##                        ConcordiaSpider.member= memberName.encode('ascii','ignore')
##                        items=[activity,typ,OwnerDescription]
##                        request3=scrapy.Request("http://www.tripadvisor.ca/members/"+ConcordiaSpider.member,callback=self.parse_page3, dont_filter=True,meta={'item':items})
##                        yield request3
##        for title in soup2('div',attrs={'class':'brandArea'}):
##            self.activity= title.find('h1').text
##            print self.activity
##            rows=[(self.activity)]
##            self.f_csv2.writerow(rows)
##            ConcordiaSpider.hrefcount=ConcordiaSpider.hrefcount+1
##            print ConcordiaSpider.hrefcount
                    

##        for type in soup2.findAll('div',attrs={'class':'listing_details'}):
##
##            print "--------------------"
            
        
##        for mmember in soup2('div',attrs={'class':'username mo'}):
##            memberName=mmember.find('span').text
##           
##            ConcordiaSpider.member= memberName.encode('ascii','ignore')
##            request3=scrapy.Request("http://www.tripadvisor.ca/members/"+ConcordiaSpider.member,callback=self.parse_page3, dont_filter=True)
##            yield request3
        
            
        

     
        pass
    def parse_page3(self,response):
        soup2 = BeautifulSoup(response.body)
        memberName=""
        memberInfo=""
        memberSince=""
        memberLocation=""
        memberAge=""
        memberGender=""
        memberCity=""
        Citiesvisited=""
        memberCountry=""
        memberDescription=[]
        rating=""
        locationlist=[]
        review=""
        for membertitle in soup2.findAll('div',attrs={'class':'memberTitle'}):
            memberName=membertitle.text
        for div1 in soup2.findAll('div', attrs={'class':'info'}):
            counter=0
            for k in div1.findAll('p'):
                if counter==1:
                    memberLocation=k.text
                    locationlist=re.split('Lives in |, ',memberLocation)
                    memberCity=locationlist[1]
                    memberCountry=locationlist[-1]
                    
                    
                    #print memberLocation
                elif counter==2 :
                    memberInfo=k.text.encode('ascii','ignore')
                    if "year old" in memberInfo.lower():
                        tempinfo=memberInfo.split("year old")
                        memberAge=tempinfo[0].encode('ascii','ignore')
                        memberGender=tempinfo[1].encode('ascii','ignore')
                    elif "female" in memberInfo.lower():
                        memberGender=memberInfo.encode('ascii','ignore')
                    elif "male" in memberInfo.lower():
                        memberGender=memberInfo.encode('ascii','ignore')
                    #print memberAge
                elif counter==3:
                    memberDescription=[k.text.encode('ascii','ignore')]
                    #print memberDescription
                                    
                
##                memberInfo=memberInfo+k.text+" "
                counter=counter+1
                k.next_sibling
        listvis2=[]
        listvis3=[]
        for div2 in soup2.findAll('div',attrs={'class':'cityName'}):
            templis=[]
##            listvis3=[]
            visiting=div2.text.encode('ascii','ignore')
          
            for k in visiting.split(','):
                listvis3.append(k.lower().encode('ascii','ignore'))
            if listvis3[-1].lower() not in listvis2:
                listvis2.append(listvis3[-1].encode('ascii','ignore'))
            listvis3.pop(-1)
##        for div2 in soup2.findAll('div',attrs={'class':'cityName'}):
##            Citiesvisited=Citiesvisited+div2.text+","
        list1=response.meta['item']
        Countriesvisited=listvis2
        Citiesvisited=listvis3

        
        acti=list1[0]
        typ1=list1[1]
##        print"description"
        description=list1[2]
##        print description
        rating=list1[3]
        review=list1[4]
##        print rating
##        print review
##        print "***********************"
        rows=[(memberName,memberCity,memberCountry,memberGender,memberAge,Citiesvisited,Countriesvisited,memberDescription,acti,typ1,description,rating,review)]
        self.f_csv.writerows(rows)
        
        pass


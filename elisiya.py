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
    name = "Elisiya_paris"
    #allowed_domains = ["www.tripadvisor.ca"]
    start_urls = [
##        "http://www.tripadvisor.ca/Attractions-g187147-Activities-c25-Paris_Ile_de_France.html"
     #  "http://www.tripadvisor.ca/Attractions-g155032-Activities-c25-oa.*.-Montreal_Quebec.html#TtD"
    ]
    def start_requests(self):
        for i in xrange(30,510,30):
            print ("http://www.tripadvisor.ca/Attractions-g187147-Activities-c25-oa%i-Paris_Ile_de_France.html" % i)
            yield self.make_requests_from_url("http://www.tripadvisor.ca/Attractions-g187147-Activities-c25-oa%i-Paris_Ile_de_France.html#TtD" % i)
    

    
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
        self.f_sv = open('itemsparis.csv', 'a')
        self.f_sv2= open('items2.csv', 'a')

        headers1=['name','memberCity','memberCounry','MemberGender','memberAge','CitiesVisited','memberDescription','Activitiy','Type','ownerdesc','rating','review']
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
        
        soup2 = BeautifulSoup(response.body)
##        self.f_sv = open('items'+str(ConcordiaSpider.count)+'.csv', 'wb')
##        headers=['name','memberLocation','memberAge','CitiesVisited','memberDescription','Activitiy']
##        self.f_csv=csv.writer(self.f_sv)
##        ConcordiaSpider.count= ConcordiaSpider.count+1
##        self.f_csv.writerow(headers)
        for acti in soup2('div',attrs={'class':'slim_ranking'}):
            activitytemp=acti.find('a').text
            ConcordiaSpider.activityre=activitytemp.encode('ascii','ignore')
            if "Activities"or"activities" in activityre:
                ConcordiaSpider.count= ConcordiaSpider.count+1
                print ConcordiaSpider.count
                print "=========="
                for ac in soup2.findAll('div',attrs={'class':'listing_details'}):
                    for k in ac.findAll('div',attrs={'class':'detail'}):
                        temp=k.text.encode('ascii','ignore')
                        Type=temp.split(':')
                        typ=Type[1]
                    
                for ac in soup2.findAll('div',attrs={'class':'listing_description'}):
                    for j in ac.findAll('span',attrs={'class':'onShow'}):
                        temp2=j.text.encode('ascii','ignore')
                        Description= temp2.split('\n')
                        OwnerDescription=Description[2]
                
                for title in soup2.findAll('div',attrs={'class':'brandArea'}):
                    activity= title.find('h1').text
                    print ConcordiaSpider.activity
                    print self.activity
                    rows=[(self.activity)]
                    self.f_csv2.writerow(rows)
                    ConcordiaSpider.hrefcount=ConcordiaSpider.hrefcount+1
                    print ConcordiaSpider.hrefcount
                    for ra in soup2.findAll('div',attrs={'class':"reviewSelector "}):
                        for k in ra.findAll('img',attrs={'class':"sprite-rating_s_fill rating_s_fill s50"}):
                            temprating=k.get('alt')
                            rating=temprating.encode('ascii','ignore')
                        for j in ra.findAll("div",attrs={'class':"entry"}):
                            tempreview=j.find('p').text
                            review=tempreview.encode('ascii','ignore')
                        for mmember in ra.findAll('div',attrs={'class':'username mo'}):
                            memberName=mmember.find('span').text
                            ConcordiaSpider.member= memberName.encode('ascii','ignore')
                            items=[activity,typ,OwnerDescription,rating,review]
                            request3=scrapy.Request("http://www.tripadvisor.ca/members/"+ConcordiaSpider.member,callback=self.parse_page3, dont_filter=True,meta={'item':items})
                            yield request3
                            

                            
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
                    memberInfo=k.text
                    if "year old" in memberInfo.lower():
                        tempinfo=memberInfo.split("year old")
                        memberAge=tempinfo[0]
                        memberGender=tempinfo[1]
                    elif "female" in memberInfo.lower():
                        memberGender=memberInfo
                    elif "male" in memberInfo.lower():
                        memberGender=memberInfo
                    #print memberAge
                elif counter==3:
                    memberDescription=[k.text]
                    #print memberDescription
                                    
                
##                memberInfo=memberInfo+k.text+" "
                counter=counter+1
                k.next_sibling
        for div2 in soup2.findAll('div',attrs={'class':'cityName'}):
            Citiesvisited=Citiesvisited+div2.text+","
        list1=response.meta['item']
        
        acti=list1[0]
        typ1=list1[1]
        description=list1[2]
        rating=list1[3]
        review=list1[4]
##        print rating
##        print review
##        print "***********************"
        rows=[(memberName,memberCity,memberCountry,memberGender,memberAge,Citiesvisited,memberDescription,acti,typ1,description,rating,review)]
        self.f_csv.writerows(rows)
        pass


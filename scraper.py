import requests, re, feedparser
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


class Scraper(object):

    def __init__(self):
        pd.options.display.width = 100
        pd.options.display.max_colwidth = 20
        pd.options.display.max_columns = 20
        self.min_date = datetime.strptime("2020-05-19","%Y-%m-%d")

    def convert(self,page_div="div",class_page=None,desc_div=None,desc_class=None,link_div="a",link_class="href",date_div=None,date_class=None,url=None,loop_begin=0,desc_int=0,date_int=0,site_type = "NA",date_formatter="%Y %m %d"):
        """This is the main function for converting a site's data to a dataframe all other sites that cannot be called in this function have their own separate functino"""

        self.dict_list = []

        self.dict = {}

        self.headers = {'User-Agent': 'Mozilla/5.0'}

        for u in url:

            self.r = requests.get(u, headers = self.headers)

            self.r.encoding = "utf-8" #" and ' returning errors need to correct. Workaround could be to replace these symbols with a blank

            self.c = self.r.content

            self.soup = BeautifulSoup(self.c,"html.parser")

            if class_page:
                class_page = re.compile(class_page) #needed for when sometimes classes have a slight change in each itteration therefore re is required

            self.all = self.soup.find_all(page_div, class_ = class_page)

            for item in self.all[loop_begin:]:
                try:
                    self.desc = item.find_all(desc_div, class_ = desc_class)[desc_int].text.strip()
                except:
                    continue

                cat = self.category_finder(self.desc)

                try:
                    if item.find(link_div)[link_class] == None:
                        self.link = item[link_class] #needed for some cases when there is not any anchors
                    else:
                        self.link = item.find(link_div)[link_class]
                except: #if not url then use the main page url
                    self.link = u

                try:
                    self.date = item.find_all(date_div, class_ = date_class)[date_int].text.strip() #add if date < date then continue for loop to begining of for loop
                    if site_type == "IFS":
                        self.date = datetime.strptime(re.sub("Published Date ", "", self.date),date_formatter)

                    else:
                        self.date = datetime.strptime(self.date,date_formatter)
                except:
                    print("Could not find a date for %s, %s, %s, %s" %(self.link,self.desc, self.date, site_type))

                if self.date < self.min_date:
                    continue

                self.dicts = {"category": cat, "description": self.desc, "link": self.url_corrector(u, self.link), "date" : self.date, "site_type": site_type}

                self.dict_list.append(self.dicts)

        self.df = pd.DataFrame(self.dict_list)

        return(self.df)


    def ecrasff(self):
        """EC RASFF function for returning dataframe of EC RASFF news"""
        self.df = pd.read_html("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationsList")[0]

        self.df["Date of case"] = pd.to_datetime(self.df["Date of case"])
        self.df = self.df.loc[self.df["Date of case"] < self.min_date, ["Subject","Reference","Date of case"]]
        self.df.insert(0, "category", "Alert")
        self.df.insert(4, "site_type", "EC RASFF")
        self.df.rename(columns={"Subject": "description", "Reference": "link", "Date of case": "date" }, inplace=True)

        self.df["link"] = self.df["link"].apply(lambda x: "{}{}".format("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationDetail&NOTIF_REFERENCE=", x))

        return(self.df)

    def fda(self):
        """FDA function for returning dataframe of FDA news"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts',
            'TE': 'Trailers',
        }

        self.params = (
            ('_', '1589124541273'),
        )

        self.response = requests.get("https://www.fda.gov/files/api/datatables/static/recalls-market-withdrawals.json", headers=self.headers, params=self.params)

        self.df = pd.read_json(response.text)
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df = self.df.loc[self.df["Date of case"] < self.min_date, ["Subject","Reference","Date of case"]].rename(columns={"field_product_description": "description", "path": "link", "field_change_date_2": "date" }, inplace=True)
        self.df.insert(0, "category", "News")
        self.df.insert(4, "site_type", "FDA")
        return(self.df)

    def ifsqn(self,date_formatter):
        """IFSQN function for returning dataframe of IFSQN news"""
        self.parsed_rss = feedparser.parse('https://www.ifsqn.com/forum/index.php/rss/forums/4-food-safety-quality-discussion/')

        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df = self.pd.DataFrame(parsed_rss['entries'])
        self.df = self.df.loc[self.df["Date of case"] < self.min_date, ["Subject","Reference","Date of case"]].rename(columns={"title": "description", "published": "date" }, inplace=True)
        self.df.loc[self.df["date"] < self.min_date]
        self.df.insert(0, "category", "Discussion")
        self.df.insert(4, "site_type", "IFSQN")
        self.df["date"] = pd.to_datetime(self.df["date"])
        return(self.df)

    def fsanzdf(self, date_formatter):
        """FSANZ function for returning dataframe of FSANZ news"""
        self.dl = []
        self.r = requests.get("https://www.foodstandards.gov.au/industry/foodrecalls/recalls/Pages/default.aspx")
        self.soup = BeautifulSoup(self.r.text,'html.parser')
        for item in self.soup.find('div',class_='searchfilter-userfilterbox').find_next('div').find_all('a'):
            self.link = item['href']
            self.date  = item.find_previous('div').text
            self.date = datetime.strptime(self.date,date_formatter)

            if self.date < self.min_date:
                continue
            self.desc = item.find_next('td').text + " :: " + item.find_next('td').find_next('td').text

            cat = self.category_finder(self.desc)

            self.dicts = {"category": cat, "description": self.desc, "link": self.link, "date" :  self.date, "site_type": "FSANZ"}

            self.dl.append(self.dicts)

        #self.dl["date"] = pd.to_datetime(self.dl["date"])

        return pd.DataFrame(self.dl)

    def dateformatter(self, df, date_formatter):
        """This function dates a dataframe and applies a date fromat to the date column"""
        return df["date"].dt.strftime(date_formatter)

    def category_finder(self, string):
        cat = ['Recall','Alert','Discussion','News']
        for i in range (len(cat)):
            if cat[i].upper() in string.upper(): #case sensitive
                return(cat[i])
        return "News"

    def url_corrector(self,url, partial_url):
        self.url_end = [".com",".gov",".ie",".uk",".eu",".org",".ca",".int"]
        self.st = []
        for u in self.url_end:
            try:
                self.st = url.split(u)[0] + u
                if url.split(u)[1]:
                    break
            except:
                continue

        if self.st[:len(self.st)] != partial_url:
            self.st = str(self.st) + partial_url

        return str(self.st)


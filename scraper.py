import requests, re, feedparser
from bs4 import BeautifulSoup
import pandas as pd
#import arrow


class Scraper(object):

    def __init__(self):
        pd.options.display.width = 100
        pd.options.display.max_colwidth = 20
        pd.options.display.max_columns = 20


    def convert(self,page_div="div",class_page=None,desc_div=None,desc_class=None,link_div="a",link_class="href",date_div=None,date_class=None,url=None,loop_begin=0,desc_int=0,date_int=0,site_type = "NA",date_formatter=""):
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
                try:
                    if item.find(link_div)[link_class] == None:
                        self.link = item[link_class] #needed for some cases when there is not any anchors
                    else:
                        self.link = item.find(link_div)[link_class]
                except: #if not url then use the main page url
                    self.link = u

                try:
                    self.date = item.find_all(date_div, class_ = date_class)[date_int].text.strip() #add if date < date then continue for loop to begining of for loop
                except:
                    self.date = '2069-04-20'

                self.dicts = {"category": "test", "description": self.desc, "link": self.link, "date" : self.date.format('YYYY-MM-DD'), "site_type": site_type}

                self.dict_list.append(self.dicts)

        self.df = pd.DataFrame(self.dict_list)
        self.df["date"] = pd.to_datetime(self.df["date"].dt.strftime(date_formatter), errors = 'coerce')

        return self.df


    def ecrasff(self):
        """EC RASFF function for returning dataframe of EC RASFF news"""
        self.df = pd.read_html("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationsList")[0]

        self.df = self.df[["Subject","Reference","Date of case"]]
        self.df.insert(0, "category", "Alert")
        self.df.insert(4, "site_type", "EC RASFF")
        self.df.rename(columns={"Subject": "description", "Reference": "link", "Date of case": "date" }, inplace=True)

        return(self.df)

    def fda(self,date_formatter):
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
        self.df = self.df[["field_product_description","path","field_change_date_2"]].rename(columns={"field_product_description": "description", "path": "link", "field_change_date_2": "date" }, inplace=True)
        self.df.insert(0, "category", "News")
        self.df.insert(4, "site_type", "FDA")

        return(self.df)

    def ifsqn(self,date_formatter):
        """IFSQN function for returning dataframe of IFSQN news"""
        self.parsed_rss = feedparser.parse('https://www.ifsqn.com/forum/index.php/rss/forums/4-food-safety-quality-discussion/')

        self.df = self.pd.DataFrame(parsed_rss['entries'])
        self.df = self.df[["title","link","published"]].rename(columns={"title": "description", "published": "date" }, inplace=True)
        self.df.insert(0, "category", "Discussion")
        self.df.insert(4, "site_type", "IFSQN")
        return(self.df)

    def fsanzdf(self,date_formatter):
        """FSANZ function for returning dataframe of FSANZ news"""
        self.dl = []
        self.r = requests.get("https://www.foodstandards.gov.au/industry/foodrecalls/recalls/Pages/default.aspx")
        self.soup = BeautifulSoup(self.r.text,'html.parser')
        for item in self.soup.find('div',class_='searchfilter-userfilterbox').find_next('div').find_all('a'):
            self.link = item['href']
            self.date  = item.find_previous('div').text
            self.desc = item.find_next('td').text + " :: " + item.find_next('td').find_next('td').text

            self.dicts = {"category": "test", "description": self.desc, "link": self.link, "date" : self.date, "site_type": "FSANZ"}

            self.dl.append(self.dicts)

        return pd.DataFrame(self.dl)

    def dateformatter(self, df, date_formatter):
        """This function dates a dataframe and applies a date fromat to the date column"""
        return df["date"].dt.strftime(date_formatter)

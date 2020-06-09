import requests, re, feedparser
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.ERROR)



class Scraper(object):

    def __init__(self,mn_date):
        pd.options.display.width = 100
        pd.options.display.max_colwidth = 20
        pd.options.display.max_columns = 20
        self.df = pd.DataFrame(columns=["Category","Description","Link","date","Source"])
        try:
            self.min_date = datetime.strptime(str(mn_date),"%Y-%m-%d").date()
        except:
            logging.warning("Could not convert date for date: %s url: %s site: %s" % (mn_date, url, Source))
            return


    def convert(self,page_div="div",class_page=None,desc_div=None,desc_class=None,link_div="a"
        ,link_class="href",date_div=None,date_class=None,url=None,loop_begin=0,desc_int=0
        ,date_int=0,Source = "NA",date_formatter="%Y %m %d"):
        """This is the main function for converting a site's data to a dataframe all other sites that cannot be called in this function have their own separate functino"""

        logging.info("Finding info for site: %s url: %s" % (Source, url))

        self.dict_list = []

        self.dict = {}

        self.headers = {'User-Agent': 'Mozilla/5.0'}

        for u in url:

            logging.info("Connecting to site %s" % u)

            try:
                self.r = requests.get(u, headers = self.headers)
            except:
                logging.warning("Could not connect to site: %s url: %s" % (Source, url))
                return

            self.r.encoding = "utf-8" #" and ' returning errors need to correct. Workaround could be to replace these symbols with a blank

            try:
                self.c = self.r.content
                self.soup = BeautifulSoup(self.c,"html.parser")

                if class_page:
                    class_page = re.compile(class_page) #needed for when sometimes classes have a slight change in each itteration therefore re is required

                self.all = self.soup.find_all(page_div, class_ = class_page)

            except:
                logging.warning("Could not retrieve content for site: %s url: %s content:%s" % (Source, url,self.r.content))
                return

            for item in self.all[loop_begin:]:

                try:
                    self.desc = item.find_all(desc_div, class_ = desc_class)[desc_int].text.strip()
                except:
                    logging.info("Could not find Description for site: %s url: %s \n div: %s \nclass: %s \nint: %s \n HTML: %s" % (Source, url, desc_div, desc_class, desc_int,item))
                    continue

                try:
                    cat = self.category_finder(self.desc)
                except:
                    logging.warning("Could not find a Category for site: %s url: %s \n deasc: %s" % (Source, url, self.desc))


                try:
                    if item.find(link_div)[link_class] == None:
                        self.link = item[link_class] #needed for some cases when there is not any anchors
                    else:
                        self.link = item.find(link_div)[link_class]
                except: #if not url then use the main page url
                    self.link = u

                try:
                    self.date = item.find_all(date_div, class_ = date_class)[date_int].text.strip() #add if date < date then continue for loop to begining of for loop
                    if Source == "IFS":
                        self.date = datetime.strptime(re.sub("Published Date ", "", self.date),date_formatter).date()

                    else:
                        self.date = datetime.strptime(self.date,date_formatter).date()
                except:
                    logging.warning("Could not find a date for %s, %s, %s, %s" %(self.link,self.desc, self.date, Source))
                    continue

                if self.date < self.min_date:
                    logging.debug("Date Skipped: %s",self.date)
                    continue
                print(u)

                print(self.link)
                self.dicts = {"Category": cat, "Description": self.desc, "Link": self.url_corrector(u, self.link), "Date" : self.date, "Source": Source}

                self.dict_list.append(self.dicts)

        self.df = pd.DataFrame(self.dict_list)

        return(self.df)

    def ecrasff(self):
        """EC RASFF function for returning dataframe of EC RASFF news"""
        logging.info("Retrieving ECRASFF data from before: %s" % self.min_date)

        try:
            self.df = pd.read_html("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationsList")[0]
        except:
            logging.warning("Could not connect to ECRASFF")
            return

        try:
            logging.info("Creating DataFrame for ECRASFF")
            self.df = self.df[["Subject","Reference","Date of case"]]
            self.df.insert(0, "Category", "Alert")
            self.df.insert(4, "Source", "EC RASFF")
            self.df.rename(columns={"Subject": "Description", "Reference": "Link", "Date of case": "Date" }, inplace=True)
            self.df["Link"] = self.df["Link"].apply(lambda x: "{}{}".format("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationDetail&NOTIF_REFERENCE=", x))

        except:
            logging.warning("Could not create datframe for ECRASFF")
            return

        try:
            logging.info("Restricting by date")
            self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
            self.df = self.df[self.df["Date"] > self.min_date]

        except:
            logging.warning("Could not apply date restriction on ECRASFF")
            return

        logging.info("ECRASFF data retrived")
        return(self.df)

    def fda(self):
        """FDA function for returning dataframe of FDA news"""
        logging.info("Retrieving FDA data from before: %s" % self.min_date)
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
        try:
            self.response = requests.get("https://www.fda.gov/files/api/datatables/static/recalls-market-withdrawals.json", headers=self.headers, params=self.params)
            self.df = pd.read_json(self.response.text)

        except:
            logging.warning("Could not connect to FDA")
            return

        try:
            logging.info("Creating DataFrame for FDA")

            self.df["Description"] = self.df[["field_company_name"] + ["field_recall_reason_description"] + ["field_recall_reason"]].agg(' :: '.join, axis=1)
            self.df["Date"] = pd.to_datetime(self.df["field_change_date_2"])
            self.df["Link"] = self.df["path"]
            self.df = self.df[["Description","Link","Date"]]
            self.df.insert(0, "Category", "News")
            self.df.insert(4, "Source", "FDA")
            self.df["Link"] = self.df["Link"].apply(lambda x: "{}{}".format("https://www.fda.gov", x))
            self.df["Date"] = self.df['Date'].dt.date

        except:
            logging.warning("Could not create datframe for FDA")
            return

        try:
            logging.info("Restricting FDA by Date")
            self.df = self.df[self.df["Date"] > self.min_date]

        except:
            logging.warning("Could not apply date restriction on FDA")
            return

        logging.info("FDA data retrived")
        return(self.df)

    def ifsqn(self):
        """IFSQN function for returning dataframe of IFSQN news"""
        logging.info("Retrieving IFSQN data from before: %s" % self.min_date)

        try:
            self.parsed_rss = feedparser.parse('https://www.ifsqn.com/forum/index.php/rss/forums/4-food-safety-quality-discussion/')
        except:
            logging.warning("Could not connect to IFSQN")
            return

        try:
            logging.info("Creating DataFrame for IFSQN")
            self.df = pd.DataFrame(self.parsed_rss['entries'])[["title","summary","Link","published"]]
            self.df['summary'] = [BeautifulSoup(text,features="lxml").get_text() for text in self.df['summary']]

            #Might be needed in the future
            #self.df["Description"] = self.df[["title"] + ["summary"]].agg(' :: '.join, axis=1)
            self.df["Description"] = self.df[["title"]]
            self.df.drop("title", axis=1, inplace=True)
            self.df.drop("summary", axis=1, inplace=True)

            self.df.rename(columns={"published": "Date" }, inplace=True)
            self.df.insert(0, "Category", "Discussion")
            self.df.insert(4, "Source", "IFSQN")
            self.df["Date"] = pd.to_datetime(self.df["Date"])
            self.df["Date"] = self.df['Date'].dt.date
            self.df = self.df[["Category","Description","Link","Date","Source"]]


        except:
            logging.warning("Could not create datframe for IFSQN")
            return

        try:
            logging.info("Restricting IFSQN by date")
            self.df = self.df[self.df["Date"] > self.min_date]

        except:
            logging.warning("Could not apply date restriction on IFSQN")
            return

        logging.info("IFSQN data retrieved")
        return(self.df)

    def fsanzdf(self, date_formatter):
        """FSANZ function for returning dataframe of FSANZ news"""
        logging.info("Retrieving FSANZ data from before: %s" % self.min_date)

        self.dl = []
        url = "https://www.foodstandards.gov.au/industry/foodrecalls/recalls/Pages/default.aspx"


        try:
            logging.info("Connections to FSANZ")
            self.r = requests.get(url)
            self.soup = BeautifulSoup(self.r.text,'html.parser')
        except:
            logging.warning("Could not connect to FSANZ")
            return

        for item in self.soup.find('div',class_='searchfilter-userfilterbox').find_next('div').find_all('a'):
            try:
                self.date  = item.find_previous('div').text
                self.date = datetime.strptime(self.date,date_formatter).date()
            except:
                continue

            if self.date < self.min_date:
                continue

            try:
                self.desc = item.find_next('td').text + " :: " + item.find_next('td').find_next('td').text
            except:
                continue

            try:
                self.link = item['href']
            except:
                self.link = url

            try:
                cat = self.category_finder(self.desc)
            except:
                logging.warning("Could not find a Category for site: %s url: %s \n desc: %s" % ("FSANZ", url, self.desc))

            try:
                self.dicts = {"Category": cat, "Description": self.desc, "Link": self.link, "Date" :  self.date, "Source": "FSANZ"}
                self.dl.append(self.dicts)
            except:
                continue

        try:
            self.df = pd.DataFrame(self.dl)
        except:
            logging.warning("Could not create DataFrame for FSANZ")
            return


        logging.info("FSANZ data retrieved")
        return(self.df)

    def dateformatter(self, df, date_formatter):
        """This function dates a dataframe and applies a date fromat to the date column"""
        return df["date"].dt.strftime(date_formatter).date()

    def category_finder(self, string):
        cat = ['Recall','Alert','Discussion','News']
        for i in range (len(cat)):
            if cat[i].upper() in string.upper(): #case sensitive
                return(cat[i])
        return "News"

    def url_corrector(self, url, partial_url):
        if partial_url[:len(url)] != url:
            return url
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


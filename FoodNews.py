import os, bs4, requests, re, datetime, openpyxl, pandas as pd
from collections import ChainMap
from urlextract import URLExtract
from IPython.display import display_html

d = [] #list of dictionaries

os.chdir('Path') #path for csv

#takes the string text and returns the category (works, but not full completed. Will have to return to this at the end to ensure that the category finder is correct)
def category(string):
    cat = ['Recall','Alert','Discussion','News']
    for i in range (len(cat)):
        if cat[i].upper() in string.upper(): #case sensitive
            return(cat[i])
    return 'News' #if no match then use News

#method that takes the url and css path and returns the string of that site
def website_text(url, element):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text,'html.parser')
    elems = soup.select(element)
    a = str(elems[0])
    return a

def ecrasff (url,urlformat,dateformat): #specific logic for this site (using pandas)
    df = pd.read_html(url)[0]

    a = df['Reference'].values.tolist() #url

    url_l = [urlformat+str(i) for i in a] #

    text_l = df['Subject'].values.tolist() #text

    date_l = df['Date of case'].values.tolist() #date

    list_dict(url_l,text_l,date_l,dateformat,urlformat,'ecrasff')

def cfia (url,element,urlformat,urlfinder,dateformat): #specific logic for this site
    df = pd.read_html(url)[0]

    s = website_text(url,element)
    #url
    url = re.findall(urlfinder,s)
    #correct all url's that are not full
    for i in range(0,len(url)):
        text = url[i]
        if text[:len(urlformat)] != urlformat:
            url[i] = urlformat+url[i]

    text = df['Recall'].values.tolist() #text

    date = df['Posted'].values.tolist() #date

    list_dict(url,text,date,dateformat,urlformat)

def date_list(ws_data,url_l,dateURLelement,datefinder,textlen,sitetype):
    tempdate = []
    date = []
    #date
    if sitetype == 'NZ_FSA': #date is stored on next page
        #If data on next page then change URL

        for i in range(textlen):
            a = website_text(url_l[i],dateURLelement) #gets all content from that page
            #print(a)
            n = re.findall(datefinder,a)
            #print(n)
            if not n:
                tempdate.append(['01 January 2001']) #if cannot find date
            else:
                tempdate.append(re.findall(datefinder,a))

        for sublist in tempdate: #change from list of lists to list
            for l in sublist:
                date.append(l)

    else:
        date = re.findall(datefinder,ws_data)

    return date

#lists of all the data. This could be merged with the list_dict method
def dictionary(url, element, urlfinder, textfinder, datefinder, dateformat, urlformat, dateURLelement, sitetype):

    ws_data = website_text(url,element) #website data

    #hyperlink text
    text_l = re.findall(textfinder,ws_data) #list of all news headlines

    url_l = url_list(url, ws_data,urlformat,urlfinder,len(text_l),sitetype) #list of all corresponding urls

    date_l = date_list(ws_data,url_l,dateURLelement,datefinder,len(text_l),sitetype) #list of all corresponding dates

    ##For testing##
    # print(s)
    # # return
    # print(url)
    # print(len(url))
    # print(text)
    # print(len(text))
    # print(date)
    # print(len(date))

    # for i in range(len(text)):
    #     print(url[i]+'\n')
    #     print(text[i]+'\n')
    #     print(date[i]+'\n')
    # return

    list_dict(url_l,text_l,date_l,dateformat,urlformat,sitetype)

#lists to dictionary
def list_dict(url_l,text_l,date_l,dateformat,urlformat,sitetype):

    for i in range (len(url_l)):

        dateformatted = datetime.datetime.strptime(date_l[i],dateformat)

        dicts = [
            {"category": category(text_l[i]), "url": url_l[i], "text": text_l[i], "date":date_l[i], "dateformat":dateformatted, "site_type":sitetype}]

        d.append(dicts)

    return d


def workbook(dic):

    wb = openpyxl.Workbook()

    #print(wb)

    sheet = wb.get_sheet_by_name('Sheet')

    #populate workbook with the applicable data
    for i in range(1,len(dic)+1):
        data = dict(ChainMap(*dic[i-1]))
        sheet.cell(row=i, column = 1, value=data['category'])
        sheet.cell(row=i, column = 2, value=data['url'])
        sheet.cell(row=i, column = 3, value=data['text'])
        sheet.cell(row=i, column = 4, value=data['date'])
        sheet.cell(row=i, column = 4, value=data['dateformat']) #formats the date column
        sheet.cell(row=i, column = 5, value=data['site_type'])

    wb.save('example.csv')
    #print(d)

def url_list(url,ws_data,urlformat,urlfinder,textlen,sitetype):

    url_l = [] #empty list

    if sitetype == 'IFS':
        #No specific url's for IFS site so fill the list with the same url

        for i in range(textlen):
            url_l = url_l.append(url)

    else:
        #url
        url_l = re.findall(urlfinder,ws_data)
        #correct all url's that are not full
        for i in range(len(url_l)):
            text = url_l[i]
            if text[:len(urlformat)] != urlformat:
                url_l[i] = urlformat+url_l[i]

    for i in range(len(url_l)):
        t = url_l[i]
        if t[:len(urlformat)] != urlformat:
            url_l[i] = urlformat+url_l[i]

    return url_l

def cfia (url,element,urlformat,urlfinder,dateformat):

    df = pd.read_html(url)[0]

    text = df['Recall'].values.tolist() #text

    ws_data = website_text(url,element) #website data

    url = url_list(url,ws_data,urlformat,urlfinder,len(text),'CFIA')

    for i in range(len(text)): #remove everything before the - symbol
        text[i] = str(text[i].partition('- ')[2])
        #print(text[i]+'\n')

    date = df['Posted'].values.tolist() #date

    list_dict(url,text,date,dateformat,urlformat,'CFIA')


# #SQFI
dictionary('http://brc.org.uk/news' #url
    ,'#latestNewsList' #element
    ,r'href="/news/(.*?)">' #urlfinder
    ,r'class="title">(.*?)<' #textfinder
    ,r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}' #datefinder
    ,'%B %d, %Y' #dateformat
    ,'http://brc.org.uk/news/'#urlformat
    ,'' #dateURLelement
    ,'SQF' #type
    )

#BRC
dictionary('http://brc.org.uk/news' #url
    ,'#latestNewsList' #element
    ,r'href="/news/(.*?)">' #urlfinder
    ,r'class="title">(.*?)<' #textfinder
    ,r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}' #datefinder
    ,'%B %d, %Y' #dateformat
    ,'http://brc.org.uk/news/'#urlformat
    ,'' #dateURLelement
    ,'BRC' #type
    )

# GFSI test
dictionary('https://mygfsi.com/news-and-resources/?type=news_updates' #url
    ,'#response' #element
    ,r'url\(\'(.*?)\'\);' #urlfinder
    ,r'<div class="section-title">\n\s{56}(.*?)\s{52}</div>' #textfinder
    ,r'\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}' #datefinder
    ,'%d %B %Y' #dateformat
    ,'https://mygfsi.com'#urlformat
    ,'' #dateURLelement
    ,'GFSI' #type
    )

# #USDAFSIS
dictionary('https://www.fsis.usda.gov/wps/portal/fsis/topics/recalls-and-public-health-alerts/current-recalls-and-alerts' #url
    ,'#sorted-content-container' #element
    ,r'<span class="title-container">\n<a href="/(.*?)"' #urlfinder
    ,r'<span class="display-title">\n{6}\t(.*?)\n{3}</span>' #textfinder
    ,r'<div class="recall-date">\n{2}\s{4}((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4})' #datefinder
    ,'%b %d, %Y' #dateformat
    ,'https://www.usda.gov'#urlformat
    ,'' #dateURLelement
    ,'USDA_FSIS' #type
    )

#USDA
dictionary('https://www.usda.gov/media/press-releases' #url
    ,'#block-usda-content > div > div > div:nth-child(2) > ul' #element
    ,r'<a href="/(.*?)"' #urlfinder
    ,r'="en">(.*?)</a></li>' #textfinder
    ,r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}' #datefinder
    ,'%b %d, %Y' #dateformat
    ,'https://www.usda.gov'#urlformat
    ,'' #dateURLelement
    ,'USDA' #type
    )


#UK_FSA
dictionary('https://www.food.gov.uk/news-alerts/search/alerts' #url
    ,'#block-mainpagecontent > div > div > div' #element
    ,r'<h3>\n<a href="(.*?)"' #urlfinder
    ,r'"field field__title">(.*?)</span>' #textfinder
    ,r'\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}' #datefinder
    ,'%d %B %Y' #dateformat
    ,'https://www.mpi.govt.nz'#urlformat
    ,'' #dateURLelement
    ,'UK_FSA' #type
    )

#cfia
cfia('https://www.inspection.gc.ca/about-the-cfia/newsroom/food-recall-warnings/eng/1299076382077/1299076493846' #url
    ,'body > main > table > tbody' #element
    ,'https://www.inspection.gc.ca'#urlformat
    ,r'<td><a href="(.*?)"' #urlfinder
    ,r'%Y-%m-%d' #dateformat
    )

# #RASFF
ecrasff("https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationsList"#url
    ,'https://webgate.ec.europa.eu/rasff-window/portal/index.cfm?event=notificationDetail&NOTIF_REFERENCE='#urlformat
    ,'%d/%m/%Y' #dateformat
    )

# # #NZ FSA
dictionary('https://www.mpi.govt.nz/food-safety/food-safety-for-consumers/recalled-food-products/' #url
    ,'#main-content > ul:nth-child(4)' #element
    ,r'<li><a href="(.*?)">' #urlfinder
    ,r'">(.*?)</a>' #textfinder
    ,r'\d{1,2}\s(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}' #datefinder
    ,'%d %B %Y' #dateformat
    ,'https://www.mpi.govt.nz/'#urlformat
    ,'#main-content > div.intro > p' #dateURLelement
    ,'NZ_FSA' #type
    )

# # #FSAI FoodAlerts
dictionary('https://www.fsai.ie/news_centre/food_alerts.html' #url
    ,'#content' #element
    ,r'<p class="title"><a href="(.*?)">' #urlfinder
   ,r'(?:.html|.aspx\?id=\d{5})">(.*?)</a><br/><em class="emp">' #textfinder
    ,r'</a><br/><em class="emp">(.*?)</em></p><p>' #datefinder
    ,'%A, %d %B %Y' #dateformat
    ,'https://www.fsai.ie/news_centre/food_alerts'#urlformat
    ,'' #N/A
    ,'FSAI' #Type
    )

# #FSAI Allergen Alerts
dictionary('https://www.fsai.ie/news_centre/allergen_alerts.html' #url
    ,'#content' #element
    ,r'<p class="title"><a href="(.*?)">' #urlfinder
    ,r'(?:.html|.aspx\?id=\d{5})">(.*?)</a><br/><em class="emp">' #textfinder
    ,r'</a><br/><em class="emp">(.*?)</em></p><p>' #datefinder
    ,'%A, %d %B %Y' #dateformat
    ,'https://www.fsai.ie/news_centre/allergen_alerts'#urlformat
    ,'' #N/A
    ,'FSAI' #Type
    )

# #FSANZ
dictionary('https://www.foodstandards.gov.au/industry/foodrecalls/recalls/Pages/default.aspx' #url
    ,'#ctl00_ctl45_g_76f28544_b3c4_43f4_b435_13e7b563f7f1 > div:nth-child(2)' #element
    ,r'<a href="(.*?)">' #urlfinder
    ,r'.aspx">(.*?)</a></h3></td></tr>' #textfinder
    ,r': right">(.*?)</div><h3><a href="' #datefinder
    ,'%d/%m/%Y' #dateformat
    ,'https://www.foodstandards.gov.au/'#urlformat
    ,'' #N/A
    ,'FSANZ' #Type
    )

#IFS currently not working
# dictionary('https://www.ifs-certification.com/index.php/en/news' #url
#     ,'#content-main > div:nth-child(3) > div > div.row.col-xs-12.col-xm-12.col-md-12.col-lg-12' #element
#     ,r'href="/news/(.*?)">' #urlfinder
#     ,r'<h4 class="media-heading">\n\t{7}(.*?)                        </h4>' #textfinder
#     ,r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}' #datefinder
#     ,'%B %d, %Y' #dateformat
#     ,'http://brc.org.uk/news/'#urlformat
#     ,'' #dateURLelement
#     ,'IFS' #type
#     )

workbook(d)

import pandas as pd
import os
from scraper import *
from tkinter import *
from frontend import *

scraper = Scraper()

class ButtonFunc(FrontEnd):

    def __init__(self, *args, **kwargs):
        self.root = args[0]
        self.data_list = []
        self.df = pd.DataFrame()
        self.tree = ttk.Treeview(self.root)
        #self.populate_selection()

    def view_command(self,ec_rasff_var, ifsqn_var, fda_var, fsai_var, uk_fsa_var, usda_var, ifs_var, fssc_var, sf360_var, fsanz_var, efsa_var, un_fao_var, cfia_var, gfsi_var, fda_fsma_var, who_var, outp):


        if ec_rasff_var.get() == False:
            self.data_list.append(scraper.ecrasff())

        if ifsqn_var.get() == True:
            self.data_list.append(scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ))

        if fda_var.get() == True:
            self.data_list.append(scraper.convert( #FDA FSMA
                page_div = "tr"
                ,desc_div = "a"
                ,date_div = "td"
                ,loop_begin = 1
                ,date_int = 1
                ,url = ["https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-rules-guidance-industry"]
                ,site_type = "FDA FSMA"
                ,date_formatter = "%Y/%m"
                ))

        if fsai_var.get() == True:
            self.data_list.append(scraper.convert( #FSAI
                class_page = "news-listing"
                ,desc_div = "p"
                ,desc_class = "title"
                ,date_div = "em"
                ,date_class = "emp"
                ,url = ["https://www.fsai.ie/news_centre/food_alerts.html","https://www.fsai.ie/news_centre/allergen_alerts.html"]
                ,site_type = "FSAI"
                ,date_formatter = "%A, %d %B %Y"
                ))

        if uk_fsa_var.get() == True:
            self.data_list.append(scraper.convert( #UK FSA
                class_page = "views-row"
                ,desc_div = "p"
                ,date_div = "span"
                ,date_class = "field field__created"
                ,url = ["https://www.food.gov.uk/news-alerts/search/alerts"]
                ,site_type = "UK FSA"
                ,date_formatter = "%d %B %Y"
                ))

        if usda_var.get() == True:
            self.data_list.append(scraper.convert( #USDA
                page_div = "li"
                ,class_page = "news-releases-item"
                ,desc_div = "a"
                ,date_div = "div"
                ,date_class = "news-release-date"
                ,url = ["https://www.usda.gov/media/press-releases"]
                ,site_type = "USDA"
                ,date_formatter = "%b %d, %Y"
                ))

        if ifs_var.get() == True:
            self.data_list.append(scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ))

        if fssc_var.get() == True:
            self.data_list.append(scraper.convert( #FSSC 22000
                page_div = "a"
                ,class_page = "news-item news-item-archive"
                ,desc_div = "h2"
                ,desc_class = "news-item__title"
                ,date_div = "time"
                ,url = ["https://www.fssc22000.com/news/"]
                ,site_type = "FSSC 22000"
                ,date_formatter = "%d %B %Y"
                ))

        if sf360_var.get() == True:
            self.data_list.append(scraper.convert( #SF360
                page_div = "a"
                ,class_page = "^av-masonry-entry"
                ,desc_div = "h3"
                ,desc_class = "av-masonry-entry-title entry-title"
                ,date_div = "span"
                ,date_class = "av-masonry-date meta-color updated"
                ,url = ["https://safefood360.com/blog/"]
                ,site_type = "SF360"
                ,date_formatter = "%B %d, %Y"
                ))

        if fsanz_var.get() == True:
            self.data_list.append(scraper.fsanzdf("%d/%m/%Y"))

        if efsa_var.get() == True:
            self.data_list.append(scraper.convert( #EFSA
                class_page = "^views-row views-row-"
                ,desc_div = "span"
                ,desc_class = "field-content"
                ,date_div = "span"
                ,date_class = "date-display-single"
                ,url = ["http://www.efsa.europa.eu/en/news"]
                ,site_type = "EFSA"
                ,date_formatter = "%d %B %Y"
                ))

        if un_fao_var.get() == True:
            self.data_list.append(scraper.convert( #FAO
                class_page = "^tx-dynalist-pi1-recordlist tx-dynalist-pi1-recordlist-"
                ,desc_div = "div"
                ,desc_class = "list-subtitle"
                ,date_div = "div"
                ,date_class = "list-date"
                ,url = ["http://www.fao.org/news/archive/news-by-date/2020/en/"]
                ,site_type = "FAO"
                ,date_formatter = "%d-%m-%Y"
                ))

        if cfia_var.get() == True:
            self.data_list.append(scraper.convert( #CFIA
                page_div="tr"
                ,desc_div="td"
                ,date_div="td"
                ,url = ["https://www.inspection.gc.ca/about-cfia/newsroom/food-recall-warnings/eng/1299076382077/1299076493846"]
                ,loop_begin = 1
                ,desc_int = 1
                ,site_type = "CFIA"
                ,date_formatter = "%Y-%m-%d"
                ))

        if gfsi_var.get() == True:
            self.data_list.append(scraper.convert( #GFSI
                class_page = "grid-body"
                ,desc_div = "div"
                ,desc_class = "section-title"
                ,date_div = "div"
                ,date_class = "post-date"
                ,url = ["https://mygfsi.com/news-and-resources/?type=news_updates"]
                ,site_type = "GFSI"
                ,date_formatter = "%d %B %Y"
                ))

        if fda_fsma_var.get() == True:
            self.data_list.append(scraper.convert( #FDA FSMA
                page_div = "tr"
                ,desc_div = "a"
                ,date_div = "td"
                ,loop_begin = 1
                ,date_int = 1
                ,url = ["https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-rules-guidance-industry"]
                ,site_type = "FDA FSMA"
                ,date_formatter = "%Y/%m"
                ))

        if who_var.get() == True:
            self.data_list.append(scraper.convert( #WHO
                class_page = "list-view--item vertical-list-item"
                ,desc_div = "p"
                ,desc_class = "heading text-underline"
                ,date_div = "span"
                ,date_class = "timestamp"
                ,url = ["https://www.who.int/news-room/releases", "https://www.who.int/news-room/releases/2"]
                ,site_type = "WHO"
                ,date_formatter = "%d %B %Y"
                ))

        self.df = pd.concat(self.data_list)

        self.df_to_list(self.df)


    def generate_csv(self):
        os.chdir(r"C:\Users\seang\Desktop\FoodNewsApp\TestDoc")
        self.df.to_csv("news.csv", sep=',', encoding='utf-8')

    def reset(self,outp):
        self.data_list = []
        self.df = pd.DataFrame()
        self.df_to_list(self.df)

    def select_all(self, all_check, outp):
        for a in all_check:
            print(all_check)

    def df_to_list(self,df):
        self.tree.delete(*self.tree.get_children())
        self.df = self.df.reset_index(drop=True)

        self.tree["columns"] = df.columns.values.tolist()
        for x in range(len(df.columns.values)):
            self.tree.column(df.columns.values[x], width=100)
            self.tree.heading(df.columns.values[x], text=df.columns.values[x], command=self.populate_selection)

        for index, row in df.iterrows():
            self.tree.insert("",0,text=index,values=list(row))

        self.tree.grid(row=50,column=0,rowspan=1,columnspan=12,sticky=N+E+W+S)

        self.tree.bind("<<TreeviewSelect>>", self.populate_selection)

    def populate_selection(self,event):
        item = self.tree.selection()
        print("you clicked on", self.tree.item(item,"text"))
        #FrontEnd.desc_tb = "test"

    def add_value_to_df(self,dics):
        self.df = self.df.append(dics, ignore_index=True)
        self.df_to_list(self.df)



if __name__ == "__main__":
    app = ButtonFunc()

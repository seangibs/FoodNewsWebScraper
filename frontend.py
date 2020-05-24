from tkinter import ttk
from tkcalendar import *
from scraper import *
import pandas as pd
from buttonfunctions import *
from functools import partial
from scraper import *
import datetime

scraper = Scraper()

class FrontEnd(object):

    def __init__(self):

        self.window = Tk()

        self.data_list = []
        self.df = pd.DataFrame()
        self.tree = ttk.Treeview(self.window)

        self.window.geometry("1000x600")

        self.window.iconbitmap(self, default = "logo.ico")
        self.window.wm_title("Food News Scraper")

        self.buttons()

        self.window.mainloop()


    def buttons(self):
        """All Check Buttons for sources of news"""
        ##Column 0
        self.ec_rasff_var = BooleanVar(value=1)
        self.ec_rasff = ttk.Checkbutton(self.window, text="EC RASFF", var = self.ec_rasff_var).grid(row=0,column=0,rowspan=1,sticky=W)

        self.ifsqn_var = BooleanVar(value=1)
        self.ifsqn = ttk.Checkbutton(self.window, text="IFSQN", var = self.ifsqn_var).grid(row=1,column=0,rowspan=1,sticky=W)

        self.fda_var = BooleanVar(value=1)
        self.fda = ttk.Checkbutton(self.window, text="FDA", var = self.fda_var).grid(row=2,column=0,rowspan=1,sticky=W)

        self.fsai_var = BooleanVar(value=1)
        self.fsai = ttk.Checkbutton(self.window, text="FSAI", var = self.fsai_var).grid(row=3,column=0,rowspan=1,sticky=W)

        ##Column 1
        self.nz_fsa_var = BooleanVar(value=1)
        self.nz_fsa = ttk.Checkbutton(self.window, text="NZ FSA", var = self.nz_fsa_var).grid(row=0,column=1,rowspan=1,sticky=W)

        self.uk_fsa_var = BooleanVar(value=1)
        self.uk_fsa = ttk.Checkbutton(self.window, text="UK FSA", var = self.uk_fsa_var).grid(row=1,column=1,rowspan=1,sticky=W)

        self.usda_var = BooleanVar(value=1)
        self.usda = ttk.Checkbutton(self.window, text="USDA", var = self.usda_var).grid(row=2,column=1,rowspan=1,sticky=W)

        self.usda_fsis_var = BooleanVar(value=1)
        self.usda_fsis = ttk.Checkbutton(self.window, text="USDA FSIS", var = self.usda_fsis_var).grid(row=3,column=1,rowspan=1,sticky=W)

        ##Column 2
        self.ifs_var = BooleanVar(value=1)
        self.ifs = ttk.Checkbutton(self.window, text="IFS", var = self.ifs_var).grid(row=0,column=2,rowspan=1,sticky=W)

        self.fssc_var = BooleanVar(value=1)
        self.fssc = ttk.Checkbutton(self.window, text="FSSC", var = self.fssc_var).grid(row=1,column=2,rowspan=1,sticky=W)

        self.sf360_var = BooleanVar(value=1)
        self.sf360 = ttk.Checkbutton(self.window, text="SF360", var = self.sf360_var).grid(row=2,column=2,rowspan=1,sticky=W)

        self.brc_var = BooleanVar(value=1)
        self.brc = ttk.Checkbutton(self.window, text="BRC", var = self.brc_var).grid(row=3,column=2,rowspan=1,sticky=W)

        ##Column 3
        self.fsanz_var = BooleanVar(value=1)
        self.fsanz = ttk.Checkbutton(self.window, text="FSANZ", var = self.fsanz_var).grid(row=0,column=3,rowspan=1,sticky=W)

        self.sqf_var = BooleanVar(value=1)
        self.sqf = ttk.Checkbutton(self.window, text="SQF (NA)", var = self.sqf_var).grid(row=1,column=3,rowspan=1,sticky=W)

        self.efsa_var = BooleanVar(value=1)
        self.efsa = ttk.Checkbutton(self.window, text="EFSA", var = self.efsa_var).grid(row=2,column=3,rowspan=1,sticky=W)

        self.un_fao_var = BooleanVar(value=1)
        self.un_fao = ttk.Checkbutton(self.window, text="UN FAO", var = self.un_fao_var).grid(row=3,column=3,rowspan=1,sticky=W)

        ##Column 4
        self.cfia_var = BooleanVar(value=1)
        self.cfia = ttk.Checkbutton(self.window, text="CFIA", var = self.cfia_var).grid(row=0,column=4,rowspan=1,sticky=W)

        self.gfsi_var = BooleanVar(value=1)
        self.gfsi = ttk.Checkbutton(self.window, text="GFSI", var = self.gfsi_var).grid(row=1,column=4,rowspan=1,sticky=W)

        self.fda_fsma_var = BooleanVar(value=1)
        self.fda_fsma = ttk.Checkbutton(self.window, text="FDA FSMA", var = self.fda_fsma_var).grid(row=2,column=4,rowspan=1,sticky=W)

        self.who_var = BooleanVar(value=1)
        self.who = ttk.Checkbutton(self.window, text="WHO", var = self.who_var).grid(row=3,column=4,rowspan=1,sticky=W)

        #Date
        self.min_date_text = ttk.Label(self.window, width = 10, text = "Last Date")
        self.min_date_text.grid(row=5,column=4,rowspan=1,columnspan=1,sticky=W)

        """Users will enter data here"""
        #Category
        self.cat_text = ttk.Label(self.window, width = 10, text = "Category")
        self.cat_text.grid(row=5,column=0,rowspan=1,columnspan=1,sticky=W)

        #list for category drop down
        self.option_list = [
        "News"
        , "Alert"
        , "Recall"
        , "Discussion"
        ]
        self.category_text = StringVar(self.window)
        self.category_text.set(self.option_list[0]) # default value

        self.w = ttk.OptionMenu(self.window, self.category_text, *self.option_list).grid(row=6,column=0,rowspan=1,sticky=W)

        #Date
        self.date_text = ttk.Label(self.window, width = 8, text = "Date")
        self.date_text.grid(row=5,column=1,rowspan=1,columnspan=1,sticky=W)

        #Enter date
        self.date_picker = DateEntry(self.window)
        self.date_picker.grid(row=6,column=1,rowspan=1,sticky=W)

        #Sources
        self.source_list = ["EC RASFF","IFSQN","FDA","FSAI","NZ FSA","UK FSA","USDA","USDA FSIS","IFS","FSSC","SF360","BRC","FSANZ","SQF","EFSA","UN FAO","CFIA","FDA FSMA","UN FAO","EC RAPID","WHO"]
        self.source_text = ttk.Label(self.window, width = 8, text = "Source")
        self.source_text.grid(row=5,column=2,rowspan=1,columnspan=1,sticky=W)
        self.source_variable = StringVar(self.window)

        self.source_variable.set(self.source_list[0]) # default value

        #Description
        self.desc_text = ttk.Label(self.window, width = 12, text = "Description:")
        self.desc_text.grid(row=8,column=0,rowspan=1,columnspan=1,sticky=W)


        self.desc_tb = ttk.Entry(self.window, width = 80)
        self.desc_tb.grid(row=8,column=1,rowspan=1,columnspan=6,sticky=W)

        #URL
        self.url_text = ttk.Label(self.window, width = 12, text = "URL:")
        self.url_text.grid(row=9,column=0,rowspan=1,columnspan=1,sticky=W)

        self.url_tb = ttk.Entry(self.window,width = 80)
        self.url_tb.grid(row=9,column=1,rowspan=1,columnspan=6,sticky=W)

        ttk.OptionMenu(self.window, self.source_variable, *self.source_list).grid(row=6,column=2,rowspan=1,sticky=W)

        """Buttons to interact with the backend"""

        #Generate all news sources selected
        ttk.Button(self.window, width = 12, text = "View All"
            , command = self.view_command).grid(row=0,column=5,rowspan=1,columnspan=1,sticky=W)

        #Export to CSV
        ttk.Button(self.window, width = 12, text = "CSV Export"
            , command = self.generate_csv).grid(row=1,column=5,rowspan=1,columnspan=1,sticky=W)

        #Clear window and dataframe
        ttk.Button(self.window, width = 12, text = "Reset"
            , command = self.reset).grid(row=2,column=5,rowspan=1,columnspan=1,sticky=W)

        #Send the entered data from enter_data to the backend
        ttk.Button(self.window, width = 12, text = "Add"
            , command = self.add_value_to_df).grid(row=3,column=5,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "Delete"
            , command = self.delete_row).grid(row=4,column=5,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "Update"
            , command = self.update_row).grid(row=5,column=5,rowspan=1,columnspan=1,sticky=W)

        #output window
        self.tree["columns"] = ["category","description","link","date","site_type"]
        self.tree.grid(row=15,column=0,rowspan=1,columnspan=12,sticky=W)
        self.tree.bind("<<TreeviewSelect>>", self.populate_selection)

    def view_command(self):

        self.data_list = []

        if self.ec_rasff_var.get() == False:
            self.data_list.append(scraper.ecrasff())

        if self.ifsqn_var.get() == True:
            self.data_list.append(scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ))

        if self.fda_var.get() == True:
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

        if self.fsai_var.get() == True:
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

        if self.uk_fsa_var.get() == True:
            self.data_list.append(scraper.convert( #UK FSA
                class_page = "views-row"
                ,desc_div = "p"
                ,date_div = "span"
                ,date_class = "field field__created"
                ,url = ["https://www.food.gov.uk/news-alerts/search/alerts"]
                ,site_type = "UK FSA"
                ,date_formatter = "%d %B %Y"
                ))

        if self.usda_var.get() == True:
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

        if self.ifs_var.get() == True:
            self.data_list.append(scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ))

        if self.fssc_var.get() == True:
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

        if self.sf360_var.get() == True:
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

        if self.fsanz_var.get() == True:
            self.data_list.append(scraper.fsanzdf("%d/%m/%Y"))

        if self.efsa_var.get() == True:
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

        if self.un_fao_var.get() == True:
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

        if self.cfia_var.get() == True:
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

        if self.gfsi_var.get() == True:
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

        if self.fda_fsma_var.get() == True:
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

        if self.who_var.get() == True:
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
        self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
        self.df = self.df.reset_index(drop=True)

        self.df_to_list(self.df)

    def generate_csv(self):
        os.chdir(r"C:\Users\seang\Desktop\FoodNewsApp\TestDoc")
        self.df.to_csv("news.csv", sep=',', encoding='utf-8')

    def reset(self):
        self.df = pd.DataFrame(columns=["category","description","link","date","site_type"])
        self.tree.delete(*self.tree.get_children())

    def select_all(self, all_check):
        for a in all_check:
            print(all_check)

    def df_to_list(self,df=pd.DataFrame()):
        self.tree.delete(*self.tree.get_children())

        for x in range(len(df.columns.values)):
            self.tree.column(df.columns.values[x], width=100)
            self.tree.heading(df.columns.values[x], text=df.columns.values[x], command=self.populate_selection)

        for index, row in df.iterrows():
            self.tree.insert("",0,text=index,values=list(row))

    def populate_selection(self,event):
        item = self.tree.item(self.tree.focus())
        self.idx_val = self.tree.selection()
        self.selected_item_idx = self.tree.item(self.idx_val,"text")

        self.category_text.set(item["values"][0])

        self.desc_tb.delete(0,END)
        self.desc_tb.insert(0,item["values"][1])

        self.url_tb.delete(0,END)
        self.url_tb.insert(0,item["values"][2])

        #date
        self.date_picker.set_date(datetime.datetime.strptime(item["values"][3], '%Y-%m-%d').date())

        self.source_variable.set(item["values"][4])

    def add_value_to_df(self):
        self.df = self.df.append({"category": self.category_text.get(), "date" : self.date_picker.get_date(), "description": self.desc_tb.get(), "link": self.url_tb.get(), "site_type": self.source_variable.get()}
            , ignore_index=True)
        self.df_to_list(self.df)

    def delete_row(self):
        self.df.drop(int(self.selected_item_idx), inplace=True)
        self.tree.delete(self.idx_val)

    def update_row(self):
        self.delete_row()
        self.add_value_to_df()


if __name__ == "__main__":
    app = FrontEnd()

from tkinter import ttk
from tkinter import *
from tkcalendar import *
from scraper import *
import pandas as pd
from functools import partial
from datetime import date, timedelta
import threading
from multiprocessing import Queue
import os
import smtplib

class FrontEnd(object):

    def __init__(self):

        self.window = Tk()

        self.tree = ttk.Treeview(self.window)

        self.window.geometry("1000x500")

        self.window.iconbitmap(self, default = "logo.ico")
        self.window.wm_title("Food News")

        self.all_var = BooleanVar(value=1)

        #os.chdir(r"C:\Users\seang\Desktop\FoodNewsApp\TestDoc")

        self.buttons()

        self.window.mainloop()



    def buttons(self):
        """All Check Buttons for sources of news"""

        #All
        self.all_check = ttk.Checkbutton(self.window, text="All", var = self.all_var).grid(row=0,column=5,rowspan=1,sticky=W)
        ##Column 0
        self.ec_rasff_var = BooleanVar(value=1)
        self.ec_rasff = ttk.Checkbutton(self.window, text="EC RASFF", var = self.ec_rasff_var).grid(row=0,column=0,rowspan=1,sticky=W)

        self.ifsqn_var = self.all_var
        self.ifsqn = ttk.Checkbutton(self.window, text="IFSQN", var = self.ifsqn_var).grid(row=1,column=0,rowspan=1,sticky=W)

        self.fda_var = self.all_var
        self.fda = ttk.Checkbutton(self.window, text="FDA", var = self.fda_var).grid(row=2,column=0,rowspan=1,sticky=W)

        self.fsai_var = self.all_var
        self.fsai = ttk.Checkbutton(self.window, text="FSAI", var = self.fsai_var).grid(row=3,column=0,rowspan=1,sticky=W)

        ##Column 1
        self.nz_fsa_var = self.all_var
        self.nz_fsa = ttk.Checkbutton(self.window, text="NZ FSA", var = self.nz_fsa_var).grid(row=0,column=1,rowspan=1,sticky=W)

        self.uk_fsa_var = self.all_var
        self.uk_fsa = ttk.Checkbutton(self.window, text="UK FSA", var = self.uk_fsa_var).grid(row=1,column=1,rowspan=1,sticky=W)

        self.usda_var = self.all_var
        self.usda = ttk.Checkbutton(self.window, text="USDA", var = self.usda_var).grid(row=2,column=1,rowspan=1,sticky=W)

        self.usda_fsis_var = self.all_var
        self.usda_fsis = ttk.Checkbutton(self.window, text="USDA FSIS", var = self.usda_fsis_var).grid(row=3,column=1,rowspan=1,sticky=W)

        ##Column 2
        self.ifs_var = self.all_var
        self.ifs = ttk.Checkbutton(self.window, text="IFS", var = self.ifs_var).grid(row=0,column=2,rowspan=1,sticky=W)

        self.fssc_var = self.all_var
        self.fssc = ttk.Checkbutton(self.window, text="FSSC", var = self.fssc_var).grid(row=1,column=2,rowspan=1,sticky=W)

        self.sf360_var = self.all_var
        self.sf360 = ttk.Checkbutton(self.window, text="SF360", var = self.sf360_var).grid(row=2,column=2,rowspan=1,sticky=W)

        self.brc_var = self.all_var
        self.brc = ttk.Checkbutton(self.window, text="BRC", var = self.brc_var).grid(row=3,column=2,rowspan=1,sticky=W)

        ##Column 3
        self.fsanz_var = self.all_var
        self.fsanz = ttk.Checkbutton(self.window, text="FSANZ", var = self.fsanz_var).grid(row=0,column=3,rowspan=1,sticky=W)

        self.sqf_var = self.all_var
        self.sqf = ttk.Checkbutton(self.window, text="SQF (NA)", var = self.sqf_var).grid(row=1,column=3,rowspan=1,sticky=W)

        self.efsa_var = self.all_var
        self.efsa = ttk.Checkbutton(self.window, text="EFSA", var = self.efsa_var).grid(row=2,column=3,rowspan=1,sticky=W)

        self.un_fao_var = self.all_var
        self.un_fao = ttk.Checkbutton(self.window, text="UN FAO", var = self.un_fao_var).grid(row=3,column=3,rowspan=1,sticky=W)

        ##Column 4
        self.cfia_var = self.all_var
        self.cfia = ttk.Checkbutton(self.window, text="CFIA", var = self.cfia_var).grid(row=0,column=4,rowspan=1,sticky=W)

        self.gfsi_var = self.all_var
        self.gfsi = ttk.Checkbutton(self.window, text="GFSI", var = self.gfsi_var).grid(row=1,column=4,rowspan=1,sticky=W)

        self.fda_fsma_var = self.all_var
        self.fda_fsma = ttk.Checkbutton(self.window, text="FDA FSMA", var = self.fda_fsma_var).grid(row=2,column=4,rowspan=1,sticky=W)

        self.who_var = self.all_var
        self.who = ttk.Checkbutton(self.window, text="WHO", var = self.who_var).grid(row=3,column=4,rowspan=1,sticky=W)


        self.min_date_text = ttk.Label(self.window, width = 10, text = "",anchor=E)
        self.min_date_text.grid(row=5,column=7,rowspan=1,columnspan=1,sticky=W)

        #Date
        self.min_date_text = ttk.Label(self.window, width = 10, text = "Last Date",anchor=W)
        self.min_date_text.grid(row=2,column=5,rowspan=1,columnspan=1,sticky=W)

        last_day = str(date.today() - timedelta(days=3)).split("-")
        #Enter date
        self.min_date_picker = DateEntry(self.window, date_pattern="DD/MM/YY", year = int(last_day[0]), month = int(last_day[1]), day = int(last_day[2]))
        self.min_date_picker.grid(row=3,column=5,rowspan=1,sticky=W)

        """Users will enter data here"""
        #Category
        self.cat_text = ttk.Label(self.window, width = 10, text = "Category:")
        self.cat_text.grid(row=6,column=0,rowspan=1,columnspan=1,pady=10,sticky=E)

        #list for category drop down
        self.option_list = [
        "News"
        , "Alert"
        , "Recall"
        , "Discussion"
        ]
        self.category_text = StringVar(self.window)
        self.category_text.set(self.option_list[0]) # default value

        self.w = ttk.OptionMenu(self.window, self.category_text, *self.option_list).grid(row=6,column=1,rowspan=1,sticky=W)

        #Date
        self.date_text = ttk.Label(self.window, width = 8, text = "Date:")
        self.date_text.grid(row=6,column=2,rowspan=1,columnspan=1,pady=5,sticky=E)

        #Enter date
        self.date_picker = DateEntry(self.window,date_pattern="DD/MM/YY")
        self.date_picker.grid(row=6,column=3,rowspan=1,pady=5,sticky=W)

        #Sources
        self.source_list = ["EC RASFF","IFSQN","FDA","FSAI","NZ FSA","UK FSA","USDA","USDA FSIS","IFS","FSSC","SF360","BRC","FSANZ","SQF","EFSA","UN FAO","CFIA","FDA FSMA","UN FAO","EC RAPID","WHO"]
        self.source_text = ttk.Label(self.window, width = 8, text = "Source:")
        self.source_text.grid(row=6,column=4,rowspan=1,columnspan=1,pady=5,sticky=E)
        self.source_variable = StringVar(self.window)

        self.source_variable.set(self.source_list[0]) # default value

        ttk.OptionMenu(self.window, self.source_variable, *self.source_list).grid(row=6,column=5,rowspan=1,sticky=W)

        #Description
        self.desc_text = ttk.Label(self.window, width = 12, text = "Description:")
        self.desc_text.grid(row=8,column=0,rowspan=1,columnspan=1,pady=5,sticky=W)


        self.desc_tb = ttk.Entry(self.window, width = 149)
        self.desc_tb.grid(row=8,column=1,rowspan=1,columnspan=7,sticky=W)

        #URL
        self.url_text = ttk.Label(self.window, width = 8, text = "URL:")
        self.url_text.grid(row=9,column=0,rowspan=1,columnspan=1,pady=5,sticky=W)

        self.url_tb = ttk.Entry(self.window,width = 149)
        self.url_tb.grid(row=9,column=1,rowspan=1,columnspan=7,pady=5,sticky=W)


        """Buttons to interact with the backend"""

        #Generate all news sources selected
        ttk.Button(self.window, width = 12, text = "View All"
            , command = self.view_command).grid(row=0,column=6,rowspan=1,columnspan=1,sticky=W)

        #Send the entered data from enter_data to the backend
        ttk.Button(self.window, width = 12, text = "Add"
            , command = self.add_value_to_df).grid(row=1,column=6,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "Delete"
            , command = self.delete_row).grid(row=3,column=6,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "Update"
            , command = self.update_row).grid(row=2,column=6,rowspan=1,columnspan=1,sticky=W)

        #Clear window and dataframe
        ttk.Button(self.window, width = 12, text = "Reset"
            , command = self.reset).grid(row=0,column=7,rowspan=1,columnspan=1,sticky=W)

        #Export to CSV
        ttk.Button(self.window, width = 12, text = "CSV Export"
            , command = self.generate_csv).grid(row=1,column=7,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "SQL"
            , command = self.generate_SQL).grid(row=2,column=7,rowspan=1,columnspan=1,sticky=W)

        ttk.Button(self.window, width = 12, text = "Email"
            , command = self.generate_SQL).grid(row=3,column=7,rowspan=1,columnspan=1,sticky=W)

        #output window
        self.tree["columns"] = ["category","description","link","date","site_type"]
        self.tree.grid(row=15,column=1,rowspan=1,columnspan=12,sticky=W,pady=10)
        self.tree.column("#0", width=50)
        self.tree.column("#1", width=75)
        self.tree.column("#2", width=310)
        self.tree.column("#3", width=310)
        self.tree.column("#4", width=75)
        self.tree.column("#5", width=75)
        self.tree.bind("<<TreeviewSelect>>", self.populate_selection)

        self.scraper = Scraper()

    def view_command(self):

        # self.popup_bonus()

        # self.progress["value"] = 50

        # self.list_vars = [
        #  self.ec_rasff_var.get()
        # ,self.ifsqn_var.get()
        # ,self.fda_var.get()
        # ,self.fsai_var.get()
        # ,self.uk_fsa_var.get()
        # ,self.usda_var.get()
        # ,self.ifs_var.get()
        # ,self.fssc_var.get()
        # ,self.sf360_var.get()
        # ,self.fsanz_var.get()
        # ,self.efsa_var.get()
        # ,self.un_fao_var.get()
        # ,self.cfia_var.get()
        # ,self.gfsi_var.get()
        # ,self.fda_fsma_var.get()
        # ,self.who_var.get()]

        self.data_list = []

        if self.ec_rasff_var.get() == True:
            self.data_list.append(self.scraper.ecrasff())

        if self.ifsqn_var.get() == True:
            self.data_list.append(self.scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.fda_var.get() == True:
            self.data_list.append(self.scraper.convert( #FDA FSMA
                page_div = "tr"
                ,desc_div = "a"
                ,date_div = "td"
                ,loop_begin = 1
                ,date_int = 1
                ,url = ["https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-rules-guidance-industry"]
                ,site_type = "FDA FSMA"
                ,date_formatter = "%Y/%m"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.fsai_var.get() == True:
            self.data_list.append(self.scraper.convert( #FSAI
                class_page = "news-listing"
                ,desc_div = "p"
                ,desc_class = "title"
                ,date_div = "em"
                ,date_class = "emp"
                ,url = ["https://www.fsai.ie/news_centre/food_alerts.html","https://www.fsai.ie/news_centre/allergen_alerts.html"]
                ,site_type = "FSAI"
                ,date_formatter = "%A, %d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.uk_fsa_var.get() == True:
            self.data_list.append(self.scraper.convert( #UK FSA
                class_page = "views-row"
                ,desc_div = "p"
                ,date_div = "span"
                ,date_class = "field field__created"
                ,url = ["https://www.food.gov.uk/news-alerts/search/alerts"]
                ,site_type = "UK FSA"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.usda_var.get() == True:
            self.data_list.append(self.scraper.convert( #USDA
                page_div = "li"
                ,class_page = "news-releases-item"
                ,desc_div = "a"
                ,date_div = "div"
                ,date_class = "news-release-date"
                ,url = ["https://www.usda.gov/media/press-releases"]
                ,site_type = "USDA"
                ,date_formatter = "%b %d, %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.ifs_var.get() == True:
            self.data_list.append(self.scraper.convert( #IFS
                class_page = "well"
                ,desc_div = "h4"
                ,desc_class = "media-heading"
                ,date_div = "h5"
                ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                ,site_type = "IFS"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.fssc_var.get() == True:
            self.data_list.append(self.scraper.convert( #FSSC 22000
                page_div = "a"
                ,class_page = "news-item news-item-archive"
                ,desc_div = "h2"
                ,desc_class = "news-item__title"
                ,date_div = "time"
                ,url = ["https://www.fssc22000.com/news/"]
                ,site_type = "FSSC 22000"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.sf360_var.get() == True:
            self.data_list.append(self.scraper.convert( #SF360
                page_div = "a"
                ,class_page = "^av-masonry-entry"
                ,desc_div = "h3"
                ,desc_class = "av-masonry-entry-title entry-title"
                ,date_div = "span"
                ,date_class = "av-masonry-date meta-color updated"
                ,url = ["https://safefood360.com/blog/"]
                ,site_type = "SF360"
                ,date_formatter = "%B %d, %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.fsanz_var.get() == True:
            self.data_list.append(self.scraper.fsanzdf("%d/%m/%Y"
                ,mn_date = self.min_date_picker.get_date()))

        if self.efsa_var.get() == True:
            self.data_list.append(self.scraper.convert( #EFSA
                class_page = "^views-row views-row-"
                ,desc_div = "span"
                ,desc_class = "field-content"
                ,date_div = "span"
                ,date_class = "date-display-single"
                ,url = ["http://www.efsa.europa.eu/en/news"]
                ,site_type = "EFSA"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.un_fao_var.get() == True:
            self.data_list.append(self.scraper.convert( #FAO
                class_page = "^tx-dynalist-pi1-recordlist tx-dynalist-pi1-recordlist-"
                ,desc_div = "div"
                ,desc_class = "list-subtitle"
                ,date_div = "div"
                ,date_class = "list-date"
                ,url = ["http://www.fao.org/news/archive/news-by-date/2020/en/"]
                ,site_type = "UN FAO"
                ,date_formatter = "%d-%m-%Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.cfia_var.get() == True:
            self.data_list.append(self.scraper.convert( #CFIA
                page_div="tr"
                ,desc_div="td"
                ,date_div="td"
                ,url = ["https://www.inspection.gc.ca/about-cfia/newsroom/food-recall-warnings/eng/1299076382077/1299076493846"]
                ,loop_begin = 1
                ,desc_int = 1
                ,site_type = "CFIA"
                ,date_formatter = "%Y-%m-%d"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.gfsi_var.get() == True:
            self.data_list.append(self.scraper.convert( #GFSI
                class_page = "grid-body"
                ,desc_div = "div"
                ,desc_class = "section-title"
                ,date_div = "div"
                ,date_class = "post-date"
                ,url = ["https://mygfsi.com/news-and-resources/?type=news_updates"]
                ,site_type = "GFSI"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.fda_fsma_var.get() == True:
            self.data_list.append(self.scraper.convert( #FDA FSMA
                page_div = "tr"
                ,desc_div = "a"
                ,date_div = "td"
                ,loop_begin = 1
                ,date_int = 1
                ,url = ["https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-rules-guidance-industry"]
                ,site_type = "FDA FSMA"
                ,date_formatter = "%Y/%m"
                ,mn_date = self.min_date_picker.get_date()
                ))

        if self.who_var.get() == True:
            self.data_list.append(self.scraper.convert( #WHO
                class_page = "list-view--item vertical-list-item"
                ,desc_div = "p"
                ,desc_class = "heading text-underline"
                ,date_div = "span"
                ,date_class = "timestamp"
                ,url = ["https://www.who.int/news-room/releases", "https://www.who.int/news-room/releases/2"]
                ,site_type = "WHO"
                ,date_formatter = "%d %B %Y"
                ,mn_date = self.min_date_picker.get_date()
                ))

        self.df = pd.concat(self.data_list)
        #self.df.loc[self.df["date"] < self.min_date]
        self.df["date"] = pd.to_datetime(self.df["date"]).dt.date
        self.df = self.df.reset_index(drop=True)

        self.df_to_list(self.df)

    def generate_csv(self):
        self.df.to_csv("news.csv", sep=',', encoding='utf-8')

    def reset(self):
        self.df = pd.DataFrame(columns=["category","description","link","date","site_type"])
        self.tree.delete(*self.tree.get_children())
        self.buttons()

    def select_all(self, all_check):
        for a in all_check:
            print(all_check)

    def df_to_list(self,df=pd.DataFrame()):
        self.tree.delete(*self.tree.get_children())

        for x in range(len(df.columns.values)):
            self.tree.column(df.columns.values[x])
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
        self.date_picker.set_date(datetime.strptime(item["values"][3], '%Y-%m-%d').date())

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

    def generate_SQL(self):

        category_type = {"News": "DE0DD814-8CCC-4F38-9924-1D7A1A257D48"
                        ,"Alert": "CE165EF9-2D89-42B5-9EB3-E1196225A9B7"
                        ,"Recall": "073E446D-84CC-4C40-9922-BC48898726A2"
                        ,"Discussion": "FE6CC9C2-1F2F-41DA-9547-693BB4BA61CA"}

        source_type = {
        'IFSQN':'0E129162-030F-43C4-9F3D-609A146A7BFA',
        'FSCE':'BE6EED10-079B-4FB3-815E-A6CDFA8CC31D',
        'SQF':'1FEACA53-19A6-473C-98D2-00C3535DE7C4',
        'IFS':'E1AA9E92-1107-4CB3-A052-0498C3322802',
        'FSSC 22000':'8840EC90-9186-418A-B060-4B5173A730DB',
        'GFSI':'2F26F9C7-EEA9-454C-A41E-79DD9AEBDE31',
        'BRC':'3454B23F-E34D-47DF-97D5-D1A31B5CFF66',
        'UN FAO':'28BAC28E-6D8B-4707-BFC2-B9D0ABAB8C82',
        'USDA':'194F4AA5-97BB-4F36-AA44-8345C26099EA',
        'SF360':'78B17D62-5EA7-4CDE-A76D-D4F00CF9D4B2',
        'EC RASFF':'0CA8198E-9B92-41C3-8C97-04BC1F1CA598',
        'NZ FSA':'4ABBB59C-2CD0-4493-B1D4-1792D23EBDC8',
        'FSANZ':'05895459-9E56-4272-AD12-4A6844EC0055',
        'CFIA':'54870791-4C4A-473F-84F3-67D30EA89267',
        'FSAI':'32CE7204-7371-442E-9C4E-A9FA855110B2',
        'UK FSA':'008D8F2F-3F0D-44A8-8CEE-E095586F26F9',
        'FDA':'3B297E74-A318-46C5-B7C9-E7C19794CF42',
        'USDA FSIS':'F38A450B-067B-4907-862C-F784D1E9D04B',
        'WHO':'DFB8B3B0-59C6-42A8-BA36-EC5EB4CF5702',
        'EC RAPID':'5805502D-889B-4881-AC4B-0C614BE37576',
        'FDA FSMA':'CA06295F-1627-4917-9A9A-339C33A86962',
        'EFSA':'8FDE2DB5-CA8F-448F-8A60-080D19F8A0E9',
        'Trello Food Safety':'5C90970F-FCA3-4CD8-8CCB-E7966F9657D0'}


        text_file = open("INSERTS.sql", "w")

        i = 1
        for row in self.df.itertuples():
            if i == len(self.df):
                return
            try:
                cat = category_type.get(str(row[1]))
            except:
                cat = str(row[1])

            try:
                source = source_type.get(str(row[5]))
            except:
                source = str(row[5])

            text_file.write("\n,(NEWID(),'"+
                cat+"','"+str(row[2])+"','"+str(row[3])+"','"+str(row[4])+"','"+source+"'')")

            i+=1

        text_file.close()

    def view_thread(self):
        # self.win = Toplevel()
        # self.win.wm_title("Window")

        # self.l = Label(self.win, text="Input")
        # self.l.grid(row=0, column=0)

        # self.b = ttk.Button(self.win, text="Okay", command=self.win.destroy)
        # self.b.grid(row=1, column=0)

        # self.progress = ttk.Progressbar(self.window,orient="horizontal", length = 200, mode = "determinate")
        # self.progress.grid(row=5,column=0,rowspan=1,columnspan=1,pady=10,sticky=W)

        # # self.submit_thread
        # self.submit_thread = threading.Thread(target=self.buttons)
        # self.submit_thread.daemon = True
        # self.progress.start()
        # self.submit_thread.start()
        # self.window.after(20, self.check_submit_thread)
        #self.q = Queue()
        self.buttons()
        # self.w1 = threading.Thread(target = self.buttons)
        # self.w1.start()

    def check_submit_thread(self):
        if self.submit_thread.is_alive():
            self.window.after(20, self.check_submit_thread)
        else:
            self.progress.stop()



if __name__ == "__main__":
    app = FrontEnd()

from tkinter import ttk,filedialog,font
from tkinter import *
from tkcalendar import *
from scraper import *
import pandas as pd
from functools import partial
from datetime import date, timedelta
import threading
import time
from PIL import Image, ImageTk
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class FrontEnd(object):

    def __init__(self):

        self.window = Tk()

        s1 = ttk.Style(self.window)

        s1.configure('Red.TCheckbutton', font=("Arial", 11))

        s1.configure('my.TButton', font=("Arial", 11, "bold"))

        window_height = 648
        window_width = 1050
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        style = ttk.Style(self.window)
        style.configure('Treeview', rowheight=31)
        self.tree = ttk.Treeview(self.window)

        self.window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        self.window.iconbitmap(self, default = "img\\logo.ico")
        self.window.wm_title("Food News - BETA")

        self.all_var = BooleanVar(value=0)
        self.df = pd.DataFrame(columns=["Category","Description","Link","Date","Source"])

        self.from_email = ""
        self.to_email = ""
        self.from_pw = ""

        self.buttons()

        self.window.mainloop()

    def all_select(self):
        for item in self.source_var:
            item.set(self.all_var.get())

    def buttons(self):
        """Display Buttons & Output Window"""
        #List of checkbutton text
        self.source_list = ["EC RASFF","IFSQN","FDA","FSAI","UK FSA","USDA","IFS","FSSC","SF360","FSANZ","EFSA","CFIA","GFSI","FDA FSMA","WHO","NZ FSA","USDA FSIS","BRC","SQF","UN FAO"]
        # #The variable for each text button which will be used later in the script to determine which method to call e.g. if self.source_var[i].get() == True: do something
        self.source_var = []

        ttk.Checkbutton(self.window, text = "All", var = self.all_var, command = self.all_select,style = "Red.TCheckbutton").grid(row=0,column=0,sticky=W)

        j = 0
        k = 1

        #loop to create checkbttons
        for i in range(len(self.source_list)):
            self.var = BooleanVar(value=0)
            self.source_var.append(self.var) #add var to list
            check_but = ttk.Checkbutton(self.window, text = self.source_list[i], var = self.source_var[i],style = "Red.TCheckbutton")
            check_but.grid(row=k,column=j,pady=2,columnspan=1,sticky=W)
            #check_but.configure(font=("Arial", 9,"bold"))
            k += 1
            #new column
            if k == 4:
                k = 0
                j += 1

        #Dictionary for checking variable state later
        self.source_dict = dict(zip(self.source_list,self.source_var))


        ttk.Label(self.window, width = 10, text = "",anchor=E).grid(row=5,column=12,rowspan=1,columnspan=1,sticky=W,pady=20)


        #Date
        self.min_date_text = ttk.Label(self.window, width = 10, text = "Last Date",anchor=W)
        self.min_date_text.grid(row=2,column=5,rowspan=1,columnspan=1,sticky=W)

        self.min_date_text.configure(font=("Arial", 10,"bold"))


        last_day = str(date.today() - timedelta(days=3)).split("-")
        #Enter date
        self.min_date_picker = DateEntry(self.window, date_pattern="DD/MM/YY", year = int(last_day[0]), month = int(last_day[1]), day = int(last_day[2]))
        self.min_date_picker.grid(row=3,column=5,rowspan=1,sticky=W)

        """Users will enter data here"""
        #Category
        self.cat_text = ttk.Label(self.window, width = 10, text = "Category:")
        self.cat_text.grid(row=6,column=0,rowspan=1,columnspan=1,pady=5,sticky=W,padx=(10,1))

        self.cat_text.configure(font=("Arial", 10,"bold"))

        #list for Category drop down
        self.option_list = [
        "News"
        , "Alert"
        , "Recall"
        , "Discussion"
        ]
        self.category_text = StringVar(self.window)
        self.category_text.set(self.option_list[0]) # default value

        self.w = ttk.OptionMenu(self.window, self.category_text, *self.option_list).grid(row=6,column=1,rowspan=1,columnspan=2,sticky=W)

        #Date
        self.date_text = ttk.Label(self.window, width = 8, text = "Date:")
        self.date_text.grid(row=6,column=2,rowspan=1,columnspan=1,pady=5,sticky=E)
        self.date_text.configure(font=("Arial", 10,"bold"))

        #Enter date
        self.date_picker = DateEntry(self.window,date_pattern="DD/MM/YY")
        self.date_picker.grid(row=6,column=3,rowspan=1,columnspan=2,sticky=W)

        #Sources
        self.source_text = ttk.Label(self.window, width = 8, text = "Source:")
        self.source_text.grid(row=6,column=4,rowspan=1,columnspan=1,pady=5,sticky=E)
        self.source_text.configure(font=("Arial", 10,"bold"))
        self.source_variable = StringVar(self.window)

        self.source_variable.set(self.source_list[0]) # default value

        ttk.OptionMenu(self.window, self.source_variable, *self.source_list).grid(row=6,column=5,rowspan=1,sticky=W)

        #Description
        self.desc_text = ttk.Label(self.window, width = 15, text = "Description:")
        self.desc_text.grid(row=8,column=0,rowspan=1,columnspan=1,pady=5,sticky=W,padx=(10,1))
        self.desc_text.configure(font=("Arial", 10,"bold"))


        self.desc_tb = ttk.Entry(self.window, width = 149)
        self.desc_tb.grid(row=8,column=1,rowspan=1,columnspan=7,sticky=W)

        #URL
        self.url_text = ttk.Label(self.window, width = 15, text = "URL:")
        self.url_text.grid(row=9,column=0,rowspan=1,columnspan=1,padx=(10,1),sticky=W)
        self.url_text.configure(font=("Arial", 10,"bold"))

        self.url_tb = ttk.Entry(self.window,width = 149)
        self.url_tb.grid(row=9,column=1,rowspan=1,columnspan=7,pady=5,sticky=W)


        """Buttons to interact with the backend"""
        width = 15
        height = 15
        img = Image.open("img\\view.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.view_img =  ImageTk.PhotoImage(img)
        #Generate all news sources selected
        self.view_button = ttk.Button(self.window, width = 12, text = "  View All  ", image = self.view_img, compound="left", style='my.TButton'
            , command = self.view_thread)

        self.view_button.grid(row=0,column=6,rowspan=1,columnspan=1,sticky=W)

        #Send the entered data from enter_data to the backend

        img = Image.open("img\\add.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.add_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   Add        ", image = self.add_img, compound=LEFT, style='my.TButton'
            , command = self.add_value_to_df).grid(row=1,column=6,rowspan=1,columnspan=1,sticky=W)

        img = Image.open("img\\delete.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.delete_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   Delete    ", image = self.delete_img, compound=LEFT, style='my.TButton'
            , command = self.delete_row).grid(row=3,column=6,rowspan=1,columnspan=1,sticky=W)

        img = Image.open("img\\update.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.update_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   Update  ", image = self.update_img, compound=LEFT, style='my.TButton'
            , command = self.update_row).grid(row=2,column=6,rowspan=1,columnspan=1,sticky=W)

        #Clear window and dataframe
        img = Image.open("img\\reset.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.reset_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   Reset     ", image = self.reset_img, compound=LEFT, style='my.TButton'
            , command = self.reset).grid(row=0,column=7,rowspan=1,columnspan=1,sticky=W)

        #Export to CSV
        img = Image.open("img\\csv.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.csv_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   CSV       ", image = self.csv_img, compound=LEFT, style='my.TButton'
            , command = self.generate_csv).grid(row=1,column=7,rowspan=1,columnspan=1,sticky=W)

        #SQL Export
        img = Image.open("img\\sql.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.sql_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   SQL       ", image = self.sql_img, compound=LEFT, style='my.TButton'
            , command = self.generate_SQL).grid(row=2,column=7,rowspan=1,columnspan=1,sticky=W)


        #Email
        img = Image.open("img\\emailim.gif")
        img = img.resize((width,height), Image.ANTIALIAS)
        self.email_img =  ImageTk.PhotoImage(img)
        ttk.Button(self.window, width = 12, text = "   Email     ", image = self.email_img, compound=LEFT, style='my.TButton'
            , command = self.send_email).grid(row=3,column=7,rowspan=1,columnspan=1,sticky=W)

        #output window
        self.tree["columns"] = ["Category","Description","Link","Date","Source"]
        self.tree.grid(row=15,column=1,rowspan=1,columnspan=12,sticky=W,pady=10)
        self.tree.column("#0", width=50)
        self.tree.column("#1", width=75)
        self.tree.column("#2", width=310)
        self.tree.column("#3", width=310)
        self.tree.column("#4", width=75)
        self.tree.column("#5", width=75)
        self.tree.bind("<<TreeviewSelect>>", self.populate_selection)

    def view_thread(self):

        self.view_button.config(state=DISABLED)
        self.t1 = threading.Thread(target=self.view_command)
        self.t1.setDaemon(True)
        self.t1.start()
        self.pop_up()
        # while t1:
        #     print("terst")

    def pop_up(self):
        self.win=Tk()

        window_height = 185
        window_width = 300
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        self.win.wm_title("Loading...")
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.win.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


        self.status_text = ttk.Label(self.win, text = "Initializing...")
        self.status_text.config(font=("Arial", 15))
        self.status_text.pack()


        space_label = ttk.Label(self.win, text = "")
        space_label.config(font=("Arial", 15))
        #space_label.config(bg="#3a8cae")
        space_label.pack()

        self.ascii_status = ttk.Label(self.win, text = "Initializing...")
        self.ascii_status.config(font=("Arial", 20))
        self.ascii_status.pack()

        blank_text = ttk.Label(self.win, text = "")
        blank_text.config(font=("Arial", 15))
        blank_text.pack()

        s = ttk.Style(self.win)
        s.theme_use('winnative')
        s.configure("red.Horizontal.TProgressbar", troughcolor ='#606a71', background='#559363')
        #s.configure(bg="red")

        self.progress=ttk.Progressbar(self.win,orient=HORIZONTAL,length=250,mode='determinate',style="red.Horizontal.TProgressbar")
        #self.progress.configure(background="red")
        self.progress.pack()

        #screen_text = "Loading data for: " + ", ".join([name for name, val in self.source_dict.items() if val.get() == True])
        self.num_selected = 0
        for name, val in self.source_dict.items():
            if val.get() == True:
                self.num_selected += 1
                if self.num_selected == 16:
                    break   #only 16 currently work as of 09/06 so will have to update this in the future

        #print(self.num_selected)
        #ttk.Label(self.win, text = screen_text).pack()

        self.win.mainloop()

    def close_pop_up(self):

        self.view_button.config(state=NORMAL)
        self.win.destroy()

    def view_command(self):

        self.scraper = Scraper(self.min_date_picker.get_date())

        self.data_list = []
        current_progress = 0

        for v in self.source_var:

            if v.get():

                if self.source_dict.get("EC RASFF").get() == True:
                    self.status_text["text"] = "Loading EC RASFF..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.ecrasff())
                    self.status_text["text"] = "Loading EC RASFF"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("IFSQN").get() == True:
                    self.status_text["text"] = "Loading IFSQN..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.ifsqn( #IFSQN
                        ))
                    self.status_text["text"] = "Finished IFSQN!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("FDA").get() == True:
                    self.status_text["text"] = "Loading IFSQN..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.fda( #FDA FSMA
                        ))
                    self.status_text["text"] = "Finished FDA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("FSAI").get() == True:
                    self.status_text["text"] = "Loading FSAI..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #FSAI
                        class_page = "news-listing"
                        ,desc_div = "p"
                        ,desc_class = "title"
                        ,date_div = "em"
                        ,date_class = "emp"
                        ,url = ["https://www.fsai.ie/news_centre/food_alerts.html","https://www.fsai.ie/news_centre/allergen_alerts.html"]
                        ,Source = "FSAI"
                        ,date_formatter = "%A, %d %B %Y"
                        ))
                    self.status_text["text"] = "Finished FSAI!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("UK FSA").get() == True:
                    self.status_text["text"] = "Loading UK FSA..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #UK FSA
                        class_page = "views-row"
                        ,desc_div = "p"
                        ,date_div = "span"
                        ,date_class = "field field__created"
                        ,url = ["https://www.food.gov.uk/news-alerts/search/alerts"]
                        ,Source = "UK FSA"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] = "Finished UK FSA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("USDA").get() == True:
                    self.status_text["text"] = "Loading USDA..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #USDA
                        page_div = "li"
                        ,class_page = "news-releases-item"
                        ,desc_div = "a"
                        ,date_div = "div"
                        ,date_class = "news-release-date"
                        ,url = ["https://www.usda.gov/media/press-releases"]
                        ,Source = "USDA"
                        ,date_formatter = "%b %d, %Y"
                        ))
                    self.status_text["text"] = "Finished UK FSA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("IFS").get() == True:
                    self.status_text["text"] = "Loading IFS..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #IFS
                        class_page = "well"
                        ,desc_div = "h4"
                        ,desc_class = "media-heading"
                        ,date_div = "h5"
                        ,url = ["https://www.ifs-certification.com/index.php/en/news"]
                        ,Source = "IFS"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] = "Finished IFS!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("FSSC").get() == True:
                    self.status_text["text"] = "Loading FSSC..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #FSSC 22000
                        page_div = "a"
                        ,class_page = "news-item news-item-archive"
                        ,desc_div = "h2"
                        ,desc_class = "news-item__title"
                        ,date_div = "time"
                        ,url = ["https://www.fssc22000.com/news/"]
                        ,Source = "FSSC 22000"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] ="Finished FSSC!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("SF360").get() == True:
                    self.status_text["text"] = "Loading SF360..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #SF360
                        page_div = "a"
                        ,class_page = "^av-masonry-entry"
                        ,desc_div = "h3"
                        ,desc_class = "av-masonry-entry-title entry-title"
                        ,date_div = "span"
                        ,date_class = "av-masonry-date meta-color updated"
                        ,url = ["https://safefood360.com/blog/"]
                        ,Source = "SF360"
                        ,date_formatter = "%B %d, %Y"
                        ))
                    self.status_text["text"] = "Finished SF360!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("FSANZ").get() == True:
                    self.status_text["text"] = "Loading FSANZ..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.fsanzdf("%d/%m/%Y"))
                    self.status_text["text"] = "Finished FSANZ!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("EFSA").get() == True:
                    self.status_text["text"] = "Loading EFSA..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #EFSA
                        class_page = "^views-row views-row-"
                        ,desc_div = "span"
                        ,desc_class = "field-content"
                        ,date_div = "span"
                        ,date_class = "date-display-single"
                        ,url = ["http://www.efsa.europa.eu/en/news"]
                        ,Source = "EFSA"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] = "Finished EFSA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("UN FAO").get() == True:
                    self.status_text["text"] = "Loading UN FAO..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #FAO
                        class_page = "^tx-dynalist-pi1-recordlist tx-dynalist-pi1-recordlist-"
                        ,desc_div = "div"
                        ,desc_class = "list-subtitle"
                        ,date_div = "div"
                        ,date_class = "list-date"
                        ,url = ["http://www.fao.org/news/archive/news-by-date/2020/en/"]
                        ,Source = "UN FAO"
                        ,date_formatter = "%d-%m-%Y"
                        ))
                    self.status_text["text"] = "Finished UN FAO!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("CFIA").get() == True:
                    self.status_text["text"] = "Loading CFIA.."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #CFIA
                        page_div="tr"
                        ,desc_div="td"
                        ,date_div="td"
                        ,url = ["https://www.inspection.gc.ca/about-cfia/newsroom/food-recall-warnings/eng/1299076382077/1299076493846"]
                        ,loop_begin = 1
                        ,desc_int = 1
                        ,Source = "CFIA"
                        ,date_formatter = "%Y-%m-%d"
                        ))
                    self.status_text["text"] = "Finished CFIA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("GFSI").get() == True:
                    self.status_text["text"] = "Loading GFSI..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #GFSI
                        class_page = "grid-body"
                        ,desc_div = "div"
                        ,desc_class = "section-title"
                        ,date_div = "div"
                        ,date_class = "post-date"
                        ,url = ["https://mygfsi.com/news-and-resources/?type=news_updates"]
                        ,Source = "GFSI"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] = "Finished GFSI!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("FDA FSMA").get() == True:
                    self.status_text["text"] = "Loading FDA FSMA..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #FDA FSMA
                        page_div = "tr"
                        ,desc_div = "a"
                        ,date_div = "td"
                        ,loop_begin = 1
                        ,date_int = 1
                        ,url = ["https://www.fda.gov/food/food-safety-modernization-act-fsma/fsma-rules-guidance-industry"]
                        ,Source = "FDA FSMA"
                        ,date_formatter = "%Y/%m"
                        ))
                    self.status_text["text"] = "Finished FDA FSMA!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)

                if self.source_dict.get("WHO").get() == True:
                    self.status_text["text"] = "Loading WHO..."
                    self.ascii_status["text"] = "♒((⇀‸↼))♒"
                    self.data_list.append(self.scraper.convert( #WHO
                        class_page = "list-view--item vertical-list-item"
                        ,desc_div = "p"
                        ,desc_class = "heading text-underline"
                        ,date_div = "span"
                        ,date_class = "timestamp"
                        ,url = ["https://www.who.int/news-room/releases", "https://www.who.int/news-room/releases/2"]
                        ,Source = "WHO"
                        ,date_formatter = "%d %B %Y"
                        ))
                    self.status_text["text"] = "Finished WHO!"
                    self.ascii_status["text"] = "＼(＾O＾)／"
                    current_progress = current_progress + (100 / self.num_selected)
                    self.progress["value"] = current_progress
                    time.sleep(0.5)


                try:
                    logging.info("Creating DataFrame")
                    self.df = pd.concat(self.data_list)
                    self.df = self.df.reset_index(drop=True).drop_duplicates(subset=None, keep="first", inplace=False)
                    self.df["Description"] = self.df["Description"].str.capitalize()
                    self.df_to_list(self.df)

                except:
                    logging.warning("Could not create dataframe")

                self.close_pop_up()
                return


        logging.info("No option selected")
        self.close_pop_up()
        return

    def generate_csv(self):
        self.save_file(str(self.df),".txt")

    def reset(self):
        self.df = pd.DataFrame(columns=["Category","Description","Link","Date","Source"])
        self.tree.delete(*self.tree.get_children())
        #self.buttons()

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
        self.url_text.bind("<Button-1>", lambda e:  webbrowser.open_new(item["values"][2]))
        self.url_text.configure(font=("Arial", 9))
        self.url_text.configure(underline = True)
        self.url_text.configure(foreground="#3a8cae")


        #date
        self.date_picker.set_date(datetime.strptime(item["values"][3], '%Y-%m-%d').date())

        self.source_variable.set(item["values"][4])

    def add_value_to_df(self):
        self.df = self.df.append({"Category": self.category_text.get(), "Date" : self.date_picker.get_date(), "Description": self.desc_tb.get(), "Link": self.url_tb.get(), "Source": self.source_variable.get()}
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

        text_file = []
        i = 1
        for row in self.df.itertuples():
            try:
                cat = category_type.get(str(row[1]))
            except:
                cat = str(row[1])

            try:
                source = source_type.get(str(row[5]))
            except:
                source = str(row[5])

            if i == 1:
                begin_comma = "INSERT INTO UPDATETABLE VALUES \n"
            else:
                begin_comma = ","

            text_file.append(begin_comma + "(NEWID(),'"+
                cat+"','"+str(row[2]).replace("'","''")+"','"+str(row[3])+"','"+str(row[4])+"','"+source+"')")

            i+=1

        self.save_file(text_file,"SQL")

    def save_file(self,file_to_save,file_type):
        if file_type == "SQL":
            filetypes=(("SQL file", "*.sql"),("Text file", "*.txt"))
            defaultextension="*.sql"

        else:
            filetypes=(("CSV file", "*.csv"),("Text file", "*.txt"))
            defaultextension="*.csv"

        file = filedialog.asksaveasfile(filetypes=filetypes,defaultextension=defaultextension)
        if file:
            if file_type == "SQL":
                for item in file_to_save:
                    file.write(item)
                    file.write("\n")
                self.sql_path = file.name
                file.close()

            else:
                self.df.to_csv(file, index=False)
                self.csv_path = file.name

    def check_submit_thread(self):
        if self.submit_thread.is_alive():
            self.window.after(20, self.check_submit_thread)
        else:
            self.progress.stop()

    def send_email(self):
        msg = MIMEMultipart()
        msg['Subject'] = "SF360 :: Task :: Dashboard Updates"
        msg['From'] = self.from_email
        msg['To'] = self.to_email
        msg_text = "Hi Support,\n\nCan you please complete the dashboard updates as per the attached files?\n\nThank you,\nFood News App \n\nThis task of Dashboard Updates has been assigned a SOC 2 risk of minor as per the document: https://go.safefood360.com/MasterData/DocumentControl/ViewDocument/4da849b1-db55-4558-9022-ab7200b32ccc"

        attachment_path_list = [self.csv_path,self.sql_path]

        for each_file_path in attachment_path_list:
            #try:
            file_name=each_file_path.split("/")[-1]
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(each_file_path, "rb").read())

            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment" ,filename=file_name)
            msg.attach(part)
            #except:
                #print("could not attache file")

        msg.attach(MIMEText(msg_text))

        mailserver = smtplib.SMTP('smtp.office365.com',587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(self.from_email,self.from_pw)
        mailserver.sendmail(msg['From'],msg['To'],msg.as_string())
        mailserver.quit()


if __name__ == "__main__":
    app = FrontEnd()

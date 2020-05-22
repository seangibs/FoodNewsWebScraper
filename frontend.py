from tkinter import *
from tkcalendar import *
from scraper import *
import pandas as pd
from buttonfunctions import *
from functools import partial

bf = ButtonFunc()

class FrontEnd(object):

    def __init__(self):


        self.window = Tk()

        self.window.geometry("800x400")

        self.source_list = ["EC RASFF","IFSQN","FDA","FSAI","NZ FSA","UK FSA","USDA","USDA FSIS","IFS","FSSC","SF360","BRC","FSANZ","SQF","EFSA","UN FAO","CFIA","FDA FSMA","UN FAO","EC RAPID","WHO"]

        self.check_buttons()
        self.last_date()
        self.last_date()
        self.entry_data_labels()
        self.entry_data()
        self.output_window()
        self.buttons()


        self.window.mainloop()


    def check_buttons(self):
        ##Column 0
        self.ec_rasff_var = BooleanVar(value=1)
        self.ec_rasff = Checkbutton(self.window, text="EC RASFF", var = self.ec_rasff_var).grid(row=0,column=0,rowspan=1,sticky=W)

        self.ifsqn_var = BooleanVar(value=1)
        self.ifsqn = Checkbutton(self.window, text="IFSQN", var = self.ifsqn_var).grid(row=1,column=0,rowspan=1,sticky=W)

        self.fda_var = BooleanVar(value=1)
        self.fda = Checkbutton(self.window, text="FDA", var = self.fda_var).grid(row=2,column=0,rowspan=1,sticky=W)

        self.fsai_var = BooleanVar(value=1)
        self.fsai = Checkbutton(self.window, text="FSAI", var = self.fsai_var).grid(row=3,column=0,rowspan=1,sticky=W)

        ##Column 1
        self.nz_fsa_var = BooleanVar(value=1)
        self.nz_fsa = Checkbutton(self.window, text="NZ FSA", var = self.nz_fsa_var).grid(row=0,column=1,rowspan=1,sticky=W)

        self.uk_fsa_var = BooleanVar(value=1)
        self.uk_fsa = Checkbutton(self.window, text="UK FSA", var = self.uk_fsa_var).grid(row=1,column=1,rowspan=1,sticky=W)

        self.usda_var = BooleanVar(value=1)
        self.usda = Checkbutton(self.window, text="USDA", var = self.usda_var).grid(row=2,column=1,rowspan=1,sticky=W)

        self.usda_fsis_var = BooleanVar(value=1)
        self.usda_fsis = Checkbutton(self.window, text="USDA FSIS", var = self.usda_fsis_var).grid(row=3,column=1,rowspan=1,sticky=W)

        ##Column 2
        self.ifs_var = BooleanVar(value=1)
        self.ifs = Checkbutton(self.window, text="IFS", var = self.ifs_var).grid(row=0,column=2,rowspan=1,sticky=W)

        self.fssc_var = BooleanVar(value=1)
        self.fssc = Checkbutton(self.window, text="FSSC", var = self.fssc_var).grid(row=1,column=2,rowspan=1,sticky=W)

        self.sf360_var = BooleanVar(value=1)
        self.sf360 = Checkbutton(self.window, text="SF360", var = self.sf360_var).grid(row=2,column=2,rowspan=1,sticky=W)

        self.brc_var = BooleanVar(value=1)
        self.brc = Checkbutton(self.window, text="BRC", var = self.brc_var).grid(row=3,column=2,rowspan=1,sticky=W)

        ##Column 3
        self.fsanz_var = BooleanVar(value=1)
        self.fsanz   = Checkbutton(self.window, text="FSANZ", var = self.fsanz_var).grid(row=0,column=3,rowspan=1,sticky=W)

        self.sqf_var = BooleanVar(value=1)
        self.sqf     = Checkbutton(self.window, text="SQF (NA)", var = self.sqf_var).grid(row=1,column=3,rowspan=1,sticky=W)

        self.efsa_var = BooleanVar(value=1)
        self.efsa    = Checkbutton(self.window, text="EFSA", var = self.efsa_var).grid(row=2,column=3,rowspan=1,sticky=W)

        self.un_fao_var = BooleanVar(value=1)
        self.un_fao  = Checkbutton(self.window, text="UN FAO", var = self.un_fao_var).grid(row=3,column=3,rowspan=1,sticky=W)

        ##Column 4
        self.cfia_var = BooleanVar(value=1)
        self.cfia   = Checkbutton(self.window, text="CFIA", var = self.cfia_var).grid(row=0,column=4,rowspan=1,sticky=W)

        self.gfsi_var = BooleanVar(value=1)
        self.gfsi     = Checkbutton(self.window, text="GFSI", var = self.gfsi_var).grid(row=1,column=4,rowspan=1,sticky=W)

        self.fda_fsma_var = BooleanVar(value=1)
        self.fda_fsma = Checkbutton(self.window, text="FDA FSMA", var = self.fda_fsma_var).grid(row=2,column=4,rowspan=1,sticky=W)

        self.who_var = BooleanVar(value=1)
        self.who = Checkbutton(self.window, text="WHO", var = self.who_var).grid(row=3,column=4,rowspan=1,sticky=W)


    def last_date(self):
        #Date
        self.min_date_text = Label(self.window,height = 1, width = 10, text = "Last Date")
        self.min_date_text.grid(row=5,column=4,rowspan=1,columnspan=1,sticky=W)

    def entry_data_labels(self):
        #Category
        self.cat_text = Label(self.window,height = 1, width = 10, text = "Category")
        self.cat_text.grid(row=5,column=0,rowspan=1,columnspan=1,sticky=W)

        self.OptionList = [
        "News"
        , "Alert"
        , "Recall"
        , "Discussion"
        ]
        self.variable = StringVar(self.window)
        self.variable.set(self.OptionList[0]) # default value

        self.w = OptionMenu(self.window, self.variable, *self.OptionList).grid(row=6,column=0,rowspan=1,sticky=W)

        #Date
        self.date_text = Label(self.window,height = 1, width = 8, text = "Date")
        self.date_text.grid(row=5,column=1,rowspan=1,columnspan=1,sticky=W)

        self.date = DateEntry(self.window).grid(row=6,column=1,rowspan=1,sticky=W)

        #Sources
        self.source_text = Label(self.window,height = 1, width = 8, text = "Source")
        self.source_text.grid(row=5,column=2,rowspan=1,columnspan=1,sticky=W)
        self.source_variable = StringVar(self.window)

        self.source_variable.set(self.source_list[0]) # default value

        self.s = OptionMenu(self.window, self.source_variable, *self.source_list).grid(row=6,column=2,rowspan=1,sticky=W)

    def entry_data(self):
        #Desription
        self.desc_text = Label(self.window,height = 1, width = 12, text = "Description:")
        self.desc_text.grid(row=8,column=0,rowspan=1,columnspan=1,sticky=W)

        self.desc_tb = Text(self.window,height = 1, width = 40)
        self.desc_tb.grid(row=8,column=1,rowspan=1,columnspan=6,sticky=W)

        #URL
        self.url_text = Label(self.window,height = 1, width = 12, text = "URL:")
        self.url_text.grid(row=9,column=0,rowspan=1,columnspan=1,sticky=W)

        self.url_tb = Text(self.window,height = 1, width = 40)
        self.url_tb.grid(row=9,column=1,rowspan=1,columnspan=6,sticky=W)

    def output_window(self):
        self.outp = Text(self.window,height = 10, width = 100)
        self.outp.grid(row=12,column=0,rowspan=1,columnspan=6,sticky=W)

    def buttons(self):

        self.view_all = Button(self.window,height = 1, width = 12, text = "View All"
            , command = partial(bf.view_command, self.ec_rasff_var, self.ifsqn_var, self.fda_var, self.fsai_var, self.uk_fsa_var, self.usda_var, self.ifs_var, self.fssc_var, self.sf360_var, self.fsanz_var, self.efsa_var, self.un_fao_var, self.cfia_var, self.gfsi_var, self.fda_fsma_var, self.who_var, self.outp)
            ).grid(row=9,column=4,rowspan=1,columnspan=1,sticky=W)

        self.generate_csv = Button(self.window,height = 1, width = 12, text = "CSV Export"
            , command = bf.generate_csv).grid(row=10,column=4,rowspan=1,columnspan=1,sticky=W)

        self.reset = Button(self.window,height = 1, width = 12, text = "Reset"
            , command = partial(bf.reset, self.outp)).grid(row=11,column=4,rowspan=1,columnspan=1,sticky=W)

        # def select_all(self)
        # all_check = [ec_rasff, ifsqn, fda, fsai, nz_fsa, uk_fsa, usda, usda_fsis, ifs, fssc, sf360, brc, fsanz, sqf, efsa, un_fao, cfia, gfsi, fda_fsma, who]
        # all_tick
        # all_tick = BooleanVar()
        # all_button = Checkbutton(self.window, text="All", var = all_tick, command = partial(bf.select_all, all_check, outp)).grid(row=0,column=5,rowspan=1,sticky=W)


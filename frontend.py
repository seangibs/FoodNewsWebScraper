from tkinter import *
from tkcalendar import *
from scraper import *
import pandas as pd
from buttonfunctions import *
from functools import partial

bf = ButtonFunc()

window = Tk()

window.geometry("800x400")

source_list = ["EC RASFF","IFSQN","FDA","FSAI","NZ FSA","UK FSA","USDA","USDA FSIS","IFS","FSSC","SF360","BRC","FSANZ","SQF","EFSA","UN FAO","CFIA","FDA FSMA","UN FAO","EC RAPID","WHO"]

##Column 0
global ec_rasff_var
ec_rasff_var = BooleanVar()
ec_rasff = Checkbutton(window, text="EC RASFF", var = ec_rasff_var).grid(row=0,column=0,rowspan=1,sticky=W)

global ifsqn_var
ifsqn_var = BooleanVar()
ifsqn   = Checkbutton(window, text="IFSQN", var = ifsqn_var).grid(row=1,column=0,rowspan=1,sticky=W)

global fda_var
fda_var = BooleanVar()
fda     = Checkbutton(window, text="FDA", var = fda_var).grid(row=2,column=0,rowspan=1,sticky=W)

global fsai_var
fsai_var = BooleanVar()
fsai    = Checkbutton(window, text="FSAI", var = fsai_var).grid(row=3,column=0,rowspan=1,sticky=W)

##Column 1
global nz_fsa_var
nz_fsa_var = BooleanVar()
nz_fsa   = Checkbutton(window, text="NZ FSA", var = nz_fsa_var).grid(row=0,column=1,rowspan=1,sticky=W)

global uk_fsa_var
uk_fsa_var = BooleanVar()
uk_fsa   = Checkbutton(window, text="UK FSA", var = uk_fsa_var).grid(row=1,column=1,rowspan=1,sticky=W)

global usda_var
usda_var = BooleanVar()
usda    = Checkbutton(window, text="USDA", var = usda_var).grid(row=2,column=1,rowspan=1,sticky=W)

global usda_fsis_var
usda_fsis_var = BooleanVar()
usda_fsis = Checkbutton(window, text="USDA FSIS", var = usda_fsis_var).grid(row=3,column=1,rowspan=1,sticky=W)

##Column 2
global ifs_var
ifs_var = BooleanVar()
ifs     = Checkbutton(window, text="IFS", var = ifs_var).grid(row=0,column=2,rowspan=1,sticky=W)

global fssc_var
fssc_var = BooleanVar()
fssc    = Checkbutton(window, text="FSSC", var = fssc_var).grid(row=1,column=2,rowspan=1,sticky=W)

global sf360_var
sf360_var = BooleanVar()
sf360   = Checkbutton(window, text="SF360", var = sf360_var).grid(row=2,column=2,rowspan=1,sticky=W)

global brc_var
brc_var = BooleanVar()
brc     = Checkbutton(window, text="BRC", var = brc_var).grid(row=3,column=2,rowspan=1,sticky=W)

##Column 3
global fsanz_var
fsanz_var = BooleanVar()
fsanz   = Checkbutton(window, text="FSANZ", var = fsanz_var).grid(row=0,column=3,rowspan=1,sticky=W)

global sqf_var
sqf_var = BooleanVar()
sqf     = Checkbutton(window, text="SQF (NA)", var = sqf_var).grid(row=1,column=3,rowspan=1,sticky=W)

global efsa_var
efsa_var = BooleanVar()
efsa    = Checkbutton(window, text="EFSA", var = efsa_var).grid(row=2,column=3,rowspan=1,sticky=W)

global un_fao_var
un_fao_var = BooleanVar()
un_fao  = Checkbutton(window, text="UN FAO", var = un_fao_var).grid(row=3,column=3,rowspan=1,sticky=W)

##Column 4
global cfia_var
cfia_var = BooleanVar()
cfia   = Checkbutton(window, text="CFIA", var = cfia_var).grid(row=0,column=4,rowspan=1,sticky=W)

global gfsi_var
gfsi_var = BooleanVar()
gfsi     = Checkbutton(window, text="GFSI", var = gfsi_var).grid(row=1,column=4,rowspan=1,sticky=W)

global fda_fsma_var
fda_fsma_var = BooleanVar()
fda_fsma = Checkbutton(window, text="FDA FSMA", var = fda_fsma_var).grid(row=2,column=4,rowspan=1,sticky=W)

global who_var
who_var = BooleanVar()
who = Checkbutton(window, text="WHO", var = who_var).grid(row=3,column=4,rowspan=1,sticky=W)

#Date
min_date_text = Label(window,height = 1, width = 10, text = "Last Date")
min_date_text.grid(row=5,column=4,rowspan=1,columnspan=1,sticky=W)

min_date = DateEntry(window).grid(row=6,column=4,rowspan=1,columnspan=1,sticky=W)

#Category
cat_text = Label(window,height = 1, width = 10, text = "Category")
cat_text.grid(row=5,column=0,rowspan=1,columnspan=1,sticky=W)

OptionList = [
"News"
, "Alert"
, "Recall"
, "Discussion"
]
variable = StringVar(window)
variable.set(OptionList[0]) # default value

w = OptionMenu(window, variable, *OptionList).grid(row=6,column=0,rowspan=1,sticky=W)

#Date
date_text = Label(window,height = 1, width = 8, text = "Date")
date_text.grid(row=5,column=1,rowspan=1,columnspan=1,sticky=W)

date = DateEntry(window).grid(row=6,column=1,rowspan=1,sticky=W)

#Sources
source_text = Label(window,height = 1, width = 8, text = "Source")
source_text.grid(row=5,column=2,rowspan=1,columnspan=1,sticky=W)
source_variable = StringVar(window)

source_variable.set(source_list[0]) # default value

s = OptionMenu(window, source_variable, *source_list).grid(row=6,column=2,rowspan=1,sticky=W)

#Desription
desc_text = Label(window,height = 1, width = 12, text = "Description:")
desc_text.grid(row=8,column=0,rowspan=1,columnspan=1,sticky=W)

desc_tb = Text(window,height = 1, width = 40)
desc_tb.grid(row=8,column=1,rowspan=1,columnspan=6,sticky=W)

#URL
url_text = Label(window,height = 1, width = 12, text = "URL:")
url_text.grid(row=9,column=0,rowspan=1,columnspan=1,sticky=W)

url_tb = Text(window,height = 1, width = 40)
url_tb.grid(row=9,column=1,rowspan=1,columnspan=6,sticky=W)

outp = Text(window,height = 10, width = 100)
outp.grid(row=12,column=0,rowspan=1,columnspan=6,sticky=W)

view_all = Button(window,height = 1, width = 12, text = "View All"
    , command = partial(bf.view_command, ec_rasff_var, ifsqn_var, fda_var, fsai_var, uk_fsa_var, usda_var, ifs_var, fssc_var, sf360_var, fsanz_var, efsa_var, un_fao_var, cfia_var, gfsi_var, fda_fsma_var, who_var, outp)
    ).grid(row=9,column=4,rowspan=1,columnspan=1,sticky=W)

generate_csv = Button(window,height = 1, width = 12, text = "CSV Export"
    , command = bf.generate_csv).grid(row=10,column=4,rowspan=1,columnspan=1,sticky=W)

reset = Button(window,height = 1, width = 12, text = "Reset"
    , command = partial(bf.reset, outp)).grid(row=11,column=4,rowspan=1,columnspan=1,sticky=W)

window.mainloop()

from django.shortcuts import render
from django.http import HttpResponse
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from zipfile import ZipFile
import numpy as np


import plotly.express as px
import plotly.graph_objects as go



#dash imports
import dash
import dash_table
import pandas as pd


def index(request):
    #API authentication
    api = KaggleApi()
    api.authenticate()

    #downloading datasets for COVID-19 data\
    api.dataset_download_file('gpreda/covid-world-vaccination-progress','country_vaccinations.csv')

    #Extract datasets
    zf = ZipFile('country_vaccinations.csv.zip')
    #extracted data is saved in the same directory as notebook
    zf.extractall() 
    zf.close()

    #read data
    df=pd.read_csv('country_vaccinations.csv')
    
 

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.country, df.iso_code, df.date, df.total_vaccinations],
               fill_color='lavender',
               align='left'))
               ])
    fig.write_html('vaccinedata/templates/test3.html')





    return render(request,'index.html',{})





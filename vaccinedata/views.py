from django.shortcuts import render
from django.http import HttpResponse
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from zipfile import ZipFile
import numpy as np
import json


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
    df = df.drop(['iso_code','daily_vaccinations_raw'], axis=1)
    grouped_df = df.groupby("country")
    maximums = grouped_df.max()
    maximums = maximums.reset_index()
    result = maximums.to_json(orient="split")
    parsed = json.loads(result)
    with open('data.json', 'w+') as outfile:
        json.dump(parsed, outfile)
    
 

    fig = go.Figure(data=[go.Table(
    header=dict(values=list(maximums.columns)),
    cells=dict(values=[maximums.country, maximums.date, maximums.total_vaccinations, maximums.vaccines],
               fill_color='white', 
               align='left'))
               ])
    fig.write_html('vaccinedata/static/table.html')
    print('hi there!')
    return render(request,'index.html',{})
    





import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
import numpy as np
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import datetime 


app = dash.Dash(__name__)

cases_data = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/full_data.csv")
vaccine_data = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv")

cases_data = cases_data.astype({'date':'datetime64'})
vaccine_data = vaccine_data.astype({'date':'datetime64'})

us_state_to_abbrev = {"Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR","California": "CA","Colorado": "CO",
    "Connecticut": "CT","Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID","Illinois": "IL",
    "Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY","Louisiana": "LA","Maine": "ME","Maryland": "MD",
    "Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO","Montana": "MT",
    "Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York State": "NY",
    "North Carolina": "NC","North Dakota": "ND","Ohio": "OH",  "Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI",
    "South Carolina": "SC","South Dakota": "SD","Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA",
    "West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC","American Samoa": "AS","Guam": "GU",
    "Northern Mariana Islands": "MP","Puerto Rico": "PR","United States Minor Outlying Islands": "UM","U.S. Virgin Islands": "VI",
}

vaccine_data['state_code'] = vaccine_data.location.map(us_state_to_abbrev)

app.layout = html.Div(className='background',children=[ html.H1('Covid-19 Dashboard'),

                                html.H2('Covid Cases'),
         
                                html.Div([
        
                                         html.Div([
                                         html.Div(html.Div([dcc.Dropdown(id='dropdown_country',
                                                            options=[{'label': x ,'value': x}
                                                                    for x in cases_data['location'].unique()
                                                            ],value ='United States',className='dropdown2'),
                                                            dcc.Dropdown(id='dropdown_case',
                                                            options=[{'label':'New Cases', 'value':'new_cases'},
                                                               {'label':'Deaths','value':'new_deaths'},
                                                               {'label':'Total Cases','value':'total_cases'},
                                                               {'label':'Total Deaths','value':'total_deaths'}
                                                              ], value='new_cases',className='dropdown1'),
                                                            ],style={'display':'flex'})),
                                         html.Div([ ],id='plot1')],className='div1'),
                                         html.Div([dcc.Dropdown(id='dropdown_case2',options=[{'label':'New Cases', 'value':'new_cases'},
                                                               {'label':'Deaths','value':'new_deaths'},
                                                               {'label':'Total Cases','value':'total_cases'},
                                                               {'label':'Total Deaths','value':'total_deaths'}
                                                              ], value='new_cases',className='dropdown3'),
                                         html.Div([ ],id='plot2')])], 
                                         style={'display':'flex'}),
                                html.H2('USA Vaccinations Status'),
                                html.Div(dcc.Dropdown(id='dropdown_vaccine_us',
                                                      options=[{'label': 'Atleast 1 Dose', 'value': 'people_vaccinated'},
                                                               {'label': 'Fully vacinated', 'value':'people_fully_vaccinated'},
                                                               {'label': 'Total Booster', 'value':'total_boosters'} 
                                                              ], value='people_vaccinated',className='dropdown5')),
                                html.Div([ ],id='plot3',className='div3'),
                                
                                html.P('References:'),
                                html.Ul(children=[html.Li('Mathieu, E., Ritchie, H., Ortiz-Ospina, E. et al. A global database of COVID-19' 
                                                           'vaccinations. Nat Hum Behav (2021).'),
                                                  dcc.Link('https://doi.org/10.1038/s41562-021-01122-8',href='https://doi.org/10.1038/s41562-021-01122-8',refresh=True),
                                                  html.Li('Hasell, J., Mathieu, E., Beltekian, D. et al. A cross-country database of COVID-19 testing. Sci Data 7, 345 (2020).'),
                                                  dcc.Link('https://doi.org/10.1038/s41597-020-00688-8',href='https://doi.org/10.1038/s41597-020-00688-8',refresh=True)])
                                ])
                            
@app.callback([Output(component_id='plot1',component_property='children'),
               Output(component_id='plot2',component_property='children'),
               Output(component_id='plot3',component_property='children')],
              [Input(component_id='dropdown_country',component_property='value'),
               Input(component_id='dropdown_case', component_property='value'),
               Input(component_id='dropdown_case2',component_property='value'),
               Input(component_id='dropdown_vaccine_us',component_property='value')])

def get_graph(country,value,case2,state_v):
    g1 = cases_data.groupby(['date','location']).sum().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=g1[g1['location']==country]['date'],y=g1[g1['location']==country][value]))
    fig.update_layout(autosize=False,
                      width=600,height=400,margin=dict(
                      l=40,r=40,b=30,t=30,pad=4),
                      paper_bgcolor="white")
    

    values =['World','High income', 'Europe','European Union','Asia','Upper middle income','North America', 'Lower middle income','South America','Africa']
    g3 = cases_data[cases_data.location.isin(values)==False]
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)

    g3= g3[g3['date']==yesterday.strftime("%Y-%m-%d")].sort_values(by=case2,ascending=False).head(10)
    g3 = g3.iloc[::-1]
    
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=g3[case2],y=g3['location'],orientation='h'))
    fig1.update_layout(title='Top 10 Countries',title_x=0.7,autosize=False,
                      width=600,height=400,margin=dict(
                      l=40,r=40,b=30,t=30,pad=4),
                      paper_bgcolor="white")

    fig2 = go.Figure(data=go.Choropleth(
    locations=vaccine_data.groupby(['state_code']).max().reset_index()['state_code'], 
    z = vaccine_data.groupby(['state_code']).max()[state_v], 
    locationmode = 'USA-states',     
     ))

    fig2.update_layout( 
    geo_scope='usa',
    width=900,height=400,margin=dict(
                      l=50,r=50,b=30,t=30,pad=4),
                      paper_bgcolor="white"
    )

    
    return [dcc.Graph(figure=fig),dcc.Graph(figure=fig1),dcc.Graph(figure=fig2)]


if __name__ == '__main__':
    app.run_server()
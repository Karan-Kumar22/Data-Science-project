# Import required packages
import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)

# Pie Chart Creation
fig = px.pie(data, values='Flights', names='DistanceGroup', title='Distance group proportion by flights')

app = dash.Dash(__name__)

app.layout = html.Div(children=[html.H1('Ailrine Dashboard', 
                                        style={'color':'brown', 'fontsize':40,
                                        'border-style':'outset','textAlign':'center'
                                        }),
                                
                                html.P('Proportion of distance group (250 mile distance interval group) by flights',
                                    style={'color':'Orange', 'fontsize':20,'border-style':'outset','textAlign':'center'}),
                        
                                dcc.Graph(figure=fig),
])

if __name__ == '__main__':
    app.run_server()

import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np

athletes_path = os.path.join('Hackathon', 'database', 'Athletes.csv')
teams_path = os.path.join('Hackathon', 'database', 'Teams.csv')
medals_tokyo_path = os.path.join('Hackathon', 'database', 'Medal-tst.csv')
all_medals_path = os.path.join('Hackathon', 'database', 'Summer_olympic_Medals.csv')
medals_path = os.path.join('Hackathon', 'database', 'Medals.csv')

athletes = pd.read_csv(athletes_path)
medals = pd.read_csv(medals_path)
teams = pd.read_csv(teams_path)
medals_tokyo = pd.read_csv(medals_tokyo_path)
all_medals = pd.read_csv(all_medals_path)

all_medals = all_medals.drop(['Country_Code', 'Host_country', 'Host_city'], axis=1)
medals_2016 = all_medals[all_medals['Year'] == 2016]
medals_2020 = all_medals[all_medals['Year'] == 2020]

total_medals_2016 = medals_2016.assign(Total_Medals=medals_2016['Gold'] + medals_2016['Silver'] + medals_2016['Bronze'])
total_medals_2016.columns = ['Year', 'National Olympic Committee', 'Gold', 'Silver', 'Bronze', 'Total Medals']
total_medals_2016 = total_medals_2016.sort_values(by='Total Medals', ascending=False)

gold_medals_2016 = medals_2016.sort_values(by='Gold', ascending=False)
gold_medals_2016.columns = ['Year', 'National Olympic Committee', 'Gold', 'Silver', 'Bronze']

total_medals_2020 = medals_2020.assign(Total_Medals=medals_2020['Gold'] + medals_2020['Silver'] + medals_2020['Bronze'])
total_medals_2020.columns = ['Year', 'National Olympic Committee', 'Gold', 'Silver', 'Bronze', 'Total Medals']
total_medals_2020 = total_medals_2020.sort_values(by='Total Medals', ascending=False)

gold_medals_2020 = medals_2020.sort_values(by='Gold', ascending=False)
gold_medals_2020.columns = ['Year', 'National Olympic Committee', 'Gold', 'Silver', 'Bronze']

all_years_data = all_medals.copy()
all_years_data['Total Medals'] = all_years_data['Gold'] + all_years_data['Silver'] + all_years_data['Bronze']

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server
app.title = 'Olympics Analysis Dashboard'
app.config.suppress_callback_exceptions = True

app.layout = html.Div(style={'backgroundColor': '#2c2f33', 'color': '#FFFFFF'}, children=[
    dbc.NavbarSimple(
        brand="Olympics Analysis Dashboard",
        brand_href="#",
        color="#2c2f33",
        dark=True,
    ),
    dbc.Tabs([
        dbc.Tab(label='Home', tab_id='home'),  
        dbc.Tab(label='Hypothesis', tab_id='hypothesis'),
        dbc.Tab(label='Top Countries 2016', tab_id='top-2016'),
        dbc.Tab(label='Bottom Countries 2016', tab_id='bottom-2016'),
        dbc.Tab(label='Top Countries 2020', tab_id='top-2020'),
        dbc.Tab(label='Bottom Countries 2020', tab_id='bottom-2020'),
        dbc.Tab(label='Scatter Plot', tab_id='scatter-plot'),
        dbc.Tab(label='Specialized Plots', tab_id='specialized-plots'),
        dbc.Tab(label='Predictions', tab_id='predictions')
    ], id='tabs', active_tab='home'),  
    html.Div(id='content'),
    html.Footer(children=[
        html.Div([
            "By ",
            html.A("CTRL + Purr Team", href="https://github.com/DaPandamonium/CTRL-Purr", style={'color': '#FFFFFF'})
        ], style={'textAlign': 'left', 'padding': '10px'})
    ], style={'backgroundColor': '#2c2f33', 'color': '#FFFFFF', 'padding': '10px'})
])


@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab')]
)
def render_content(tab):
    if tab == 'home':
        return html.Div([
            html.H2('Welcome to the Olympics Analysis Dashboard', style={'textAlign': 'left'}),
        ])
    elif tab == 'hypothesis':
        return html.Div([
            html.H3('Hypothesis'),
            html.P("Judging the medals won in the last two Olympics, we can make assumptions of who would be able to get on the top 10 for the next one."),
            html.P("The United States can continue being very consistent in getting number one."),
            html.P("Due to trends, China and Great Britain will continue competing right afterwards."),
            html.P("Japan might not be a great contender, considering a way lower trend on the Rio Olympics than on Tokyo, where they could've had the advantage of being on home-field.")
        ])
    elif tab == 'top-2016':
        return html.Div([
            html.H3('Top Countries 2016'),
            html.P("The United States dominated with a whopping number of 46 Gold Medals and 121 total Medals."),
            html.P("The closest contender was Great Britain, from afar, getting 27 Gold Medals."),
            html.P("China was a close third, being only one Gold Medal behind Great Britain. This shows the country's tradition of excellence in the Olympics, maintaining its presence on the top 10."),
            dcc.Dropdown(
                id='medal-type-top-2016',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='top-graph-2016')
        ])
    elif tab == 'bottom-2016':
        return html.Div([
            html.H3('Bottom Countries 2016'),
            html.P("None of the worst countries in the medal winning list got a Gold Medal, which shows a pattern of higher number of Gold Medals for specific countries - following possible disparity in fundings for the Olympics and the training of the athletes."),
            dcc.Dropdown(
                id='medal-type-bottom-2016',
                options=[{'label': i, 'value': i} for i in ['Total Medals', 'Gold', 'Silver', 'Bronze']],
                value='Total Medals',
                style={'color': 'black'}
            ),
            dcc.Graph(id='bottom-graph-2016')
        ])
    elif tab == 'top-2020':
        return html.Div([
            html.H3('Top Countries 2020'),
            html.P("The United States, once more, topped the Gold Medal tally, being first for both Gold Medals and Total Medals."),
            html.P("This time, though, it was followed more closely by China, which was only one Gold Medal behind. In total, the disparity between the two countries is more evident."),
            html.P("Japan changed its own pattern from the previous year, more than doubling their number of Gold Medals. This year, they had the home-field advantage."),
            html.P("Following events in Russia, which was expected to participate on the Olympics this year, the National Olympic Committee was renamed to Russian Olympic Committee. This way, the athletes could participate and the Games wouldn't be left with a gap in participants. Even under the circumstances, the russian athletes did really well, reaching 20 Gold Medals and ranking 5th."),
            dcc.Dropdown(
                id='medal-type-top-2020',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='top-graph-2020')
        ])
    elif tab == 'bottom-2020':
        return html.Div([
            html.H3('Bottom Countries 2020'),
            dcc.Dropdown(
                id='medal-type-bottom-2020',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Total Medals',
                style={'color': 'black'}
            ),
            dcc.Graph(id='bottom-graph-2020')
        ])
    elif tab == 'scatter-plot':
        return html.Div([
            html.H3('Gold vs Silver Medals from 1896 to 2020'),
            html.H4('Fun Facts'),
            html.P("A trend from the USA can be seen here, where the country mostly gets more Gold Medals than Silver ones, with few exceptions, as in 1976, 2004, 2008 and 2020."),
            html.P("Through the data used here, we noticed the USA got a lot more Gold Medals when they had the home-field in 1984. They won 83! For reference, they got 34 before and 36 afterwards. So maybe there is an advantage to playing home!"),
            html.P("Hungary had a growth and showed up with over 20 Silver Medals and over 40 Gold ones! But the last time they got as much as 10 in either category was in 1992, in the Barcelona Olympics."),
            dcc.Graph(id='scatter-plot-graph'),
        ])
    elif tab == 'specialized-plots':
        return html.Div([
            html.H3('Specialized Plots'),
            
            dcc.Graph(id='specialized-graph'),
        ])
    elif tab == 'predictions':
        return html.Div([
            html.H3('Predictions for 2024'),
            html.P("Based on current trends and performance data from the last two Summer Olympic Games, the United States is expected to continue its dominance in overall medal count, with an uprising pattern."),
            html.P("Even so, China remains a strong contender, having stayed very close to the USA in Gold Medals - although being further away if you consider the total amount of medals."),
            html.P("Considering the statistics from both Olympics that were analyzed, there appears to be a potential decline for Japan. They also had the home-field advantage at the Tokyo Olympics."),
            html.P("Considering the statistics from both Olympics that were analyzed, there appears to be a potential decline for Japan. They also had the home-field advantage at the Tokyo Olympics, so last Games’ results had an anomaly in Japan’s patterns."),
            dcc.Dropdown(
                id='prediction-type',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Total Medals',
                style={'color': 'black'}
            ),
            dcc.Graph(id='predictions-graph'),
        ])



@app.callback(
    Output('top-graph-2016', 'figure'),
    Input('medal-type-top-2016', 'value')
)
def update_top_graph_2016(medal_type):
    top_countries = total_medals_2016.nlargest(10, medal_type)
    fig = px.bar(top_countries, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'Top 10 Countries by {medal_type} Medals in 2016')
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': f'Top 10 Countries by {medal_type} Medals in 2016',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig

@app.callback(
    Output('bottom-graph-2016', 'figure'),
    Input('medal-type-bottom-2016', 'value')
)
def update_bottom_graph_2016(medal_type):
    bottom_countries = total_medals_2016.nsmallest(10, medal_type)
    fig = px.bar(bottom_countries, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'Bottom 10 Countries by {medal_type} Medals in 2016')
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': f'Bottom 10 Countries by {medal_type} Medals in 2016',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig

@app.callback(
    Output('top-graph-2020', 'figure'),
    Input('medal-type-top-2020', 'value')
)
def update_top_graph_2020(medal_type):
    top_countries = total_medals_2020.nlargest(10, medal_type)
    fig = px.bar(top_countries, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'Top 10 Countries by {medal_type} Medals in 2020')
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': f'Top 10 Countries by {medal_type} Medals in 2020',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig

@app.callback(
    Output('bottom-graph-2020', 'figure'),
    Input('medal-type-bottom-2020', 'value')
)
def update_bottom_graph_2020(medal_type):
    bottom_countries = total_medals_2020.nsmallest(10, medal_type)
    fig = px.bar(bottom_countries, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'Bottom 10 Countries by {medal_type} Medals in 2020')
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': f'Bottom 10 Countries by {medal_type} Medals in 2020',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig

@app.callback(
    Output('scatter-plot-graph', 'figure'),
    Input('tabs', 'active_tab')
)
def update_scatter_plot(medal_type):
    fig = px.scatter(all_years_data, x='Gold', y='Silver', size='Total Medals', color='National Olympic Committee', 
                     hover_name='National Olympic Committee', title='Gold vs Silver Medals from 1896 to 2020')
    fig.update_traces(marker=dict(size=14,
                                  line=dict(width=2,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': 'Gold vs Silver Medals from 1896 to 2020',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Gold Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Silver Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig

@app.callback(
    Output('specialized-graph', 'figure'),
    Input('tabs', 'active_tab')
)
def update_specialized_graph(tab):
    combined_medals = pd.concat([total_medals_2016, total_medals_2020])
    fig = px.density_heatmap(combined_medals, x='National Olympic Committee', y='Total Medals', title='Density Heatmap of Total Medals')
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': 'Density Heatmap of Total Medals',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Total Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig


@app.callback(
    Output('predictions-graph', 'figure'),
    Input('prediction-type', 'value')
)
def update_predictions_graph(medal_type):
    combined_medals = pd.concat([total_medals_2016, total_medals_2020])

    predictions = combined_medals.groupby('National Olympic Committee').mean().reset_index()
    predictions['Year'] = 2024

    predictions[medal_type] = np.floor(predictions[medal_type])
     
    predictions = predictions[predictions['National Olympic Committee'] != 'Russian Olympic Committee']
    top_predictions = predictions.nlargest(10, medal_type)
    bottom_predictions = predictions.nsmallest(10, medal_type)
    combined_predictions = pd.concat([top_predictions, bottom_predictions])

    fig = px.line(combined_predictions, x='National Olympic Committee', y=medal_type, color='National Olympic Committee', title=f'Predicted {medal_type} Medals for 2024')
    fig.update_traces(mode='lines+markers', marker=dict(size=20))
    fig.update_layout(
        plot_bgcolor='#2c2f33',
        paper_bgcolor='#2c2f33',
        font=dict(
            family="Arial, sans-serif",
            size=14,
            color="white",
            weight="bold"
        ),
        title={
            'text': f'Predicted {medal_type} Medals for Paris 2024',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {
                'family': 'Arial, sans-serif',
                'size': 20,
                'color': 'white',
                'weight': 'bold'
            }
        },
        xaxis={
            'title': 'Country Name',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
        yaxis={
            'title': 'Medals',
            'titlefont': {
                'family': 'Arial, sans-serif',
                'size': 18,
                'color': 'white',
                'weight': 'bold'
            },
            'tickfont': {
                'family': 'Arial, sans-serif',
                'size': 14,
                'color': 'white'
            }
        },
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc

medals_tokyo_path = os.path.join('Hackathon', 'database', 'Medal-tst.csv')
all_medals_path = os.path.join('Hackathon', 'database', 'Summer_olympic_Medals.csv')

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

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
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
        dbc.Tab(label='Medals 2016', tab_id='medals-2016'),
        dbc.Tab(label='Medals 2020', tab_id='medals-2020'),
        dbc.Tab(label='Best/Worst Countries', tab_id='best-worst'),
        dbc.Tab(label='Total Medals', tab_id='total-medals'),
        dbc.Tab(label='Scatter Plot', tab_id='scatter-plot')
    ], id='tabs', active_tab='medals-2016'),
    html.Div(id='content')
])

@app.callback(
    Output('content', 'children'),
    [Input('tabs', 'active_tab')]
)
def render_content(tab):
    if tab == 'medals-2016':
        return html.Div([
            html.H3('Total Medals 2016'),
            dcc.Dropdown(
                id='medal-type-2016',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='medals-graph-2016'),
            html.Div([
                html.H4('the Medals in 2016', style={'color': 'red', 'fontFamily': 'helvetica'}),
                html.P('This section contains a story or additional information about the medals won in 2016.'),
                html.Img(src='https://CATIMAGEWHEREDOSOMEPURRRRRRRR.com', style={'width': '100%'})
            ], style={'marginTop': 50})
        ])
    elif tab == 'medals-2020':
        return html.Div([
            html.H3('Total Medals 2020'),
            dcc.Dropdown(
                id='medal-type-2020',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='medals-graph-2020'),
            html.Div([
                html.H4('the Medals in 2020', style={'color': 'red', 'fontFamily': 'helvetica'}),
                html.P('This section contains a story or additional information about the medals won in 2020.'),
                html.Img(src='https://CATIMAGEWHEREDOSOMEPURRRRRRRR.com', style={'width': '100%'})
            ], style={'marginTop': 50})
        ])
    elif tab == 'best-worst':
        return html.Div([
            html.H3('Best and Worst Countries'),
            dcc.Dropdown(
                id='medal-type-best-worst',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver', 'Bronze', 'Total Medals']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='best-worst-graph'),
            html.Div([
                html.H4('Best/Worst Countries', style={'color': 'red', 'fontFamily': 'helvetica'}),
                html.P('This section contains a story or additional information about the best and worst performing countries.'),
                html.Img(src='https://CATIMAGEWHEREDOSOMEPURRRRRRRR.com', style={'width': '100%'})
            ], style={'marginTop': 50})
        ])
    elif tab == 'total-medals':
        return html.Div([
            html.H3('Total Medals 2016 & 2020'),
            dcc.Graph(id='total-medals-graph'),
            html.Div([
                html.H4('Total Medals', style={'color': 'red', 'fontFamily': 'helvetica'}),
                html.P('This section contains a story or additional information about the total medals won in 2016 and 2020.'),
                html.Img(src='https://CATIMAGEWHEREDOSOMEPURRRRRRRR.com', style={'width': '100%'})
            ], style={'marginTop': 50})
        ])
    elif tab == 'scatter-plot':
        return html.Div([
            html.H3('Gold vs Silver Medals in 2016'),
            dcc.Dropdown(
                id='scatter-dropdown',
                options=[{'label': i, 'value': i} for i in ['Gold', 'Silver']],
                value='Gold',
                style={'color': 'black'}
            ),
            dcc.Graph(id='scatter-plot-graph'),
            html.Div([
                html.H4('Scatter Plot', style={'color': 'red', 'fontFamily': 'helvetica'}),
                html.P('This section contains a story or additional information about the scatter plot.'),
                html.Img(src='https://CATIMAGEWHEREDOSOMEPURRRRRRRR.com', style={'width': '100%'})
            ], style={'marginTop': 50})
        ])

@app.callback(
    Output('medals-graph-2016', 'figure'),
    Input('medal-type-2016', 'value')
)
def update_medals_graph_2016(medal_type):
    fig = px.bar(total_medals_2016, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'{medal_type} Medals per Country in 2016')
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
            'text': f'{medal_type} Medals per Country in 2016',
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
        },
    )
    return fig

@app.callback(
    Output('medals-graph-2020', 'figure'),
    Input('medal-type-2020', 'value')
)
def update_medals_graph_2020(medal_type):
    fig = px.bar(total_medals_2020, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'{medal_type} Medals per Country in 2020')
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
            'text': f'{medal_type} Medals per Country in 2020',
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
    Output('best-worst-graph', 'figure'),
    Input('medal-type-best-worst', 'value')
)
def update_best_worst_graph(medal_type):
    best_countries = total_medals_2016.nlargest(10, medal_type)
    worst_countries = total_medals_2016.nsmallest(10, medal_type)
    combined = pd.concat([best_countries, worst_countries])
    fig = px.bar(combined, x='National Olympic Committee', y=medal_type, color=medal_type, title=f'Best and Worst Countries by {medal_type} Medals in 2016')
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
            'text': f'Best and Worst Countries by {medal_type} Medals in 2016',
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
    Output('total-medals-graph', 'figure'),
    Input('tabs', 'active_tab')
)
def update_total_medals_graph(tab):
    fig = px.bar(total_medals_2016.append(total_medals_2020), x='National Olympic Committee', y='Total Medals', color='Year', barmode='group', title='Total Medals in 2016 and 2020')
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
            'text': 'Total Medals in 2016 and 2020',
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
    Output('scatter-plot-graph', 'figure'),
    Input('scatter-dropdown', 'value')
)
def update_scatter_plot(medal_type):
    fig = px.scatter(total_medals_2016, x='Gold', y='Silver', size='Total Medals', color='National Olympic Committee', hover_name='National Olympic Committee', title='Gold vs Silver Medals in 2016')
    fig.update_traces(marker=dict(size=12,
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
            'text': 'Gold vs Silver Medals in 2016',
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

if __name__ == '__main__':
    app.run_server(debug=True)


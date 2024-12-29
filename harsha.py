import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

original_data = pd.read_csv('googleplaystore.csv')

cleaned_data = original_data.dropna(subset=['Rating', 'Reviews', 'Installs'])

cleaned_data = cleaned_data[cleaned_data['Installs'].str.contains('^[0-9+,]+$', regex=True)]
cleaned_data['Installs'] = cleaned_data['Installs'].str.replace('[+,]', '', regex=True).astype(int)
cleaned_data['Reviews'] = pd.to_numeric(cleaned_data['Reviews'], errors='coerce')

cleaned_data.to_csv('cleaned_googleplaystore.csv', index=False)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Top Android Apps Dashboard"),

    html.Label("Select Apps:"),
    dcc.Dropdown(
        id='app-dropdown',
        options=[{'label': app, 'value': app} for app in cleaned_data['App'].unique()],
        multi=True
    ),

    dcc.Graph(id='barplot'),

    html.Label("Select Criterion for Pie Chart:"),
    dcc.Dropdown(
        id='pie-criteria-dropdown',
        options=[
            {'label': 'Installs', 'value': 'Installs'},
            {'label': 'Reviews', 'value': 'Reviews'},
            {'label': 'Rating', 'value': 'Rating'}
        ],
        value='Installs'
    ),
    dcc.Graph(id='piechart'),

    dcc.Graph(id='lineplot')
])

@app.callback(
    Output('barplot', 'figure'),
    Input('app-dropdown', 'value')
)
def update_barplot(selected_apps):
    if not selected_apps:
        selected_apps = cleaned_data['App'].unique()[:10]
    filtered_data = cleaned_data[cleaned_data['App'].isin(selected_apps)]
    bar_fig = px.bar(
        filtered_data, 
        x='App', y='Installs',
        title='App Installs Barplot',
        labels={'Installs': 'Downloads'},
        color='App'
    )
    return bar_fig

@app.callback(
    Output('piechart', 'figure'),
    [Input('app-dropdown', 'value'), Input('pie-criteria-dropdown', 'value')]
)
def update_piechart(selected_apps, criteria):
    if not selected_apps:
        selected_apps = cleaned_data['App'].unique()[:10]
    filtered_data = cleaned_data[cleaned_data['App'].isin(selected_apps)]
    pie_fig = px.pie(
        filtered_data, 
        names='App', 
        values=criteria, 
        title=f'{criteria} Comparison of Selected Apps',
        hole=0.3
    )
    return pie_fig

@app.callback(
    Output('lineplot', 'figure'),
    Input('app-dropdown', 'value')
)
def update_lineplot(selected_apps):
    if not selected_apps:
        selected_apps = cleaned_data['App'].unique()[:10]
    filtered_data = cleaned_data[cleaned_data['App'].isin(selected_apps)]
    line_fig = px.line(
        filtered_data, 
        x='App', y='Installs', 
        title='App Installs Lineplot',
        labels={'Installs': 'Downloads'},
        markers=True
    )
    return line_fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

# Importing the libraries
import pickle
import pandas as pd
import plotly.express as px
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = "Sentiment Analysis with Insights"


def pie_c():
    df1 = pd.read_csv('balanced_reviews.csv')
    positi= df1[df1.Positivity==1]
    negati= df1[df1.Positivity==0]
    pos=len(positi.index)
    neg=len(negati.index)
    fig1 = px.pie(df1, values=(pos,neg), names=['positive','Negative'], color_discrete_sequence=px.colors.sequential.RdBu)
    return fig1


def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def load_model():
    global pickle_model
    global vocab
    global scrappedReviews
    
    
    scrappedReviews = pd.read_csv('scrappedreviews.csv')
    
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    file = open("features.pkl", 'rb') 
    vocab = pickle.load(file)
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    main_layout = dbc.Container(
        dbc.Jumbotron(
                [
                    html.H1(id = 'heading', children = project_name,className = 'display-3 mb-4'),
                    html.Br(),
                    html.Div([
            html.Img(src = app.get_asset_url('Sentiment-analysis.png'))
        ], style={'textAlign': 'center'}),
                    html.Br(),
                    html.Br(),
                    html.H2(id= 'pichart',children = 'Pie Chart', className = 'piechart-1'),
                    dcc.Graph(figure = pie_c()),
                    html.H2(id= 'positivewords',children = 'Positive words', className = 'wordcloud-1'),
                    html.Div([
            html.Img(src = app.get_asset_url('posword.png'))
        ], style={'textAlign': 'center'}),
                    html.Br(),
                    html.H2(id= 'negativewords',children = 'Negative words', className = 'wordcloud-2'),
                    html.Div([
            html.Img(src = app.get_asset_url('negword.png'))
        ], style={'textAlign': 'center'}),
                    html.Br(),
                    
                    html.H2(id= 'reviewentry',children = 'Type your Review', className = 'reviewtype-1'),
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value='This ia a good product',style = {'height': '150px'}),
                    html.Br(),
                    
                    html.H2(id= 'reviewdropdown',children = 'Choose a review from below', className = 'reviewtype-2'),
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in scrappedReviews.reviews],
                    value = scrappedReviews.reviews[0],
                    style = {'margin-bottom': '30px'}
                )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'}),
                    html.Div(id = 'result'),
                    html.Div(id = 'result1')
                    ],
                className = 'text-center'
                ),
        className = 'mt-4'
        )
    
    return main_layout

@app.callback(
    Output('result', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
    State('textarea', 'value')
    ]
    )    
def update_app_ui(n_clicks, textarea):
    result_list = check_review(textarea)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
     State('dropdown', 'value')
     ]
    )
def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")
    
def main():
    global app
    global project_name
    load_model()
    open_browser()
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
    app = None
    project_name = None
if __name__ == '__main__':
    main()
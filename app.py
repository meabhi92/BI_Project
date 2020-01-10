import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime as dt
# import datetime as dt1
# from dateutil.relativedelta import relativedelta

# import base64

external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

df = pd.read_excel("C:/Users/PC KLINIK/Documents/BCM Docs/Sem 2/DW & BI/Project Related Data/Dataset/merged.xlsx",
                   sheet_name=0)

value_counts = df['TIME_ID'].value_counts(sort=False)
value_counts = value_counts.rename_axis('Dates').reset_index(name='counts')
value_counts = value_counts.sort_values(by=['Dates'], ascending=True)
search_counts = df['TIME_ID'][df['VISITOR_SEARCH_IND'] != 0].value_counts(sort=False)
search_counts = search_counts.rename_axis('Dates').reset_index(name='counts')
search_counts = search_counts.sort_values(by=['Dates'], ascending=True)
book_counts = df['TIME_ID'][df['VISITOR_BOOK_IND'] != 0].value_counts(sort=False)
book_counts = book_counts.rename_axis('Dates').reset_index(name='counts')
book_counts = book_counts.sort_values(by=['Dates'], ascending=True)
browser_counts = df['BROWSER_NME'].value_counts(sort=True)
browser_counts = browser_counts.rename_axis('Browser').reset_index(name='counts')

df_time = df['TIME_ID']

trace1 = [go.Scatter(x=value_counts['Dates'], y=value_counts['counts'], fill='tozeroy', name="Visit Counts", fillcolor="#eb8338")]
trace2 = [go.Scatter(x=search_counts['Dates'], y=search_counts['counts'], fill='tonexty', name="Search Counts", fillcolor="#6462de")]
traces_ls1 = [trace1, trace2]

trace3 = [go.Scatter(x=search_counts['Dates'], y=value_counts['counts'], fill='tozeroy', name="Search Counts", fillcolor="#eb8338")]
trace4 = [go.Scatter(x=book_counts['Dates'], y=search_counts['counts'], fill='tonexty', name="Book Counts", fillcolor="#6462de")]
traces_ls2 = [trace3, trace4]

fig1 = px.bar(browser_counts, y='Browser', x='counts', color='Browser', orientation='h', width=600, height=400,
              title='Device Browser Chart')
fig1 = fig1.update(layout_showlegend=False)
# image_filename = 'Capture.PNG'
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

colors = {
    'background': '#111111',
    'text': 'black'
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.Div(
        [
            html.Div(
                [
                    html.H1(children='Dashboards for ABC EU HOTELS', className='nine columns'),

                    html.Img(
                        src="https://www.pinclipart.com/picdir/big/89-890938_svg-library-download-wave-hatenylo-com-png-hotel.png",
                        className='three columns',
                        style={
                            'height': '10%',
                            'width': '10%',
                            'float': 'right',
                            'position': 'relative',
                            'margin-top': 5, },
                    ),

                    html.Div(children='''
                            A Decision Support System by BCM Consulting 
                        ''', className='nine columns'
                             ),

                ], className="row", style={'backgroundColor': '#d2e4f7'}
            ),

            html.Div(
                html.H6(children='KPI 1: Device Engagement', style={'textAlign': 'center', 'color': colors['text']}), ),

            html.Div([
                dcc.DatePickerRange(
                    style={'width': '300px'},
                    id='date-picker-range',
                    start_date=dt(2014, 5, 1),
                    end_date_placeholder_text='Select a date'
                ),

                html.Br(),
                html.Br(),

                dcc.Dropdown(
                    style={'width': '300px'},
                    options=[
                        {'label': 'iPhone', 'value': 'iph'},
                        {'label': 'Desktop', 'value': 'des'},
                        {'label': 'iPad', 'value': 'ipa'},
                        {'label': 'Other', 'value': 'oth'},
                        {'label': 'Unknown', 'value': 'unkw'},
                        {'label': 'Android', 'value': 'and'}
                    ],
                    multi=True,
                    placeholder="Select OS Type",
                    value="MTL"
                )
            ]
            ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(
                                id='kpi-device-engagement1',
                                figure={
                                    'data': [
                                        go.Pie(labels=df['OS_NME'])
                                    ],
                                    'layout': {
                                        'title': 'OS Device Breakdown'
                                    }
                                }
                            ),
                        ], className='six columns'
                    ),
                    html.Div(
                        [
                            dcc.Graph(
                                id='example-graph1',
                                figure=fig1
                            ),
                        ], className='six columns'
                    )
                ], className="row"
            ),

            html.Div(
                html.H6(children='KPI 2: User Engagement', style={'textAlign': 'center', 'color': colors['text']})),

            html.Div(
                dcc.DatePickerRange(
                    style={'width': '300px'},
                    id='date-picker-range2',
                    start_date=dt(2014, 5, 1),
                    end_date_placeholder_text='Select a date'
                ),
            ),

            dcc.Graph(
                id='kpi-user-engagement',
                figure={
                    'data': [val for sublist in traces_ls1 for val in sublist],
                    'layout': {
                        'title': 'User Engagement'
                    }
                }
            ),

            html.Div(
                html.H6(children='KPI 3: Conversion Ratio', style={'textAlign': 'center', 'color': colors['text']})),

            html.Div(
                dcc.DatePickerRange(
                    style={'width': '300px'},
                    id='date-picker-range3',
                    start_date=dt(2014, 5, 1),
                    end_date_placeholder_text='Select a date'
                ),
            ),

            dcc.Graph(
                id='kpi-conversion-ratio',
                figure={
                    'data': [val for sublist in traces_ls2 for val in sublist],
                    'layout': {
                        'title': 'Conversion Ratio'
                    }
                }
            ),

            html.Div(
                html.H6(children='KPI 4: Advertising ROI', style={'textAlign': 'center', 'color': colors['text']})),

            html.Div([
                dcc.DatePickerRange(
                    style={'width': '300px'},
                    id='date-picker-range4',
                    start_date=dt(2014, 5, 1),
                    end_date_placeholder_text='Select a date'
                ),

                html.Br(),
                html.Br(),

                dcc.Dropdown(
                    style={'width': '300px'},
                    options=[
                        {'label': 'Pinterest', 'value': 'pin'},
                        {'label': 'Facebook', 'value': 'fac'},
                        {'label': 'Google', 'value': 'goo'},
                        {'label': 'Instagram', 'value': 'ins'},
                        {'label': 'LinkedIn', 'value': 'link'},
                        {'label': 'Twitter', 'value': 'twi'},
                        {'label': 'Youtube', 'value': 'you'}
                    ],
                    multi=True,
                    value="MTL"
                )
            ]
            ),

            dcc.Graph(
                id='kpi-advertising-roi',
                figure={
                    'data': [
                        go.Pie(labels=df['ADVERT_SRC'][df['ADVERT_SRC'] != 'Organic'])
                    ],
                    'layout': {
                        'title': 'Advertisement Source Breakdown'
                    }
                }
            )
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

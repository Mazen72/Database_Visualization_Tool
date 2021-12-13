# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
import pandas as pd
import dash_table
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from sqlalchemy.types import String
import base64
import datetime
import io

server = Flask(__name__) # creating a flask server

app = dash.Dash(       # creating dash app using dash framework with flask on backend ( dash here for providing styling without using css and html
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ] , external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.config.suppress_callback_exceptions = True   # server configeration to manage callbacks

# this is for the first app launch , if no table exist in database create from csv
try:
    df=pd.read_sql_table('table',con='sqlite:///database.db')
except:
    df=pd.read_csv('table.csv')
    df = df.applymap(str)
    #pd.DataFrame(columns=['Job No', 'Abi Serial No', 'Customer Name', 'Customer Address', 'Customer Phone'])
    df.to_sql('table',con='sqlite:///database.db',index=False,if_exists='replace')


# after that you can upload any csv from any location to database


# this is navigation bar to choose which page to show

navigation_header=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("All Filters", active='exact', href="/Home", id='Home',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Filter 1", active='exact', href="/Filter-1",id='Filter 1',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Filter 2", href="/Filter-2",active='exact',id='Filter 2',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Filter 3", href="/Filter-3", active='exact',
                                id='Filter 3',style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Filter 4", href="/Filter-4", active='exact',
                                id='Filter 4', style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("Main Table", href="/Main-Table", active='exact',
                                id='Main Table', style=dict(fontSize='1.8vh')))

    ],
    pills=True,
)

# navigation bar spacing

db_navigation_header=dbc.Col([navigation_header],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=12, offset=0), lg=dict(size=5, offset=0), xl=dict(size=5, offset=0)
                             )

# header text
header_text=html.Div('Database Visualization App',style=dict(color='black',
                     fontWeight='bold',fontSize='3vh'))
# header text spacing
db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=2), sm=dict(size=10,offset=2),
        md=dict(size=6,offset=0), lg=dict(size=3,offset=0), xl=dict(size=3,offset=0))


upload_database_text=html.H1('Update database from CSV',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black',textAlign='center'))

# upload component to upload csv files from computer
upload_database =dcc.Upload(id='upload_csv',children=dbc.Button("Upload CSV", color="primary", size='lg',
                                       n_clicks=0,id="upload_database",style=dict(fontSize='1.8vh')
                            ) )
# upload component spacing
db_upload_database=dbc.Col([upload_database]
        , xl=dict(size=2, offset=0), lg=dict(size=2, offset=0),
        md=dict(size=3, offset=0), sm=dict(size=10, offset=0), xs=dict(size=10, offset=0))

db_upload_database_text=dbc.Col([upload_database_text], xl=dict(size=2, offset=8), lg=dict(size=2, offset=8),
                                md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))





# button to add row

add_row=dbc.Button("Add Row", color="primary", size='lg', n_clicks=0,id="add_row"
                            ,style=dict(fontSize='1.8vh')
                            )
db_add_row=dbc.Col([add_row], xl=dict(size=1, offset=2), lg=dict(size=1, offset=2),
                              md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
                              xs=dict(size=8, offset=2))

# button to save modifications to database
save_to_database=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_database"
                            ,style=dict(fontSize='1.8vh')
                            )
db_save_to_database=dbc.Col([save_to_database]
        , xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
        md=dict(size=3, offset=0), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

# confrim saving msg
save_msg=html.Div([''],id='save_msg',style=dict(fontSize='1.8vh',color='black',fontWeight='bold') )

db_save_msg=dbc.Col([save_msg]
        , xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
        md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
        xs=dict(size=8, offset=2))



# table 1 header text
table1_msg=html.H1('Filter 1',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black',textAlign='center'))
# table 2 header text
table2_msg=html.H1('Filter 2',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black',textAlign='center'))
# table 3 header text
table3_msg=html.H1('Filter 3',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black',textAlign='center'))
# table 4 header text
table4_msg=html.H1('Filter 4',
                           style=dict(fontSize='2.2vh',fontWeight='bold',color='black',textAlign='center'))


# the app initial layout object


app.layout=html.Div([dbc.Row([ db_header_text] ,style=dict(backgroundColor='#26abff'),id='header' ),
                     dbc.Row([db_navigation_header]) ,html.Div(id='page-content'),
                     dcc.Location(id='url', refresh=True,pathname='/Home')


                     ])

# callback to switch between pages depending on navigation bar button pressed
# this callback create the page layout depending on which page pressed

@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def update_page(pathname):
    tables_df = pd.read_sql_table('table', con='sqlite:///database.db')
    unique_filters=list(tables_df.iloc[:, 0].unique())
    if pathname=='/Home':

        table1_df=tables_df[tables_df.iloc[:, 0]==unique_filters[0]]
        table1 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table1_df.columns
            ], id='table1', page_size=10,data=table1_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table1_div')

        table2_df=tables_df[tables_df.iloc[:, 0]==unique_filters[1]]
        table2 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table2_df.columns
            ], id='table2', page_size=10,data=table2_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table2_div')

        table3_df=tables_df[tables_df.iloc[:, 0]==unique_filters[2]]
        table3 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table3_df.columns
            ], id='table3', page_size=10,data=table3_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table3_div')

        table4_df=tables_df[tables_df.iloc[:, 0]==unique_filters[3]]
        table4 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table4_df.columns
            ], id='table4', page_size=10,data=table4_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table4_div')
        home_layout=html.Div([dbc.Row([dbc.Col([html.Br(),table1_msg,html.Br(),table1]
                                    ,xl=dict(size=4, offset=1), lg=dict(size=4, offset=1),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)),

                                    dbc.Col([html.Br(), table2_msg, html.Br(), table2]
                                    ,xl=dict(size=4, offset=1), lg=dict(size=4, offset=1),
                                    md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                    xs=dict(size=10, offset=1))


                                       ]),html.Br(),html.Br(),

                            dbc.Row([dbc.Col([html.Br(),table3_msg,html.Br(),table3]
                                    ,xl=dict(size=4, offset=1), lg=dict(size=4, offset=1),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)),

                                       dbc.Col([html.Br(), table4_msg, html.Br(), table4]
                                    ,xl=dict(size=4, offset=1), lg=dict(size=4, offset=1),
                                    md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                    xs=dict(size=10, offset=1))

                              ]),
        ])
        return [home_layout]

    elif pathname=='/Filter-1':
        table1_df=tables_df[tables_df.iloc[:, 0]==unique_filters[0]]
        table1 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table1_df.columns
            ], id='table1', page_size=20,data=table1_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table1_div')

        filter1_layout=html.Div([html.Br(),dbc.Row([dbc.Col([html.Br(),table1]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)) ])
            ])
        return [filter1_layout]

    elif pathname=='/Filter-2':
        table2_df=tables_df[tables_df.iloc[:, 0]==unique_filters[1]]
        table2 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table2_df.columns
            ], id='table2', page_size=20,data=table2_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table2_div')

        filter2_layout=html.Div([html.Br(),dbc.Row([dbc.Col([html.Br(),table2]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)) ])
            ])
        return [filter2_layout]

    elif pathname=='/Filter-3':
        table3_df=tables_df[tables_df.iloc[:, 0]==unique_filters[2]]
        table3 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table3_df.columns
            ], id='table3', page_size=20,data=table3_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table3_div')

        filter3_layout=html.Div([html.Br(),dbc.Row([dbc.Col([html.Br(),table3]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)) ])
            ])
        return [filter3_layout]

    elif pathname=='/Filter-4':
        table4_df=tables_df[tables_df.iloc[:, 0]==unique_filters[3]]
        table4 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in table4_df.columns
            ], id='table4', page_size=20,data=table4_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table4_div')

        filter4_layout=html.Div([html.Br(),dbc.Row([dbc.Col([html.Br(),table4]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)) ])
            ])
        return [filter4_layout]

    elif pathname=='/Main-Table':
        table = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),'id': str(x),'deletable': False,
                } for x in tables_df.columns
            ], id='table', page_size=20,data=tables_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,row_deletable=True,filter_action="native",sort_action="native",
            sort_mode="single",page_action='native',  style_table={'overflowX': 'auto'}
            # 'overflowY': 'auto',
        )]
            , id='table_div')

        table_layout=html.Div([dbc.Row([db_upload_database_text,db_upload_database]),

                               html.Br(),dbc.Row([dbc.Col([html.Br(),table]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1)) ]), html.Br(),

                               dbc.Row([db_add_row, db_save_to_database, html.Br(), db_save_msg])
            ])
        return [table_layout]


# callback to use upload component to upload csv then replace it with the existing table in database


@app.callback(Output('table_div', 'children'),
               Input('upload_csv', 'contents'),
               State('upload_csv', 'filename'),
              prevent_initial_call=True)
def update_output(list_of_contents,filename):
    if list_of_contents is not None:
        content_type, content_string = list_of_contents.split(',')
        decoded = base64.b64decode(content_string)
        df1=pd.DataFrame()
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df1 = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xlsx' in filename:
                # Assume that the user uploaded an excel file
                df1 = pd.read_excel(io.BytesIO(decoded))
        except :
            return (html.Div([
                'There was an error processing this file.',
            ],style=dict(fontSize='2.5vh',fontWeight='bold',color='red',textAlign='center')) )

        df1.to_sql('table', con='sqlite:///database.db', index=False, if_exists='replace', method='multi')
        return  [dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in df1.columns
            ], id='table', page_size=20,
            data=df1.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#26abff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='native',  # render all of the data at once. No paging.
            style_table={'overflowX': 'auto'}

        )   ]


# callback to add row to table


@app.callback(
    Output('table', 'data'),
    [Input('add_row', 'n_clicks')],
    [State('table', 'data'),
     State('table', 'columns')],
    prevent_initial_call=True)

def add_row(n_clicks1,rows, columns):
    rows.append({c['id']: '' for c in columns})
    return rows


# call back to save changes to database
@app.callback(
    Output('save_msg', 'children'),
    Input('save_to_database', 'n_clicks'),
    State('table', 'data'),
    prevent_initial_call=True)
def save_to_database(clicks,data):
    if clicks>0:
        df2 = pd.read_sql_table('table', con='sqlite:///database.db')
        df2 = pd.DataFrame(data=data,columns=list(df2.columns))
        df2.to_sql('table',con='sqlite:///database.db',index=False,if_exists='replace',method='multi')
        return 'saved successfully to Database'
    else:
        return ['']


if __name__ == '__main__':
    app.run_server(port=8500,debug=True)
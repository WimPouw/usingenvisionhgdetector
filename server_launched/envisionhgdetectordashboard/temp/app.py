import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import json
import os

app = Dash(__name__, requests_pathname_prefix='/karnatak/', assets_folder='/data/www/wimpouw/web/karnatak/assets/')
dir_path = os.path.dirname(os.path.abspath(__file__))

# set the current working directory to this directory
os.chdir(dir_path)
# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("assets/data.csv")

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Multimodal motifs in Karnatak vocal performances", style={'text-align': 'center'}),
    html.H3("Anonymized, Anonymized, Anonymized", style={'text-align': 'center'}),
    html.H3("A UMAP representation of the acoustic distances between motifs. Select the scatter points to view the multimodal event.", style={'text-align': 'center'}),
    dcc.Dropdown(id="performer",
                 options=[
                     {"label": "Performer: all", "value": "all"},
                     {"label": "Performer: performer 1", "value": "Performer1"},
                     {"label": "Performer: performer 2", "value": "Performer2"},
                     {"label": "Performer: performer 3", "value": "Performer3"}],
                 multi=False,
                 value="all",
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="comparison_type",
                 options=[
                     {"label": "Distance type: pitch", "value": "_pitch"},
                     {"label": "Distance type: 3D hand position trajectory", "value": "_pos3D"},
                     {"label": "Distance type: 3D hand acceleration", "value": "_acc3D"},
                     {"label": "Distance type: 3D head acceleration", "value": "_hacc3D"}
                     ],
                 multi=False,
                 value="_pitch",
                 style={'width': "40%"}
                 ),
    dcc.Dropdown(id="color_type",
                 options=[
                     {"label": "Coloring: by performer", "value": "performer"},
                     {"label": "Coloring: by raga", "value": "raga"},
                     {"label": "Coloring: by performance", "value": "performance"}],
                 multi=False,
                 value="performer",
                 style={'width': "40%"}
                 ),            
    html.Div(id='output_container', children=[], style = {'color': 'white'}),
    html.Br(),
    dcc.Graph(id='MY_XY_Map', figure={},style={'width': '60%','height': '70%', 'textAlign': 'center','display': 'inline-block'}),
    html.Video(controls=True, id='videoplayer', src='', style={'width': '30%', 'textAlign': 'center', 'display': 'inline-block', 'vertical-align': 'top'}, autoPlay=True)
], style={'height': '100vh'})


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='MY_XY_Map', component_property='figure'),
     Output(component_id ='videoplayer', component_property='src')],
    [Input(component_id='performer', component_property='value'), Input(component_id='comparison_type', component_property='value'),
    Input(component_id='color_type', component_property='value'), Input('MY_XY_Map', 'clickData')]
)

def update_graph(option_slctd, option_slctd2, option_slctd3, clickData):
    container = "Click on any point to inspect the multimodal event associated with it. \n You subselected events for: {}".format(option_slctd)
    dff = df.copy()
    if option_slctd=="Performer1":
        dff = dff[dff["performer"] == option_slctd]
    if option_slctd=="Performer2":
        dff = dff[dff["performer"] == option_slctd]
    if option_slctd=="Performer3":
        dff = dff[dff["performer"] == option_slctd]
   
    
    # Plotly Express
    fig = px.scatter(
        data_frame=dff,
        x=dff['X'+option_slctd2],
        y=dff['Y'+option_slctd2],
        color = dff[option_slctd3].astype(str),
        opacity=0.66,
        #color='Pct of Colonies Impacted',
        hover_data=['index'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'X t-sne': 'Y t-sne'},
        template='plotly_dark'
    )
    fig.update_traces(marker_size=7)
    fig.update_layout(legend=dict(orientation="h"))
    fig['layout']['uirevision'] = 42
    #get the video clicked on
    check = str(clickData)
    converted_to_legal_json = check.replace("'", '"')
    test = eval(converted_to_legal_json)
    src = ''
    if test is not None:
        test = eval(str(converted_to_legal_json))
        test = eval(str(test['points']))
        test = eval(str(test[0]))
        vidname = test['customdata'][0]
        #src = 'assets/' + os.path.splitext(str(vidname))[0]+'-converted.mp4'
        src = 'assets/' + os.path.splitext(str(vidname))[0]+'.mp4'
    #print(src)
    #root_dir = os.getcwd()
    #src = root_dir+src
    

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )
    return container, fig, src

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

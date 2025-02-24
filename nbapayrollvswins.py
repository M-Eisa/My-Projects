import pandas as pd
import numpy as np
import plotly.express as px
import webbrowser
import logging
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Define dataset with NBA team payroll and wins data
data = {
    'team_payroll': np.array([
        # 2023-2024 season
        209354737, 201366679, 193838882, 187346674, 186940921, 180922992, 177143542, 169876920, 167755884, 167403924,
        166874287, 166434327, 166271894, 165630436, 165263993, 164990518, 163054678, 162649524, 162515272, 159153393,
        155015136, 153564021, 150856313, 149356730, 148722330, 142867770, 139233014, 135774484, 133738448, 132643598,

        # 2022-2023 season
        192905421, 192386134, 182930771, 178633307, 177244238, 176042453, 169391473, 162338665, 159566723, 152008934,
        151966241, 151964990, 151408266, 150992313, 150496913, 149836313, 148987936, 148856338, 148738241, 148360910,
        145793656, 144997250, 139423615, 137579793, 129153570, 127139520, 126107324, 125874047, 125706114, 104545376,

        # 2021-2022 season
        178980766, 174811922, 168378382, 164409293, 160875421, 149760719, 148922969, 140840240, 138181486, 137963926,
        137432702, 136557646, 136476474, 136385911, 136083814, 135793968, 135166020, 134896484, 132267085, 131120355,
        130457848, 128019790, 127655401, 126786646, 126696965, 124788473, 122139566, 120644081, 117284457, 82022873,

        # 2020-2021 season
        171105334, 170444633, 147825311, 139722606, 139334713, 136881324, 136623929, 134731235, 133901495, 132931565,
        132022601, 131904647, 131784255, 131294012, 130334934, 130237102, 129793210, 129605319, 129537825, 129131910,
        128963580, 128858241, 127657823, 121739163, 118804016, 117041599, 108218809, 106847430, 102137151, 95774839,

        # 2019-2020 season
        132017938, 131979953, 131506341, 131059022, 129912339, 129867871, 129254928, 128746180, 128109922, 126095610,
        123971686, 122612183, 122463495, 121296256, 120871082, 119217331, 118910311, 118889943, 117868297, 117759332,
        114202982, 113796966, 112872260, 112601901, 110702618, 104527576, 100232129, 98539675, 98495848, 96552033,

        # 2018-2019 season
        153171497, 146291276, 144916427, 137793831, 130988604, 130256600, 126557932, 126474100, 125334993, 125188633,
        123747588, 123387454, 123255073, 121962221, 121588790, 121427859, 118850600, 118327016, 118026816, 116052756,
        115127167, 114394213, 113826156, 112598201, 110724804, 108692835, 107225482, 101466920, 86958881, 79180081
    ]),
    'wins': np.array([
        # 2023-2024 season
        46, 51, 49, 49, 64, 57, 46, 47, 50, 49, 48, 56, 47, 39, 21, 50, 25, 27, 57, 32,
        46, 15, 41, 47, 44, 22, 14, 21, 31, 47,

        # 2022-2023 season
        44, 44, 58, 57, 38, 45, 43, 53, 45, 35, 51, 40, 44, 41, 54, 41, 47, 40, 37, 42,
        42, 33, 48, 22, 17, 51, 34, 27, 35, 22,

        # 2021-2022 season
        53, 44, 42, 33, 51, 49, 51, 53, 25, 48, 46, 51, 64, 44, 46, 36, 43, 48, 20, 23,
        30, 35, 34, 22, 52, 27, 43, 37, 56, 24,

        # 2020-2021 season
        44, 55, 56, 54, 48, 59, 52, 46, 35, 41, 43, 48, 19, 39, 26, 39, 54, 25, 38, 31,
        35, 58, 48, 24, 47, 23, 38, 35, 47, 25,

        # 2019-2020 season
        49, 39, 55, 21, 48, 49, 17, 52, 49, 37, 58, 63, 60, 28, 48, 36, 49, 39, 34, 54,
        21, 35, 51, 25, 22, 22, 24, 38, 38, 26,

        # 2018-2019 season
        39, 57, 49, 58, 60, 53, 41, 53, 49, 33, 32, 17, 19, 36, 48, 39, 42, 54, 48, 33,
        51, 42, 50, 22, 48, 19, 37, 39, 33, 29
    ]),
    'season': np.array([
        *['2023-2024'] * 30,
        *['2022-2023'] * 30,
        *['2021-2022'] * 30,
        *['2020-2021'] * 30,
        *['2019-2020'] * 30,
        *['2018-2019'] * 30
    ])
}

# Convert the data dictionary to a pandas DataFrame for easier manipulation
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the Dash app using a Div container
app.layout = html.Div([
    dcc.Dropdown(
        id='season-dropdown',
        options=[{'label': season, 'value': season} for season in df['season'].unique()] + [{'label': 'All Seasons', 'value': 'All'}],
        value='All',
        clearable=False
    ),
    dcc.Graph(id='scatter-plot')
])

# Callback function to update the scatter plot based on the selected season from the dropdown menu
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('season-dropdown', 'value')
)

# Generate a scatter plot of team payroll vs wins, filtering data by the selected season
def update_graph(selected_season):
    filtered_df = df if selected_season == 'All' else df[df['season'] == selected_season]
    fig = px.scatter(
        filtered_df, x='team_payroll', y='wins',
        title=f'NBA Team Payroll vs Wins ({selected_season if selected_season != "All" else "All Seasons"})',
        labels={'team_payroll': 'Team Payroll (USD)', 'wins': 'Wins'}
    )
    return fig

# Start the Dash server, open the app in a web browser, and suppress default werkzeug logs
if __name__ == '__main__':
    url = "http://127.0.0.1:8050/"
    print(f"Dash app is running. If the browser does not open automatically, click here: {url}")
    webbrowser.open(url)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run_server(debug=False)


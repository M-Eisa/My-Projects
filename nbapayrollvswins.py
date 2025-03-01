import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import webbrowser
import logging
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Define dataset with NBA team payroll, wins data, and team names for each season
data = {
    '2023-2024': {
        'team_payroll': [209354737, 201366679, 193838882, 187346674, 186940921, 180922992, 177143542, 169876920, 167755884, 167403924,
                         166874287, 166434327, 166271894, 165630436, 165263993, 164990518, 163054678, 162649524, 162515272, 159153393,
                         155015136, 153564021, 150856313, 149356730, 148722330, 142867770, 139233014, 135774484, 133738448, 132643598],
        'wins': [46, 51, 49, 49, 64, 57, 46, 47, 50, 49, 48, 56, 47, 39, 21, 50, 25, 27, 57, 32,
                 46, 15, 41, 47, 44, 22, 14, 21, 31, 47],
        'team_name': ['Golden State Warriors', 'LA Clippers', 'Phoenix Suns', 'Milwaukee Bucks', 'Boston Celtics', 'Denver Nuggets',
                      'Miami Heat', 'LA Lakers', 'Dallas Mavericks', 'New Orleans Pelicans', 'Cleveland Cavaliers', 'Minnesota Timberwolves',
                      'Philadelphia 76ers', 'Chicago Bulls', 'Portland Trail Blazers', 'New York Knicks', 'Toronto Raptors', 'Memphis Grizzlies',
                      'Oklahoma City Thunder', 'Atlanta Hawks', 'Brooklyn Nets', 'Sacramento Kings', 'Washington Wizards', 'Houston Rockets',
                      'Indiana Pacers', 'San Antonio Spurs', 'Detroit Pistons', 'Charlotte Hornets', 'Utah Jazz', 'Orlando Magic']
    },
    '2022-2023': {
        'team_payroll': [192905421, 192386134, 182930771, 178633307, 177244238, 176042453, 169391473, 162338665, 159566723, 152008934,
                         151966241, 151964990, 151408266, 150992313, 150496913, 149836313, 148987936, 148856338, 148738241, 148360910,
                         145793656, 144997250, 139423615, 137579793, 129153570, 127139520, 126107324, 125874047, 125706114, 104545376],
        'wins': [44, 44, 58, 57, 38, 45, 43, 53, 45, 35, 51, 40, 44, 41, 54, 41, 47, 40, 37, 42,
                 42, 33, 48, 22, 17, 51, 34, 27, 35, 22],
        'team_name': ['LA Clippers', 'Golden State Warriors', 'Milwaukee Bucks', 'Boston Celtics', 'Dallas Mavericks', 'Phoenix Suns',
                      'LA Lakers', 'Denver Nuggets', 'Brooklyn Nets', 'Washington Wizards', 'Cleveland Cavaliers', 'Chicago Bulls',
                      'Miami Heat', 'Toronto Raptors', 'Philadelphia 76ers', 'Atlanta Hawks', 'New York Knicks', 'Oklahoma City Thunder',
                      'Utah Jazz', 'New Orleans Pelicans', 'Minnesota Timberwolves', 'Portland Trail Blazers', 'Sacramento Kings',
                      'Houston Rockets', 'Detroit Pistons', 'Memphis Grizzlies', 'Orlando Magic', 'Charlotte Hornets', 'Indiana Pacers',
                      'San Antonio Spurs']
    },
    '2021-2022': {
        'team_payroll': [178980766, 174811922, 168378382, 164409293, 160875421, 149760719, 148922969, 140840240, 138181486, 137963926,
                         137432702, 136557646, 136476474, 136385911, 136083814, 135793968, 135166020, 134896484, 132267085, 131120355,
                         130457848, 128019790, 127655401, 126786646, 126696965, 124788473, 122139566, 120644081, 117284457, 82022873],
        'wins': [53, 44, 42, 33, 51, 49, 51, 53, 25, 48, 46, 51, 64, 44, 46, 36, 43, 48, 20, 23,
                 30, 35, 34, 22, 52, 27, 43, 37, 56, 24],
        'team_name': ['Golden State Warriors', 'Brooklyn Nets', 'LA Clippers', 'LA Lakers', 'Milwaukee Bucks', 'Utah Jazz',
                      'Philadelphia 76ers', 'Miami Heat', 'Indiana Pacers', 'Denver Nuggets', 'Minnesota Timberwolves', 'Boston Celtics',
                      'Phoenix Suns', 'Cleveland Cavaliers', 'Chicago Bulls', 'New Orleans Pelicans', 'Atlanta Hawks', 'Toronto Raptors',
                      'Houston Rockets', 'Detroit Pistons', 'Sacramento Kings', 'Washington Wizards', 'San Antonio Spurs', 'Orlando Magic',
                      'Dallas Mavericks', 'Portland Trail Blazers', 'Charlotte Hornets', 'New York Knicks', 'Memphis Grizzlies',
                      'Oklahoma City Thunder']
    },
    '2020-2021': {
        'team_payroll': [171105334, 170444633, 147825311, 139722606, 139334713, 136881324, 136623929, 134731235, 133901495, 132931565,
                         132022601, 131904647, 131784255, 131294012, 130334934, 130237102, 129793210, 129605319, 129537825, 129131910,
                         128963580, 128858241, 127657823, 121739163, 118804016, 117041599, 108218809, 106847430, 102137151, 95774839],
        'wins': [44, 55, 56, 54, 48, 59, 52, 46, 35, 41, 43, 48, 19, 39, 26, 39, 54, 25, 38, 31,
                 35, 58, 48, 24, 47, 23, 38, 35, 47, 25],
        'team_name': ['Golden State Warriors', 'Brooklyn Nets', 'Philadelphia 76ers', 'LA Clippers', 'LA Lakers', 'Utah Jazz',
                      'Milwaukee Bucks', 'Miami Heat', 'New Orleans Pelicans', 'Boston Celtics', 'Memphis Grizzlies', 'Portland Trail Blazers',
                      'Houston Rockets', 'Washington Wizards', 'Minnesota Timberwolves', 'Indiana Pacers', 'Denver Nuggets', 'Cleveland Cavaliers',
                      'San Antonio Spurs', 'Toronto Raptors', 'Chicago Bulls', 'Phoenix Suns', 'Dallas Mavericks', 'Orlando Magic',
                      'Atlanta Hawks', 'Detroit Pistons', 'Charlotte Hornets', 'Sacramento Kings', 'New York Knicks', 'Oklahoma City Thunder']
    },
    '2019-2020': {
        'team_payroll': [132017938, 131979953, 131506341, 131059022, 129912339, 129867871, 129254928, 128746180, 128109922, 126095610,
                         123971686, 122612183, 122463495, 121296256, 120871082, 119217331, 118910311, 118889943, 117868297, 117759332,
                         114202982, 113796966, 112872260, 112601901, 110702618, 104527576, 100232129, 98539675, 98495848, 96552033],
        'wins': [49, 39, 55, 21, 48, 49, 17, 52, 49, 37, 58, 63, 60, 28, 48, 36, 49, 39, 34, 54,
                 21, 35, 51, 25, 22, 22, 24, 38, 38, 26],
        'team_name': ['Oklahoma City Thunder', 'Portland Trail Blazers', 'LA Clippers', 'Cleveland Cavaliers', 'Philadelphia 76ers',
                      'Miami Heat', 'Golden State Warriors', 'Denver Nuggets', 'Houston Rockets', 'Orlando Magic', 'LA Lakers',
                      'Milwaukee Bucks', 'Toronto Raptors', 'Washington Wizards', 'Dallas Mavericks', 'San Antonio Spurs', 'Utah Jazz',
                      'Brooklyn Nets', 'New Orleans Pelicans', 'Boston Celtics', 'Minnesota Timberwolves', 'Sacramento Kings',
                      'Indiana Pacers', 'Chicago Bulls', 'Atlanta Hawks', 'Detroit Pistons', 'New York Knicks', 'Phoenix Suns',
                      'Memphis Grizzlies', 'Charlotte Hornets']
    },
    '2018-2019': {
        'team_payroll': [153171497, 146291276, 144916427, 137793831, 130988604, 130256600, 126557932, 126474100, 125334993, 125188633,
                         123747588, 123387454, 123255073, 121962221, 121588790, 121427859, 118850600, 118327016, 118026816, 116052756,
                         115127167, 114394213, 113826156, 112598201, 110724804, 108692835, 107225482, 101466920, 86958881, 79180081],
        'wins': [39, 57, 49, 58, 60, 53, 41, 53, 49, 33, 32, 17, 19, 36, 48, 39, 42, 54, 48, 33,
                 51, 42, 50, 22, 48, 19, 37, 39, 33, 29],
        'team_name': ['Miami Heat', 'Golden State Warriors', 'Oklahoma City Thunder', 'Toronto Raptors', 'Milwaukee Bucks',
                      'Portland Trail Blazers', 'Detroit Pistons', 'Houston Rockets', 'Boston Celtics', 'Memphis Grizzlies',
                      'Washington Wizards', 'New York Knicks', 'Cleveland Cavaliers', 'Minnesota Timberwolves', 'San Antonio Spurs',
                      'Charlotte Hornets', 'Brooklyn Nets', 'Denver Nuggets', 'LA Clippers', 'New Orleans Pelicans',
                      'Philadelphia 76ers', 'Orlando Magic', 'Utah Jazz', 'Chicago Bulls', 'Indiana Pacers', 'Phoenix Suns',
                      'LA Lakers', 'Sacramento Kings', 'Dallas Mavericks', 'Atlanta Hawks']
    }
}

# Combine data into a single DataFrame
df_list = []
for season, season_data in data.items():
    season_df = pd.DataFrame(season_data)
    season_df['season'] = season
    # Add pure team name (without season) for filtering
    season_df['pure_team_name'] = season_df['team_name']
    # Format team names to include the season
    season_df['team_name_with_season'] = season + ' ' + season_df['team_name']
    df_list.append(season_df)

df = pd.concat(df_list, ignore_index=True)

# Calculate efficiency metric (wins per million dollars)
df['efficiency'] = (df['wins'] * 1000000) / df['team_payroll']

# Get unique team names for the filter dropdown
unique_teams = sorted(df['pure_team_name'].unique())

# Calculate correlation coefficient for each season
season_correlations = {}
for season in df['season'].unique():
    season_data = df[df['season'] == season]
    season_correlations[season] = np.corrcoef(season_data['team_payroll'], season_data['wins'])[0, 1]

# Calculate overall correlation
overall_correlation = np.corrcoef(df['team_payroll'], df['wins'])[0, 1]

# Define light theme styles
light_theme = {
    'graph_bg': 'white',
    'paper_bg': 'white',
    'grid_color': 'lightgray',
    'text_color': 'black',
    'bg_color': 'white',
    'card_bg': 'white',
    'card_header_bg': '#f8f9fa',  # Light gray header background
    'card_header_text': 'black',  # Black text for header
    'table_style': {'striped': True, 'bordered': True, 'hover': True, 'responsive': True, 'className': 'table-sm'},
}

# Initialize the Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "NBA Payroll Analysis Dashboard"

# Define the layout of the Dash app
app.layout = html.Div([
    # Main container
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("NBA Team Payroll vs. Performance Analysis",
                            className="text-center my-4 text-dark"),
                    html.P("An analysis of how NBA team payrolls impact season performance",
                           className="text-center mb-4 text-secondary"),
                ], className="dashboard-header")
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters",
                                   className="text-dark bg-light"),  # Light background, dark text
                    dbc.CardBody([
                        html.Label("Select Season:"),
                        dcc.Dropdown(
                            id='season-dropdown',
                            options=[{'label': season, 'value': season} for season in sorted(df['season'].unique(), reverse=True)] +
                                    [{'label': 'All Seasons', 'value': 'All'}],
                            value='All',
                            clearable=False,
                            className="mb-3"
                        ),

                        html.Label("Select Team(s):"),
                        dcc.Dropdown(
                            id='team-dropdown',
                            options=[{'label': team, 'value': team} for team in unique_teams],
                            value=[],
                            clearable=True,
                            multi=True,
                            className="mb-3",
                            placeholder="Select teams or leave empty for all teams"
                        ),

                        html.Label("View Mode:"),
                        dbc.RadioItems(
                            id='view-mode',
                            options=[
                                {'label': 'Payroll vs Wins', 'value': 'payroll_wins'},
                                {'label': 'Efficiency (Wins per $M)', 'value': 'efficiency'}
                            ],
                            value='payroll_wins',
                            inline=True,
                            className="mb-3"
                        ),

                        html.Div(id="correlation-display", className="mt-3 p-2 border rounded bg-light"),
                    ])
                ], className="mb-4 shadow-sm")
            ], width=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Visualization",
                                   className="text-dark bg-light"),  # Light background, dark text
                    dbc.CardBody([
                        dcc.Graph(id='main-graph', style={'height': '60vh'})
                    ])
                ], className="mb-4 shadow-sm")
            ], width=9)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Team Performance Table",
                                   className="text-dark bg-light"),  # Light background, dark text
                    dbc.CardBody([
                        html.Div(id="table-container", style={"maxHeight": "300px", "overflow": "auto"})
                    ])
                ], className="shadow-sm")
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                html.Footer([
                    html.P("Data source: HoopsHype (Salaries) and NBA.com (Standings)",
                           className="text-center text-muted mt-4 mb-4")
                ])
            ], width=12)
        ])
    ], fluid=True, className="p-4")
], style={'background-color': light_theme['bg_color'], 'min-height': '100vh', 'color': light_theme['text_color']})

# Callback to update the correlation display
@app.callback(
    Output('correlation-display', 'children'),
    [Input('season-dropdown', 'value')]
)
def update_correlation(selected_season):
    if selected_season == 'All':
        correlation = overall_correlation
        message = f"Overall correlation between payroll and wins: {correlation:.3f}"
    else:
        correlation = season_correlations[selected_season]
        message = f"Correlation for {selected_season} season: {correlation:.3f}"

    # Interpretation message
    if correlation > 0.7:
        interpretation = "Strong positive correlation"
    elif correlation > 0.4:
        interpretation = "Moderate positive correlation"
    elif correlation > 0.1:
        interpretation = "Weak positive correlation"
    elif correlation > -0.1:
        interpretation = "No significant correlation"
    else:
        interpretation = "Negative correlation"

    # Add an icon based on correlation strength
    if correlation > 0.4:
        icon = html.I(className="fas fa-arrow-trend-up me-2 text-success")
    elif correlation > 0.1:
        icon = html.I(className="fas fa-arrow-trend-up me-2 text-info")
    elif correlation > -0.1:
        icon = html.I(className="fas fa-minus me-2 text-warning")
    else:
        icon = html.I(className="fas fa-arrow-trend-down me-2 text-danger")

    return html.Div([
        html.P(message, className="mb-1"),
        html.P([icon, interpretation], className="font-weight-bold")
    ])

# Callback to update the main graph based on filters
@app.callback(
    Output('main-graph', 'figure'),
    [
        Input('season-dropdown', 'value'),
        Input('team-dropdown', 'value'),
        Input('view-mode', 'value')
    ]
)
def update_graph(selected_season, selected_teams, view_mode):
    # Filter by season
    if selected_season == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['season'] == selected_season]

    # Filter by team(s) if any are selected
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['pure_team_name'].isin(selected_teams)]

    # Determine what to plot based on view mode
    if view_mode == 'efficiency':
        # Efficiency view (Wins per million dollars)
        filtered_df = filtered_df.sort_values('efficiency', ascending=False)

        fig = px.bar(
            filtered_df,
            x='pure_team_name' if selected_season != 'All' else 'team_name_with_season',
            y='efficiency',
            color='efficiency',
            color_continuous_scale='Blues',
            title=f'Team Efficiency (Wins per $Million) {selected_season if selected_season != "All" else "All Seasons"}',
            labels={
                'pure_team_name': 'Team',
                'team_name_with_season': 'Team',
                'efficiency': 'Wins per $Million'
            },
            custom_data=['season', 'wins', 'team_payroll']
        )

        fig.update_traces(
            hovertemplate='%{x}<br>Season: %{customdata[0]}<br>Efficiency: %{y:.2f} wins/$M<br>Wins: %{customdata[1]}<br>Payroll: $%{customdata[2]:,.0f}<extra></extra>'
        )

        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            yaxis_title="Wins per $Million",
            xaxis_title="",
            plot_bgcolor=light_theme['graph_bg'],
            paper_bgcolor=light_theme['paper_bg'],
            font=dict(color=light_theme['text_color'])
        )

    else:
        # Default payroll vs wins view
        fig = go.Figure()

        marker_color = 'royalblue'

        # Add scatter points
        if selected_season == 'All':
            # Color by season when showing all seasons
            colors = px.colors.qualitative.Plotly

            for i, season in enumerate(sorted(filtered_df['season'].unique())):
                season_data = filtered_df[filtered_df['season'] == season]
                fig.add_trace(go.Scatter(
                    x=season_data['team_payroll'],
                    y=season_data['wins'],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=colors[i % len(colors)],
                        line=dict(width=1, color='black')
                    ),
                    name=season,
                    customdata=np.stack((
                        season_data['pure_team_name'],
                        season_data['season'],
                        season_data['efficiency']
                    ), axis=-1),
                    hovertemplate='%{customdata[0]}<br>Season: %{customdata[1]}<br>Payroll: $%{x:,.0f}<br>Wins: %{y}<br>Efficiency: %{customdata[2]:.2f} wins/$M<extra></extra>'
                ))
        else:
            # Single color for single season
            highlight_teams = False

            # Check if specific teams are selected
            if selected_teams and len(selected_teams) > 0:
                highlight_teams = True

            fig.add_trace(go.Scatter(
                x=filtered_df['team_payroll'],
                y=filtered_df['wins'],
                mode='markers+text' if highlight_teams and len(filtered_df) < 15 else 'markers',
                marker=dict(
                    size=15,
                    color=marker_color,
                    line=dict(width=1, color='black')
                ),
                text=filtered_df['pure_team_name'] if highlight_teams and len(filtered_df) < 15 else None,
                textposition='top center',
                name='Teams',
                customdata=np.stack((
                    filtered_df['pure_team_name'],
                    filtered_df['season'],
                    filtered_df['efficiency']
                ), axis=-1),
                hovertemplate='%{customdata[0]}<br>Season: %{customdata[1]}<br>Payroll: $%{x:,.0f}<br>Wins: %{y}<br>Efficiency: %{customdata[2]:.2f} wins/$M<extra></extra>'
            ))

        # Add trendline if there are enough data points
        if len(filtered_df) > 1:
            # Calculate trend line points
            x = filtered_df['team_payroll']
            y = filtered_df['wins']
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)

            # Create x points for the line
            x_trend = [min(x), max(x)]
            y_trend = [p(min(x)), p(max(x))]

            # Add the trend line
            fig.add_trace(go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                line=dict(color='red', dash='dash', width=2),
                name='Trend Line',
                hoverinfo='skip'
            ))

        # Update layout
        fig.update_layout(
            title=f'NBA Team Payroll vs Wins ({selected_season if selected_season != "All" else "All Seasons"})',
            xaxis_title="Team Payroll (USD)",
            yaxis_title="Wins",
            plot_bgcolor=light_theme['graph_bg'],
            paper_bgcolor=light_theme['paper_bg'],
            font=dict(color=light_theme['text_color'])
        )

    # Common layout updates
    fig.update_layout(
        font=dict(family="Montserrat", size=12, color=light_theme['text_color']),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=light_theme['text_color']),
            bgcolor='rgba(255,255,255,0.5)'
        ),
        title=dict(
            y=0.98,
            x=0.5,
            xanchor='center',
            font=dict(size=16)
        )
    )

    # Add gridlines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=light_theme['grid_color'],
        showline=True,
        linewidth=1,
        linecolor=light_theme['grid_color'],
        mirror=True
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=light_theme['grid_color'],
        showline=True,
        linewidth=1,
        linecolor=light_theme['grid_color'],
        mirror=True
    )

    return fig

# Callback to generate the data table
@app.callback(
    Output('table-container', 'children'),
    [
        Input('season-dropdown', 'value'),
        Input('team-dropdown', 'value')
    ]
)
def update_table(selected_season, selected_teams):
    # Filter by season
    if selected_season == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['season'] == selected_season]

    # Filter by team(s) if any are selected
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['pure_team_name'].isin(selected_teams)]

    # Create a copy of the DataFrame with formatted values for display
    display_df = filtered_df.copy()

    # Format payroll as currency
    display_df['team_payroll'] = display_df['team_payroll'].apply(lambda x: f"${x:,.0f}")

    # Format efficiency with 2 decimal places
    display_df['efficiency'] = display_df['efficiency'].apply(lambda x: f"{x:.2f}")

    # Select and reorder columns for display
    if selected_season == 'All':
        display_columns = ['season', 'pure_team_name', 'team_payroll', 'wins', 'efficiency']
        display_df = display_df[display_columns]
        display_df.columns = ['Season', 'Team', 'Payroll', 'Wins', 'Wins per $Million']
    else:
        display_columns = ['pure_team_name', 'team_payroll', 'wins', 'efficiency']
        display_df = display_df[display_columns]
        display_df.columns = ['Team', 'Payroll', 'Wins', 'Wins per $Million']

    # Sort by wins in descending order
    display_df = display_df.sort_values('Wins', ascending=False)

    # Generate the table with light theme styling
    table = dbc.Table.from_dataframe(
        display_df,
        striped=True,
        bordered=True,
        hover=True,
        responsive=True,
        className='table-sm'
    )

    return table

# Add server line for deployment
server = app.server

# Run the app
if __name__ == '__main__':
    url = "http://127.0.0.1:8050/"
    print(f"Dash app is running. If the browser does not open automatically, click here: {url}")
    webbrowser.open(url)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run_server(debug=False)

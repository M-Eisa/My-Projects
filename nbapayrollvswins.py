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
from sklearn.linear_model import LinearRegression

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

# Define modern theme styles
modern_theme = {
    'graph_bg': '#f8f9fa',
    'paper_bg': 'white',
    'grid_color': '#e9ecef',
    'text_color': '#343a40',
    'bg_color': 'white',
    'card_bg': 'white',
    'card_header_bg': '#f8f9fa',
    'card_header_text': '#343a40',
    'table_style': {'striped': True, 'bordered': False, 'hover': True, 'responsive': True, 'className': 'table-sm'},
    'primary_color': '#4361ee',
    'secondary_color': '#3f37c9',
    'accent_color': '#4895ef',
    'hover_box_bg': 'rgba(255, 255, 255, 0.95)',
    'hover_box_border': '#4895ef'
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
                            className="text-center my-4",
                            style={'color': modern_theme['text_color'], 'font-weight': '600'}),
                    html.P("An analysis of how NBA team payrolls impact season performance",
                           className="text-center mb-4",
                           style={'color': '#6c757d', 'font-weight': '300'})
                ], className="dashboard-header")
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filters",
                                   className="text-dark",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'border-bottom': 'none',
                                          'font-weight': '500',
                                          'border-radius': '12px 12px 0 0'}),
                    dbc.CardBody([
                        html.Label("Select Season:", style={'font-weight': '500', 'color': modern_theme['text_color']}),
                        dcc.Dropdown(
                            id='season-dropdown',
                            options=[{'label': season, 'value': season} for season in sorted(df['season'].unique(), reverse=True)] +
                                    [{'label': 'All Seasons', 'value': 'All'}],
                            value='All',
                            clearable=False,
                            className="mb-3",
                            style={'border-radius': '8px'}
                        ),

                        html.Label("Select Team(s):", style={'font-weight': '500', 'color': modern_theme['text_color']}),
                        dcc.Dropdown(
                            id='team-dropdown',
                            options=[{'label': team, 'value': team} for team in unique_teams],
                            value=[],
                            clearable=True,
                            multi=True,
                            className="mb-3",
                            placeholder="Select teams or leave empty for all teams",
                            style={'border-radius': '8px'}
                        ),

                        html.Label("View Mode:", style={'font-weight': '500', 'color': modern_theme['text_color']}),
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

                        html.Div(id="correlation-display", className="mt-3 p-3 border rounded",
                                 style={'border-radius': '10px', 'border-color': '#dee2e6', 'background-color': '#f8f9fa'})
                    ], style={'padding': '1.25rem'})
                ], className="mb-4 shadow-sm", style={'border-radius': '12px', 'border': 'none'})
            ], width=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Visualization",
                                   className="text-dark",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'border-bottom': 'none',
                                          'font-weight': '500',
                                          'border-radius': '12px 12px 0 0'}),
                    dbc.CardBody([
                        dcc.Graph(id='main-graph', style={'height': '60vh'})
                    ], style={'padding': '1.25rem'})
                ], className="mb-4 shadow-sm", style={'border-radius': '12px', 'border': 'none'})
            ], width=9)
        ]),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Team Performance Table",
                                   className="text-dark",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'border-bottom': 'none',
                                          'font-weight': '500',
                                          'border-radius': '12px 12px 0 0'}),
                    dbc.CardBody([
                        html.Div(id="table-container", style={"maxHeight": "300px", "overflow": "auto"})
                    ], style={'padding': '1.25rem'})
                ], className="shadow-sm", style={'border-radius': '12px', 'border': 'none'})
            ], width=12)
        ]),

        dbc.Row([
            dbc.Col([
                html.Footer([
                    html.P("Data source: HoopsHype (Salaries) and NBA.com (Standings)",
                           className="text-center mt-4 mb-4", style={'color': '#6c757d', 'font-size': '0.9rem'})
                ])
            ], width=12)
        ])
    ], fluid=True, className="p-4")
], style={'background-color': modern_theme['bg_color'], 'min-height': '100vh', 'color': modern_theme['text_color']})

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
        icon_color = "#198754"  # success green
    elif correlation > 0.4:
        interpretation = "Moderate positive correlation"
        icon_color = "#0dcaf0"  # info blue
    elif correlation > 0.1:
        interpretation = "Weak positive correlation"
        icon_color = "#0d6efd"  # primary blue
    elif correlation > -0.1:
        interpretation = "No significant correlation"
        icon_color = "#6c757d"  # gray
    else:
        interpretation = "Negative correlation"
        icon_color = "#dc3545"  # danger red

    # Add an icon based on correlation strength
    if correlation > 0.4:
        icon = html.I(className="fas fa-arrow-trend-up me-2", style={"color": icon_color})
    elif correlation > 0.1:
        icon = html.I(className="fas fa-arrow-trend-up me-2", style={"color": icon_color})
    elif correlation > -0.1:
        icon = html.I(className="fas fa-minus me-2", style={"color": icon_color})
    else:
        icon = html.I(className="fas fa-arrow-trend-down me-2", style={"color": icon_color})

    return html.Div([
        html.P(message, className="mb-1", style={"font-weight": "400"}),
        html.P([icon, interpretation], className="mb-0", style={"font-weight": "500"})
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
            hovertemplate='<b>%{x}</b><br>Season: %{customdata[0]}<br>Efficiency: %{y:.2f} wins/$M<br>Wins: %{customdata[1]}<br>Payroll: $%{customdata[2]:,.0f}<extra></extra>'
        )

        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            yaxis_title="Wins per $Million",
            xaxis_title="",
            plot_bgcolor=modern_theme['graph_bg'],
            paper_bgcolor=modern_theme['paper_bg'],
            font=dict(color=modern_theme['text_color'])
        )

    else:
        # Default payroll vs wins view
        fig = go.Figure()

        marker_color = modern_theme['primary_color']

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
                        line=dict(width=0)  # Removed black outline
                    ),
                    name=season,
                    customdata=np.stack((
                        season_data['pure_team_name'],
                        season_data['season'],
                        season_data['efficiency']
                    ), axis=-1),
                    hovertemplate='<b>%{customdata[0]}</b><br>Season: %{customdata[1]}<br>Payroll: $%{x:,.0f}<br>Wins: %{y}<br>Efficiency: %{customdata[2]:.2f} wins/$M<extra></extra>'
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
                    opacity=0.85,
                    line=dict(width=0)  # Removed black outline
                ),
                text=filtered_df['pure_team_name'] if highlight_teams and len(filtered_df) < 15 else None,
                textposition='top center',
                name='Teams',
                customdata=np.stack((
                    filtered_df['pure_team_name'],
                    filtered_df['season'],
                    filtered_df['efficiency']
                ), axis=-1),
                hovertemplate='<b>%{customdata[0]}</b><br>Season: %{customdata[1]}<br>Payroll: $%{x:,.0f}<br>Wins: %{y}<br>Efficiency: %{customdata[2]:.2f} wins/$M<extra></extra>'
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
                line=dict(color=modern_theme['secondary_color'], dash='dot', width=2),
                name='Trend Line',
                hoverinfo='skip'
            ))

        # Update layout
        fig.update_layout(
            title=f'NBA Team Payroll vs Wins ({selected_season if selected_season != "All" else "All Seasons"})',
            xaxis_title="Team Payroll (USD)",
            yaxis_title="Wins",
            plot_bgcolor=modern_theme['graph_bg'],
            paper_bgcolor=modern_theme['paper_bg'],
            font=dict(color=modern_theme['text_color'])
        )

    # Common layout updates
    fig.update_layout(
        font=dict(family="Montserrat, Arial, sans-serif", size=12, color=modern_theme['text_color']),
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=modern_theme['text_color']),
            bgcolor='rgba(255,255,255,0.5)'
        ),
        title=dict(
            y=0.98,
            x=0.5,
            xanchor='center',
            font=dict(size=16, family="Montserrat, Arial, sans-serif", color=modern_theme['text_color'])
        ),
        hoverlabel=dict(
            bgcolor=modern_theme['hover_box_bg'],
            bordercolor=modern_theme['hover_box_border'],
            font=dict(family="Montserrat, Arial, sans-serif", size=12, color=modern_theme['text_color']),
            # Add rounded corners to hover boxes
            namelength=-1
        )
    )

    # Set hover mode to closest for better hover experience
    fig.update_layout(hovermode='closest')

    # Add subtle gridlines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=modern_theme['grid_color'],
        showline=True,
        linewidth=1,
        linecolor=modern_theme['grid_color'],
        mirror=True,
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor=modern_theme['grid_color'],
        showline=True,
        linewidth=1,
        linecolor=modern_theme['grid_color'],
        mirror=True,
        zeroline=False
    )

    # Format hover templates for better appearance with curve edges (CSS is handled through config)
    fig.update_layout(
        hoverlabel=dict(
            bgcolor=modern_theme['hover_box_bg'],
            bordercolor=modern_theme['hover_box_border'],
            font=dict(family="Montserrat, Arial, sans-serif", size=12, color=modern_theme['text_color']),
        )
    )

    # Apply template (optional, helps with styling consistency)
    fig.update_layout(template="plotly_white")

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

    # Sort by wins (descending) by default
    display_df = display_df.sort_values('wins', ascending=False)

    # Select and rename columns for display
    display_df = display_df[['season', 'pure_team_name', 'team_payroll', 'wins', 'efficiency']]
    display_df.columns = ['Season', 'Team', 'Payroll', 'Wins', 'Wins per $Million']

    # Create the table
    table = dbc.Table.from_dataframe(
        display_df,
        striped=True,
        bordered=False,
        hover=True,
        responsive=True,
        className="table-sm"
    )

    return table

# Add download functionality
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    [State('season-dropdown', 'value'),
     State('team-dropdown', 'value')],
    prevent_initial_call=True,
)
def generate_csv(n_clicks, selected_season, selected_teams):
    # Filter by season
    if selected_season == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['season'] == selected_season]

    # Filter by team(s) if any are selected
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['pure_team_name'].isin(selected_teams)]

    # Select relevant columns
    export_df = filtered_df[['season', 'pure_team_name', 'team_payroll', 'wins', 'efficiency']]
    export_df.columns = ['Season', 'Team', 'Payroll', 'Wins', 'Wins_per_Million']

    return dcc.send_data_frame(export_df.to_csv, "nba_payroll_analysis.csv", index=False)

# Add an export button to the layout
app.layout.children[0].children.append(
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Button("Export Data as CSV", id="btn-download-csv", color="primary",
                           className="mb-3 mt-3", style={'border-radius': '8px'}),
                dcc.Download(id="download-dataframe-csv")
            ], className="d-flex justify-content-end")
        ], width=12)
    ])
)

# Add summary statistics card
@app.callback(
    Output('summary-stats', 'children'),
    [
        Input('season-dropdown', 'value'),
        Input('team-dropdown', 'value')
    ]
)
def update_summary_stats(selected_season, selected_teams):
    # Filter by season
    if selected_season == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['season'] == selected_season]

    # Filter by team(s) if any are selected
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['pure_team_name'].isin(selected_teams)]

    # Calculate summary statistics
    avg_payroll = filtered_df['team_payroll'].mean()
    min_payroll = filtered_df['team_payroll'].min()
    max_payroll = filtered_df['team_payroll'].max()

    avg_wins = filtered_df['wins'].mean()
    min_wins = filtered_df['wins'].min()
    max_wins = filtered_df['wins'].max()

    avg_efficiency = filtered_df['efficiency'].mean()
    min_efficiency = filtered_df['efficiency'].min()
    max_efficiency = filtered_df['efficiency'].max()

    # Most and least efficient teams
    most_efficient_team = filtered_df.loc[filtered_df['efficiency'].idxmax()]
    least_efficient_team = filtered_df.loc[filtered_df['efficiency'].idxmin()]

    # Create cards for summary statistics
    stats_content = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Payroll Statistics",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.P(f"Average: ${avg_payroll:,.0f}", className="mb-1"),
                        html.P(f"Minimum: ${min_payroll:,.0f}", className="mb-1"),
                        html.P(f"Maximum: ${max_payroll:,.0f}", className="mb-0")
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Wins Statistics",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.P(f"Average: {avg_wins:.1f}", className="mb-1"),
                        html.P(f"Minimum: {min_wins}", className="mb-1"),
                        html.P(f"Maximum: {max_wins}", className="mb-0")
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Efficiency Statistics",
                                   style={'background-color': modern_theme['card_header_bg'],
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.P(f"Average: {avg_efficiency:.2f} wins/$M", className="mb-1"),
                        html.P(f"Minimum: {min_efficiency:.2f} wins/$M", className="mb-1"),
                        html.P(f"Maximum: {max_efficiency:.2f} wins/$M", className="mb-0")
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=4)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Most Efficient Team",
                                   style={'background-color': modern_theme['primary_color'],
                                          'color': 'white',
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.H5(most_efficient_team['pure_team_name'], className="mb-1"),
                        html.P(f"Season: {most_efficient_team['season']}", className="mb-1"),
                        html.P(f"Payroll: ${most_efficient_team['team_payroll']:,.0f}", className="mb-1"),
                        html.P(f"Wins: {most_efficient_team['wins']}", className="mb-1"),
                        html.P(f"Efficiency: {most_efficient_team['efficiency']:.2f} wins/$M", className="mb-0")
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Least Efficient Team",
                                   style={'background-color': '#6c757d',
                                          'color': 'white',
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.H5(least_efficient_team['pure_team_name'], className="mb-1"),
                        html.P(f"Season: {least_efficient_team['season']}", className="mb-1"),
                        html.P(f"Payroll: ${least_efficient_team['team_payroll']:,.0f}", className="mb-1"),
                        html.P(f"Wins: {least_efficient_team['wins']}", className="mb-1"),
                        html.P(f"Efficiency: {least_efficient_team['efficiency']:.2f} wins/$M", className="mb-0")
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=6)
        ])
    ]

    return stats_content

# Add summary statistics section to the layout
app.layout.children[0].children.insert(3,
                                       dbc.Row([
                                           dbc.Col([
                                               dbc.Card([
                                                   dbc.CardHeader("Summary Statistics",
                                                                  className="text-dark",
                                                                  style={'background-color': modern_theme['card_header_bg'],
                                                                         'border-bottom': 'none',
                                                                         'font-weight': '500',
                                                                         'border-radius': '12px 12px 0 0'}),
                                                   dbc.CardBody([
                                                       html.Div(id="summary-stats")
                                                   ], style={'padding': '1.25rem'})
                                               ], className="mb-4 shadow-sm", style={'border-radius': '12px', 'border': 'none'})
                                           ], width=12)
                                       ])
                                       )

# Add insights tab to the layout

@app.callback(
    Output('insights-content', 'children'),
    [
        Input('season-dropdown', 'value'),
        Input('team-dropdown', 'value')
    ]
)
def update_insights(selected_season, selected_teams):
    # Filter by season
    if selected_season == 'All':
        filtered_df = df.copy()
        correlation = overall_correlation
    else:
        filtered_df = df[df['season'] == selected_season]
        correlation = season_correlations[selected_season]

    # Filter by team(s) if any are selected
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['pure_team_name'].isin(selected_teams)]

    # Generate insights based on the correlation value
    if correlation > 0.7:
        insight_title = "Strong Relationship Between Payroll and Performance"
        insight_text = """
        The data shows a strong positive correlation between team payroll and wins, indicating that higher-spending teams tend to perform better. 
    This is often due to teams with larger payrolls being able to afford star players, experienced veterans, and deeper rosters, which are critical for sustained success.
    However, it's important to note that injuries can significantly impact performance, even for high-spending teams. For example, a team with a top-heavy payroll might struggle if their star player gets injured.
    Additionally, teams that spend heavily often have the resources to retain key players, build chemistry, and make mid-season adjustments, which can lead to more wins.
        """
    elif correlation > 0.4:
        insight_title = "Moderate Relationship Between Payroll and Performance"
        insight_text = """
        The data shows a moderate positive correlation between payroll and wins, suggesting that while spending more can help, it's not the only factor driving success.
    Teams with moderate payrolls often strike a balance between investing in star talent and developing young players. For instance, a team might sign a veteran leader while also nurturing a rookie who outperforms their contract.
    Injuries and player development play a significant role here. A team with a moderate payroll might overperform if their young players develop quickly or if they avoid major injuries to key players.
    Additionally, teams with strong coaching and front-office strategies can maximize the value of their payroll, achieving better results than their spending might suggest.
        """
    elif correlation > 0.1:
        insight_title = "Weak Relationship Between Payroll and Performance"
        insight_text = """
        The data shows only a weak correlation between payroll and wins, indicating that spending more doesn't guarantee success.
    In the NBA, factors like player development, coaching, and team chemistry often outweigh payroll. For example, a team with a low payroll might overperform if they draft a future star on a rookie contract or if their coaching staff maximizes the potential of role players.
    Injuries also play a huge role. A team with a high payroll might underperform if their star player is injured, while a low-payroll team might exceed expectations if they stay healthy and develop their young talent.
    Additionally, teams that focus on building through the draft and developing players internally can achieve success without breaking the bank, as seen with teams like the Golden State Warriors during their championship run in 2014-2015.
        """
    else:
        insight_title = "Little to No Relationship Between Payroll and Performance"
        insight_text = """
        The data shows minimal correlation between payroll and wins, highlighting that how money is spent is far more important than how much is spent.
    In the NBA, teams can achieve success through smart drafting, player development, and strategic signings. For example, a team might draft a future MVP on a rookie contract, allowing them to allocate resources elsewhere while still competing at a high level.
    Injuries, coaching, and team chemistry are critical factors. A high-payroll team might underperform if they lack depth or if their star player is injured, while a low-payroll team might overperform if they have a strong culture and a cohesive game plan.
        """

    # Calculate expected wins using linear regression
    X = filtered_df[['team_payroll']]
    y = filtered_df['wins']
    model = LinearRegression()
    model.fit(X, y)
    filtered_df['expected_wins'] = model.predict(X)
    filtered_df['performance_diff'] = filtered_df['wins'] - filtered_df['expected_wins']

    # Sort by over/underperformance
    overperformers = filtered_df.sort_values('performance_diff', ascending=False).head(3)
    underperformers = filtered_df.sort_values('performance_diff', ascending=True).head(3)

    # Create cards for insights
    insights_content = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(insight_title,
                                   style={'background-color': modern_theme['primary_color'],
                                          'color': 'white',
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.P(insight_text)
                    ])
                ], className="shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=12)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Overperforming Teams",
                                   style={'background-color': '#198754',
                                          'color': 'white',
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H5(f"{row['pure_team_name']} ({row['season']})", className="mb-1"),
                                html.P(f"Wins: {row['wins']} (Expected: {row['expected_wins']:.1f})", className="mb-1"),
                                html.P(f"Payroll: ${row['team_payroll']:,.0f}", className="mb-1"),
                                html.P(f"Overperformance: +{row['performance_diff']:.1f} wins",
                                       className="mb-3",
                                       style={'color': '#198754', 'font-weight': '500'})
                            ]) for _, row in overperformers.iterrows()
                        ])
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Underperforming Teams",
                                   style={'background-color': '#dc3545',
                                          'color': 'white',
                                          'font-weight': '500'}),
                    dbc.CardBody([
                        html.Div([
                            html.Div([
                                html.H5(f"{row['pure_team_name']} ({row['season']})", className="mb-1"),
                                html.P(f"Wins: {row['wins']} (Expected: {row['expected_wins']:.1f})", className="mb-1"),
                                html.P(f"Payroll: ${row['team_payroll']:,.0f}", className="mb-1"),
                                html.P(f"Underperformance: {row['performance_diff']:.1f} wins",
                                       className="mb-3",
                                       style={'color': '#dc3545', 'font-weight': '500'})
                            ]) for _, row in underperformers.iterrows()
                        ])
                    ])
                ], className="h-100 shadow-sm", style={'border-radius': '8px', 'border': 'none'})
            ], width=6)
        ])
    ]

    return insights_content

# Add insights section to the layout
app.layout.children[0].children.insert(4,
                                       dbc.Row([
                                           dbc.Col([
                                               dbc.Card([
                                                   dbc.CardHeader("Data Insights",
                                                                  className="text-dark",
                                                                  style={'background-color': modern_theme['card_header_bg'],
                                                                         'border-bottom': 'none',
                                                                         'font-weight': '500',
                                                                         'border-radius': '12px 12px 0 0'}),
                                                   dbc.CardBody([
                                                       html.Div(id="insights-content")
                                                   ], style={'padding': '1.25rem'})
                                               ], className="mb-4 shadow-sm", style={'border-radius': '12px', 'border': 'none'})
                                           ], width=12)
                                       ])
                                       )

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Run the Dash app
if __name__ == '__main__':
    url = "http://127.0.0.1:8050/"
    print(f"Dash app is running. If the browser does not open automatically, click here: {url}")
    webbrowser.open(url)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run_server(debug=False)

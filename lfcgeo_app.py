#!/usr/bin/env python
# coding: utf-8
"""lfcgeo App. 

A python streamlit web app that maps each LFC squad player's shortest journey from their place of birth to Anfield for a selected season

To run:
    $streamlit lfcgeo_app.py

History
v1.0.0 - Sep 2020, Initial version with python3, pydeck, pandas and streamlit
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import ast

st.beta_set_page_config(
    page_title="lfcgeo",
    page_icon="redglider.ico",
    layout="wide",
    initial_sidebar_state="auto")

# define defaults
DEBUG = True
SQUAD_PLAYERS_GEO_CSV_FILE = 'data\dflfc_squad_players_geo_Sep2020.csv'
ANFIELD_LATITUTE = 53.4308358
ANFIELD_LONGITUDE = -2.9609095414165294
DEFAULT_SEASON = '1962-1963' # Shankly's first season back in the top flight, and somewhere in the middle!
ZOOM_MAX = 11
ZOOM_MIN = 0.5
ZOOM_DEFAULT = 4
GREEN = [0, 255, 0] # RGB
RED = [255, 0, 0] # RGB
WHITE = [255, 255, 255] # RGB
PICKING_RADIUS = 10
LINE_WIDTH=3
MAP_STYLE = 'mapbox://styles/mapbox/dark-v10' # ref: https://docs.mapbox.com/api/maps

# define helper functions
@st.cache
def read_lfcgeo_df():
    df = pd.read_csv(SQUAD_PLAYERS_GEO_CSV_FILE, parse_dates=['Birthdate'])
    return(df)

# introduce the web app
st.title("lfcgeo")
st.header("Map each LFC squad player's shortest journey from their place of birth to Anfield for a selected season")

# read all squad players' data, with geo and tooltip
dflfc_squad_player_geo = read_lfcgeo_df()
seasons = list(dflfc_squad_player_geo.Season.unique())

# select season using slider
selected_season = st.select_slider(label='Select a season to map using the slider:',
                                   options=seasons,
                                   value=DEFAULT_SEASON)
st.write(f"{selected_season} - the map is interactive, hover over a line to see player details; zoom in and out")

### show quick zoom radio buttons
### not used as issues with streamlit positioning of Anfield when moving to max zoom"
##zoom_choice = st.radio('The map is interactive, hover over a line to see player details; you can zoom in and out',
##                       ('Zoom in to Anfield view', 'Zoom out to world view', 'Zoom default'), index=2)
##if zoom_choice == 'Zoom in to Anfield view':
##    zoom_level = ZOOM_MAX
##elif zoom_choice == 'Zoom out to world view':
##    zoom_level = ZOOM_MIN
##else:
##    zoom_level = ZOOM_DEFAULT

# filter selected season in dataframe and prepare dataframe for mapping
FILTER = (dflfc_squad_player_geo.Season == selected_season)
df_plot = dflfc_squad_player_geo[FILTER].dropna().reset_index(drop=True)
df_plot['Source_coords_xfm'] = df_plot.Source_coords_xfm.apply(lambda s: tuple(ast.literal_eval(s)))
df_plot['Target_coords'] = df_plot.Target_coords.apply(lambda s: tuple(ast.literal_eval(s)))
df_plot['Anfield_dist_mi_rnd'] = round(df_plot.Anfield_dist_mi, 1)

# map using great circle layer
layer = pdk.Layer(
    "GreatCircleLayer",
    df_plot,
    pickable=True,
    get_source_position='Source_coords_xfm', # column in dataframe with source (birthplace) coordinates (x, y)
    get_target_position='Target_coords', # column in dataframe with target (Anfield) coordinates (x, y)
    get_source_color=GREEN,
    get_target_color=RED,
    auto_highlight=True,
    get_width=LINE_WIDTH,
    picking_radius=PICKING_RADIUS,
    highlightColor=WHITE
)

# Set the viewport location
view_state = pdk.ViewState(latitude=ANFIELD_LATITUTE, longitude=ANFIELD_LONGITUDE, zoom=ZOOM_DEFAULT, bearing=0, pitch=0)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=MAP_STYLE,
             tooltip={"text": "{Source_name} to {Target_name} ({Anfield_dist_mi_rnd} miles)"})
st.pydeck_chart(r)
st.markdown("_Data source: [lfchistory.net](https://www.lfchistory.net/)_")

# display dataframe if debug
if DEBUG:
    choice = st.checkbox('Show data')
    if choice:
        st.write(df_plot[['Season', 'Player', 'Birthplace_upd', 'Source_coords_xfm']]\
                 .rename(columns={'Birthplace_upd': 'Birthplace', 'Source_coords_xfm': 'Geo-location'}))

    

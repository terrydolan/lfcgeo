#!/usr/bin/env python
# coding: utf-8
"""
lfcgeo App

A python streamlit web app that maps each LFC squad player's shortest journey from their place of birth to Anfield for a selected season

To run:
    $streamlit lfcgeo_app.py

History
v1.0.0 - Sep 2020, Initial version with python, pandas, ast, pydeck and streamlit
"""

import logging
import logging.config
import lfcgeo_log_config # dict with logging config
import streamlit as st
import pydeck as pdk
import pandas as pd
import ast

__author__ = "Terry Dolan"
__copyright__ = "Terry Dolan"
__license__ = "MIT"
__email__ = "terrydolan1892@gmail.com"
__status__ = "Beta"
__version__ = "1.0.0"
__updated__ = "September 2020"

# set up logging
logging.config.dictConfig(lfcgeo_log_config.dictLogConfig)
logger = logging.getLogger('lfcgeo')

# define defaults
MODE_RUN = 'Run the lfcgeo app'
MODE_ABOUT = 'About the lfcgeo app'
MODE_ANI = 'Run the PTWR animation'

ABOUT_MD_FILE = 'README.md'
SHOW_DATAFRAME = True
SQUAD_PLAYERS_GEO_CSV_FILE = 'data/dflfc_squad_players_geo_Sep2020.csv'
ANFIELD_LATITUTE = 53.4308358
ANFIELD_LONGITUDE = -2.9609095414165294
DEFAULT_SEASON = '1900-1901' # Liverpool's first title winning season
ZOOM_ANFIELD = 11
ZOOM_WORLD = 0.6
ZOOM_DEFAULT = 4
GREEN = [0, 255, 0] # RGB
RED = [255, 0, 0] # RGB
WHITE = [255, 255, 255] # RGB
LINE_WIDTH=7
PICKING_RADIUS = 5*LINE_WIDTH
MAP_STYLE = 'mapbox://styles/mapbox/dark-v10' # ref: https://docs.mapbox.com/api/maps
ANI_GIF = "LFC PTWR 1892-1893 to 2020-2021.gif"
ANI_MP4 = "LFC PTWR 1892-1893 to 2020-2021.mp4"

# set initial values
view_zoom_level = ZOOM_DEFAULT
view_latitude = ANFIELD_LATITUTE
view_longitude = ANFIELD_LONGITUDE
        
# define helper functions
@st.cache
def read_lfcgeo_df():
    """Read the csv with squad players geo and return as a dataframe."""
    df = pd.read_csv(SQUAD_PLAYERS_GEO_CSV_FILE, parse_dates=['Birthdate'])
    return(df)

@st.cache
def read_about_md(filename):
    """Read the about markdown file and return as a string."""
    with open(filename, "r") as f:
        about_md = f.read()
    return about_md

# define page config
st.beta_set_page_config(
    page_title="lfcgeo proto",
    page_icon="redglider.ico",
    layout="wide",
    initial_sidebar_state="auto") #collapsed expanded

# define sidebar to select mode (default mode is to run the app)
select_mode = st.sidebar.radio('Select mode:', (MODE_RUN, MODE_ABOUT, MODE_ANI), index=0)

st.sidebar.markdown(f"*lfcgeo, version {__version__}*")

if select_mode == MODE_RUN:
   
    # introduce the web app
    st.title("lfcgeo proto")
    st.header("Map each LFC squad player's shortest journey from their birthplace to Anfield")

    # read all squad players' data, with geo and tooltip
    dflfc_squad_player_geo = read_lfcgeo_df()
    seasons = list(dflfc_squad_player_geo.Season.unique())

    # select season using slider
    selected_season = st.select_slider(label='Select a season to map using the slider:',
                                       options=seasons,
                                       value=DEFAULT_SEASON)
    st.write(f"{selected_season} - the map is interactive, hover over a line to see player details; zoom in and out")

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

    # set the viewport location
    view_state = pdk.ViewState(latitude=view_latitude, longitude=view_longitude, zoom=view_zoom_level, bearing=0, pitch=0)

    # render
    logger.info(f"Render the lfcgeo map for season: {selected_season}")
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, map_style=MAP_STYLE,
                 tooltip={"text": "{Player}\nfrom {Birthplace_upd}\nto Anfield ({Anfield_dist_mi_rnd} miles)"})
    r.picking_radius=2*PICKING_RADIUS
    st.pydeck_chart(r)
    st.markdown("_Data source: [lfchistory.net](https://www.lfchistory.net/)_")

    # display dataframe
    if SHOW_DATAFRAME:
        show_data = st.checkbox(f"Show data for the {selected_season} season")
        if show_data:
            logger.info(f"Show the dataframe for season: {selected_season}")
            st.write(df_plot[['Season', 'Player', 'Birthplace_upd', 'Source_coords_xfm']]\
                     .rename(columns={'Birthplace_upd': 'Birthplace', 'Source_coords_xfm': 'Geo-location'}))

elif select_mode == MODE_ABOUT:
    logger.info('Show info about lfcgeo')
    st.markdown(read_about_md(ABOUT_MD_FILE))

elif select_mode == MODE_ANI:
    logger.info('Show PTWR animation')
    #st.video(ANI_MP4)
    st.image(ANI_GIF)
    st.markdown("_Data source: [lfchistory.net](https://www.lfchistory.net/)_")

    
